import numpy as np
from .probability import joint
from scipy.stats import entropy


def H(p, axis=None):
    """Entropy of p, $H(X) = - \sum_x x \log p(x)$"""
    return entropy(p, base=2, axis=axis)


def MI(pXY):
    """Mutual information, $I(X;Y)$"""
    return H(pXY.sum(axis=0)) + H(pXY.sum(axis=1)) - H(pXY)


def DKL(p, q, axis=None):
    """KL divergence, $D_{KL}[p~||~q]$"""
    return entropy(p, q, axis=axis)


# Common pattern for rate-distortion optimizations
def information_cond(pA: np.ndarray, pB_A: np.ndarray) -> float:
    """Compute the mutual information $I(A;B)$ from a joint distribution defind by $P(A)$ and $P(B|A)$

    Args:
        pA: array of shape `|A|` the prior probability of an input symbol (i.e., the source)

        pB_A: array of shape `(|A|, |B|)` the probability of an output symbol given the input
    """
    pXY = joint(pY_X=pB_A, pX=pA)
    mi = MI(pXY=pXY)
    if mi < 0.0 and not np.isclose(mi, 0.0, atol=1e-5):
        raise Exception
    return mi
