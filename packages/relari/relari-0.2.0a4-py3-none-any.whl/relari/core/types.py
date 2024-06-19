from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, TypedDict, Union

UID = str


def args_to_dict(*args, **kwargs):
    arg_dict = dict(kwargs)
    for index, value in enumerate(args):
        arg_dict[f"_arg{index}"] = value
    return arg_dict


class ToolCall(TypedDict):
    name: str
    kwargs: Dict[str, Any]


class HTTPMethod(str, Enum):
    GET = "get"
    POST = "post"
    PUT = "put"
    DELETE = "delete"


@dataclass(frozen=True, eq=True)
class DatasetDatum:
    label: str
    data: dict

    def asdict(self):
        return {
            "label": self.label,
            "data": self.data,
        }


MetricsArgs = Union[DatasetDatum, Dict[str, Any]]
