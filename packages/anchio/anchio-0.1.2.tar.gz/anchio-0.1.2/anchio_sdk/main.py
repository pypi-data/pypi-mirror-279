

from concurrent.futures import ThreadPoolExecutor
from functools import wraps
import httpx
from threading import Thread
import asyncio
from logging import getLogger
from typing import List, Tuple
from asyncio import Queue, sleep
from time import sleep as sync_sleep, time
from async_anchio.models.meter_entry_schema import MeterEntrySchema
from async_anchio import Configuration, ApiClient, DefaultApi
from anchio_sdk.exceptions import AnchioMaxEnqueuedAttempts
from anchio_sdk.types import MeterEntryArgs
from datetime import datetime
from zoneinfo import ZoneInfo
from uuid import UUID, uuid4

utc = ZoneInfo("UTC")

logger = getLogger(__name__)


class Full(Exception):
    pass


def batch(iterable, n=1):
    iter_length = len(iterable)
    for ndx in range(0, iter_length, n):
        yield iterable[ndx:min(ndx + n, iter_length)]


def run_queue_monitor_sync(service: "AnchioInit") -> None:
    asyncio.run(service.queue_monitor())


class AnchioInit:
    thread: Thread | None
    queue: Queue[MeterEntrySchema]
    token: str
    max_queue_size: int
    service_to_uuid: dict[str, UUID]

    def __init__(self, token: str , max_queue_size: int = 1000):
        self.token = token
        self.max_queue_size = max_queue_size
        self.thread: Thread | None = None
        self.queue = Queue[MeterEntrySchema](maxsize=max_queue_size)
        self.thread = self.start()
        self.service_to_uuid = dict()
        if self.thread is not None:
            while not self.thread.is_alive():
               sync_sleep(0.5)

    def process_entry(self, entry: MeterEntryArgs) -> MeterEntrySchema:
        now = datetime.now(utc)
        if "start" not in entry:
            entry["start"] = now
        if "end" not in entry:
            entry["end"] = now
        if "service" not in entry:
            entry["service"] = "default"
            if entry["service"] in self.service_to_uuid:
                entry["service"] = self.service_to_uuid[entry["service"]]
        if "id" not in entry:
            entry["id"] = str(uuid4())

        return MeterEntrySchema(**entry)

    async def post_entries(self) -> None:
        configuration = Configuration(
            host = "https://anchio.app",
            access_token = self.token
        )
        data_list = []
        time_start = time()
        while not self.queue.empty() and time() - time_start < 60:
            data_list.append(await self.queue.get())
            if len(data_list) > 100:
                break
        
        
        if len(data_list) > 0:
            async with ApiClient(configuration) as api_client:
                api_instance = DefaultApi(api_client)
                res = await api_instance.create_meter_entries_api_v1_metering_meter_entry_post(
                    data_list
                )
                for datum, result in zip(data_list, res):
                    try:
                        UUID(datum.service)
                    except ValueError:
                        self.service_to_uuid[datum.service] = result.service
                data_list = []

    async def queue_monitor(self):
        while True:
            await self.post_entries()
            await sleep(0.1)

    def start(self) -> Thread:
        #NOTE: We're going to run one sub-thread to monitor the queue for simplicity
        thread = Thread(target=run_queue_monitor_sync, args=(self,), daemon=True)
        thread.start()
        return thread

    def get_loop(self) -> Tuple[asyncio.AbstractEventLoop, bool]:
        is_loop_external = False
        try:
            loop = asyncio.get_running_loop()
            is_loop_external= True
        except RuntimeError:
            loop = asyncio.new_event_loop()
        return loop, is_loop_external

    def send_entry(
            self,
            entry: MeterEntryArgs,
            max_attempts = 10
    ) -> None:
        posted = False
        attempts = 0

        # NOTE This logic is to ensure that the thread is running when we try to post
        if not (self.thread is not None and self.thread.is_alive()):
            self.thread = self.start()
        
        # NOTE: We want to be async compatible so we need to check if we're in a loop's context
        # if we're not we'll shut out loop down after we're done
        with ThreadPoolExecutor(1) as executor:
            while not posted:
                try:
                    if attempts >= max_attempts:
                        raise AnchioMaxEnqueuedAttempts
                    # NOTE: We automatically round the max_queue_size to the nearest 10th
                    # of the max to prevent the queue from getting too large or getting to close to the
                    # max size
                    executor.submit(asyncio.run, self.queue.put(self.process_entry(entry))).result()
                    if self.queue.qsize() > self.max_queue_size - 1:
                        raise Full
                    posted = True
                except Full:
                    sync_sleep(1)
                    attempts += 1


    async def async_send_entry(
            self,
            entry: MeterEntryArgs,
            max_attempts = 10
    ) -> None:
        posted = False
        attempts = 0

        # NOTE This logic is to ensure that the thread is running when we try to post
        if not (self.thread is not None and self.thread.is_alive()):
            self.thread = self.start()
        
        # NOTE: We want to be async compatible so we need to check if we're in a loop's context
        # if we're not we'll shut out loop down after we're done
        while not posted:
            try:
                if attempts >= max_attempts:
                    raise AnchioMaxEnqueuedAttempts
                # NOTE: We automatically round the max_queue_size to the nearest 10th
                # of the max to prevent the queue from getting too large or getting to close to the
                # max size
                await self.queue.put(self.process_entry(entry))
                if self.queue.qsize() > self.max_queue_size - 1:
                    raise Full
                posted = True
            except Full:
                sync_sleep(1)
                attempts += 1
                await self.post_entries()

    def wrap_client(self, client: httpx.Client) -> DefaultApi:
        def request(callable):
            @wraps(callable)
            def wrapper(*args, **kwargs):
                self.send_entry(
                    {
                        "value": 1,
                        "service": client.__qualname__
                    }
                )
                return callable(*args, **kwargs)
            
            return wrapper
        client.put = request(client.put)
        client.get = request(client.get)
        client.patch = request(client.patch)
        client.post = request(client.post)
        client.delete = request(client.delete)
        client.options = request(client.options)
        client.head = request(client.head)

        return client
    
    def wrap_async_client(self, client: httpx.AsyncClient) -> DefaultApi:
        def request(callable):
            @wraps(callable)
            async def wrapper(*args, **kwargs):
                self.send_entry(
                    {
                        "value": 1,
                    }
                )
                return await callable(*args, **kwargs)
            return wrapper
        client.put = request(client.put)
        client.get = request(client.get)
        client.patch = request(client.patch)
        client.post = request(client.post)
        client.delete = request(client.delete)
        client.options = request(client.options)
        client.head = request(client.head)

        return client

__all__ = [
    "AnchioInit"
]
