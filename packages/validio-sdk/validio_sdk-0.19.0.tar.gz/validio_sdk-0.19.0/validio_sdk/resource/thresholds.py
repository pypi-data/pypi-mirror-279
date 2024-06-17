"""Threshold configuration."""

from abc import abstractmethod
from typing import Any

from validio_sdk.graphql_client.base_model import BaseModel
from validio_sdk.graphql_client.input_types import (
    ComparisonOperator,
    DecisionBoundsType,
    DifferenceOperator,
    DifferenceThresholdCreateInput,
    DifferenceType,
    DynamicThresholdCreateInput,
    FixedThresholdCreateInput,
    ValidatorWithDifferenceThresholdUpdateInput,
    ValidatorWithDynamicThresholdUpdateInput,
    ValidatorWithFixedThresholdUpdateInput,
)
from validio_sdk.resource._diffable import Diffable
from validio_sdk.resource._serde import NODE_TYPE_FIELD_NAME


class Threshold(Diffable):
    """
    Base class for a threshold configuration.

    https://docs.validio.io/docs/thresholds
    """

    def __init__(self) -> None:
        """Constructor."""
        self._node_type = self.__class__.__name__

    @abstractmethod
    def _immutable_fields(self) -> set[str]:
        pass

    @abstractmethod
    def _mutable_fields(self) -> set[str]:
        pass

    def _nested_objects(self) -> dict[str, Diffable | list[Diffable] | None]:
        return {}

    def _encode(self) -> dict[str, object]:
        return self.__dict__

    @staticmethod
    def _decode(obj: dict[str, Any]) -> "Threshold":
        cls = eval(obj[NODE_TYPE_FIELD_NAME])
        return cls(**{k: v for k, v in obj.items() if k != NODE_TYPE_FIELD_NAME})

    @abstractmethod
    def _api_create_input(self) -> BaseModel:
        pass

    @abstractmethod
    def _api_update_input(self, validator_id: str) -> BaseModel:
        pass


class DifferenceThreshold(Threshold):
    """A dynamic threshold configuration.

    https://docs.validio.io/docs/thresholds#difference-threshold
    """

    def __init__(
        self,
        difference_type: DifferenceType,
        operator: DifferenceOperator,
        number_of_windows: int,
        value: int,
    ):
        """
        Constructor.

        :param difference_type: The type of difference, i.e. absolute or
            percentage
        :param operator: The operator type, e.g. increasing or decreasing
        :param number_of_windows: The number of windows to monitor over
        :param value: The value which steers the bounds
        """
        super().__init__()

        self.difference_type = (
            difference_type
            if isinstance(difference_type, DifferenceType)
            else DifferenceType(difference_type)
        )
        self.operator = (
            operator
            if isinstance(operator, DifferenceOperator)
            else DifferenceOperator(operator)
        )
        self.number_of_windows = number_of_windows
        self.value = value

    def _immutable_fields(self) -> set[str]:
        return set({})

    def _mutable_fields(self) -> set[str]:
        return {"difference_type", "operator", "number_of_windows", "value"}

    def _api_create_input(self) -> BaseModel:
        return DifferenceThresholdCreateInput(
            difference_type=self.difference_type,
            operator=self.operator,
            number_of_windows=self.number_of_windows,
            value=self.value,
        )

    def _api_update_input(self, validator_id: str) -> BaseModel:
        return ValidatorWithDifferenceThresholdUpdateInput(
            validator_id=validator_id,
            difference_type=self.difference_type,
            operator=self.operator,
            number_of_windows=self.number_of_windows,
            value=self.value,
        )


class DynamicThreshold(Threshold):
    """A dynamic threshold configuration.

    https://docs.validio.io/docs/thresholds#dynamic-threshold
    """

    def __init__(
        self,
        sensitivity: float = 3,
        decision_bounds_type: DecisionBoundsType = DecisionBoundsType.UPPER_AND_LOWER,
    ):
        """
        Constructor.

        :param sensitivity: Steers how narrow/wide the threshold's bounds
            (accepted range of values) evolves over time. Typically starts
            at 2 or 3, lower values produce wider bounds while larger values
            produce wider bounds
        :param decision_bounds_type: Configures whether to treat a value deviation
            above (UPPER) or below (LOWER) the boundary as an anomaly.
        """
        super().__init__()

        self.sensitivity = sensitivity
        self.decision_bounds_type = (
            decision_bounds_type
            if isinstance(decision_bounds_type, DecisionBoundsType)
            else DecisionBoundsType(decision_bounds_type)
        )

    def _immutable_fields(self) -> set[str]:
        return set({})

    def _mutable_fields(self) -> set[str]:
        return {"sensitivity", "decision_bounds_type"}

    def _api_create_input(self) -> BaseModel:
        return DynamicThresholdCreateInput(
            sensitivity=self.sensitivity,
            # type: ignore[call-arg]
            decision_bounds_type=self.decision_bounds_type,
        )

    def _api_update_input(self, validator_id: str) -> BaseModel:
        return ValidatorWithDynamicThresholdUpdateInput(
            sensitivity=self.sensitivity,
            # type: ignore[call-arg]
            decision_bounds_type=self.decision_bounds_type,
            # type: ignore[call-arg]
            validator_id=validator_id,
        )


class FixedThreshold(Threshold):
    """A fixed threshold configuration.

    https://docs.validio.io/docs/thresholds#fixed-threshold
    """

    def __init__(
        self,
        value: float,
        operator: ComparisonOperator,
    ):
        """
        Constructor.

        :param value: Threshold value
        :param operator: Operator applied on the threshold value.
        """
        super().__init__()

        self.value = value
        self.operator = (
            operator
            if isinstance(operator, ComparisonOperator)
            else ComparisonOperator(operator)
        )

    def _immutable_fields(self) -> set[str]:
        return set({})

    def _mutable_fields(self) -> set[str]:
        return {"value", "operator"}

    def _api_create_input(self) -> BaseModel:
        return FixedThresholdCreateInput(
            value=self.value,
            operator=self.operator,
        )

    def _api_update_input(self, validator_id: str) -> BaseModel:
        return ValidatorWithFixedThresholdUpdateInput(
            # type: ignore[call-arg]
            validator_id=validator_id,
            value=self.value,
            operator=self.operator,
        )


THRESHOLD_CLASSES: set[type] = {
    DifferenceThreshold,
    DynamicThreshold,
    FixedThreshold,
}
