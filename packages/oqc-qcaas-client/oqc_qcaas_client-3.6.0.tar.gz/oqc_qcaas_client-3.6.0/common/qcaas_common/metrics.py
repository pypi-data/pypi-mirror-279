import inspect
import re
from inspect import getmembers, ismethod
from typing import Callable, Union

from qcaas_common.logger import get_logger

logger = get_logger(__name__)


class IncrementMutableOutcome:
    def __init__(self):
        self._count: float = 0.0

    def increment(self, amount: float = 1.0):
        self._count += amount

    def __float__(self):
        return self._count

    def __int__(self):
        return int(self._count)


class BinaryMutableOutcome:
    def __init__(self):
        self._success: bool = None

    def succeed(self):
        # Failure is sticky
        if self._success is None or self._success:
            self._success = True

    def fail(self):
        self._success = False

    def __int__(self):
        return int(self._success)

    def __float__(self):
        return 1.0 if self._success else 0.0

    def __eq__(self, other):
        if isinstance(other, BinaryMutableOutcome):
            return other is not None and other._success == self._success
        if isinstance(other, bool):
            return (self is not None and not other) or (other == self._success)


class MetricFieldWrapper:
    def __init__(
        self,
        func: Callable,
        outcome: Union[IncrementMutableOutcome, BinaryMutableOutcome],
    ):
        self.callable = func
        self.outcome = outcome

    def __enter__(self):
        # Loan out the mutable outcome for change
        return self.outcome

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Apply the outcome to target callable
        try:
            self.callable(self.outcome)
        except Exception as ex:
            logger.warning(f"Metric setting errored {str(ex)}")


class MetricExporter:
    """
    Factory for context managers for metrics reporting over different
    backend reporting frameworks

    Dynamically builds member functions that mirror the backend it is given.
    The Backend is the API specification.
    """

    def __init__(self, backend):
        if isinstance(backend, type):
            raise ValueError("Argument must be an instance not a type")
        methods = [
            member
            for member in getmembers(backend, predicate=ismethod)
            if not re.match("^_", member[0])
        ]

        def decorate(f):
            # factory function avoids closure issues
            try:
                sign = inspect.signature(f)
                parameters = sign.parameters
                outcome_param = parameters.get("outcome")
                outcome_type = outcome_param.annotation
                return lambda: MetricFieldWrapper(f, outcome_type())
            except KeyError as ex:
                logger.error(
                    f" An error occurred while processing "
                    f"the function's outcome parameter {ex}"
                )
                raise ex

        for func_name, func in methods:
            nargs = func.__code__.co_argcount
            if not nargs == 2:
                raise ValueError(
                    f"Backends must have one non-self argument on each "
                    f"function. Found {nargs} while evaluating {func_name}"
                    f" on {str(type(backend))}"
                )
            # build no-arg setting functions on this matching backend public name
            setattr(self, func_name, decorate(func))
