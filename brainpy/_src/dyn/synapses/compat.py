# -*- coding: utf-8 -*-

import warnings
from typing import Union, Dict, Callable

from brainpy._src.connect import TwoEndConnector
from brainpy._src.dyn.base import NeuGroup
from brainpy._src.dyn.synouts import COBA, CUBA
from brainpy._src.initialize import Initializer
from brainpy.types import ArrayType
from .abstract_models import Delta, Exponential, DualExponential, NMDA

__all__ = [
  'DeltaSynapse',
  'ExpCUBA',
  'ExpCOBA',
  'DualExpCUBA',
  'DualExpCOBA',
  'AlphaCUBA',
  'AlphaCOBA',
  'NMDA',
]


class DeltaSynapse(Delta):
  """Delta synapse.

  .. deprecated:: 2.1.13
     Please use "brainpy.dyn.synapses.Delta" instead.

  """

  def __init__(
      self,
      pre: NeuGroup,
      post: NeuGroup,
      conn: Union[TwoEndConnector, ArrayType, Dict[str, ArrayType]],
      conn_type: str = 'sparse',
      weights: Union[float, ArrayType, Initializer, Callable] = 1.,
      delay_step: Union[float, ArrayType, Initializer, Callable] = None,
      post_input_key: str = 'V',
      post_has_ref: bool = False,
      name: str = None,
  ):
    warnings.warn('Please use "brainpy.dyn.synapses.Delta" instead.', DeprecationWarning)
    super(DeltaSynapse, self).__init__(pre=pre,
                                       post=post,
                                       conn=conn,
                                       output=CUBA(post_input_key),
                                       name=name,
                                       comp_method=conn_type,
                                       g_max=weights,
                                       delay_step=delay_step,
                                       post_ref_key='refractory' if post_has_ref else None)


class ExpCUBA(Exponential):
  r"""Current-based exponential decay synapse model.

  .. deprecated:: 2.1.13
     Please use "brainpy.dyn.synapses.Exponential" instead.

  """

  def __init__(
      self,
      pre: NeuGroup,
      post: NeuGroup,
      conn: Union[TwoEndConnector, ArrayType, Dict[str, ArrayType]],
      conn_type: str = 'sparse',
      g_max: Union[float, ArrayType, Initializer, Callable] = 1.,
      delay_step: Union[int, ArrayType, Initializer, Callable] = None,
      tau: Union[float, ArrayType] = 8.0,
      name: str = None,
      method: str = 'exp_auto',
  ):
    super(ExpCUBA, self).__init__(pre=pre,
                                  post=post,
                                  conn=conn,
                                  name=name,
                                  comp_method=conn_type,
                                  g_max=g_max,
                                  delay_step=delay_step,
                                  tau=tau,
                                  method=method,
                                  output=CUBA())


class ExpCOBA(Exponential):
  """Conductance-based exponential decay synapse model.

  .. deprecated:: 2.1.13
     Please use "brainpy.dyn.synapses.Exponential" instead.
  """

  def __init__(
      self,
      pre: NeuGroup,
      post: NeuGroup,
      # connection
      conn: Union[TwoEndConnector, ArrayType, Dict[str, ArrayType]],
      conn_type: str = 'sparse',
      # connection strength
      g_max: Union[float, ArrayType, Initializer, Callable] = 1.,
      # synapse parameter
      tau: Union[float, ArrayType] = 8.0,
      E: Union[float, ArrayType] = 0.,
      # synapse delay
      delay_step: Union[int, ArrayType, Initializer, Callable] = None,
      # others
      method: str = 'exp_auto',
      name: str = None
  ):
    super(ExpCOBA, self).__init__(pre=pre,
                                  post=post,
                                  conn=conn,
                                  comp_method=conn_type,
                                  g_max=g_max,
                                  delay_step=delay_step,
                                  tau=tau,
                                  method=method,
                                  name=name,
                                  output=COBA(E=E))


class DualExpCUBA(DualExponential):
  r"""Current-based dual exponential synapse model.

  .. deprecated:: 2.1.13
     Please use "brainpy.dyn.synapses.DualExponential" instead.

  """

  def __init__(
      self,
      pre: NeuGroup,
      post: NeuGroup,
      conn: Union[TwoEndConnector, ArrayType, Dict[str, ArrayType]],
      conn_type: str = 'dense',
      g_max: Union[float, ArrayType, Initializer, Callable] = 1.,
      tau_decay: Union[float, ArrayType] = 10.0,
      tau_rise: Union[float, ArrayType] = 1.,
      delay_step: Union[int, ArrayType, Initializer, Callable] = None,
      method: str = 'exp_auto',
      name: str = None
  ):
    super(DualExpCUBA, self).__init__(pre=pre,
                                      post=post,
                                      conn=conn,
                                      comp_method=conn_type,
                                      g_max=g_max,
                                      tau_decay=tau_decay,
                                      tau_rise=tau_rise,
                                      delay_step=delay_step,
                                      method=method,
                                      name=name,
                                      output=CUBA())


class DualExpCOBA(DualExponential):
  """Conductance-based dual exponential synapse model.


  .. deprecated:: 2.1.13
     Please use "brainpy.dyn.synapses.DualExponential" instead.

  """

  def __init__(
      self,
      pre: NeuGroup,
      post: NeuGroup,
      conn: Union[TwoEndConnector, ArrayType, Dict[str, ArrayType]],
      conn_type: str = 'dense',
      g_max: Union[float, ArrayType, Initializer, Callable] = 1.,
      delay_step: Union[int, ArrayType, Initializer, Callable] = None,
      tau_decay: Union[float, ArrayType] = 10.0,
      tau_rise: Union[float, ArrayType] = 1.,
      E: Union[float, ArrayType] = 0.,
      method: str = 'exp_auto',
      name: str = None
  ):
    super(DualExpCOBA, self).__init__(pre=pre,
                                      post=post,
                                      conn=conn,
                                      comp_method=conn_type,
                                      g_max=g_max,
                                      tau_decay=tau_decay,
                                      tau_rise=tau_rise,
                                      delay_step=delay_step,
                                      method=method,
                                      name=name,
                                      output=COBA(E=E))


class AlphaCUBA(DualExpCUBA):
  r"""Current-based alpha synapse model.

  .. deprecated:: 2.1.13
     Please use "brainpy.dyn.synapses.Alpha" instead.

  """

  def __init__(
      self,
      pre: NeuGroup,
      post: NeuGroup,
      conn: Union[TwoEndConnector, ArrayType, Dict[str, ArrayType]],
      conn_type: str = 'dense',
      g_max: Union[float, ArrayType, Initializer, Callable] = 1.,
      delay_step: Union[int, ArrayType, Initializer, Callable] = None,
      tau_decay: Union[float, ArrayType] = 10.0,
      method: str = 'exp_auto',
      name: str = None
  ):
    super(AlphaCUBA, self).__init__(pre=pre,
                                    post=post,
                                    conn=conn,
                                    conn_type=conn_type,
                                    delay_step=delay_step,
                                    g_max=g_max,
                                    tau_decay=tau_decay,
                                    tau_rise=tau_decay,
                                    method=method,
                                    name=name)


class AlphaCOBA(DualExpCOBA):
  """Conductance-based alpha synapse model.

  .. deprecated:: 2.1.13
     Please use "brainpy.dyn.synapses.Alpha" instead.

  """

  def __init__(
      self,
      pre: NeuGroup,
      post: NeuGroup,
      conn: Union[TwoEndConnector, ArrayType, Dict[str, ArrayType]],
      conn_type: str = 'dense',
      g_max: Union[float, ArrayType, Callable, Initializer] = 1.,
      delay_step: Union[int, ArrayType, Initializer, Callable] = None,
      tau_decay: Union[float, ArrayType] = 10.0,
      E: Union[float, ArrayType] = 0.,
      method: str = 'exp_auto',
      name: str = None
  ):
    super(AlphaCOBA, self).__init__(pre=pre,
                                    post=post,
                                    conn=conn,
                                    conn_type=conn_type,
                                    delay_step=delay_step,
                                    g_max=g_max, E=E,
                                    tau_decay=tau_decay,
                                    tau_rise=tau_decay,
                                    method=method,
                                    name=name)