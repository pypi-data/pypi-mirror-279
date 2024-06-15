import asyncio
import functools
from typing import Any, Dict, Optional, List, AsyncIterator, Set

import aiobotocore.session
import aiobotocore.client
from botocore.config import Config

from async_s3.group_by_prefix import group_by_prefix


MAX_CONCURRENT_TASKS = 100


@functools.lru_cache()
def create_session() -> aiobotocore.session.AioSession:
    """Create a session object."""
    return aiobotocore.session.get_session()


def get_s3_client() -> aiobotocore.client.AioBaseClient:
    """Get S3 client."""
    session = create_session()
    config = Config(
        retries={"max_attempts": 3, "mode": "adaptive"},
    )
    return session.create_client("s3", config=config)


class ListObjectsAsync:
    def __init__(self, bucket: str) -> None:
        self._bucket = bucket
        self.semaphore = asyncio.Semaphore(MAX_CONCURRENT_TASKS)

    async def _list_objects(  # pylint: disable=too-many-arguments, too-many-locals
        self,
        s3_client: aiobotocore.client.AioBaseClient,
        prefix: str,
        current_depth: int,
        max_depth: Optional[int],
        max_folders: Optional[int],
        objects_keys: Set[str],
        queue: asyncio.Queue[List[Dict[str, Any]]],
        active_tasks: Set[asyncio.Task[None]],
    ) -> None:
        """Emit object pages to the queue."""
        paginator = s3_client.get_paginator("list_objects_v2")
        prefixes = []

        params = {"Bucket": self._bucket, "Prefix": prefix}
        if (current_depth != -1) and (max_depth is None or current_depth < max_depth):
            params["Delimiter"] = "/"

        async for page in paginator.paginate(**params):
            objects = page.get("Contents", [])
            new_keys = {
                obj["Key"]
                for obj in objects
                if not obj["Key"].endswith("/") and obj["Key"] not in objects_keys
            }
            cleared_objects = [obj for obj in objects if obj["Key"] in new_keys]
            objects_keys.update(new_keys)
            await queue.put(cleared_objects)

            if "Delimiter" in params:
                prefixes.extend([prefix["Prefix"] for prefix in page.get("CommonPrefixes", [])])

        level = -1 if current_depth == -1 else current_depth + 1
        if max_folders is not None and (len(prefixes) > max_folders):
            prefixes = list(group_by_prefix(prefixes, max_folders))
            level = -1

        for folder in prefixes:
            await self.semaphore.acquire()
            try:
                task = asyncio.create_task(
                    self._list_objects(
                        s3_client,
                        folder,
                        level,
                        max_depth,
                        max_folders,
                        objects_keys,
                        queue,
                        active_tasks,
                    )
                )
                active_tasks.add(task)
                task.add_done_callback(lambda t: self._task_done(t, active_tasks))
            except Exception as e:
                self.semaphore.release()
                raise e

    async def pages(
        self, prefix: str = "/", max_depth: Optional[int] = None, max_folders: Optional[int] = None
    ) -> AsyncIterator[List[Dict[str, Any]]]:
        """Generator that yields objects in the bucket with the given prefix.

        Yield objects by separate pages (list of AWS S3 object dicts).

        max_depth: The maximum folders depth to traverse in separate requests. If None, traverse all levels.
        max_folders: The maximum number of folders to load in separate requests. If None, requests all folders.
        Otherwise, the folders are grouped by prefixes before loading in separate requests.
        Try to group in the given number of folders if possible.
        """
        # if we group by prefixes, some objects may be listed multiple times
        # to avoid this, we store the keys of the objects already listed
        objects_keys: Set[str] = set()

        # queue to store the objects pages from the tasks
        queue: asyncio.Queue[List[Dict[str, Any]]] = asyncio.Queue()

        # set to keep track of active tasks
        active_tasks: Set[asyncio.Task[None]] = set()

        async with get_s3_client() as s3_client:
            root_task = asyncio.create_task(
                self._list_objects(
                    s3_client, prefix, 0, max_depth, max_folders, objects_keys, queue, active_tasks
                )
            )
            active_tasks.add(root_task)
            root_task.add_done_callback(lambda t: self._task_done(t, active_tasks))

            while active_tasks:
                try:
                    yield queue.get_nowait()
                except asyncio.QueueEmpty:
                    await asyncio.sleep(0)

            if active_tasks:
                await asyncio.gather(*active_tasks)

    def _task_done(self, task: asyncio.Task[None], active_tasks: Set[asyncio.Task[None]]) -> None:
        """Callback for when a task is done."""
        active_tasks.discard(task)
        self.semaphore.release()

    async def list_objects(
        self, prefix: str = "/", max_depth: Optional[int] = None, max_folders: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """List all objects in the bucket with the given prefix.

        max_depth: The maximum folders depth to traverse in separate requests. If None, traverse all levels.
        max_folders: The maximum number of folders to load in separate requests. If None, requests all folders.
        Otherwise, the folders are grouped by prefixes before loading in separate requests.
        Try to group to the given `max_folders` if possible.
        """
        objects = []
        async for objects_page in self.pages(prefix, max_depth, max_folders):
            objects.extend(objects_page)
        return objects
