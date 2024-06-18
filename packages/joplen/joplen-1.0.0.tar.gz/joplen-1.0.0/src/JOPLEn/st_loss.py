from __future__ import annotations

from abc import ABC, abstractmethod

# import jnp
import numpy as np
from sklearn.metrics import mean_squared_error
import jax.numpy as jnp

from JOPLEn.enums import LossType

from .enums import DTYPE


def sigmoid(x: jnp.ndarray) -> jnp.ndarray:
    return jnp.reciprocal(1 + jnp.exp(-x))


class Loss(ABC):
    def __init__(self: Loss, loss_type: LossType) -> None:
        self.loss_type = loss_type

    @abstractmethod
    def __call__(
        self: Loss,
        w: jnp.ndarray,
        x: jnp.ndarray,
        y: jnp.ndarray,
        s: jnp.ndarray,
    ) -> float:
        pass

    @abstractmethod
    def grad(
        self: Loss,
        w: jnp.ndarray,
        x: jnp.ndarray,
        y: jnp.ndarray,
        s: jnp.ndarray,
    ) -> jnp.ndarray:
        pass

    @abstractmethod
    def predict(
        self: Loss,
        w: jnp.ndarray,
        x: jnp.ndarray,
        s: jnp.ndarray,
    ) -> jnp.ndarray:
        pass

    def _raw_output(
        self: Loss,
        w: jnp.ndarray,
        x: jnp.ndarray,
        s: jnp.ndarray,
    ) -> jnp.ndarray:
        return jnp.sum((x @ w) * s, axis=1, keepdims=True)

    @abstractmethod
    def error(
        self: Loss,
        y_true: np.ndarray,
        y_pred: np.ndarray,
    ) -> float:
        pass


class SquaredError(Loss):
    def __init__(self: SquaredError) -> None:
        super().__init__(LossType.regression)

    def __call__(
        self: SquaredError,
        w: jnp.ndarray,
        x: jnp.ndarray,
        y: jnp.ndarray,
        s: jnp.ndarray,
    ) -> float:
        y_pred = self.predict(w, x, s)

        return float(jnp.mean((y_pred - y) ** 2))

    def grad(
        self: SquaredError,
        w: jnp.ndarray,
        x: jnp.ndarray,
        y: jnp.ndarray,
        s: jnp.ndarray,
    ) -> jnp.ndarray:
        y_pred = self._raw_output(w, x, s)
        return x.T @ ((y_pred - y) * s) / x.shape[0]

    def predict(
        self: SquaredError,
        w: jnp.ndarray,
        x: jnp.ndarray,
        s: jnp.ndarray,
    ) -> jnp.ndarray:
        return self._raw_output(w, x, s)

    def error(
        self: SquaredError,
        y_true: np.ndarray,
        y_pred: np.ndarray,
    ) -> float:
        return float(mean_squared_error(y_true, y_pred, squared=False))


class LogisticLoss(Loss):
    def __init__(self: LogisticLoss) -> None:
        super().__init__(LossType.binary_classification)

    def encode(self: LogisticLoss, y: np.ndarray) -> np.ndarray:
        return (y * 2) - 1

    def __call__(
        self: LogisticLoss,
        w: jnp.ndarray,
        x: jnp.ndarray,
        y: jnp.ndarray,
        s: jnp.ndarray,
    ) -> float:
        raw_output = self._raw_output(w, x, s)
        y = self.encode(y)

        return float(jnp.mean(jnp.log(1 + jnp.exp(-y * raw_output))))

    def grad(
        self: LogisticLoss,
        w: jnp.ndarray,
        x: jnp.ndarray,
        y: jnp.ndarray,
        s: jnp.ndarray,
    ) -> jnp.ndarray:
        raw_output = self._raw_output(w, x, s)
        y = self.encode(y)

        return -x.T @ ((y / (jnp.exp(raw_output * y) + 1)) * s) / x.shape[0]

    def predict(
        self: LogisticLoss,
        w: jnp.ndarray,
        x: jnp.ndarray,
        s: jnp.ndarray,
    ) -> jnp.ndarray:
        return sigmoid(self._raw_output(w, x, s))

    def error(
        self: LogisticLoss,
        y_true: np.ndarray,
        y_pred: np.ndarray,
    ) -> float:
        return np.mean((y_true > 0) == (y_pred > 0))
