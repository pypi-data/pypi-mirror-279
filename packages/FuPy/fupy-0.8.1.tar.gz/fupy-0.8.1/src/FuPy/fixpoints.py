"""
Definitions to support various fixpoints, both on the type level and the value level.

Copyright (c) 2024 - Eindhoven University of Technology, The Netherlands

This software is made available under the terms of the MIT License.
"""
from dataclasses import dataclass
from typing import Final, Callable, Protocol

from FuPy.basics import *
from FuPy.laziness import *

__all__ = [
    "fix",
    "Functor", "fmap", "Fmap",
    "Fix", "in_", "out",
    "F_Algebra", "cata", "cata_",
    "F_CoAlgebra", "ana", "ana_",
    "hylo"
]


@func
def fix[A](f: Callable[[A], A]) -> A:
    """Return fixpoint of f.

    Uses laziness to avoid infinite recursion.
    The call fix(f) will result in f(Lazy(lambda: fix(f))).
    Thus, the argument of f is made lazy.  TODO: Why "make fix lazy"?  Terminology needs reconsideration.
    """
    f = func(f)
    # return f(Lazy(lambda: fix(f)))
    return f(lazy(fix)(f))


class Functor[X](Protocol):
    """Type class for functors.

    Deprecated (for use with (co)inductive types).
    """
    def __fmap__[Y](self, f: Callable[[X], Y]) -> "Functor[Y]":
        """Apply f inside self.
        """


@func
def fmap[F, X, Y](f: Callable[[X], Y]) -> "Callable[[F[X]], F[Y]]":
    """Apply functor F to function f in X -> Y to get function F[X] -> F[Y].

    Deprecated (for use with (co)inductive types).
    """
    @func(name=f"fmap({f})")
    def fmf(fx: "F[X]") -> "F[Y]":
        """Define F[f].
        """
        return fx.__fmap__(f)

    return fmf


# How a functor operates on functions
type Fmap[F, X, Y] = "Callable[ [Callable[[X], Y]], Callable[[F[X]], F[Y]] ]"


# type Iter[F: Functor, A] = A | F[Iter[F, A]]  # not accepted


@dataclass
class Fix[F: Functor]:
    """Fix[F] is fixpoint data type for functor F.

    For a lazy Fix, invoke as Fix(Lazy(lambda: v)).
    An alternative would be to define locally:

    .. code-block:: python

        class LazyFix[F, X](Fix[F[X]]):
            def unFix(self) -> F[Fix[F]]:
                return v

        ... LazyFix(None) ...

    """
    _unFix: "Final[F[Fix[F]] | Lazy[F[Fix[F]]]]"

    def unFix(self) -> "F[Fix[F]]":
        return evaluate(self._unFix)

    def __fmap__[G](self, f: Callable[[F], G]) -> "Callable[[Fix[F]], Fix[G]]":
        return Fix(f(self.unFix()))


@func(name="in")
def in_[F: Functor](a: "F[Fix[F]]") -> Fix[F]:
    """Constructor F-algebra of Fix[F].

    Deprecated type bound Functor.
    """
    return Fix(a)


@func
def out[F: Functor](a: Fix[F] | Lazy[Fix[F]]) -> "F[Fix[F]]":
    """Deconstructor F-coalgebra of Fix[F].

    Inverse of in.
    Deprecated type bound Functor.
    """
    return evaluate(a).unFix()  # TODO: why is evaluate needed?


type F_Algebra[F: Functor, X] = Callable[[F[X]], X]
# Deprecated type bound Functor.


@func(name="⦇ … ⦈_F")
def cata[F, X, Y](fmap: Fmap[F, X, Y]
                  ) -> "Callable[[F_Algebra[F, X]], Callable[[Fix[F]], X]]":
    """Construct catamorphism given functor and F-algebra (curried).
    """
    # below, lazy(rec) is needed in case the cata is applied to an infinite input
    # see prelude_test.py, test_cata_on_infinite_value()
    # N.B. This does mean that the algebra must call evaluate on the recursive input(s)
    # when this is not done automatically while processing infinite structures.
    return Func(lambda alg: (fix(lambda rec: alg @ fmap(lazy(rec)) @ out)
                             ).rename(f"⦇ {alg} ⦈_{fmap}"),
                name=f"⦇ … ⦈_{fmap}")


@func(name="⦇ … ⦈")
def cata_[F: Functor, X](alg: F_Algebra[F, X]) -> Callable[[Fix[F]], X]:
    """For F-algebra alg, construct catamorphism in Fix[F] -> X.

    Deprecated.
    """
    # return fix(lambda rec: alg @ fmap(rec) @ out)  # efficiency?
    @func(name=f"⦇ {alg} ⦈")
    def rec(a: Fix[F]) -> X:
        """rec = alg o F.rec o out"""
        return alg(fmap(rec)(out(a)))  # lazyf(rec) needed?
        # return (alg @ fmap(rec) @ out)(a)  # less efficient?

    return rec


type F_CoAlgebra[F: Functor, X] = Callable[[X], F[X]]
# Deprecated type bound Functor.


@func(name="〖 … 〗_F")
def ana[F, X, Y](fmap: Fmap[F, X, Y]
                 ) -> "Callable[[F_CoAlgebra[F, X]], Callable[[X], Fix[F]]]":
    """Construct anamorphism given functor and F-coalgebra (curried).
    """
    # below, lazy(rec) is needed in case the ana produces an (potentially) infinite result
    # N.B. lazy(fmap(rec)) is not good enough
    return Func(lambda coalg: (fix(lambda rec: in_ @ fmap(lazy(rec)) @ coalg)
                               ).rename(f"〖 {coalg} 〗_{fmap}"),
                name=f"〖 … 〗_{fmap}")


@func(name="〖 … 〗")
def ana_[F: Functor, X](coalg: F_CoAlgebra[F, X]) -> Callable[[X], Fix[F]]:
    """For F-coalgebra coalg, construct anamorphism in X -> Fix[F].

    Laziness needs to be built into the functor (?).
    Deprecated. ?
    """
    # return fix(lambda rec: in_ @ fmap(rec) @ coalg)  # not lazy; efficiency?
    @func(name=f"〖 {coalg} 〗")
    def rec(x: X) -> Fix[F]:
        """rec = in o F.rec o coalg"""
        return in_(fmap(rec)(coalg(x)))
        # return (in_ @ fmap(rec) @ coalg)(x)  # less efficient

    return rec


@func(name="⦇ … ⦈_F ⚬〖 … 〗_F")
def hylo[F, X, Y](fmap: Fmap[F, X, Y]
                ) -> "Callable[[F_Algebra[F, X], F_CoAlgebra[F, X]], Callable[[X], Y]]":
    """Construct hylomorphism given functor and F-(co)algebras (curried).
    """
    return lambda alg, coalg: Func(fix(lambda rec: alg @ fmap(lazy(rec)) @ coalg),
                                   name=f"⦇ {alg} ⦈ ⚬〖 {coalg} 〗")
