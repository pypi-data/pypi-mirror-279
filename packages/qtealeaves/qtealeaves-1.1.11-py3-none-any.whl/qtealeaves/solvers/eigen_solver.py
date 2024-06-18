# This code is part of qtealeaves.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""
The module contains solvers for the Krylov eigensolver as an API (multiplication
matrix-vector are passed as function, vector class needs only a few attributes).

**Attributes needed for vector class**

* `norm`
* `dot` for inner product between two vectors.
* `add_update(self, other, factor_self, factor_other)
* `__itruediv__`
* `__imul__`
"""

# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-arguments

import numpy as np

__all__ = ["EigenSolverH"]


class EigenSolverH:
    """
    Eigensolver for hermitian matrix.

    **Arguments**

    vec0 : vector to apply epxonential matrix to / initial guess

    matvec_func : callable, mutliplies matrix in exponential with vector.

    args_func : list, arguments for matvec_func

    kwargs_func : dict, keyword arguments for matvec_func
    """

    def __init__(
        self, vec0, matvec_func, conv_params, args_func=None, kwargs_func=None
    ):
        self.vec = vec0
        self.conv_params = conv_params
        self.func = matvec_func
        self.args = [] if args_func is None else args_func
        self.kwargs = {} if kwargs_func is None else kwargs_func

        self.nn_max = conv_params.arnoldi_maxiter
        self.tolerance = conv_params.sim_params["arnoldi_tolerance"]
        self.basis = []

        self.init_basis()

    def init_basis(self):
        """Initialize the basis and create diagonal / subdiagonal entries."""

        self.diag = np.zeros(self.nn_max + 1)
        self.sdiag = np.zeros(self.nn_max)
        self.sdiag_0 = self.vec.norm_sqrt()

        if abs(1 - self.sdiag_0) > 10 * self.tolerance:
            eps = abs(1 - self.sdiag_0)
            raise Exception(f"Expecting normalized vector, but {eps}.")

        self.basis.append(self.vec.copy())

    def solve(self, verbose=0):
        """Sovler step executing iterations until new vector is returned."""

        nn = self.nn_max
        for ii in range(self.nn_max):
            # Matrix-vector multiplication interface
            self.vec = self.func(self.vec, *self.args, **self.kwargs)

            overlap = self.vec.dot(self.basis[ii])
            self.vec.add_update(self.basis[ii], factor_other=-overlap)

            if ii > 0:
                self.vec.add_update(
                    self.basis[ii - 1], factor_other=-self.sdiag[ii - 1]
                )

            self.diag[ii] = overlap.real
            self.sdiag[ii] = self.vec.norm_sqrt()

            mat = np.diag(self.diag[: ii + 1])
            for jj in range(ii):
                mat[jj, jj + 1] = self.sdiag[jj]
                mat[jj + 1, jj] = self.sdiag[jj]

            evals, evecs = np.linalg.eigh(mat)

            # Check on exit criteria
            precision_fom = np.abs(evecs[ii, 0] * self.sdiag[ii])
            if precision_fom < self.tolerance:
                if verbose > 0:
                    print(
                        f"Eigenh solver converged in {nn} steps with {precision_fom}."
                    )
                break

            if ii + 1 == self.nn_max:
                if verbose > 0:
                    precision_fom = evecs[ii, 0] * self.sdiag[ii]
                    print(f"Eigenh solver stopped at max_iter with {precision_fom}.")
                break

            self.vec /= self.sdiag[ii]
            self.basis.append(self.vec.copy())

        # Build solution (expecting list of eigenvalues even if size-one)
        val = [evals[0]]
        vec = self.basis[0] * evecs[0, 0]

        for jj in range(1, ii + 1):
            vec.add_update(self.basis[jj], factor_other=evecs[jj, 0])

        return val, vec
