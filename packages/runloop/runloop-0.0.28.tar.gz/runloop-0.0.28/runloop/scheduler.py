import abc
from typing import Union, overload

from runloop.latches import (
    ApiFulfillment,
    ApiFulfillmentResult,
    FunctionCompleteFulfillment,
    FunctionCompleteFulfillmentResult,
    FunctionOutput,
    Latch,
    LatchType,
    TimeFulfillment,
    TimeFulfillmentResult,
)
from runloop.manifest.manifest import FunctionInvocation


class Scheduler(abc.ABC):
    """The Runloop Scheduler provides the ability to schedule `function` invocation at a given time in the future.
    # TODO: Flesh out use cases, consider place among other event primitives.
    """

    @abc.abstractmethod
    def schedule_at_time(self, function_invocation: FunctionInvocation, scheduled_time_ms: int) -> str:
        """Schedule a function to be executed."""
        raise NotImplementedError()

    @overload
    @abc.abstractmethod
    def create_latch(self, latch_name: str, fulfillment: TimeFulfillment) -> Latch[TimeFulfillmentResult]:
        ...

    @overload
    @abc.abstractmethod
    def create_latch(
        self, latch_name: str, fulfillment: FunctionCompleteFulfillment[FunctionOutput]
    ) -> Latch[FunctionCompleteFulfillmentResult[FunctionOutput]]:
        ...

    @overload
    @abc.abstractmethod
    def create_latch(
        self, latch_name: str, fulfillment: ApiFulfillment[LatchType]
    ) -> Latch[ApiFulfillmentResult[LatchType]]:
        ...

    @abc.abstractmethod
    def create_latch(
        self,
        latch_name: str,
        fulfillment: Union[FunctionCompleteFulfillment[FunctionOutput], TimeFulfillment, ApiFulfillment[LatchType]],
    ) -> Union[
        Latch[TimeFulfillmentResult],
        Latch[ApiFulfillmentResult[LatchType]],
        Latch[FunctionCompleteFulfillmentResult[FunctionOutput]],
    ]:
        raise NotImplementedError()

    @abc.abstractmethod
    def launch(
        self, function_invocation: FunctionInvocation[FunctionOutput]
    ) -> Latch[FunctionCompleteFulfillmentResult[FunctionOutput]]:
        """Schedule a function to be executed."""
        raise NotImplementedError()
