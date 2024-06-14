"""Weighted Information Bottleneck and MSE Rate Distortion problem (IBMSE) optimizer."""

import numpy as np

from collections import namedtuple
from tqdm import tqdm

from .ib import IBOptimizer, IBResult, next_ln_qy_xhat, next_ln_qx_xhat
from .rd import next_ln_qxhat, next_ln_qxhat_x
from ..information import information_cond
from ..distortions import ib_mse

##############################################################################
# Return type of each item in `get_results()`
##############################################################################

IBMSEResult = namedtuple(
    "IBMSEResult",
    [
        "qxhat_x",
        "fxhat",
        "rate",
        "distortion",
        "accuracy",
        "beta",
        "alpha",
    ],
)

##############################################################################
# Update equations
##############################################################################


def next_fxhat(fx: np.ndarray, ln_px: np.ndarray, ln_qxhat_x: np.ndarray) -> np.ndarray:
    ln_qx_xhat = next_ln_qx_xhat(ln_px, ln_qxhat_x)  # `(xhat, x)`

    # f(xhat) = sum_x f(x) p(x|xhat),
    fxhat = np.sum(
        fx[None, :, :] * np.exp(ln_qx_xhat[:, :, None]),  # `(xhat, x, y)`
        axis=1,
    )
    return fxhat


##############################################################################
# IB+MSE Optimizer
##############################################################################


class IBMSEOptimizer(IBOptimizer):
    def __init__(
        self,
        pxy: np.ndarray,
        fx: np.ndarray,
        betas: np.ndarray,
        alphas: np.ndarray,
        *args,
        **kwargs,
    ) -> None:
        """Estimate the optimal encoder for given values of `beta` and `alpha` for the following modified IB objective:

        $\min_{q, f} \\frac{1}{\\beta} I[X:\hat{X}] + \\alpha \mathbb{E}[D_{KL}[p(y|x) || p(y|\hat{x})]] + (1 - \\alpha) \mathbb{E}[l(x, \hat{x})],$

        where $l$ is a weighted quadratic loss between feature vectors for $x, \hat{x}$:

        $l(x, \hat{x}) = \\frac{1}{N} \sum_{i=1}^{N} w_i \cdot \left( f(x)_i - f(\hat{x})_i \\right)^2$,

        and $f(x)$ is the feature vector of $x$, and the optimal $f(\hat{x})$ satisfies:

        $f(\hat{x}) = \sum_x q(x|\hat{x}) f(x)$

        Args:
            pxy: 2D array of shape `(|X|, |Y|)` representing the joint probability mass function of the source and relevance variables.

            fx: 2D array of shape `(|X|, |f|)` representing the unique vector representations of each value of the source variable X. Here `|f|` denotes the number of features in each vector x. Feature values can be real-valued, not restricted to [0,1] weights.

            beta: (scalar) the slope of the rate-distoriton function at the point where evaluation is required

            alpha: (scalar) a float between 0 and 1, specifying the trade-off between KL divergence and domain specific (MSE) distortion between feature vectors.

            weights: 1D array of shape `(|f|)` representing weights for feature values
        """
        super().__init__(pxy, betas, *args, **kwargs)
        self.alphas = alphas

        self.fx = fx  # `(x,f)`
        self.fxhat = None  # `(xhat,f)`

    def get_results(self) -> list[IBMSEResult]:
        return super().get_results()

    def beta_iterate(
        self,
        *args,
        num_restarts: int = 1,
        ensure_monotonicity: bool = True,
        **kwargs,
    ) -> None:
        """Run the BA iteration for many values of beta and alpha."""
        # Reverse deterministic annealing
        alpha_results: list[IBMSEResult] = []

        for alpha in tqdm(self.alphas, desc="sweeping alpha"):
            # Run beta_iterate for a single alpha
            kwargs["alpha"] = alpha
            super().beta_iterate(
                *args,
                num_restarts=num_restarts,
                ensure_monotonicity=ensure_monotonicity,
                disable_tqdm=True,
                **kwargs,
            )
            # Collect and reset internal results
            beta_results = self.results
            self.results = []
            alpha_results.extend(beta_results)

        self.results = alpha_results
        return self.results

    def update_eqs(
        self,
        beta,
        *args,
        **kwargs,
    ) -> None:
        """Iterate the IB+MSE objective update equations."""
        self.ln_qxhat = next_ln_qxhat(self.ln_px, self.ln_qxhat_x)
        self.ln_qy_xhat = next_ln_qy_xhat(self.ln_pxy, self.ln_qxhat_x)
        self.fxhat = next_fxhat(self.fx, self.ln_px, self.ln_qxhat_x)
        self.next_dist_mat(*args, **kwargs)
        self.ln_qxhat_x = next_ln_qxhat_x(self.ln_qxhat, beta, self.dist_mat)

    def next_dist_mat(self, *args, **kwargs) -> None:
        """IB+MSE distortion matrix."""
        alpha = kwargs["alpha"]

        weights = None
        if "weights" in kwargs:
            weights = kwargs["weights"]

        self.dist_mat = ib_mse(
            np.exp(self.ln_py_x),
            np.exp(self.ln_qy_xhat),
            self.fx,
            self.fxhat,
            alpha,
            weights=weights,
        )

    def next_result(self, beta, alpha, *args, **kwargs) -> IBResult:
        """Get the result of the converged BA iteration for the IB+MSE objective.

        Returns:
            an IBMSEResult namedtuple of `(qxhat_x, fxhat, rate, distortion, accuracy, beta, alpha)` values. This is:

                `qxhat_x`, the optimal encoder,

                `fxhat`, corresponding feature vectors such that the

                `rate` (in bits) of compressing X into X_hat, is minimized for the level of

                `distortion` between X, X_hat with respect to Y and f(x), and

                `accuracy` I[X_hat:Y] is maximized, for the specified

                `beta` trade-off parameter, and the specified

                `alpha` combination distortion trade-off parameter.

        """
        return IBMSEResult(
            np.exp(self.ln_qxhat_x),
            self.fxhat,
            self.compute_rate(),
            self.compute_distortion(),
            information_cond(
                np.exp(self.ln_qxhat),
                np.exp(self.ln_qy_xhat),
            ),
            beta,
            alpha,
        )
