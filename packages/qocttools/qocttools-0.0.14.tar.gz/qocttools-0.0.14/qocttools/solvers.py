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

"""Solvers for the Schrödinger/Lindblad equation

The code may use the qutip solvers, or use some internal solvers
that may be faster in some circumstances.


"""

import sys
import numpy as np
from qutip import *
from qocttools.math_extra import rk4
from scipy.linalg import expm


def distribute_systems(comm, nelements):
    if comm == None:
        nprocs = 1
        rank = 0
    else:
        nprocs = comm.Get_size()
        rank = comm.Get_rank()

    st_ = np.empty(nprocs, dtype = 'int')
    for j in range(nprocs):
        st_[j] = int(np.floor(nelements * j / nprocs))
    st = int(np.floor(nelements * rank / nprocs))

    length_ = np.empty(nprocs, dtype = 'int')
    for j in range(nprocs):
        length_[j] = int(np.floor(nelements * (j+1) / nprocs)) - st_[j]
    length = int(np.floor(nelements * (rank+1) / nprocs)) - st

    end_ = np.empty(nprocs, dtype = 'int')
    for j in range(nprocs):
        end_[j] = st_[j] + length_[j]-1
    end = st + length - 1

    return st, st_, length, length_, end, end_


def broadcast_systems(comm, nelements, result):
    if comm == None:
        return
    else:
        nprocs = comm.Get_size()
    st, st_, length, length_, end, end_ = distribute_systems(comm, nelements)
    for k in range(nprocs):
        for j in range(st_[k], end_[k]+1):
            result[j] = comm.bcast(result[j], root = k)
    return result


def solve(solve_method, H, f, y0, time,
          returnQoutput = True,
          options = None,
          interaction_picture = False):
    """
    solve(solve_method, H, f, u, y0, time)
    
    This function propagate the object y0 using either the Schrödinger equation 
    with H = H0 + f(t)*V as Hamiltonian, or Lindblad's equation. If an inverse time array is given, the solver
    take y0 as the state at final time, making a backward propagation.

    The problem may be solved in the interaction picture if interaction_picture = True.
    Note that in that case H0 should be diagonal on entry (the system should be represented
    in the eigenbasis of H0). In this case, the output will also be in the interaction 
    picture.
    
    Parameters
    ----------
    solve_method: string indicating the propagation method
    H0: hamiltonian
        Hamiltonian's time independet part 
    V:  list of functions
        Hamiltonian's perturbation component 
    f:  list of pulse
       pulse class defined in typical_pulse.py based on Fourier expansion 
       parametrization
    y0: 
       initial state
    time: ndarray
       array that contain each time step.
    u: ndarray
       array that contain the control parameters of the pulse, needed to
       build the args diccionary defined in pulse class
           
    Returns
    .......
    qutip.result:
        qutiip.result type object with the propagation data 
    """
    if not isinstance(f, list):
        f = [f]

    if solve_method == 'sesolve':
        return qutipsolver(H, f, y0, time,
                           returnQoutput = returnQoutput,
                           interaction_picture = interaction_picture,
                           options = options)
        
    elif solve_method == 'rk4':
        return rk4solver(H, f, y0, time,
                         returnQoutput = returnQoutput, 
                         interaction_picture = interaction_picture)

    elif solve_method == 'cfmagnus2':
        return cfmagnus2solver(H, f, y0, time,
                               returnQoutput = returnQoutput,
                               interaction_picture = interaction_picture)

    elif solve_method == 'cfmagnus4':
        return cfmagnus4solver(H, f, y0, time,
                               returnQoutput = returnQoutput,
                               interaction_picture = interaction_picture)


def solvep(solve_method, H, f, y0, time,
           returnQoutput = None,
           options = None,
           interaction_picture = None,
           nprocs = 1,
           comm = None):

    if comm == None:
        nprocs = 1
        rank = 0
    else:
        nprocs = comm.Get_size()
        rank = comm.Get_rank()
    nelements = len(y0)

    st, st_, length, length_, end, end_ = distribute_systems(comm, nelements)

    if nprocs > 1:
        result = [ [None]*time.shape[0] ] * nelements
        for j in range(st, end + 1):
            result[j] = solve(solve_method, H[j], f, y0[j], time,
                              returnQoutput = returnQoutput,
                              options = options,
                              interaction_picture = interaction_picture)
    else:
        result = []
        for j in range(nelements):
            result.append(solve(solve_method, H[j], f, y0[j], time,
                                returnQoutput = returnQoutput,
                                options = options,
                                interaction_picture = interaction_picture))

    return result


def op(M, cops, y, costate_prop = False):
    if cops is None:
        return np.matmul( -1j * M, y)
    else:
        opy = - 1j * np.matmul(M, y) + 1j * np.matmul(y, M)
        if not costate_prop:
            for j in range(len(cops)):
                cops_ = cops[j].full()
                copsd_ = (cops[j].dag()).full()
                opy = opy + np.matmul(np.matmul(cops_, y), copsd_) \
                      - 0.5 * np.matmul(np.matmul(y, copsd_), cops_) \
                      - 0.5 * np.matmul(np.matmul(copsd_, cops_), y)
        else:
            for j in range(len(cops)):
                cops_ = cops[j].full()
                copsd_ = (cops[j].dag()).full()
                opy = opy - np.matmul(np.matmul(copsd_, y), cops_) \
                      + 0.5 * np.matmul(np.matmul(y, copsd_), cops_) \
                      + 0.5 * np.matmul(np.matmul(copsd_, cops_), y)
        return opy


def exppsi(M, cops, dt, y, order = 4):
    opy = y.copy()
    expy = y.copy()
    factor = 1.0
    for i in range(1, order+1):
        factor = factor/i
        if dt < 0.0:
            opy = dt * op(M, cops, opy, costate_prop = True)
        else:
            opy = dt * op(M, cops, opy, costate_prop = False)
        expy = expy + factor * opy
    return expy


def intoper(v, e, t):
    dim = v.shape[0]
    m = np.kron( np.exp(1j * t * e).reshape(dim, 1), np.exp(-1j * t * e).reshape(1, dim) )
    vi = v * m
    return vi


def qutipsolver(H, f, y0, time,
                returnQoutput = True,
                interaction_picture = False,
                options = None):

    H0 = H.H0
    V = H.V
    cops = H.A

    # What are we propagating?
    obj = None
    if y0.type == 'oper':
        if cops is not None:
            obj = 'density'
        else:
            obj = 'propagator'
    else:
        obj = 'state'
    if obj is None:
        raise Exception('Do not know what is the object to propagate')

    if obj == 'propagator':
        if not y0.isunitary:
            q_, r_ = np.linalg.qr(y0.full())
            y0 = Qobj(q_)
            r = Qobj(r_)

    if H.function:

        args = { "f": [f[l].fu for l in range(len(f))] }
        Ht = H.H0

    else:

        if interaction_picture:
            vsch = []
            for vop in V:
                vsch.append(vop.full())
            Hargs = {'V': V, 'eigenvalues': H0.diag()}
            def Hamiltonianfunc(t): #, Hargs):
                V = Hargs["V"]
                e = Hargs["eigenvalues"]
                dim = e.shape[0]
                Ht = Qobj(np.zeros([dim, dim]))
                ft = [f[l].fu(t) for l in range(len(f))]
                for j in range(len(V)):
                    v = vsch[j].copy()
                    for m in range(dim):
                        for n in range(dim):
                            v[m, n] = np.exp(-1j*t*(e[n]-e[m])) * v[m, n]
                    Ht = Ht + ft[j] * Qobj(v)
                return Ht
            Ht = QobjEvo(Hamiltonianfunc)
            args = Hargs
        else:
            Ht = [H0]
            for j in range(len(V)):
                def make_f(j):
                    def func(t, args):
                        ft = [f[l].fu(t) for l in range(len(f))]
                        return float(ft[j])
                    return func
                Ht.append([V[j], make_f(j)])
            if options == None:
                options = {"progress_bar" : False}
            args = None

    if cops is None:
        result = sesolve(Ht, y0, time, args = args, options = options)
    else:
        result = mesolve(Ht, y0, time, cops, args = args, options = options)

    if obj == 'propagator' and 'r' in locals():
        for j in  range(time.size):
           result.states[j] = result.states[j] * r

    if returnQoutput:
        return result.states
    else:
        return result_as_nparray(result)


def cfmagnus2solver(H, f, y0, time,
                    returnQoutput = True,
                    interaction_picture = False):
    """ Implementation of the exponential midpoint rule.

    It is also the second-order commutator-free Magnus method.
    """
    H0 = H.H0
    V = H.V
    cops = H.A

    if type(H0) is not qutip.qobj.Qobj:
        raise TypeError

    h0 = H0.full()
    dt = time[1]-time[0]
    dim = H0.shape[0]

    if returnQoutput:
        output = solver.Result(e_ops = None, options = solver.SESolver(H.H0).options)
        output.solver = 'cfmagnus2'
        output.times = time
        output.states = []
        output.states.append(y0)
    else:
        if y0.type == 'oper':
            output = np.zeros([time.size, dim, dim], dtype = complex)
            output[0, :, :] = y0.full()
        else:
            output = np.zeros([time.size, dim], dtype = complex)
            output[0, :] = y0.full()[:, 0]

    if y0.type == 'ket' or y0.type == 'bra':
        y = y0.full()[:, 0]
    else:
        y = y0.full()

    for j in range(time.size-1):
        t = time[j] + 0.5*dt
        ft = [ f[k].fu(t) for k in range(len(f)) ]
        if interaction_picture:
            M = np.zeros_like(h0)
            for k in range(len(V)):
                vi = intoper(V[k].full(), np.diag(h0), t)
                M = M + ft[k] * vi
        else:
            M = h0.copy()
            for k in range(len(V)):
                M = M + ft[k] * V[k].full()
        y = exppsi(M, cops, dt, y)
        if returnQoutput:
            youtput = y.copy()
            output.states.append(Qobj(youtput))
        else:
            output[j+1, :] = y[:]

    if returnQoutput:
        return output.states
    else:
        return output


def cfmagnus4solver(H, f, psi0, time,
                    returnQoutput = True,
                    interaction_picture = False):
    """ Implementation of the fourth order commutator-free Magnus method.
    """
    H0 = H.H0
    V = H.V
    cops = H.A
    v = [V[j].full() for j in range(len(V))]

    if type(H0) is not qutip.qobj.Qobj:
        raise TypeError

    h0 = H0.full()
    dt = time[1]-time[0]
    dim = H0.shape[0]

    if returnQoutput:
        output = solver.Result(e_ops = None, options = solver.SESolver(H.H0).options)
        output.solver = 'cfmagnus4'
        output.times = time
        output.states = []
        output.states.append(psi0)
    else:
        if psi0.type == 'oper':
            output = np.zeros([time.size, dim, dim], dtype = complex)
            output[0, :, :] = psi0.full()
        else:
            output = np.zeros([time.size, dim], dtype = complex)
            output[0, :] = psi0.full()[:, 0]

    if psi0.type == 'ket' or psi0.type == 'bra':
        psi = psi0.full()[:, 0]
    else:
        psi = psi0.full()

    a1 = (3.0-2.0*np.sqrt(3.0))/12.0
    a2 = (3.0+2.0*np.sqrt(3.0))/12.0
    c1 = 0.5 - np.sqrt(3.0)/6.0
    c2 = 0.5 + np.sqrt(3.0)/6.0

    for j in range(time.size-1):
        t1 = time[j] + c1*dt
        t2 = time[j] + c2*dt
        ft1 = [ f[k].fu(t1) for k in range(len(f)) ]
        ft2 = [ f[k].fu(t2) for k in range(len(f)) ]
        if interaction_picture:
            # We will assume that H0 is diagonal on entry.
            M1 = np.zeros_like(h0)
            M2 = np.zeros_like(h0)
            for k in range(len(V)):
                vi1 = intoper(v[k], np.diag(h0), t1)
                vi2 = intoper(v[k], np.diag(h0), t2)
                M1 = M1 + a1 * ft1[k] * vi1 + a2 * ft2[k] * vi2
                M2 = M2 + a2 * ft1[k] * vi1 + a1 * ft2[k] * vi2

        else:
            M1 = (a1 + a2) * h0
            M2 = (a1 + a2) * h0
            for k in range(len(V)):
                M1 = M1 + (a1 * ft1[k] + a2 * ft2[k]) * v[k]
                M2 = M2 + (a2 * ft1[k] + a1 * ft2[k]) * v[k]

        M = M2
        psi = exppsi(2*M, cops, dt/2, psi)
        M = M1
        psi = exppsi(2*M, cops, dt/2, psi)

        if returnQoutput:
            output.states.append(Qobj(psi))
        else:
            if psi0.type == 'oper':
                output[j+1, :, :] = psi[:, :]
            else:
                output[j+1, :] = psi[:]

    if returnQoutput:
        return output.states
    else:
        return output


def rk4solver(H, f, psi0, time, returnQoutput = True,
             interaction_picture = False):
    # WARNING: This may not work with operators, specially in the interaction picture.
    H0 = H.H0
    V = H.V
    # WARNING: cops are not used. This will not work with Lindblad's equation
    cops = H.A
    if type(H0) is not qutip.qobj.Qobj:
        raise TypeError

    h0 = H0.full()
    dt = time[1]-time[0]
    dim = H0.shape[0]
    if returnQoutput:
        output = solver.Result(e_ops = None, options = solver.SESolver(H.H0).options)
        output.solver = 'rk4'
        output.times = time
        output.states = []
        output.states.append(psi0)
    else:
        if psi0.type == 'oper':
            output = np.zeros([time.size, dim, dim], dtype = complex)
            output[0, :, :] = psi0.full()
        else:
            output = np.zeros([time.size, dim], dtype = complex)
            output[0, :] = psi0.full()[:, 0]

    def dynfun(t, xi):
        ft = [ f[k].fu(t) for k in range(len(f)) ]
        if cops is None:
            if interaction_picture:
                y = np.zeros_like(xi)
                for j in range(len(V)):
                    vi = intoper(V[j].full(), np.diag(h0), t)
                    y = y - 1j * ft[j] * np.matmul(vi, xi)
                return y
            else:
                M = h0.copy()
                for j in range(len(V)):
                    M = M + ft[j] * V[j].full()
                return -1j * np.matmul(M, xi)
        else:
            # Lindblad equation
            M = h0.copy()
            for j in range(len(V)):
                M = M + ft[j] * V[j].full()
            opy = - 1j * np.matmul(M, xi) + 1j * np.matmul(xi, M)
            if dt > 0:
                for j in range(len(cops)):
                    cops_ = cops[j].full()
                    copsd_ = (cops[j].dag()).full()
                    opy = opy + np.matmul(np.matmul(cops_, xi), copsd_) \
                          - 0.5 * np.matmul(np.matmul(xi, copsd_), cops_) \
                          - 0.5 * np.matmul(np.matmul(copsd_, cops_), xi)
                return opy
            else:
                for j in range(len(cops)):
                    cops_ = cops[j].full()
                    copsd_ = (cops[j].dag()).full()
                    opy = opy - np.matmul(np.matmul(copsd_, y), cops_) \
                          + 0.5 * np.matmul(np.matmul(y, copsd_), cops_) \
                          + 0.5 * np.matmul(np.matmul(copsd_, cops_), y)
                return opy

    if psi0.type == 'oper':
        xi = psi0.full()
    else:
        xi = psi0.full()[:, 0]

    for j in range(time.size-1):
        xi = rk4(xi, dynfun, time[j], dt)
        if returnQoutput:
            output.states.append(Qobj(xi))
        else:
            if psi0.type == 'oper':
                output[j+1, :, :] = xi[:, :]
            else:
                output[j+1, :] = xi[:]

    if returnQoutput:
        return output.states
    else:
        return output
 

def result_as_nparray(result):
    dim = result.states[0].full().shape[0]
    dim2 = result.states[0].full().shape[1]
    tsize = len(result.states)
    if dim2 > 1:
        output = np.zeros([tsize, dim, dim], dtype = complex)
        for j in range(tsize):
            output[j, :, :] = result.states[j].full()
    else:
        output = np.zeros([tsize, dim], dtype = complex)
        for j in range(tsize):
            output[j, :] = result.states[j].full()[:, 0]
    return output

