# -*- coding: utf-8 -*-

from importlib import import_module

import numpy.linalg

_all = [
    'cholesky', 'cond', 'det', 'eig', 'eigh', 'eigvals', 'eigvalsh', 'inv', 'svd',
    'lstsq', 'matrix_power', 'matrix_rank', 'norm', 'pinv', 'qr', 'slogdet', 'solve',
]

cholesky = numpy.linalg.cholesky
cond = numpy.linalg.cond
det = numpy.linalg.det
eig = numpy.linalg.eig
eigh = numpy.linalg.eigh
eigvals = numpy.linalg.eigvals
eigvalsh = numpy.linalg.eigvalsh
inv = numpy.linalg.inv
svd = numpy.linalg.svd
lstsq = numpy.linalg.lstsq
matrix_power = numpy.linalg.matrix_power
matrix_rank = numpy.linalg.matrix_rank
norm = numpy.linalg.norm
pinv = numpy.linalg.pinv
qr = numpy.linalg.qr


def _reload(backend):
    global_vars = globals()

    if backend == 'numpy':
        for __ops in _all:
            global_vars[__ops] = getattr(numpy.linalg, __ops)

    elif backend == 'numba':
        from ._backends import numba

        for __ops in _all:
            if hasattr(numba, __ops):
                global_vars[__ops] = getattr(numba, __ops)
            else:
                global_vars[__ops] = getattr(numpy.linalg, __ops)

    elif backend == 'jax':
        jax = import_module('jax')

        for __ops in _all:
            global_vars[__ops] = getattr(jax.linalg, __ops)

    elif backend == 'tensorflow':
        pass


    else:
        raise ValueError(f'Unknown backend device: {backend}')