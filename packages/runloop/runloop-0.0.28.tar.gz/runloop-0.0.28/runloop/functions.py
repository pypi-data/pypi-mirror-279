import inspect
from typing import Any, Callable, Generic, ParamSpec, Type, TypeVar

from pydantic import BaseModel

from runloop.manifest.manifest import (
    ExternalLatchType,
    FunctionDescriptor,
    FunctionInvocation,
    RunloopParameter,
    RunloopType,
    runloop_manifest,
)
from runloop.serialization import value_to_json_string
from runloop.typing import (
    FunctionSchemaJson,
    generate_rpc_json_schema,
    make_runloop_parameter,
    make_runloop_pydantic_type,
    make_runloop_return_type,
)


def _make_function_descriptor(
    func: Callable[..., Any],
    parameters: list[RunloopParameter],
    return_type: RunloopType,
    rpc_json_schema: FunctionSchemaJson,
) -> FunctionDescriptor:
    module = "" if func.__module__ is None else func.__module__
    return FunctionDescriptor(
        name=func.__name__,
        module=module,
        parameters=parameters,
        return_type=return_type,
        rpc_json_schema=rpc_json_schema,
    )


def _extract_function_descriptor(func: Callable[..., Any]) -> FunctionDescriptor:
    sig = inspect.signature(func)
    rpc_json_schema = generate_rpc_json_schema(func)

    parameter_values = sig.parameters.values()
    params = [make_runloop_parameter(param.name, param.annotation) for param in parameter_values]

    return_type = make_runloop_return_type(sig.return_annotation)
    return _make_function_descriptor(func, params, return_type, rpc_json_schema)


def _get_arg_dict(descriptor: FunctionDescriptor, args, kwargs) -> dict[str, Any]:
    """Flatten args with their parameters with kwargs into dict object."""
    arg_dict = {}
    for i, param in enumerate(descriptor.parameters):
        if i < len(args):
            arg_dict[param.name] = args[i]
        else:
            break

    # Roll in kwargs
    arg_dict.update(kwargs)
    return arg_dict


def _session_id_if_present(descriptor: FunctionDescriptor, arg_dict) -> str | None:
    """Find and extract session id from invocation parameters."""
    for i, param in enumerate(descriptor.parameters):
        if param.type.session:
            # TODO: More validation, nice error messaging.
            return arg_dict.get(param.name, None).id
    return None


def _flattened_parameters_to_json(arg_dict: dict[str, Any]) -> str:
    """Convert arg dict into valid json
    TODO: More validation, nice error messaging.
    """
    # Return json string
    return value_to_json_string(arg_dict)


O = TypeVar("O")
P = ParamSpec("P")


class WrappedFunction(Generic[P, O]):
    """A class representing our wrapped function, providing an accessor to the underlying.
    TODO: Trouble with people across proc boundaries, introducing this to work around. See
    if we need this.
    """

    def __init__(self, func: Callable[P, O], descriptor: FunctionDescriptor):
        self.func = func
        self.descriptor = descriptor

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> FunctionInvocation[O]:
        args_as_dict = _get_arg_dict(self.descriptor, args, kwargs)

        session_id = _session_id_if_present(descriptor=self.descriptor, arg_dict=args_as_dict)

        parameters = _flattened_parameters_to_json(arg_dict=args_as_dict)

        return FunctionInvocation(
            fn=self.func,
            args=args,
            kwargs=kwargs,
            descriptor=self.descriptor,
            parameters=parameters,
            session_id=session_id,
        )

    def fn(self) -> Callable[P, O]:
        return self.func


def function(func: Callable[P, O]) -> Callable[P, FunctionInvocation[O]]:
    """Register Runloop async function.

    Raises
    ------
        ValueError: If function signature is invalid

    """
    descriptor = _extract_function_descriptor(func)
    runloop_manifest.register_function(descriptor)

    return WrappedFunction(func, descriptor)


# Define a type variable that is bound to BaseModel or any subclass of it
LatchType = TypeVar("LatchType", bound=BaseModel)


def latch(latch: Type[LatchType]) -> Type[LatchType]:
    """Register Runloop latch type."""
    latch_type = ExternalLatchType(name=latch.__name__, type=make_runloop_pydantic_type(latch))
    runloop_manifest.register_external_latch_type(latch_type)

    return latch
