

from typing import NotRequired, TypedDict


class MeterEntryArgs(TypedDict):
    value: int
    start: NotRequired[str]
    end: NotRequired[str]
    service: NotRequired[str]
    id: NotRequired[str]