import functools
import warnings

import numpy as np


def deprecated(func):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used."""

    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.simplefilter('always', DeprecationWarning)  # turn off filter
        warnings.warn("Call to deprecated function {}.".format(func.__name__),
                      category=DeprecationWarning,
                      stacklevel=2)
        warnings.simplefilter('default', DeprecationWarning)  # reset filter
        return func(*args, **kwargs)

    return new_func


@deprecated
def normalize(dm):
    return dm / dm.std() if dm.std() != 0 else dm


def get_D(A):
    return np.diag(np.sum(A, axis=0))


def get_D_1(A):
    """
    D_1 = D^{-1}
    """
    return np.diag(1. / np.sum(A, axis=0))


def get_L(A):
    return get_D(A) - A


def H0_to_H(H0):
    """
    H = element - wise log(H0)
    """
    return np.log(H0)


def H_to_D(H):
    """
    D = (h * 1^T + 1 * h^T - H - H ^ T) / 2
    """
    size = H.shape[0]
    h = np.diagonal(H).reshape(-1, 1)
    i = np.ones((size, 1))
    return 0.5 * ((h.dot(i.transpose()) + i.dot(h.transpose())) - H - H.transpose())


def D_to_K(D):
    """
    K = -1 / 2 HΔH
    H = I - E/n
    """
    size = D.shape[0]
    I, E = np.eye(size), np.ones((size, size))
    H = I - (E / size)
    K = -0.5 * H.dot(D).dot(H)
    return K
