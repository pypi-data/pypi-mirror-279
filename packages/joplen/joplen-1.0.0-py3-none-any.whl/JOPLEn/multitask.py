from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from typing import Callable, Sequence

import jax.numpy as jnp
from jax import jit
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import pyplot as plt
from numpy.random import RandomState
from sklearn.exceptions import NotFittedError
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
from tqdm import tqdm

from .enums import DTYPE, LossType, NormType
from .partitioner import Partitioner, VPartition, numpify
from .proj_l1_ball import euclidean_proj_l1ball
from .st_loss import LogisticLoss, SquaredError


def core_l21_prox(
    v: jnp.ndarray,
    lam: float,
) -> jnp.ndarray:
    """Compute the proximal operator of the l2,1 norm.

    Args:
        v (jnp.ndarray): The input vector.
        lam (float): The regularization parameter.

    Returns:
        jnp.ndarray: The proximal operator of the l2,1 norm.
    """
    norm = jnp.linalg.norm(v, axis=(0, 2), keepdims=True, ord="fro")
    return jnp.maximum(1 - lam / norm, 0) * v


def task_l21_prox(
    v: jnp.ndarray,
    lam: float,
) -> jnp.ndarray:
    """Compute the proximal operator of the l2,1 norm.

    Args:
        v (jnp.ndarray): The input vector.
        lam (float): The regularization parameter.

    Returns:
        jnp.ndarray: The proximal operator of the l2,1 norm.
    """
    norm = jnp.linalg.norm(v, axis=2, keepdims=True, ord=2)
    return jnp.maximum(1 - lam / norm, 0) * v


def core_l21_norm(
    v: jnp.ndarray,
) -> float:
    """Compute the l2,1 norm where the 2 norm is computed over all cells and tasks.

    Args:
        v (jnp.ndarray): The input vector.
        lam (float): The regularization parameter.

    Returns:
        float: The l2,1 norm.
    """
    return jnp.linalg.norm(v, axis=(0, 2), ord="fro").reshape(-1)


def task_l21_norm(
    v: jnp.ndarray,
) -> jnp.ndarray:
    """Compute the l2,1 norm where the 2 norm is computed over all cells and tasks.

    Args:
        v (jnp.ndarray): The input vector.
        lam (float): The regularization parameter.

    Returns:
        float: The l2,1 norm.
    """
    return jnp.linalg.norm(v, axis=-1, ord=2)


def sq_fnorm(v: jnp.ndarray) -> float:
    """Compute the squared frobenius norm of the input vector.

    Args:
        v (jnp.ndarray): The input vector.

    Returns:
        float: The squared frobenius norm.
    """
    return float(jnp.sum(v**2))


def task_linf1_prox(
    v: jnp.ndarray,
    lam: float,
) -> jnp.ndarray:
    """Compute the linf,1 proximal operator, where the inf norm is computed over
    all cells and each task invidivually.

    Args:
        v (jnp.ndarray): The input vector. Has shape (n_t, n_f, n_c*n_p)
        lam (float): The regularization parameter.

    Returns:
        jnp.ndarray: The projected vector.
    """

    for t in range(v.shape[0]):
        v = v.at[t].set(euclidean_proj_l1ball(v[t] / lam))

    return v


def core_linf1_prox(
    v: jnp.ndarray,
    lam: float,
) -> jnp.ndarray:
    """Compute the linf,1 proximal operator, where the inf norm is computed over
    all cells and tasks together.

    Args:
        v (jnp.ndarray): The input vector.
        lam (float): The regularization parameter.

    Returns:
        jnp.ndarray: The projected vector.
    """
    # (n_t, n_f, n_c*n_p) -> (n_f, n_t * n_c * n_p) and back so that
    # the 1 norm is computed over all cells and tasks. This is easier than trying
    # to compute the proximal operator over a 3D tensor.
    v = jnp.moveaxis(v, 0, 1)
    v_shape = v.shape
    v = v.reshape(v_shape[0], -1)

    v -= lam * euclidean_proj_l1ball(v / lam)

    v = v.reshape(*v_shape)
    return jnp.moveaxis(v, 1, 0)


def core_linf1_norm(
    v: jnp.ndarray,
) -> jnp.ndarray:
    """Compute the linf,1 norm where the inf norm is computed over all cells and
    tasks together.

    Args:
        v (jnp.ndarray): The input vector.

    Returns:
        float: The linf,1 norm.
    """
    return jnp.sum(jnp.max(jnp.abs(v), axis=2), axis=0)


def task_linf1_norm(
    v: jnp.ndarray,
) -> float:
    """Compute the linf,1 norm where the inf norm is computed over all cells and
    tasks together.

    Args:
        v (jnp.ndarray): The input vector.

    Returns:
        float: The linf,1 norm.
    """
    return jnp.max(jnp.abs(v), axis=-1)


class MTJOPLEn:
    def __init__(
        self: MTJOPLEn,
        partitioner: type[Partitioner],
        n_cells: int = 1,
        n_partitions: int = 1,
        random_state: int | RandomState = 0,
        part_kwargs: dict[str, int] | None = None,
        is_regression: bool = True,
    ) -> None:
        if not issubclass(partitioner, Partitioner):
            raise ValueError("Value of partitioner must be a subclass of Partitioner.")

        if n_cells == 1 and n_partitions > 1:
            raise RuntimeWarning(
                "Multiple partitions with a single cell is redundant and will only increase execution time."
            )

        if n_cells < 1:
            raise ValueError("Number of cells must be greater than 0.")
        if n_partitions < 1:
            raise ValueError("Number of partitions must be greater than 0.")

        self.pclass = partitioner
        self.n_cells = n_cells
        self.n_partitions = n_partitions
        self.partitioners: list[Partitioner] | None = None
        self.cws: list[jnp.ndarray] | None = None
        self.cwb: list[jnp.ndarray] | None = None
        self.x_scalers: list[StandardScaler] | None = None
        self.y_scalers: list[StandardScaler] | None = None
        self.part_kwargs: dict[str, int] | None = part_kwargs or {}
        self.is_regression = is_regression
        self.loss = SquaredError() if is_regression else LogisticLoss()

        if not isinstance(random_state, RandomState):
            self.random_state: RandomState = RandomState(random_state)
        else:
            self.random_state: RandomState = random_state

    def _create_partitioners(
        self: MTJOPLEn,
        lst_x: list[np.ndarray],
        lst_y: list[np.ndarray],
    ) -> list[Partitioner]:
        """Create the partitioners for each round.

        Args:
            self (JOPLEn): The JOPLEn object.
            lst_x (list[np.ndarray]): The input data as a list. Each element of
                the list is a numpy array of shape (n_samples, n_features). They
                do not have to have the same dimensionality
            lst_y (list[np.ndarray]): The input labels. See x for more details.
        """
        partitioners = []

        for x, y in tqdm(zip(lst_x, lst_y), total=len(lst_x), desc="Partition tasks"):
            partitioners.append(
                self.pclass(
                    x,
                    y,
                    self.n_cells,
                    self.n_partitions,
                    LossType.regression,
                    self.random_state.randint(0, 2**32 - 1),
                    **self.part_kwargs,
                )
            )

        return partitioners

    def _get_cells(
        self: MTJOPLEn,
        x: np.ndarray,
        task_idx: int,
    ) -> jnp.ndarray:
        """Get the partitions for each round.

        Args:
            self (JOPLEn): The JOPLEn object.
            x (jnp.ndarray): The input data.
            task_idx (int): The index of the task.

        Returns:
            jnp.ndarray: A n_points x n_partitions array of partition indices.
        """
        if self.partitioners is None:
            raise ValueError("Must fit the model before getting partitions.")

        partitioner = self.partitioners[task_idx]
        p_idx = partitioner.partition(x)
        p_idx = p_idx + np.arange(self.n_partitions) * self.n_cells

        binary_mask = np.zeros((x.shape[0], self.n_partitions * self.n_cells))
        binary_mask[np.arange(x.shape[0])[:, None], p_idx] = 1

        return jnp.asarray(binary_mask, dtype=DTYPE)

    def add_bias(self: MTJOPLEn, x: np.ndarray) -> np.ndarray:
        """Add a bias term to the input data.

        Args:
            x (np.ndarray): The input data.

        Returns:
            np.ndarray: The input data with a bias term.
        """
        return np.hstack((x, np.ones((x.shape[0], 1), dtype=DTYPE)))

    def fit(
        self: MTJOPLEn,
        lst_x: list[np.ndarray],
        lst_y: list[np.ndarray],
        lam_core: float = 0.001,
        lam_task: float = 0.001,
        mu: float = 0.001,
        max_iters: int = 1000,
        print_epochs: int = 100,
        verbose: bool = True,
        lst_val_x: list[np.ndarray] | None = None,
        lst_val_y: list[np.ndarray] | None = None,
        threshold: float = 1e-3,
        norm_type: NormType = NormType.L21,
        core_alpha: float = 0.001,
        task_alpha: float = 0.001,
        rel_lr: Sequence[float] | None = None,
    ) -> dict[str, list[float]]:
        """Fit the JOPLEn model.

        Args:
            self (JOPLEn): The JOPLEn object.
            x (list[np.ndarray]): The input data as a list. Each element of the
                list is a numpy array of shape (n_samples, n_features). They do
                not have to have the same dimensionality
            y (list[np.ndarray]): The input labels. See x for more details.
            lam_core (float, optional): The regularization parameter for the
                core weights. Defaults to 0.001.
            lam_task (float, optional): The regularization parameter for the
                task weights. Defaults to 0.001.
            mu (float, optional): The step size. Defaults to 0.001.
            max_iters (int, optional): The maximum number of iterations.
                Defaults to 1000.
            print_epochs (int, optional): The number of epochs between each
                logging. Defaults to 100.
            verbose (bool, optional): Whether to print the logs. Defaults to
                True.
            lst_val_x (Union[list[np.ndarray], None], optional): The validation
                input data. Defaults to None.
            lst_val_y (Union[list[np.ndarray], None], optional): The validation
                input labels. Defaults to None.
            prox (Callable[[jnp.ndarray, float], jnp.ndarray], optional): The
            threshold (float, optional): The threshold for a feature to be
                considered selected. Defaults to 1e-3.
            core_prox (Callable[[jnp.ndarray, float], jnp.ndarray], optional):
                The proximal operator for the core weights. Defaults to
                core_l21_prox.
            task_prox (Callable[[jnp.ndarray, float], jnp.ndarray], optional):
                The proximal operator for the task weights. Defaults to
                task_l21_prox.
        """
        # Rescale/preprocess the data
        lst_x = [numpify(x) for x in lst_x]
        lst_y = [numpify(y) for y in lst_y]

        self.x_scalers = [StandardScaler().fit(x) for x in lst_x]
        self.y_scalers = [StandardScaler().fit(y) for y in lst_y]

        lst_x = [xs.transform(x) for xs, x in zip(self.x_scalers, lst_x)]
        lst_y = [ys.transform(y) for ys, y in zip(self.y_scalers, lst_y)]

        # fit the partitioners and cache the partitions
        self.partitioners = self._create_partitioners(lst_x, lst_y)
        lst_s = [self._get_cells(x, i) for i, x in enumerate(lst_x)]

        lst_x_aug = list(map(self.add_bias, lst_x))

        # Move the training data to the GPU
        lst_x_aug = [jnp.asarray(x, dtype=DTYPE) for x in lst_x_aug]
        lst_y = [jnp.asarray(y, dtype=DTYPE) for y in lst_y]

        del lst_x

        if lst_val_x is not None and lst_val_y is not None:
            lst_val_x = [numpify(x) for x in lst_val_x]
            lst_val_y = [numpify(y) for y in lst_val_y]

            lst_val_x = [xs.transform(x) for xs, x in zip(self.x_scalers, lst_val_x)]
            lst_val_y = [ys.transform(y) for ys, y in zip(self.y_scalers, lst_val_y)]

            lst_val_s = [self._get_cells(x, i) for i, x in enumerate(lst_val_x)]

            lst_val_x = [jnp.asarray(x, dtype=DTYPE) for x in lst_val_x]
            lst_val_y = [jnp.asarray(y, dtype=DTYPE) for y in lst_val_y]

            lst_val_x = list(map(self.add_bias, lst_val_x))
        else:
            lst_val_x = None
            lst_val_y = None
            lst_val_s = None

        lst_wb_prev = jnp.zeros(
            (
                len(lst_x_aug),
                lst_x_aug[0].shape[1],
                self.n_partitions * self.n_cells,
            ),
            dtype=DTYPE,
        )
        lst_ws_prev = lst_wb_prev.copy()

        lst_wb_next = lst_wb_prev
        lst_ws_next = lst_ws_prev

        history = defaultdict(list)

        # Reweight the learning rates for each task
        if rel_lr is None:
            sqrt_ds_sizes = [np.sqrt(x.shape[0]) for x in lst_x_aug]
            rel_lr = jnp.asarray(sqrt_ds_sizes, dtype=DTYPE)
        else:
            assert len(rel_lr) == len(
                lst_x_aug
            ), "Must have a learning rate for each task."
            assert all(lr > 0 for lr in rel_lr), "Learning rates must be positive."

            rel_lr = jnp.asarray(rel_lr, dtype=DTYPE)

        rel_lr /= rel_lr.max()

        # set up the proximal operators and norms
        if norm_type == NormType.L21:
            core_prox = core_l21_prox
            task_prox = task_l21_prox
            core_norm = core_l21_norm
            task_norm = task_l21_norm
        elif norm_type == NormType.LINF1:
            core_prox = core_linf1_prox
            task_prox = task_linf1_prox
            core_norm = core_linf1_norm
            task_norm = task_linf1_norm

        t_curr = 1
        t_next = 1

        # proximal gradient descent
        for i in range(max_iters):
            lst_wb_tmp = lst_wb_next
            lst_ws_tmp = lst_ws_next

            t_next = (1 + jnp.sqrt(1 + 4 * t_curr**2)) / 2
            beta = (t_curr - 1) / t_next

            for j in range(len(lst_x_aug)):
                # Perform accelerated gradient descent
                momentum_b = lst_wb_next[j] + beta * (lst_wb_next[j] - lst_wb_prev[j])
                momentum_s = lst_ws_next[j] + beta * (lst_ws_next[j] - lst_ws_prev[j])

                grad_update = mu * self.loss.grad(
                    momentum_b + momentum_s,
                    lst_x_aug[j],
                    lst_y[j],
                    lst_s[j],
                )

                # lst_wb_next[j] -= rel_lr[j] * grad_update
                # lst_ws_next[j] -= rel_lr[j] * grad_update
                lst_wb_next = lst_wb_next.at[j].set(
                    lst_wb_next[j] - rel_lr[j] * grad_update
                )
                lst_ws_next = lst_ws_next.at[j].set(
                    lst_ws_next[j] - rel_lr[j] * grad_update
                )

                if core_alpha > 0:
                    # lst_wb_next[j, :-1] -= mu * core_alpha * momentum_b[:-1]
                    lst_wb_next = lst_wb_next.at[j].set(
                        lst_wb_next[j] - mu * core_alpha * momentum_b
                    )
                if task_alpha > 0:
                    # lst_ws_next[j, :-1] -= mu * task_alpha * momentum_b[:-1]
                    lst_wb_next = lst_wb_next.at[j].set(
                        lst_wb_next[j] - mu * task_alpha * momentum_s
                    )

            # apply proximal operator
            if lam_core > 0:
                # lst_wb_next[:, :-1] = core_prox(lst_wb_next[:, :-1], mu * lam_core)
                lst_wb_next = lst_wb_next.at[:, :-1].set(
                    core_prox(lst_wb_next[:, :-1], mu * lam_core)
                )
            if lam_task > 0:
                # lst_ws_next[:, :-1] = task_prox(lst_ws_next[:, :-1], mu * lam_task)
                lst_ws_next = lst_ws_next.at[:, :-1].set(
                    task_prox(lst_ws_next[:, :-1], mu * lam_task)
                )

            lst_wb_prev = lst_wb_tmp
            lst_ws_prev = lst_ws_tmp

            # logging
            if (i + 1) % print_epochs == 0:
                res = self.record_performance(
                    lst_wb_next,
                    lst_ws_next,
                    lst_x_aug,
                    lst_y,
                    lst_s,
                    i,
                    verbose,
                    lst_val_x,
                    lst_val_y,
                    lst_val_s,
                    threshold,
                    core_norm,
                    task_norm,
                    lam_core,
                    lam_task,
                    core_alpha,
                    task_alpha,
                )

                for k, v in res.items():
                    if v is not None:
                        history[k].append(v)

        self.cwb = lst_wb_next
        self.cws = lst_ws_next

        return dict(history)

    def record_performance(
        self: MTJOPLEn,
        lst_wb_next: jnp.ndarray,
        lst_ws_next: jnp.ndarray,
        lst_x_aug: list[jnp.ndarray],
        lst_y: list[jnp.ndarray],
        lst_s: list[jnp.ndarray],
        i: int,
        verbose: bool,
        lst_val_x: list[jnp.ndarray] | None,
        lst_val_y: list[jnp.ndarray] | None,
        lst_val_s: list[jnp.ndarray] | None,
        threshold: float,
        core_norm: Callable[[jnp.ndarray], float],
        task_norm: Callable[[jnp.ndarray], float],
        lam_core: float,
        lam_task: float,
        core_alpha: float,
        task_alpha: float,
    ) -> dict[str, tuple[float, ...] | float]:
        tmp_hist = []
        loss_strs = []
        raw_loss = []

        for j in range(len(lst_x_aug)):
            loss_next = self._score(
                lst_wb_next[j] + lst_ws_next[j],
                lst_x_aug[j],
                lst_y[j],
                lst_s[j],
                j,
            )
            raw_loss.append(
                self.loss(
                    lst_wb_next[j] + lst_ws_next[j],
                    lst_x_aug[j],
                    lst_y[j],
                    lst_s[j],
                )
            )

            tmp_hist.append(loss_next)
            loss_strs.append(f"{loss_next:.6f}")

        current_time = datetime.now().strftime("%H:%M:%S")
        report_str = f"[{current_time}]:"

        report_str += f" Epoch {i + 1:>6d} | TrL: {', '.join(loss_strs)}"

        if lst_val_x is not None and lst_val_y is not None:
            tmp_hist_val = []
            val_loss_strs = []
            for j in range(len(lst_val_x)):
                val_loss = self._score(
                    lst_wb_next[j] + lst_ws_next[j],
                    lst_val_x[j],
                    lst_val_y[j],
                    lst_val_s[j],
                    j,
                )
                val_loss_strs.append(f"{val_loss:.6f}")
                tmp_hist_val.append(val_loss)
            report_str += f" | VaL: {', '.join(val_loss_strs)}"
            val_loss = tuple(tmp_hist_val)
        else:
            val_loss = None

        wb_norm = core_norm(lst_wb_next[:, :-1])
        ws_norm = task_norm(lst_ws_next[:, :-1])
        wb_norm_sum = float(wb_norm.sum())
        ws_norm_sum = float(ws_norm.sum())

        report_str += f" | CNorm: {float(wb_norm_sum):.6f}"
        report_str += f" | TNorm: {float(ws_norm_sum):.6f}"

        wb_fnorm = sq_fnorm(lst_wb_next[:, :-1])
        wb_fnorm = sq_fnorm(lst_ws_next[:, :-1])
        report_str += f" | CFNorm: {wb_fnorm:.6f}"
        report_str += f" | TFNorm: {wb_fnorm:.6f}"

        wb_sel_idx = wb_norm > threshold
        ws_sel_idx = ws_norm > threshold
        ws_sel_idx = ws_sel_idx & ~wb_sel_idx
        ws_sel_idx_str = ", ".join([f"{w.sum():>4d}" for w in ws_sel_idx])
        report_str += f" | WbNz: {wb_sel_idx.sum():>4d}"
        report_str += f" | WsNz: {ws_sel_idx_str}"

        b_n_features = float(wb_sel_idx.sum())
        s_n_features = tuple([float(w.sum()) for w in ws_sel_idx])
        train_loss = tuple(tmp_hist)

        # Compensate since all terms are scaled by P for the gradient
        objective = sum(raw_loss)
        objective += lam_core * wb_norm_sum
        objective += lam_task * ws_norm_sum
        objective += core_alpha * wb_fnorm
        objective += task_alpha * wb_fnorm

        if verbose:
            print(report_str)

        return {
            "train_loss": train_loss,
            "raw_loss": raw_loss,
            "val_loss": val_loss,
            "wb_norm": wb_norm_sum,
            "ws_norm": ws_norm_sum,
            "b_n_features": b_n_features,
            "s_n_features": s_n_features,
            "wb_fnorm": wb_fnorm,
            "wb_fnorm": wb_fnorm,
            "objective": objective,
        }

    def _score(
        self: MTJOPLEn,
        w: jnp.ndarray,
        x: jnp.ndarray,
        y_true: jnp.ndarray,
        s: jnp.ndarray,
        task_idx: int,
    ) -> float:
        """Compute the loss function.

        Args:
            self (JOPLEn): The JOPLEn object.
            w (jnp.ndarray): The weight matrix.
            x (jnp.ndarray): The input data.
            y (jnp.ndarray): The input labels.
            s (jnp.ndarray): The partition matrix.
            task_idx (int): The index of the task.

        Returns:
            float: The loss value.
        """
        y_pred = np.array(self.loss.predict(w, x, s))
        y_pred = self.y_scalers[task_idx].inverse_transform(y_pred)

        y_true = self.y_scalers[task_idx].inverse_transform(np.array(y_true))

        return float(mean_squared_error(y_true, y_pred, squared=False))

    def predict(self: MTJOPLEn, x: jnp.ndarray, task_idx: int) -> np.ndarray:
        """Predict the output for the given input and task.

        Args:
            self (JOPLEn): The JOPLEn object.
            x (jnp.ndarray): The input data.
            task_idx (int): The index of the task.

        Returns:
            jnp.ndarray: The predicted output.
        """
        if self.cws is None:
            raise NotFittedError("Must fit the model before predicting.")

        x = numpify(x)

        x = self.x_scalers[task_idx].transform(x)
        s = self._get_cells(x, task_idx)

        x_aug = self.add_bias(x)

        x_aug = jnp.asarray(x_aug)

        y_pred = np.array(
            self.loss.predict(
                self.cwb[task_idx] + self.cws[task_idx],
                x_aug,
                s,
            )
        )
        return self.y_scalers[task_idx].inverse_transform(y_pred)


if __name__ == "__main__":
    import time
    from pathlib import Path
    from pprint import pprint
    from sklearn.datasets import make_regression

    import pandas as pd
    from lightgbm import LGBMRegressor

    # Generate synthetic data for multitask regression
    n_samples = 1000
    n_features = 20
    n_tasks = 3
    noise = 0.1

    np.random.seed(0)

    # Generate synthetic data
    x = np.random.randn(n_samples, n_features)
    tmat = np.random.randn(n_features, n_tasks)
    cmat = np.random.randn(n_features, 1)
    cmat = np.tile(cmat, (1, n_tasks))

    tmat[np.abs(tmat) < 1.5] = 0
    cmat[np.abs(cmat) < 1.5] = 0

    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    axs[0].matshow(cmat)
    axs[1].matshow(tmat)
    plt.show()

    assert cmat.shape == tmat.shape

    w = cmat + tmat  # Generate weight matrix

    noise_vector = noise * np.random.randn(n_samples, n_tasks)  # Generate noise vector

    # Calculate target variable y using matrix multiplication
    y = np.dot(x, w) + noise_vector

    x_train, x_val, x_test = x[:800], x[800:900], x[900:]
    y_train, y_val, y_test = y[:800], y[800:900], y[900:]

    print(x_train.shape, y_train.shape)

    # Tile the input data for multiple tasks
    x_train = np.tile(x_train, (n_tasks, 1, 1))
    x_val = np.tile(x_val, (n_tasks, 1, 1))
    x_test = np.tile(x_test, (n_tasks, 1, 1))

    # Transpose the targets
    y_train = np.transpose(y_train)
    y_val = np.transpose(y_val)
    y_test = np.transpose(y_test)

    n_cells = 2
    n_partitions = 10
    print_epochs = 100
    lam_task = 0.2
    lam_core = 0.2
    mu = 1e-2
    max_iters = 1000
    norm_type = NormType.L21
    core_alpha = 0.0
    task_alpha = 0.0
    rel_lr = [1] * n_tasks

    def rmse(y_true, y_pred):  # noqa: ANN001, ANN201
        return mean_squared_error(y_true, y_pred, squared=False)

    # get current file path
    path = Path().absolute()

    dummy_pred = []
    for _, ytr, _, yte in zip(x_train, y_train, x_test, y_test):
        dummy = np.mean(ytr)
        y_pred = np.full(yte.shape, dummy)
        dummy_pred.append(rmse(yte, y_pred.flatten()))

    print("Dummy")
    print(dummy_pred)

    lgbm_pred = []
    for xtr, ytr, xte, yte in tqdm(
        zip(x_train, y_train, x_test, y_test), total=n_tasks
    ):
        lgbm = LGBMRegressor(verbose=-1, max_depth=3, n_estimators=100)
        lgbm.fit(xtr, ytr.flatten())
        y_pred = lgbm.predict(xte)
        lgbm_pred.append(rmse(yte, y_pred.flatten()))

    print("LGBM")
    print(lgbm_pred)

    jp = MTJOPLEn(
        VPartition,
        n_cells=n_cells,
        n_partitions=n_partitions,
    )

    start_time = time.time()

    history = jp.fit(
        x_train,
        y_train,
        print_epochs=print_epochs,
        lam_core=lam_core,
        lam_task=lam_task,
        mu=mu,
        max_iters=max_iters,
        verbose=True,
        lst_val_x=x_test,
        lst_val_y=y_test,
        norm_type=norm_type,
        core_alpha=core_alpha,
        task_alpha=task_alpha,
        rel_lr=rel_lr,
    )

    end_time = time.time()

    print("Time:", (end_time - start_time))

    print(len(history["b_n_features"]))

    fig, axs = plt.subplots(1, 3, figsize=(15, 5))
    axs[0].plot(history["raw_loss"])
    axs[1].plot(history["ws_norm"])
    axs[2].plot(history["objective"])

    # set titles
    axs[0].set_title("Raw Training Loss")
    axs[1].set_title("Core Norm")
    axs[2].set_title("Objective Function")

    plt.show()

    core_weights = np.array(jp.cwb)[:, :-1]
    task_weights = np.array(jp.cws)[:, :-1]

    n_tasks, n_feats, n_cells = core_weights.shape
    core_weights = core_weights.transpose(1, 0, 2).reshape(n_feats, -1)
    task_weights = task_weights.transpose(1, 0, 2).reshape(n_feats, -1)

    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    axs[0].matshow(core_weights)
    axs[1].matshow(task_weights)

    axs[0].set_title("Core Weights")
    axs[1].set_title("Task Weights")

    plt.show()

    # get the selected features for each task
    wb_norm = np.linalg.norm(np.array(jp.cwb), axis=(0, 2), ord="fro")[:-1]
    ws_norm = np.linalg.norm(np.array(jp.cws), axis=2, ord=2)[:, :-1]

    wb_sel_idx = wb_norm > 1e-3
    ws_sel_idx = ws_norm > 1e-3
    ws_sel_idx = ws_sel_idx & ~wb_sel_idx

    x_train = [x[:, wb_sel_idx + ws_sel_idx[i]] for i, x in enumerate(x_train)]
    x_test = [x[:, wb_sel_idx + ws_sel_idx[i]] for i, x in enumerate(x_test)]

    masked_pred = []
    for xtr, ytr, xte, yte in zip(x_train, y_train, x_test, y_test):
        lgbm = LGBMRegressor(verbose=-1)
        lgbm.fit(xtr, ytr.flatten())
        y_pred = lgbm.predict(xte)
        masked_pred.append(rmse(yte, y_pred.flatten()))

    # combine into a table using pandas
    print(
        pd.DataFrame(
            {
                "Dummy": dummy_pred,
                "LGBM": lgbm_pred,
                "LGBM via JOPLEn": masked_pred,
            },
        )
    )
