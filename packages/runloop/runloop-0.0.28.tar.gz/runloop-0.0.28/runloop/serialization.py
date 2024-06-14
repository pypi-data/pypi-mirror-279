import base64
import json

from pydantic import BaseModel

from runloop.typing import SupportedTypes

from .scheduler import Scheduler
from .session import Session
from .system_coordinator import SystemCoordinator

_ignored_runloop_types = [Session, Scheduler, SystemCoordinator]


def _concrete_to_json_compatible(value: SupportedTypes) -> any:
    """Recursively convert a value to a JSON parseable type (ie a value fully able to json.dumps()).
    For scalar types, this is simply the value.
    For BaseModel types, this is the result of model_dump().
    For lists / dicts, this needs to be recursively evaluated.
    """
    if isinstance(value, BaseModel):
        return value.model_dump()
    elif isinstance(value, list):
        # Pull out type, recurse
        return [_concrete_to_json_compatible(x) for x in value]
    elif isinstance(value, dict):
        return {
            k: _concrete_to_json_compatible(v)
            for k, v in value.items()
            if not any(isinstance(v, x) for x in _ignored_runloop_types)
        }
    elif any(isinstance(value, t) for t in _ignored_runloop_types):
        return str(value)
    elif isinstance(value, bytes):
        return base64.encodebytes(value).decode("utf-8")
    return value


def value_to_json_string(value: SupportedTypes) -> str:
    """Convert a value to a fully formed JSON string."""
    if isinstance(value, BaseModel):
        return value.model_dump_json()
    else:
        return json.dumps(_concrete_to_json_compatible(value))
