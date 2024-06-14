import inspect
import json
import typing
from inspect import Signature
from typing import Any, Type, TypeVar, get_args, get_origin, get_type_hints

from pydantic import BaseModel, TypeAdapter, create_model

from runloop.manifest.manifest import (
    ArrayType,
    DictionaryType,
    FunctionSchemaJson,
    ModelChildren,
    RunloopParameter,
    RunloopType,
    SessionType,
)

from .scheduler import Scheduler
from .session import Session
from .system_coordinator import SystemCoordinator

# Representation of types as strings
_bytes_type_literal = "bytes"
_float_type_literal = "float"
_string_type_literal = "string"
_int_type_literal = "int"
_bool_type_literal = "boolean"
_array_type_literal = "array"
_dict_type_literal = "dictionary"
_model_type_literal = "model"

_scalar_type_map = {
    str: _string_type_literal,
    int: _int_type_literal,
    bool: _bool_type_literal,
    bytes: _bytes_type_literal,
    float: _float_type_literal,
}


# null type allowed only as return types
_null_type_literal = "null"
_session_type_literal = "session"
_scheduler_type_literal = "scheduler"
_system_coordinator_type_literal = "system_coordinator"
_typed_dict_literal = "typed_dictionary"

# NOTE: not supported: set, tuple, bytearray
# NOTE: bytearray not supported due to no built-in pydantic support for bytearray, leading to
# further complication in pydantic modeling / serialization

# Instance of supported scalar types
_supported_scalars = [str, int, bool, bytes, float]
# Type annotation for supported scalar types
_supported_scalar_type = int | str | bool | float | bytes
SupportedTypes = _supported_scalar_type | BaseModel | dict | list


def generate_rpc_json_schema(func) -> FunctionSchemaJson:
    # Extract out the json schema by create pydantic models for the request/response
    # Then use pydantic helpers to generate the json schema
    sig = inspect.signature(func)
    # TODO use type hints instead so uers don't have to explicitly type things maybe
    # type_hints = get_type_hints(func)
    return_annotation = sig.return_annotation
    if return_annotation == inspect.Signature.empty:
        # Infer None return type
        return_annotation = None

    sig_parameters = sig.parameters.values()

    def filter_out_function_provided_paramters(param_annotation):
        if (
            param_annotation is Scheduler
            or (param_annotation is SystemCoordinator)
            or (typing.get_origin(param_annotation) is Session)
        ):
            return False
        return True

    # We have to filter out any types we inject into the function from the runloop platform
    filtered_parameters = [
        param for param in sig_parameters if filter_out_function_provided_paramters(param.annotation)
    ]
    request_fields = {param.name: (param.annotation, ...) for param in filtered_parameters}
    request_model = create_model(func.__name__ + "RequestModel", **request_fields)  # type: ignore  # noqa: PGH003
    response_model = TypeAdapter(type=return_annotation)
    rpc_json_schema = FunctionSchemaJson(
        request_json_schema=json.dumps(request_model.model_json_schema()),
        response_json_schema=json.dumps(response_model.json_schema()),
    )
    return rpc_json_schema


def _make_scalar_type(param_type: _supported_scalar_type) -> RunloopType:
    if param_type not in _supported_scalars:
        raise TypeError(f"Unsupported Runloop type={param_type}")
    return RunloopType(type_name=_scalar_type_map[param_type], annotation=param_type)


def _make_array_type(annotation: type[Any]) -> RunloopType:
    type_args = get_args(annotation)
    if len(type_args) != 1:
        raise TypeError(f"list type must have key and value type annotations={annotation}")

    return RunloopType(
        type_name=_array_type_literal,
        annotation=annotation,
        array=ArrayType(element_type=_make_runloop_type(type_args[0])),
    )


def _make_dict_type(annotation: type[Any]) -> RunloopType:
    type_args = get_args(annotation)
    if len(type_args) != 2:
        raise TypeError(f"dict type must have key and value type annotations={annotation}")

    if type_args[0] not in _supported_scalars:
        raise TypeError(f"dict key type must be one simple supported type={_supported_scalars}")

    return RunloopType(
        type_name=_dict_type_literal,
        annotation=annotation,
        dictionary=DictionaryType(
            key_type=_make_runloop_type(type_args[0]), value_type=_make_runloop_type(type_args[1])
        ),
    )


def _make_model_type(annotation: type[Any]) -> RunloopType:
    children = [
        make_runloop_parameter(field_name, field_info.annotation)
        for (field_name, field_info) in annotation.__fields__.items()
    ]
    return RunloopType(type_name=_model_type_literal, annotation=annotation, model=ModelChildren(children=children))


def _make_typed_dict_type(annotation: type[Any]) -> RunloopType:
    type_hints = get_type_hints(annotation)
    children = [make_runloop_parameter(field_name, field_type) for (field_name, field_type) in type_hints.items()]
    return RunloopType(
        type_name=_typed_dict_literal, annotation=annotation, typed_dictionary=ModelChildren(children=children)
    )


def _make_session_type(annotation: type[Any]) -> RunloopType:
    session_type = get_args(annotation)
    kv_type = _make_runloop_type(session_type[0])
    # TODO: Session parsing incomplete
    return RunloopType(type_name=_session_type_literal, annotation=Session, session=SessionType(kv_type=kv_type))


def _make_scheduler_type() -> RunloopType:
    return RunloopType(type_name=_scheduler_type_literal, annotation=Scheduler)


def _make_system_coordinator_type() -> RunloopType:
    return RunloopType(type_name=_system_coordinator_type_literal, annotation=SystemCoordinator)


def _make_runloop_type(annotation: Any | None) -> RunloopType:
    if annotation is None:
        raise TypeError("type of None not supported, type must be annotated")

    origin = get_origin(annotation)
    if origin is None:
        if annotation in _supported_scalars:
            return _make_scalar_type(annotation)
        elif issubclass(annotation, BaseModel):
            return _make_model_type(annotation)
        elif annotation == dict:
            # dict without type hints, ie dict class
            raise TypeError("dict type must explicitly declare key value types")
        elif annotation == list:
            # list without type hints, ie dict class
            raise TypeError("list type must explicitly declare key value types")
        elif issubclass(annotation, Scheduler):
            return _make_scheduler_type()
        elif issubclass(annotation, SystemCoordinator):
            return _make_system_coordinator_type()
        # TODO: Restore typed_dicts
        # elif type(annotation) == typing_extensions.TypedDict:
        #     return _make_typed_dict_type(annotation)
        else:
            raise TypeError(f"Unsupported Runloop type={annotation}")
    elif origin == Session:
        return _make_session_type(annotation)
    elif origin == list:
        return _make_array_type(annotation)
    elif origin == dict:
        return _make_dict_type(annotation)
    else:
        raise TypeError(f"Unsupported Runloop type={annotation}")


def make_runloop_parameter(name: str, annotation: Type[Any]) -> RunloopParameter:
    return RunloopParameter(name=name, type=_make_runloop_type(annotation))


def make_runloop_return_type(annotation: Any | None) -> RunloopType:
    # none type supported for return types only, where annotation is None (explicit)
    # or annotation is Signature.empty (omitted)
    if annotation is None or annotation == Signature.empty:
        return RunloopType(type_name=_null_type_literal, annotation=None)
    return _make_runloop_type(annotation)


PydanticType = TypeVar("PydanticType", bound=BaseModel)


def make_runloop_pydantic_type(annotation: Type[PydanticType]) -> RunloopType:
    return _make_runloop_type(annotation)
