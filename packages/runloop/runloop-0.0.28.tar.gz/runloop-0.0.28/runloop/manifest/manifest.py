from typing import Any, Callable, Generic, List, ParamSpec, TypeVar, Union

from pydantic import BaseModel, Field

# forward declaration
RunloopParameter = TypeVar("RunloopParameter")
RunloopType = TypeVar("RunloopType")


class DictionaryType(BaseModel):
    key_type: RunloopType
    value_type: RunloopType


class ModelChildren(BaseModel):
    children: List[RunloopParameter]


class ArrayType(BaseModel):
    element_type: RunloopType


class SessionType(BaseModel):
    kv_type: RunloopType


class RunloopType(BaseModel):
    type_name: str
    # TODO: Ensure continued compatibility among supported python versions
    annotation: Any = Field(None, exclude=True)
    typed_dictionary: Union[None, ModelChildren] = None
    dictionary: Union[None, DictionaryType] = None
    array: Union[None, ArrayType] = None
    model: Union[None, ModelChildren] = None
    session: Union[None, SessionType] = None


class RunloopParameter(BaseModel):
    name: str
    type: RunloopType


class FunctionSchemaJson(BaseModel):
    request_json_schema: str
    response_json_schema: str


class FunctionDescriptor(BaseModel):
    name: str
    module: str
    parameters: List[RunloopParameter]
    return_type: RunloopType
    rpc_json_schema: FunctionSchemaJson


O = TypeVar("O")
P = ParamSpec("P")


class FunctionInvocation(Generic[O]):
    """A FunctionInvocation represents an intent to invoke a given function with the provider parameters.

    The FunctionInvocation, once created, can be passed to any Runloop compute operators
    to be executed at a later time.
    """

    def __init__(
        self, fn: Callable[P, O], args, kwargs, parameters: str, descriptor: FunctionDescriptor, session_id: str | None
    ):
        self._fn = fn
        self._args = args
        self._kwargs = kwargs
        self.descriptor = descriptor
        self._parameters = parameters
        self.session_id = session_id

    def invoke(self) -> O:
        return self._fn(*self._args, **self._kwargs)

    def parameters(self) -> str:
        """Return a flattened JSON string representation of the function invocation parameters."""
        return self._parameters


class ExternalLatchType(BaseModel):
    name: str
    type: RunloopType


class RunloopManifest(BaseModel):
    functions: List[FunctionDescriptor] = []
    external_latch_types: List[ExternalLatchType] = []

    def register_function(self, function: FunctionDescriptor):
        self.functions.append(function)

    def register_external_latch_type(self, latch_type: ExternalLatchType):
        self.external_latch_types.append(latch_type)


runloop_manifest: RunloopManifest = RunloopManifest()
