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

import subprocess
import os
import tempfile
import shutil
import numpy as np
from distutils.dir_util import copy_tree
import pytest


def run_test(n, name = None, datafile = None, reltol = 1.0e-6, abstol = 1.0e-12):
    tempdir = tempfile.mkdtemp()
    if type(n) is int:
         n = str(n)
    dirname = os.path.dirname(__file__) + '/../sampleruns/' + n
    copy_tree(dirname, tempdir)
    cdir = os.getcwd()
    os.chdir(tempdir)
    if name is not None:
        fname = name
    else:
        fname = ' sample'+n
    i = subprocess.call('jupyter nbconvert ' + fname + '.ipynb --to python', shell = True)
    j = subprocess.call('python ' + fname +'.py', shell = True)
    datacomp = True
    if datafile is not None:
        data = np.loadtxt(datafile)
        dataref = np.loadtxt(datafile+'.ref')
        datacomp = (data == pytest.approx(dataref, rel = reltol, abs = abstol))
    os.chdir(cdir)
    if (i, j) == (0 , 0) and datacomp:
        shutil.rmtree(tempdir)
    else:
        print("Failed test directory at " + tempdir)
    return i, j, datacomp


def run_test2(name, datafile = None):
    tempdir = tempfile.mkdtemp()
    cdir = os.getcwd()
    fname = os.path.dirname(__file__) + '/../../docs/tutorials/' + name
    shutil.copyfile(fname, tempdir + '/' + name)
    os.chdir(tempdir)
    i = subprocess.call('jupyter nbconvert ' + name + ' --execute --to python', shell = True)
    datacomp = True
    if datafile is not None:
        data = np.loadtxt('data')
        dataref = np.loadtxt( os.path.dirname(__file__) + '/../../docs/tutorials/' + datafile )
        datacomp = (data == pytest.approx(dataref))
    return i, datacomp


def test_rotations():
    i, j, datacomp = run_test('rotations', name = 'rotations', datafile = 'data')
    assert  (i, j) == (0, 0) and datacomp

def test_propagators_psi():
    i, j, datacomp = run_test('propagators-psi', name = 'propagators-psi', datafile = 'data',
                              reltol = 1.0e-3, abstol = 1.0e-8)
    assert  (i, j) == (0, 0) and datacomp

def test_propagators_U():
    i, j, datacomp = run_test('propagators-U', name = 'propagators-U', datafile = 'data',
                              reltol = 1.0e-3, abstol = 1.0e-8)
    assert  (i, j) == (0, 0) and datacomp

def test_propagators_rho():
    i, j, datacomp = run_test('propagators-rho', name = 'propagators-rho', datafile = 'data',
                              reltol = 1.0e-3, abstol = 1.0e-8)
    assert  (i, j) == (0, 0) and datacomp

def test_gradient_psi():
    i, j, datacomp = run_test('gradient-psi', name = 'gradient-psi', datafile = 'data')
    assert  (i, j) == (0, 0) and datacomp

def test_gradient_U():
    i, j, datacomp = run_test('gradient-U', name = 'gradient-U', datafile = 'data')
    assert  (i, j) == (0, 0) and datacomp

def test_gradient_rho():
    i, j, datacomp = run_test('gradient-rho', name = 'gradient-rho', datafile = 'data')
    assert  (i, j) == (0, 0) and datacomp

def test_qoctbasic():
    i, j, datacomp = run_test('qoctbasic', name = 'qoctbasic', datafile = 'data')
    assert  (i, j) == (0, 0) and datacomp

def test_floquet():
    i, j, datacomp = run_test('floquet', name = 'floquet', datafile = 'data')
    assert  (i, j) == (0, 0) and datacomp

def test_tutorials_closed():
    i, datacomp = run_test2("closed.ipynb", datafile = 'data.closed')
    assert i == 0 and datacomp

def test_tutorials_closed_gate():
    i, datacomp = run_test2("closed-gate.ipynb", datafile = 'data.closed_gate')
    assert i == 0 and datacomp

def test_tutorials_closed_gate_cnot():
    i, datacomp = run_test2("closed-gate-cnot.ipynb", datafile = 'data.closed_gate_cnot')
    assert i == 0 and datacomp

def test_tutorials_floquet_closed():
    i, datacomp = run_test2("floquet-closed.ipynb", datafile = 'data.floquet_closed')
    assert i == 0 and datacomp

def test_tutorials_floquet_open():
    i, datacomp = run_test2("floquet-open.ipynb", datafile = 'data.floquet_open')
    assert i == 0 and datacomp

# This file should be run as "py.test -v qocttools_tests.py"
# Or, even better: "pytest -n NPROCS --durations=0 -v qocttools_tests.py"
# where NPROCS is the number of cores that can be used in parallel.
