# -*- coding: utf-8 -*-

import math as pmath

from brainpy import errors
from brainpy import math as bmath
from brainpy.simulation.brainobjects.base import DynamicalSystem
from brainpy.simulation.utils import size2len

__all__ = [
  'Delay',
  'ConstantDelay',
]


class Delay(DynamicalSystem):
  """Base class to model delay variables.

  """
  def __init__(self, steps=('update',), name=None):
    super(Delay, self).__init__(steps=steps, monitors=None, name=name)

  def update(self, _t, _dt):
    raise NotImplementedError


class ConstantDelay(Delay):
  """Class used to model constant delay variables.

  For examples:

  >>> import brainpy as bp
  >>>
  >>> bp.ConstantDelay(size=10, delay=10.)
  >>> bp.ConstantDelay(size=100, delay=lambda: bp.math.random.randint(5, 10))
  >>> bp.ConstantDelay(size=100, delay= bp.math.random.random(100) * 4 + 10)

  Parameters
  ----------
  size : int, list of int, tuple of int
      The delay data size.
  delay : int, float, function, ndarray
      The delay time. With the unit of `brainpy.math.get_dt()`.
  name : str, optional
      The name.
  """

  def __init__(self, size, delay, name=None, dtype=None):
    # delay data size
    if isinstance(size, int):
      size = (size,)
    if not isinstance(size, (tuple, list)):
      raise errors.BrainPyError(f'"size" must a tuple/list of int, '
                                f'but we got {type(size)}: {size}')
    self.size = tuple(size)

    # delay time length
    self.delay = delay

    # data and operations
    if isinstance(delay, (int, float)):  # uniform delay
      self.uniform_delay = True
      self.num_step = int(pmath.ceil(delay / bmath.get_dt())) + 1
      self.data = bmath.Variable(bmath.zeros((self.num_step,) + self.size, dtype=dtype))
      self.out_idx = bmath.Variable(0)
      self.in_idx = bmath.Variable(self.num_step - 1)

      self.push = self._push_for_uniform_delay
      self.pull = self._pull_for_uniform_delay
    else:  # non-uniform delay
      self.uniform_delay = False
      if not len(self.size) == 1:
        raise NotImplementedError(f'Currently, BrainPy only supports 1D '
                                  f'heterogeneous delays, while we got the '
                                  f'heterogeneous delay with {len(self.size)}'
                                  f'-dimensions.')
      self.num = size2len(size)
      if callable(delay):  # like: "delay=lambda: np.random.randint(5, 10)"
        temp = bmath.zeros(size)
        for i in range(size[0]):
          temp[i] = delay()
        delay = temp
      else:
        if bmath.shape(delay) != self.size:
          raise errors.BrainPyError(f"The shape of the delay time size must be "
                                    f"the same with the delay data size. But we "
                                    f"got {bmath.shape(delay)} != {self.size}")
      delay = bmath.around(delay / bmath.get_dt())
      self.diag = bmath.array(bmath.arange(self.num), dtype=bmath.int_)
      self.num_step = bmath.array(delay, dtype=bmath.int_) + 1
      self.data = bmath.Variable(bmath.zeros((self.num_step.max(),) + size, dtype=dtype))
      self.in_idx = bmath.Variable(self.num_step - 1)
      self.out_idx = bmath.Variable(bmath.zeros(self.num, dtype=bmath.int_))

      self.push = self._push_for_nonuniform_delay
      self.pull = self._pull_for_nonuniform_delay

    super(ConstantDelay, self).__init__(name=name)

  def _pull_for_uniform_delay(self):
    """Pull delayed data for variables with the uniform delay.
    """
    return self.data[self.out_idx]

  def _pull_for_nonuniform_delay(self):
    """Pull delayed data for variables with the non-uniform delay.
    """
    return self.data[self.out_idx, self.diag]

  def _push_for_uniform_delay(self, value):
    """Push the latest data to the delay bottom.
    """
    self.data[self.in_idx] = value

  def _push_for_nonuniform_delay(self, value):
    """Push the latest data to the delay bottom.
    """
    self.data[self.in_idx, self.diag] = value

  def update(self, _t, _dt):
    """Update the delay index.
    """
    self.in_idx[...] = (self.in_idx + 1) % self.num_step
    self.out_idx[...] = (self.out_idx + 1) % self.num_step

  def reset(self):
    """Reset the variables.
    """
    self.data[...] = 0
    self.in_idx[...] = self.num_step - 1
    self.out_idx[...] = 0