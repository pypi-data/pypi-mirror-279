## Copyright 2019-present The qocttools developing team
##
## This file is part of qocttools.
##
## qocttools is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## qocttools is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with qocttools.  If not, see <https://www.gnu.org/licenses/>.

"""(...)


"""

import numpy as np
import qutip as qt

def dmtovector(rho):
    """
    Transforms a Qobj [[d], [d]] shaped operator  object into a [[d^2], [1]] shaped
    ket.

    Parameters
    ----------
    rho : Qobj
         Density matrix

    Returns
    -------
    Qobj
        A Qobj vector containing the vectorized version of the input density matrix

    """
    dim = rho.dims[0][0]
    return qt.Qobj(qt.operator_to_vector(rho), dims = [[dim**2], [1]])


def vectortodm(rhovec):
    """
    Transforms a numpy array of dimension (d^2) into an "operator" Qobj object; this object has
    dimension [[d], [d]]. The input 1D array is supposed to store the operator with stacked
    columns.

    Parameters
    ----------
    rhovec : ndarray
        A one-dimensional numpy complex array with d^2 elements

    Returns
    -------
        A [[d], [d]] shaped qutip Qobj
    """
    dim = round(np.sqrt(rhovec.shape[0]))
    return qt.vector_to_operator(qt.Qobj(rhovec, dims = [[[dim], [dim]], [1]]))


def toliouville(A, unitary = True, factor = 1.0):
    """
    (...)
    """
    if unitary:
        dim = A.dims[0][0]
        return qt.Qobj( factor * qt.liouvillian(A), dims = [[dim**2], [dim**2]] )
    else:
        dim = A[0].dims[0][0]
        return qt.Qobj( factor * qt.liouvillian(None, A), dims = [[dim**2], [dim**2]] )


def fromliouville(A):
    """
    (...)
    """
    dim = round(np.sqrt(A.shape[0][0]))
    A_ = qt.Qobj(A, dims = [[[dim], [dim]], [[dim], [dim]]] )
    return (1/dim) * A_.ptrace(1)
