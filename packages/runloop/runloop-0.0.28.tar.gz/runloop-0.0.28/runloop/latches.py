from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, Protocol, Type, TypeVar

from pydantic import BaseModel

# from runloop.typing import make_runloop_pydantic_type

# Define a type variable that is bound to BaseModel or any subclass of it
LatchType = TypeVar("LatchType", bound=BaseModel)


@dataclass
class TimeFulfillment:
    time_ms: int


FunctionOutput = TypeVar("FunctionOutput")


@dataclass
class FunctionCompleteFulfillment(Generic[FunctionOutput]):
    output_type: Type[FunctionOutput]


@dataclass
class ApiFulfillment(Generic[LatchType]):
    # Reference to the type of object in python.
    type: Type[LatchType]


@dataclass
class LatchFulfillmentResult(Protocol):
    pass


@dataclass
class TimeFulfillmentResult(LatchFulfillmentResult):
    time_ms: int


@dataclass
class FunctionCompleteFulfillmentResult(LatchFulfillmentResult, Generic[FunctionOutput]):
    output: FunctionOutput


@dataclass
class ApiFulfillmentResult(LatchFulfillmentResult, Generic[LatchType]):
    # Reference to the type of object in python.
    result: LatchType


LatchResultType = TypeVar("LatchResultType", bound=LatchFulfillmentResult)


class Latch(ABC, Generic[LatchResultType]):
    """The Runloop Latch type provides a way to wait for a specific event to occur before continuing execution."""

    # Constructor initialization with latch ID
    def __init__(self, latch_id: str, latch_name: str):
        self.latch_id = latch_id
        self.latch_name = latch_name

    @abstractmethod
    def await_result(self) -> LatchResultType:
        """Wait for the latch to be completed."""
        raise NotImplementedError()
