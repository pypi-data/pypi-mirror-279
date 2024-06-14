"""Vanilla Rate Distortion optimizer."""

import numpy as np

from collections import namedtuple
from scipy.special import logsumexp

from .base import BaseRDOptimizer


##############################################################################
# Return type of each item in `get_results()`
##############################################################################

RateDistortionResult = namedtuple(
    "RateDistortionResult",
    [
        "qxhat_x",
        "rate",
        "distortion",
        "beta",
    ],
)

##############################################################################
# Update equations
##############################################################################


def next_ln_qxhat(ln_px: np.ndarray, ln_qxhat_x: np.ndarray) -> np.ndarray:
    # q(xhat) = sum_x p(x) q(xhat | x),
    # shape `(xhat)`
    return logsumexp(ln_px[:, None] + ln_qxhat_x, axis=0)


def next_ln_qxhat_x(ln_qxhat: np.ndarray, beta: float, dist_mat: np.ndarray):
    # q(x_hat | x) = q(x_hat) exp(- beta * d(x_hat, x)) / Z(x)
    ln_qxhat_x = ln_qxhat[None, :] - beta * dist_mat
    ln_qxhat_x = ln_qxhat_x - logsumexp(
        ln_qxhat_x,
        axis=1,
        keepdims=True,
    )
    return ln_qxhat_x


##############################################################################
# Vanilla Rate Distortion Optimizer
##############################################################################


class RateDistortionOptimizer(BaseRDOptimizer):
    def __init__(
        self,
        px: np.ndarray,
        dist_mat: np.ndarray,
        betas: np.ndarray,
        *args,
        **kwargs,
    ) -> None:
        """Compute the rate-distortion function of an i.i.d distribution p(x), using the objective:

        $\min_{q} I[X:\hat{X}] + \\beta \mathbb{E}[d(x, \\hat{x})],$

        where $d(x, \\hat{x})$ is any distortion measure.

        Args:
            px: (1D array of shape `|X|`) representing the probability mass function of the source.

            dist_mat: array of shape `(|X|, |X_hat|)` representing the distortion matrix between the input alphabet and the reconstruction alphabet.

            beta: (scalar) the slope of the rate-distoriton function at the point where evaluation is required

            args: propagated to `BaseRDOptimizer`

            kwargs: propagated to `BaseRDOptimizer`
        """
        super().__init__(betas, *args, **kwargs)
        self.px = px
        self.diag_px = np.diag(px)
        self.ln_px = np.log(px)
        self.dist_mat = dist_mat
        self.results: list[RateDistortionResult] = []

    def get_results(self) -> list[RateDistortionResult]:
        return super().get_results()

    def next_result(self, beta, *args, **kwargs) -> None:
        """Get the result of the converged BA iteration.

        Returns:
            a RateDistortionResult namedtuple of `(qxhat_x, rate, distortion, accuracy)` values. This is:

                `qxhat_x`, the optimal encoder, such that the

                `rate` (in bits) of compressing X into X_hat, is minimized for the level of

                `distortion` between X, X_hat with respect to Y, i.e. the

                `accuracy` I[X_hat:Y] is maximized, for the specified

                `beta` trade-off parameter
        """
        return RateDistortionResult(
            np.exp(self.ln_qxhat_x),
            self.compute_rate(),
            self.compute_distortion(),
            beta,
        )

    def update_eqs(
        self,
        beta,
        *args,
        **kwargs,
    ) -> None:
        """Iterate the vanilla RD update equations."""
        self.ln_qxhat = next_ln_qxhat(self.ln_px, self.ln_qxhat_x)
        self.ln_qxhat_x = next_ln_qxhat_x(self.ln_qxhat, beta, self.dist_mat)

    def compute_distortion(self, *args, **kwargs) -> float:
        return np.exp(logsumexp(self.ln_px + self.ln_qxhat_x + np.log(self.dist_mat)))
