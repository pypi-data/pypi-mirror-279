"""Base Rate Distortion optimization class, including the main Blahut-Arimoto iteration.
"""
import numpy as np

from typing import Any
from tqdm import tqdm
from ..information import information_cond
from ..probability import random_stochastic_matrix
from ..postprocessing import compute_lower_bound


##############################################################################
# Base Rate Distortion class
##############################################################################


class BaseRDOptimizer:
    def __init__(
        self,
        betas: np.ndarray,
        *args,
        max_it: int = 1000,
        eps: float = 1e-15,
        ignore_converge: bool = False,
        **kwargs,
    ) -> None:
        """Base initializer for a Blahut-Arimoto-based optimizer of the Rate Distortion function.

        Args:
            betas: 1D array, values of beta to search

            max_it: max number of iterations

            args: propagated to `self.beta_iterate` as *kwargs

            eps: accuracy required by the algorithm: the algorithm stops if there is no change in distortion value of more than `eps` between consecutive iterations

            ignore_converge: whether to run the optimization until `max_it`, ignoring the stopping criterion specified by `eps`.

            kwargs: propagated to `self.beta_iterate` as **kwargs
        """
        self.betas = betas
        self.max_it = max_it
        self.eps = eps
        self.ignore_converge = ignore_converge

        self.init_args = args
        self.init_kwargs = kwargs

        self.ln_px = None  # shape `(x)`
        self.ln_qxhat_x = None  # shape `(x, xhat)`
        self.dist_mat = None  # shape `(x, xhat)`
        self.result = None  # namedtuple
        self.results: list[Any] = []  # list of namedtuples

    def get_results(self) -> list[Any]:
        # Re-initialize results
        self.result = None
        self.results = []

        self.beta_iterate(*self.init_args, **self.init_kwargs)
        return self.results

    def update_eqs(
        self,
        *args,
        **kwargs,
    ) -> None:
        """Main Blahut-Arimoto update steps."""
        raise NotImplementedError

    def next_result(self, beta, *args, **kwargs) -> None:
        """Get the result of the converged BA iteration."""
        raise NotImplementedError

    def beta_iterate(
        self,
        *args,
        num_restarts: int = 1,
        ensure_monotonicity: bool = True,
        disable_tqdm: bool = False,
        **kwargs,
    ) -> None:
        """Iterate the BA algorithm for an array of values of beta, using reverse deterministic annealing.

        Args:
            num_restarts: number of times to restart each beta-optimization

            ensure_monotonicity: whether to remove points that would make a rate distortion curve non-monotonic
        """
        # Reverse deterministic annealing
        results = []
        betas = np.sort(self.betas)[::-1]  # sort betas in decreasing order

        init_q = np.eye(
            len(self.ln_px)
        )  # this assumes you're starting with very high beta.
        pbar = tqdm(
            betas,
            disable=disable_tqdm,
            desc="annealing beta",
        )
        for beta in pbar:
            pbar.set_description(f"beta={beta:.5f}")
            candidates = []
            for _ in range(num_restarts):
                self.blahut_arimoto(beta, *args, init_q=init_q, **kwargs)
                cand = self.results[-1]
                init_q = cand.qxhat_x
                candidates.append(cand)
            best = min(candidates, key=lambda x: x.rate + beta * x.distortion)
            results.append(best)

        # Postprocessing
        results = results[::-1]
        if ensure_monotonicity:
            indices = compute_lower_bound(
                [(item.rate, item.distortion) for item in results]
            )
            results = [x if i in indices else None for i, x in enumerate(results)]
        self.results = results

    ############################################################################
    # Blahut Arimoto iteration
    ############################################################################

    def blahut_arimoto(
        self,
        beta,
        *args,
        **kwargs,
    ) -> None:
        """Update the self-consistent equations for a Rate Distortion objective.

        Args:
            beta: (scalar) the slope of the rate-distoriton function at the point where evaluation is required
        """
        len_x = len(self.ln_px)
        if "init_q" in kwargs:
            self.ln_qxhat_x = np.log(kwargs["init_q"])
        else:
            self.ln_qxhat_x = np.log(random_stochastic_matrix((len_x, len_x)))

        it = 0
        converged = False
        while not converged:
            it += 1
            prev_q = np.copy(self.ln_qxhat_x)

            # Main BA update
            self.update_eqs(beta, *args, **kwargs)

            # convergence check
            # TODO: consider updating the Result tuple to include convergence field. if converged, record the iteration. If not, record False/None
            if self.ignore_converge:
                converged = it >= self.max_it
            else:
                converged = (
                    it == self.max_it
                    or np.sum(np.abs(np.exp(self.ln_qxhat_x) - np.exp(prev_q)))
                    < self.eps  # note this is in logspace
                )

        self.results.append(self.next_result(beta, *args, **kwargs))

    def compute_distortion(self, *args, **kwargs) -> float:
        """Compute the expected distortion for the current p(x), q(xhat|x) and dist_mat."""
        raise NotImplementedError

    def compute_rate(
        self,
        *args,
        **kwargs,
    ) -> float:
        """Compute the information rate for the current p(x), q(xhat|x)."""
        return information_cond(np.exp(self.ln_px), np.exp(self.ln_qxhat_x))
