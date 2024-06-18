import typing as tp

from scoringrules.backend import backends
from scoringrules.core import energy
from scoringrules.core.utils import multivariate_array_check

if tp.TYPE_CHECKING:
    from scoringrules.core.typing import Array, ArrayLike, Backend



def iqd(obs, fct, axis=-1, backend=None):
    """Compute the integrated quadratic distance (IQD) for a finite ensemble.
    
    The IQD is a multivariate scoring rule expressed as
    
    $$\text{IQD}(F_{ens}, \mathbf{y})= \frac{1}{M} \sum_{m=1}^{M} \| \mathbf{x}_{m} - \mathbf{y} \|^{2} - \frac{1}{M^{2}} \sum_{m=1}^{M} \sum_{j=1}^{M} \| \mathbf{x}_{m} - \mathbf{x}_{j} \|^{2} $$
    
    where $\mathbf{X}$ and $\mathbf{X'}$ are independent samples from $F$
    and $||\cdot||$ is the euclidean norm over the input dimensions (the variables).
    
    Parameters
    ----------
    obs: Array
        The observed values, where the variables dimension is by default the last axis.
    fct: Array
        The predicted forecast ensemble, where the ensemble dimension is by default
        represented by the second last axis and the variables dimension by the last axis.
    axis: int
        The axis corresponding to the ensemble dimension on the forecasts array. Defaults to -2.
    backend: str
        The name of the backend used for computations. Defaults to 'numba' if available, else 'numpy'.
    
    Returns
    -------
    iqd: Array of shape (...)
        The computed IQD.
    """
    B = backends.active if backend is None else backends[backend]
    obs, fct = map(B.asarray, (obs, fct))

    E_fg = B.mean(B.abs(fct[...,None] - obs[...,None,:]), axis=(-2, -1))
    E_f = B.mean(B.abs(fct[...,None] - fct[...,None,:]), axis=(-2, -1))
    E_g = B.mean(B.abs(obs[...,None] - obs[...,None,:]), axis=(-2, -1))

    return E_fg - 0.5 * (E_f + E_g)