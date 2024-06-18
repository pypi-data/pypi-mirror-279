"""
Source: https://gist.github.com/daien/1272551/edd95a6154106f8e28209a1c7964623ef8397246

Proximal operator for l_infinity norm: https://math.stackexchange.com/questions/527872/the-proximal-operator-of-the-l-infty-infinity-norm
"""

import jax.numpy as jnp

FLOAT = jnp.float32
INT = jnp.int32


def euclidean_proj_simplex1(v: jnp.ndarray, s: float = 1.0) -> jnp.ndarray:
    assert s > 0, "Radius s must be strictly positive (%d <= 0)" % s
    shape = v.shape
    # get the array of cumulative sums of a sorted (decreasing) copy of v
    u = -jnp.sort(-v, axis=-1)
    cssv = jnp.cumsum(u, axis=-1, dtype=FLOAT)
    # get the number of > 0 components of the optimal solution
    rho = jnp.sum(
        u * jnp.arange(1, shape[-1] + 1, dtype=FLOAT)[None, :] > (cssv - s),
        axis=-1,
        dtype=INT,
    )
    # compute the Lagrange multiplier associated to the simplex constraint
    theta = jnp.divide(
        (cssv[jnp.arange(0, shape[0], dtype=INT), rho] - s), (rho + 1), dtype=FLOAT
    )
    # compute the projection by thresholding v using theta
    return (v - theta[:, None]).clip(min=0)


def euclidean_proj_l1ball(v: jnp.ndarray, s: float = 1.0) -> jnp.ndarray:
    assert s > 0, "Radius s must be strictly positive (%d <= 0)" % s
    # compute the vector of absolute values
    u = jnp.abs(v)
    # check if v is already a solution
    if u.sum() <= s:
        # L1-norm is <= s
        return v
    # v is not already a solution: optimum lies on the boundary (norm == s)
    # project *u* on the simplex
    w = euclidean_proj_simplex1(u, s=s)
    # compute the solution to the original problem on v
    w *= jnp.sign(v)
    return w
