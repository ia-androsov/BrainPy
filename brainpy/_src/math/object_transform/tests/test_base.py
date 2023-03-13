# -*- coding: utf-8 -*-

import unittest

import jax.tree_util

import brainpy as bp
import brainpy.math as bm


class TestCollectionFunction(unittest.TestCase):
  def test_f_nodes(self):
    class C(bp.DynamicalSystem):
      def __init__(self):
        super(C, self).__init__()

    class B(bp.DynamicalSystem):
      def __init__(self):
        super(B, self).__init__()

        self.child1 = C()
        self.child2 = C()

    class A(bp.DynamicalSystem):
      def __init__(self):
        super(A, self).__init__()

        self.child1 = B()
        self.child2 = B()

    net = bp.Network(a1=A(), a2=A())
    print(net.nodes(level=2))
    self.assertTrue(len(net.nodes(level=0)) == 1)
    self.assertTrue(len(net.nodes(level=0, include_self=False)) == 0)
    self.assertTrue(len(net.nodes(level=1)) == (1 + 2))
    self.assertTrue(len(net.nodes(level=1, include_self=False)) == 2)
    self.assertTrue(len(net.nodes(level=2)) == (1 + 2 + 4))
    self.assertTrue(len(net.nodes(level=2, include_self=False)) == (2 + 4))
    self.assertTrue(len(net.nodes(level=3)) == (1 + 2 + 4 + 8))
    self.assertTrue(len(net.nodes(level=3, include_self=False)) == (2 + 4 + 8))

  def test_f_vars(self):
    class C(bp.DynamicalSystem):
      def __init__(self):
        super(C, self).__init__()

        self.var1 = bm.Variable(bm.zeros(1))
        self.var2 = bm.Variable(bm.zeros(1))

    class B(bp.DynamicalSystem):
      def __init__(self):
        super(B, self).__init__()

        self.child1 = C()
        self.child2 = C()

        self.var1 = bm.Variable(bm.zeros(1))
        self.var2 = bm.Variable(bm.zeros(1))

    class A(bp.DynamicalSystem):
      def __init__(self):
        super(A, self).__init__()

        self.child1 = B()
        self.child2 = B()

        self.var1 = bm.Variable(bm.zeros(1))
        self.var2 = bm.Variable(bm.zeros(1))

    net = bp.Network(a1=A(), a2=A())
    print(net.vars(level=2))
    self.assertTrue(len(net.vars(level=0)) == 0)
    self.assertTrue(len(net.vars(level=0, include_self=False)) == 0)
    self.assertTrue(len(net.vars(level=1)) == 2 * 2)
    self.assertTrue(len(net.vars(level=1, include_self=False)) == 2 * 2)
    self.assertTrue(len(net.vars(level=2)) == (2 + 4) * 2)
    self.assertTrue(len(net.vars(level=2, include_self=False)) == (2 + 4) * 2)
    self.assertTrue(len(net.vars(level=3)) == (2 + 4 + 8) * 2)
    self.assertTrue(len(net.vars(level=3, include_self=False)) == (2 + 4 + 8) * 2)


class Test_retrival(unittest.TestCase):
  def test_NodeList_1(self):
    class Object(bp.DynamicalSystemNS):
      def __init__(self):
        super().__init__()

        self.l1 = bp.layers.Dense(5, 10)
        self.ls = bm.NodeList([bp.layers.Dense(10, 4),
                               bp.layers.Activation(bm.tanh),
                               bp.layers.Dropout(0.1),
                               bp.layers.Dense(4, 5),
                               bp.layers.Activation(bm.relu)])

      def update(self, x):
        x = self.l1(x)
        for l in self.ls:
          x = l(x)
        return x

    with bm.environment(mode=bm.NonBatchingMode()):
      obj = Object()
      self.assertTrue(len(obj.vars()) == 1)
      self.assertTrue(len(obj.nodes()) == 7)
      self.assertTrue(len(jax.tree_util.tree_leaves(obj)) == 1)

      print(obj.nodes().keys())
      print("obj.nodes(method='relative'): ",
            obj.nodes(method='relative').keys())
      # print(jax.tree_util.tree_structure(obj))

    with bm.environment(mode=bm.TrainingMode()):
      obj = Object()
      self.assertTrue(len(obj.vars()) == 7)
      self.assertTrue(len(obj.nodes()) == 7)
      self.assertTrue(len(jax.tree_util.tree_leaves(obj)) == 7)

      print(obj.nodes().keys())
      print("obj.nodes(method='relative'): ",
            obj.nodes(method='relative').keys())
      # print(jax.tree_util.tree_structure(obj))

  def test_NodeDict_1(self):
    class Object(bp.DynamicalSystemNS):
      def __init__(self):
        super().__init__()

        self.l1 = bp.layers.Dense(5, 10)
        self.ls = bm.NodeDict(
          {
            'l1': bp.layers.Dense(10, 4),
            'l2': bp.layers.Activation(bm.tanh),
            'l3': bp.layers.Dropout(0.1),
            'l4': bp.layers.Dense(4, 5),
            'l5': bp.layers.Activation(bm.relu)
          }
        )

      def update(self, x):
        x = self.l1(x)
        for l in self.ls:
          x = l(x)
        return x

    with bm.environment(mode=bm.NonBatchingMode()):
      obj = Object()
      self.assertTrue(len(obj.vars()) == 1)
      self.assertTrue(len(obj.nodes()) == 7)
      self.assertTrue(len(jax.tree_util.tree_leaves(obj)) == 1)

      print(obj.nodes().keys())
      print("obj.nodes(method='relative'): ",
            obj.nodes(method='relative').keys())
      # print(jax.tree_util.tree_structure(obj))

    with bm.environment(mode=bm.TrainingMode()):
      obj = Object()
      self.assertTrue(len(obj.vars()) == 7)
      self.assertTrue(len(obj.nodes()) == 7)
      self.assertTrue(len(jax.tree_util.tree_leaves(obj)) == 7)

      print(obj.nodes().keys())
      print("obj.nodes(method='relative'): ",
            obj.nodes(method='relative').keys())
      # print(jax.tree_util.tree_structure(obj))

  def test_ListVar_1(self):
    class Object(bp.DynamicalSystemNS):
      def __init__(self):
        super().__init__()
        self.vs = bm.ListVar([1., 2., bm.ones(10)])

      def update(self):
        self.vs[0] += 10.
        self.vs[1] += 10.
        self.vs[2] += 10.

    obj = Object()
    self.assertTrue(len(obj.vars()) == 1)
    self.assertTrue(len(obj.nodes()) == 1)
    self.assertTrue(len(jax.tree_util.tree_leaves(obj)) == 3)

    @jax.jit
    def f1(ob):
      ob()
      return ob

    obj = f1(obj)
    print(obj.vs)
    self.assertTrue(obj.vs[0] == 11.)
    self.assertTrue(obj.vs[1] == 12.)
    self.assertTrue(bm.allclose(obj.vs[2], bm.ones(10) * 11.))

    @bm.jit(child_objs=obj)
    def f2():
      obj()

    f2()
    print(obj.vs)
    self.assertTrue(obj.vs[0] == 21.)
    self.assertTrue(obj.vs[1] == 22.)
    self.assertTrue(bm.allclose(obj.vs[2], bm.ones(10) * 21.))

  def test_DictVar_1(self):
    class Object(bp.DynamicalSystemNS):
      def __init__(self):
        super().__init__()
        self.vs = bm.DictVar({'a': 1., 'b': 2., 'c': bm.ones(10)})

      def update(self):
        self.vs['a'] += 10.
        self.vs['b'] += 10.
        self.vs['c'] += 10.

    obj = Object()
    self.assertTrue(len(obj.vars()) == 1)
    self.assertTrue(len(obj.nodes()) == 1)
    self.assertTrue(len(jax.tree_util.tree_leaves(obj)) == 3)

    @jax.jit
    def f1(ob):
      ob()
      return ob

    obj = f1(obj)
    print(obj.vs)
    self.assertTrue(obj.vs['a'] == 11.)
    self.assertTrue(obj.vs['b'] == 12.)
    self.assertTrue(bm.allclose(obj.vs['c'], bm.ones(10) * 11.))

    @bm.jit(child_objs=obj)
    def f2():
      obj()

    f2()
    print(obj.vs)
    self.assertTrue(obj.vs['a'] == 21.)
    self.assertTrue(obj.vs['b'] == 22.)
    self.assertTrue(bm.allclose(obj.vs['c'], bm.ones(10) * 21.))


class TestListVar(unittest.TestCase):
  def test_grad(self):
    # TODO
    pass

  def test_vector_grad(self):
    # TODO
    pass

  def test_forloop(self):
    # TODO
    pass

  def test_ifelse(self):
    # TODO
    pass


