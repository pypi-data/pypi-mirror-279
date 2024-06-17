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

"""This module contains all the procedures needed to do Floquet optimization.
"""

import qutip as qt
import numpy as np
import scipy as scp
import scipy.linalg as la
import qocttools.pulses as pulses
import qocttools.cythonfuncs as cyt
from qocttools.math_extra import diff_ridders
from qocttools.liouville import dmtovector, vectortodm


def epsi(UT, T):
    """
    Given a matrix UT, returns the Floquet quasienergies associated to it.

    In principle, the matrix should be unitary (or otherwise, there is no
    guarantee that the matrix will have unit eigenvalues). However, the routine
    accepts non-unitary matrix, as it computes the Schur decomposition, and it uses
    the diagonal elements of the Schur form. If the matrix is indeed unitary, the 
    output will be proper Floquet quasienergies.

    Parameters
    ----------
    UT : ndarray
        A unitary matrix, representing an evolution operator.
    T : float
        The Floquet period

    Returns
    -------
    ndarray:
        The Floquet quasienergies (ordered, and in the Floquet Brillouin zone)
    """
    # In principle, one needs the eigenvalues. But what if UT cannot be diagonalized?
    # We will use then the Schur decomposition, and use the diagonal elements of the
    # Schur matrix.
    #evals, evecs = la.eig(UT)
    dim = UT.shape[0]
    S, Z = la.schur(UT)
    evals = np.zeros(dim, dtype = complex)
    for l in range(dim):
        evals[l] = S[l, l]
    eargs = np.angle(evals)
    eargs += (eargs <= -np.pi) * (2 * np.pi) + (eargs > np.pi) * (-2 * np.pi)
    epsilon = -eargs / T
    return np.sort(epsilon)


def depsi(UT, T, delta = 1.0e-4):
    """
    Given a unitary UT, returns the derivatives of the Floquet quasienergies
    with respect to it. Specifically, it returns the derivative of each
    Floquet quasienergy with respect to each matrix element :math:`U_{ij}^*`
    (technically, a Wirtinger derivative, with respect to the complex conjugate
    of the parameter).

    Parameters
    ----------
    UT : ndarray
        A unitary matrix, representing an evolution operator.
    T : float
        The Floquet period
    delta : float, default = 1.0e-4
        The small displacement used to compute the derivatives
        through a finite-difference formula.

    Returns
    -------
    ndarray :
        The numpy array containing the derivatives; the shape is
        (dim, dim, dim): depsi[alpha, :, :] is the matrix of derivatives
        of the alpha-th quasienergy with respect to all the elements of
        the unitary.
    """
    dim = UT.shape[0]
    depsi_ = np.empty([dim, dim, dim], dtype = complex)
    for i in range(dim):
        for j in range(dim):
            UTp = UT.copy()
            UTp[i, j] = UTp[i, j] + delta
            epsilonp = epsi(UTp, T)
            UTm = UT.copy()
            UTm[i, j] = UTm[i, j] - delta
            epsilonm = epsi(UTm, T)
            dx = (epsilonp-epsilonm) / (2*delta)

            UTp = UT.copy()
            UTp[i, j] = UTp[i, j] + 1j*delta
            epsilonp = epsi(UTp, T)
            UTm = UT.copy()
            UTm[i, j] = UTm[i, j] - 1j*delta
            epsilonm = epsi(UTm, T)
            dy = (epsilonp-epsilonm) / (2*delta)

            depsi_[:, i, j] = 0.5 * (dx + 1j*dy)
    return depsi_


def epsilon(H, T, args = None):
    """Computes Floquet quasienergies corresponding to the Hamiltonian H and the period T.

    For this to make sense, the Hamiltonian time-dependence must be periodic. The Hamiltonian
    must be given as a "qutip Hamiotonian", i.e. anything that could be accepted by the qutip
    propagation functions as valid Hamiltonians.

    Parameters
    ----------
    H : qutip Hamiltonian
        The (periodic) Hamiltonian
    T : float
        The period
    args : dict, default = None
        An "args" argument that can b passed to the qutip sesolve function that is used
        to compute the unitary evolution operator at time T.

    Returns
    -------
    ndarray:
        The ordered set of quasienergies.

    """
    #options = qt.Options(nsteps = 10000)
    options = { 'nsteps':10000 }
    #ntsteps = 5
    #dim = 3 # WARNING: This is hard-coded here, but it should not be.
    #U = (qt.sesolve(H, qt.qeye(dim), np.linspace(0, T, ntsteps), options = options, args = args)).states[-1]
    #ualpha, epsilon = qt.floquet_modes(H, T, U = U)
    floquet_basis = qt.FloquetBasis(H, T, args = args) #, U = U)
    epsilon = floquet_basis.e_quasi
    idx = epsilon.argsort()
    return epsilon[idx]


def epsilon3(H, f, u, T):
    """
    Given an Hamiltonian H (:class:`hamiltonians.hamiltonian`), a set of driving periodic
    perturbations f, returns the Floquet quasienergies

    Parameters
    ----------
    H : :class:`hamiltonians.hamiltonian`
        The Hamiltonian of the system, given as a hamiltonian class object.
    f : list of :class:`pulses.pulse`
        A list of periodic drivings -- the number should match the number of
       perturbations of the Hamiltonian
    u : ndarray
        The control parameters
    T : float
        The period

    Returns
    -------
    ndarray
        An array with the Floquet quasienergies
    """
    pulses.pulse_collection_set_parameters(f, u)
    if H.function:
        args = { "f": [f[l].fu for l in range(len(f))] }
        H_ = H.H0
    else:
        args = None
        H_ = [H.H0]
        k = 0
        for V in H.V:
            H_.append([V, f[k].f])
            k = k + 1
    return epsilon(H_, T, args = args)


def gradepsilon(H, f, u, T):
    """
    Returns the gradient of the Floquet quasienergies with respect to the control parameters
    of the set of periodic drivings.

    Parameters
    ----------
    H : :class:`hamiltonians.hamiltonian`
        The Hamiltonian of the system, given as a hamiltonian class object.
    f : list of :class:`pulses.pulse`
        A list of periodic drivings -- the number should match the number of
       perturbations of the Hamiltonian
    u : ndarray
        The control parameters
    T : float
        The period

    Returns
    -------
    ndarray
        An array shaped (dim, nu) where dim is the Hilert space dimension, and
        nu is the number of control parameters, containing the derivatives of the
        Floquet quasienergies with respect to those parameters.
    """
    dim = H.dim
    pulses.pulse_collection_set_parameters(f, u)

    if H.function:
        #options = qt.Options(nsteps = 10000)
        options = { "nsteps":10000}
        args = { "f": [f[l].fu for l in range(len(f))] }
        H_ = H.H0
        ntsteps = 5
        U = (qt.sesolve(H_, qt.qeye(dim), np.linspace(0, T, ntsteps), options = options, args = args)).states[-1]
    else:
        args = None
        H0 = H.H0
        Vs = H.V
        H_ = [H.H0]
        k = 0
        for V in H.V:
            H_.append([V, f[k].f])
            k = k + 1
        #options = qt.Options(nsteps = 10000)
        options = { "nsteps":10000}
        U = qt.propagator(H_, T, options = options)

    floquet_basis = qt.FloquetBasis(H_, T, args = args)
    epsilon = floquet_basis.e_quasi
    #print(epsilon)
    #ualpha = floquet_basis.mode(0.0)
    #ualpha, epsilon = qt.floquet_modes(H_, T, U = U)
    #idx = epsilon.argsort()
    #epsilon = epsilon[idx]
    #print(epsilon)
    #ualpha_ = [ualpha[j] for j in idx]
    #ualpha = ualpha_
    #times = np.linspace(0, T, 100)
    #dt = times[1]
    #ualphat = qt.floquet_modes_table(ualpha, epsilon, times, H_, T, args = args)
    
    times = np.linspace(0, T, 100)
    dt = times[1]
    ualphat = []
    for j in range(times.shape[0]):
        ualphat.append( floquet_basis.mode(times[j]) )
 
    nu = 0
    for ip in range(len(f)):
        nu = nu + f[ip].nu
    res = np.zeros((dim, nu))

    if H.function:
       Vs_ = []
       for ip in range(len(f)):
           Vs_.append( np.empty(times.shape[0], dtype = qt.Qobj) )
       for j in range(times.shape[0]):
           t = times[j]
           for ip in range(len(f)):
               Vs_[ip][j] = H.V[ip](times[j], args)

    m = 0
    for ip in range(len(f)):
        ft = f[ip]
        if H.function:
            V = Vs_[ip]
        else:
            V = Vs[ip]
        for k in range(f[ip].nu):
            if H.function:
                for alpha in range(dim):
                    res[alpha, m] = 0.5 * (qt.expect(V[0], ualphat[0][alpha]) * ft.dfu(times[0], k) )
                    for j in range(1, times.shape[0]-1):
                        res[alpha, m] = res[alpha, m] + (qt.expect(V[j], ualphat[j][alpha]) * ft.dfu(times[j], k) )
                    res[alpha, m] = res[alpha, m] + 0.5 * (qt.expect(V[j], ualphat[-1][alpha]) * ft.dfu(times[-1], k) )
            else:
                for alpha in range(dim):
                    res[alpha, m] = 0.5 * (qt.expect(V, ualphat[0][alpha]) * ft.dfu(times[0], k) )
                    for j in range(1, times.shape[0]-1):
                        res[alpha, m] = res[alpha, m] + (qt.expect(V, ualphat[j][alpha]) * ft.dfu(times[j], k) )
                    res[alpha, m] = res[alpha, m] + 0.5 * (qt.expect(V, ualphat[-1][alpha]) * ft.dfu(times[-1], k) )
            m = m + 1

    return res * dt/T


def ness(T, ntsteps, L, f, compute_gradient = False):
    """
    Computes the NESS and, if required, the gradient of the NESS with respect
    to the control parameters of the periodic drivings.

    See :ref:`gradient_floqueto` for details about how the gradient is computed.
    """
    if compute_gradient:
        nu = [g.nu for g in f]
        dgt = [g.gradf for g in f]

    if L.function:
        args = { "f": [f[l].fu for l in range(len(f))] }
        L0 = L.H0
        LVlist = []
        for k in range(len(L.V)):
            LVlist.append([L.V[k], f[k].f])
    else:
        L0 = L.H0.full()
        LVlist = []
        for k in range(len(L.V)):
            LVlist.append([L.V[k].full(), f[k].f])

    nv = len(LVlist)
    if compute_gradient:
        if len(nu) != nv or len(dgt) != nv:
            raise Exception("The lengths of nu and dgt should be equal to the length of LVlist")
        Nu = sum(nu)

    LV = []
    gt = []
    for h in range(nv):
        LV.append(LVlist[h][0])
        gt.append(LVlist[h][1])

    times = np.linspace(0, T, ntsteps+1)
    dt = times[1]

    dim = L0.shape[0]
    #dim = L0(0.0, args).shape[0]
    #print("dim = {}".format(dim))
    d = round(np.sqrt(dim))

    gfunc = np.zeros([nv, ntsteps])
    if compute_gradient:
        gradg = np.zeros([Nu, ntsteps])
    for h in range(nv):
        for j in range(ntsteps):
            gfunc[h, j] = gt[h](times[j], None)
            if compute_gradient:
                l = 0
                for h in range(nv):
                    for k in range(nu[h]):
                        gradg[l, j] = dgt[h](times[j])[k]
                        l = l + 1


    lind = np.zeros([dim, dim, ntsteps], dtype = complex)
    for j in range(ntsteps):
        if L.function:
            lind[:, :, j] = L0(times[j], args).full()
        else:
            lind[:, :, j] = L0[:, :]
            for h in range(nv):
                gt_ = gt[h](times[j], None)
                for alpha in range(dim):
                    for beta in range(dim):
                        lind[alpha, beta, j] = lind[alpha, beta, j] + gt_ * LV[h][alpha, beta]

    if compute_gradient:
        dlind = np.zeros([Nu, dim, dim, ntsteps], dtype = complex)
        l = 0
        for h in range(nv):
            for k in range(nu[h]):
                for j in range(ntsteps):
                    dgt_ = dgt[h](times[j])[k]
                    if L.function:
                        dlind[l, :, :, j] = dgt_ * LV[h](times[j], args).full()
                    else:
                        dlind[l, :, :, j] = dgt_ * LV[h][:, :]
                l = l + 1
                
    ws = np.zeros(ntsteps, dtype = float)
    for m in range((ntsteps)//2):
        ws[m] = (2.0*np.pi/T) * m
    for m in range((ntsteps)//2, ntsteps):
        ws[m] = (2.0*np.pi/T) * (m-ntsteps)

    lindw = np.zeros([dim, dim, ntsteps], dtype = complex)
    for alpha in range(dim):
        for beta in range(dim):
            lindw[alpha, beta, :] = scp.fft.fft(lind[alpha, beta, :]) / (ntsteps)

    if compute_gradient:
        dlindw = np.zeros([Nu, dim, dim, ntsteps], dtype = complex)
        for k in range(Nu):
            for alpha in range(dim):
                for beta in range(dim):
                    dlindw[k, alpha, beta, :] = scp.fft.fft(dlind[k, alpha, beta, :]) / (ntsteps)

    def tracef(x):
        tr = 0.0
        for j in range(d):
            tr = tr + x[j*(d+1)*ntsteps: j*(d+1)*ntsteps+ntsteps].sum()
        return tr

    fdim = dim * ntsteps
    lindb = cyt.floquetcomponent(dim, ntsteps, ws, lindw)
    if compute_gradient:
        dlindb = cyt.floquetcomponent2(Nu, dim, ntsteps, dlindw)

    b = scp.linalg.null_space(lindb)[:, 0:1]
    bw = b.reshape([dim, ntsteps])
    bt = np.zeros([dim, ntsteps], dtype = complex)
    for alpha in range(dim):
        bt[alpha, :] = scp.fft.ifft(bw[alpha, :]) * ntsteps
    rho0__ = bt[:, 0]
    rho0 = vectortodm(rho0__)
    trace = rho0.tr()
    trace2 = tracef(b)
    b = b / trace2
    bt = bt / trace2
    rho0 = rho0 / rho0.tr()

    if compute_gradient:

        rhs = np.zeros([dim*ntsteps, Nu], dtype = complex)
        for k in range(Nu):
            rhs[:, k] = - np.matmul(dlindb[k, :, :], b)[:, 0]
        x, residuals, rank, svs = np.linalg.lstsq(lindb, rhs, rcond = None)

        for k in range(Nu):
            x[:, k] = x[:, k] - tracef(x[:, k]) * b[:, 0]

        xw = np.zeros([Nu, dim, ntsteps], dtype = complex)
        for k in range(Nu):
            xw[k, :, :] = x[:, k].reshape([dim, ntsteps])

        xt = np.zeros([Nu, dim, ntsteps], dtype = complex)
        for k in range(Nu):
            for alpha in range(dim):
                xt[k, alpha, :] = scp.fft.ifft(xw[k, alpha, :]) * ntsteps

    if compute_gradient:
        return bt, xt, x
    else:
        return bt


class Nessopt:
    """
    class used for optimization of NESSs
    """
    def __init__(self, nessobjective, T, nts, L, glist):
        self.nessobjective = nessobjective
        self.target_operator = nessobjective[2]
        if self.target_operator is not None: 
            if self.nessobjective[0] == 'power':
                pass
            else:
                self.avector = dmtovector(self.target_operator).full()[:, 0]
        self.T = T
        self.nts = nts
        self.glist = glist
        self.L = L
        if len(self.nessobjective) > 3:
            self.Pu = self.nessobjective[3]
            self.dPdu = self.nessobjective[4]
        else:
            self.Pu = None
            self.dPdu = None

    def Afunc(self, y):
        if self.nessobjective[0] == 'purity':
            return np.vdot(y, y).real
        elif self.nessobjective[0] == 'entropy':
            rho = vectortodm(y).full()
            return np.trace(np.matmul( rho, scp.linalg.logm(rho) )).real
        elif self.nessobjective[0] == 'fidelity':
            sigma = vectortodm(self.avector).full()
            rho = vectortodm(y).full()
            return np.vdot(y, self.avector).real + 2.0 * np.sqrt( np.linalg.det(sigma).real * np.linalg.det(rho).real )
        else:
            return np.vdot(y, self.avector).real

    def F(self, y):
        if self.nessobjective[0] == 'purity':
            return self.Afunc(y[:, 0])
        elif self.nessobjective[0] == 'entropy':
            return self.Afunc(y[:, 0])
        elif self.nessobjective[0] == 'fidelity':
            return self.Afunc(y[:, 0])
        elif self.nessobjective[0] == 'power':
            if isinstance(self.nessobjective[2], list):
                Hfunc = self.nessobjective[2][0]
                Lfunc = self.nessobjective[2][1]
                P = self.nessobjective[3]
                V0 = Hfunc.V[0]
                args = { "f": [self.glist[l].fu for l in range(len(self.glist))] }
                times = np.linspace(0, self.T, self.nts+1)
                ft = pulses.pulse_time_derivative(self.glist[0])
                integrand = np.zeros(self.nts+1)
                for j in range(self.nts):
                    rhoness = vectortodm(qt.Qobj(y[:, j]))
                    integrand[j] = ft.fu(times[j]) * (rhoness * V0(times[j], args)).tr().real
                return -integrand[:-1].sum() / self.nts #+ P(self.glist[0].u)
            else:
                times = np.linspace(0, self.T, self.nts+1)
                ft = pulses.pulse_time_derivative(self.glist[0])
                integrand = np.zeros(self.nts+1)
                for j in range(self.nts):
                    integrand[j] = ft.fu(times[j]) * self.Afunc(y[:, j])
                return integrand[:-1].sum() / self.nts
        else:
            if self.nessobjective[1]:
                times = np.linspace(0, self.T, self.nts+1)
                integrand = np.zeros(self.nts+1)
                for j in range(self.nts):
                    integrand[j] = self.Afunc(y[:, j])
                integrand[self.nts] = integrand[0]
                return (1/self.T) * scp.integrate.simps(integrand, times)
            else:
                return self.Afunc(y[:, 0])

    def Fdy(self, y, dy):
        if self.nessobjective[0] == 'purity':
            nu = dy.shape[0]
            dfdy = np.zeros(nu)
            for j in range(nu):
                dfdy[j] = 2.0 * np.vdot(dy[j, :, 0], y[:, 0]).real
            return dfdy
        elif self.nessobjective[0] == 'entropy':
            rho = vectortodm(y[:, 0]).full()
            nu = dy.shape[0]
            dfdy = np.zeros(nu)
            for j in range(nu):
                drho = vectortodm(dy[j, :, 0]).full()
                dfdy[j] = np.trace( np.matmul(drho, scp.linalg.logm(rho) ) ).real
            return dfdy
        elif self.nessobjective[0] == 'fidelity':
            nu = dy.shape[0]
            amat = vectortodm(self.avector).full()
            rhomat = vectortodm(y[:, 0]).full()

            deta = np.linalg.det(amat).real
            detrho = np.linalg.det(rhomat).real

            dfdy = np.zeros(nu)
            for j in range(nu):
                dfdy[j] = np.vdot(dy[j, :, 0], self.avector).real
                drhomat = vectortodm(dy[j, :, 0]).full()
                ddetrho = drhomat[0, 0] * rhomat[1, 1] + drhomat[1, 1] * rhomat[0, 0] \
                          - rhomat[0, 1] * drhomat[1, 0] - rhomat[1, 0] * drhomat[0, 1]
                dfdy[j] = dfdy[j] + (deta / np.sqrt( deta * detrho)) * ddetrho.real
            return dfdy
        elif self.nessobjective[0] == 'power':
            if isinstance(self.nessobjective[2], list):
                Hfunc = self.nessobjective[2][0]
                Lfunc = self.nessobjective[2][1]
                V0 = Hfunc.V[0]
                args = { "f": [self.glist[l].fu for l in range(len(self.glist))] }

                nuf0 = self.glist[0].nu
                nu = dy.shape[0]
                nts = dy.shape[2]
                times = np.linspace(0, self.T, nts+1)
                integrand = np.zeros([nu, nts+1])

                ft = self.glist[0]
                dftdt = pulses.pulse_time_derivative(self.glist[0])

                for l in range(nuf0):
                    dftdu = pulses.pulse_parameter_derivative(self.glist[0], l)
                    d2dfdudt = pulses.pulse_time_derivative(dftdu)
                    for j in range(nts):
                        rhoness = vectortodm(qt.Qobj(y[:, j]))
                        drhoness = vectortodm(qt.Qobj(dy[l, :, j]))
                        integrand[l, j] = dftdt.fu(times[j]) * (drhoness * V0(times[j], args)).tr().real + \
                                          d2dfdudt.fu(times[j]) * (rhoness * V0(times[j], args)).tr().real

                for l in range(nuf0, nu):
                    for j in range(nts):
                        rhoness = vectortodm(qt.Qobj(y[:, j]))
                        drhoness = vectortodm(qt.Qobj(dy[l, :, j]))
                        integrand[l, j] = dftdt.fu(times[j]) * (drhoness * V0(times[j], args)).tr().real

                return -np.array( [ integrand[l, :-1].sum() / self.nts for l in range(nu)] )
            else:
                nu = dy.shape[0]
                nts = dy.shape[2]
                times = np.linspace(0, self.T, nts+1)
                integrand = np.zeros([nu, nts+1])
                dftdt = pulses.pulse_time_derivative(self.glist[0])
                for l in range(nu):
                    dftdu = pulses.pulse_parameter_derivative(self.glist[0], l)
                    d2dfdudt = pulses.pulse_time_derivative(dftdu)
                    for j in range(nts):
                        integrand[l, j] = dftdt.fu(times[j]) * self.Afunc(dy[l, :, j]) + \
                                          d2dfdudt.fu(times[j]) * self.Afunc(y[:, j])
                return np.array( [ integrand[l, :-1].sum() / self.nts for l in range(nu)] )
        else:
            nu = dy.shape[0]
            nts = dy.shape[2]
            times = np.linspace(0, self.T, nts+1)
            integrand = np.zeros([nu, nts+1])
            if self.nessobjective[1]:
                for l in range(nu):
                    for j in range(nts):
                        integrand[l, j] = self.Afunc(dy[l, :, j])
                    integrand[l, nts] = self.Afunc(dy[l, :, 0])
                return np.array( [ (1/self.T) * scp.integrate.simps(integrand[l, :], times) for l in range(nu)] )
            else:
                return np.array( [ self.Afunc(dy[l, :, 0]) for l in range(nu) ] )

    def G(self, u):
        pulses.pulse_collection_set_parameters(self.glist, u)
        y0 = ness(self.T, self.nts, self.L, self.glist)
        if self.Pu is None:
            return self.F(y0)
        else:
            return self.F(y0) + self.Pu(u)

    def gradG(self, u):
        pulses.pulse_collection_set_parameters(self.glist, u)
        y0, drhostdu, dy_ = ness(self.T, self.nts, self.L, self.glist, compute_gradient = True)
        Fy0 = self.F(y0)

        if self.Pu is None:
            gradG = self.Fdy(y0, drhostdu)
            return Fy0, gradG
        else:
            dpdu = np.zeros(u.shape[0])
            for m in range(u.shape[0]):
                dpdu[m] = self.nessobjective[4](u, m)
            gradG = self.Fdy(y0, drhostdu) + dpdu
        return Fy0 + self.Pu(u), gradG

    def dGdu_fd(self, u, m, delta = 0.01):
        pulses.pulse_collection_set_parameters(self.glist, u)
        def f(x):
            u0 = u.copy()
            u0[m] = x
            return self.G(u0)
        val, err = diff_ridders(f, u[m], delta)
        pulses.pulse_collection_set_parameters(self.glist, u)
        return val

    def gradG_fd(self, u):
        p = u.shape[0]
        dGdunum = np.zeros(p)
        for m in range(p):
            dGdunum[m] = self.dGdu_fd(u, m)
        return dGdunum

    def make_G(self):
        def Gfunction(u, grad = None):
            g1 = self.glist[0]
            g2 = self.glist[1]
            pulses.pulse_collection_set_parameters([g1, g2], u)
            if (grad is not None) and (grad.size > 0):
                Gu, grad[:] = self.gradG(u)
                pulses.pulse_collection_set_parameters([g1, g2], u)
                return Gu
            else:
                return self.G(u)
        return Gfunction
