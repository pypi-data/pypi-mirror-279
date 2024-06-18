"""
Definitions to support lazy expressions.

Copyright (c) 2024 - Eindhoven University of Technology, The Netherlands

This software is made available under the terms of the MIT License.
"""
from typing import Callable, Optional, override, Any

import FuPy.tracing as tr
from FuPy import utils
from FuPy.basics import *
from FuPy.tracing_laziness import *

__all__ = [
    "Lazy", "IterLazy", "evaluate", "lazy", "lazyf",
]


class Lazy[A]:
    """A lazy value of type A, with memoization upon evaluation.

    See: https://en.wikipedia.org/wiki/Lazy_evaluation
    A.k.a. as thunk: https://en.wikipedia.org/wiki/Thunk
    Sharing of lazy values is encouraged, since they need to be evaluated only once.

    Usage:

    - Construct by v = Lazy(lambda: expression)

      N.B. the lambda captures local names occurring in expression, in its closure

    - Get value by evaluate(v); for internal use only: v._get()

    """
    next_thunk_number = 0
    # full_regime = False  # laziness regime: full or minimal

    def __init__(self, value: Callable[[], A] | A, name: Optional[str] = None) -> None:
        self.value = value  # unevaluated expression or cached evaluation result of the expression
        self.name = name
        self.nesting_count = 0  # number of times that nested Lazy expression is copied
        self.hit_count = 0  # number of times the cached value was used; 0 means unevaluated
        self.thunk_number = Lazy.next_thunk_number
        Lazy.next_thunk_number += 1
        tr.trace_step(lambda: SuspensionStep(f"{self}"))

    @override
    def __repr__(self) -> str:
        if self.nesting_count:
            nesting_state = f", nesting_count={self.nesting_count}"
        else:
            nesting_state = ""
        if self.hit_count:
            state = f"value={utils.show_value(self.value)}, thunk_number={self.thunk_number}{nesting_state}, hit_count={self.hit_count}"
        else:
            state = f"unevaluated={self.name or '`...`'}, thunk_number={self.thunk_number}"
        return f"Lazy({state})"

    def __str__(self) -> str:
        if self.hit_count:
            status = f"= {utils.show_value(self.value)}"
        else:
            status = f": {self.name or '`...`'}"
        return f"(θ_{self.thunk_number} {status})"

    def _get(self) -> A:
        """Evaluate lazy value, with caching/memoization.
        Repeats until result is not Lazy.
        This is useful to implement tail call elimination.
        """
        unevaluated = not self.hit_count
        nesting_comment = ""

        while unevaluated:
            tr.trace_step(lambda: EvaluationStep(f"{self}{nesting_comment}"))
            tr.inc_depth()
            self.value = self.value()  # take off lambda: wrapper; result could be Lazy again
            tr.dec_depth()
            if isinstance(self.value, Lazy):  # flatten, avoiding recursion (that would burden the stack)
                self.nesting_count += 1
                nesting_comment = f" {{nesting count: {self.nesting_count}}}" if self.nesting_count else ''
                unevaluated = not self.value.hit_count
                self.name = self.value.name
                self.value = self.value.value
            else:
                unevaluated = False

        self.hit_count += 1
        tr.trace_step(lambda: GettingStep(f"{self}"))
        return self.value

    def __call__[A, B](self: "Lazy[Callable[[A], B]]", arg) -> "Lazy[B]":
        """Apply as function.

        Assumption: self is Func instance

        For Weak Head Normal Form, the function itself is evaluated first.
        """
        # if Lazy.full_regime:
        #     return Lazy[B](lambda: lambda a: self._get()(a))
        # else:
        self._get()
        if not callable(self.value):
            raise TypeError(f"value in {self!r} is not callable")
        return self.value(arg)  # wrap this in Lazy again?

    def __add__(self, other):
        # if Lazy.full_regime:
        #     print("LAZY ADD")
        #     return Lazy(lambda: self._get() + other)
        # else:
        return self._get() + other

    def __radd__(self, other):
        # if Lazy.full_regime:
        #     return Lazy(lambda: other + self._get())
        # else:
        return other + self._get()

    def __sub__(self, other):
        # if Lazy.full_regime:
        #     return Lazy(lambda: self._get() - other)
        # else:
        return self._get() - other

    def __rsub__(self, other):
        # if Lazy.full_regime:
        #     return Lazy(lambda: other - self._get())
        # else:
        return other + self._get()

    def __mul__(self, other):
        # if Lazy.full_regime:
        #     return Lazy(lambda: self._get() * other)
        # else:
        return self._get() * other

    def __rmul__(self, other):
        # if Lazy.full_regime:
        #     return Lazy(lambda: other * self._get())
        # else:
        return other * self._get()

    def __getitem__(self, item):
        """Subscription triggers evaluation.
        Assumption: type A is subscriptable
        """
        # if Lazy.full_regime:
        #     return Lazy(lambda: self._get()[item])
        # else:
        return self._get()[item]

    # TODO: support other operators that automatically evaluate: __add__, etc.


type IterLazy[A] = A | Lazy[IterLazy[A]]  # for use in case of Tail Call Elimination


@func
def evaluate[A](v: Lazy[A] | A) -> A:
    """Evaluate v.
    """
    if isinstance(v, Lazy):
        return v._get()
    else:
        return v


def lazy[A, B](expr: Callable[[A], B] | str) -> Func[A, Lazy[B]] | Lazy[Any]:
    """Make expr lazy.

    Assumption: if expr is a string, then it doesn't contain local variables
    TODO: capture local variables; la needs to look one further stack frame up.

    If expr is callable, then expr(a) is equivalent to Lazy(lambda: expr(a)).
    """
    if callable(expr):
        expr = func(expr)
        return Func(lambda arg: Lazy(lambda: expr(arg), name=f"`{expr}({utils.show_value(arg)})`"))
    else:  # string
        return Lazy(la(f": {expr}"), name=f"`{expr}`")


def lazyf[X, Y](f: Callable[[X], Y]) -> Callable[[Lazy[X]], Lazy[Y]]:
    """Apply Lazy as functor to f.
    That is, apply f inside Lazy.
    """
    return Func(lambda x: Lazy(lambda: f(x._get())))
