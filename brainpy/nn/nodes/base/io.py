# -*- coding: utf-8 -*-

from typing import Tuple, Union

from brainpy.nn.base import Node
from brainpy.nn.constants import PASS_ONLY_ONE
from brainpy.tools.others import to_size

__all__ = [
  'Input',
]


class Input(Node):
  """The input node."""

  data_pass_type = PASS_ONLY_ONE

  def __init__(self,
               shape: Union[Tuple[int], int],
               name: str = None):
    super(Input, self).__init__(name=name, input_shape=shape)
    self.set_input_shapes({self.name: (None,) + to_size(shape)})
    self._ff_init()

  def init_ff(self):
    self.set_output_shape(self.input_shapes)

  def forward(self, ff, **kwargs):
    return ff
