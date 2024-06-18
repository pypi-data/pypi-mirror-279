"""
Definitions to support functional programming in Python.
Especially aimed at educational use and not at industrial application.

Copyright (c) 2024 - Eindhoven University of Technology, The Netherlands

This software is made available under the terms of the MIT License.
"""
import collections.abc as abc
import inspect
import FuPy.tracing as tr
from dataclasses import dataclass
from functools import update_wrapper, wraps
from typing import Any, Final, Optional, Callable, Protocol, override

from FuPy import utils
from FuPy.tracing_basics import *

__all__ = [
    "Empty", "Unit", "unit",
    "Either", "Both",
    "Func", "func", "la",
    "undefined", "eq",
    "id_", "const", "left", "right", "guard", "first", "second",
    "curry", "uncurry", "flip", "ap",
    "compose", "split", "case_", "ftimes", "fplus", "fpower",
    "fpower_left",
    "x_",
]


class Empty:
    def __new__(cls, *args, **kwargs):
        raise TypeError("Empty cannot be instantiated")


class Unit:
    """The Unit type 𝟙 with only the unit value.

    A singleton class.
    """
    _has_instance = False

    def __init__(self) -> None:
        """Enforce singleton.
        """
        if Unit._has_instance:
            raise RuntimeError("Unit is a singleton class; use `unit` instead")
        Unit._has_instance = True

    @override
    def __repr__(self) -> str:
        return "unit"

    @override
    def __str__(self) -> str:
        return "_"  # 2IPH0 math notation

    def __len__(self) -> int:
        return 0

    def __iter__(self):
        """Makes unit unpackable.
        Also see __rmatmul__ (@) in Func.
        """
        return iter(())


unit: Final[Unit] = Unit()  # the unit value
# We could also have used () as unit value,
# but then we could not type hint it with tuple[]
# Also, then we could not give it a custom str/repr.


@dataclass
class Left[A]:
    """The left option of the sum type Either.
    """
    value: Final[A]


@dataclass
class Right[B]:
    """The right option of the sum type Either.
    """
    value: Final[B]


# Sum type A + B is Either[A, B]
type Either[A, B] = Left[A] | Right[B]


# Product type A x B is Both[A, B]
type Both[A, B] = tuple[A, B]


class Func[A, B]:
    """Wrapper for functions A -> B.

    Supports various operations on functions:

    - application (:code:`f(arg)`), composition (:code:`f @ g`)
    - split (:code:`f & g`), case (:code:`f | g`)
    - product (:code:`f * g`), sum (:code:`f + g`)
    - iteration (:code:`f ** n`)

    These operators can be sectioned.

    It would be nice if this could be incorporated into types.FunctionType
    (which is immutable; so, these cannot be added dynamically.)

    Note that in an FP language like Haskell, functions take exactly one argument
    (and return one result).
    That is why we give a Func the unit value as default argument.
    There is some tension between this view and the broader view of Python on functions
    (the latter can have no arguments or multiple arguments).
    The Func wrapper handles this by automatically (un)packing of arguments.
    Consider the call Func(f)(*args) where args is a tuple and
    f is defined as `def f(*fargs): ...` where fargs is also a tuple.
    Let R be the number of _required_ non-keyword arguments of f
    and :code:`A =  len(args)` the number of arguments of f.
    The call :code:`Func(f)(*args)` is handled as follows:

    +--------+-----------+-------------------+--------------+
    |        | A == 0    | A == 1            | A >= 2       |
    +========+===========+===================+==============+
    | R == 0 | f(*args)  | f(*(args[0])) (a) | TypeError    |
    +--------+-----------+-------------------+--------------+
    | R == 1 | f(unit)   | f(args[0])        | f(args) (b)  |
    +--------+-----------+-------------------+--------------+
    | R >= 2 | TypeError | f(*(args[0])) (c) | f(*args) (d) |
    +--------+-----------+-------------------+--------------+

    Notes:

    * (a) args[0] must behave like an empty tuple, e.g. unit.
    * (b) pack the arguments and pas them as a single tuple.
    * (c) unpack the argument and pass the unpacked values separately;
          N.B. the single argument must be an iterable of appropriate length
    * (d) the number of arguments provided and expected must match.
    * Keyword parameters are passed on.
    """
    COMBINATORS = {'@': '⚬', '&': '△', '|': '▽', '*': '⨯', '+': '+'}
    PRIORITIES = {'': 9, '.': 8, '^': 7, '@': 5, '&': 3, '*': 3, '|': 1, '+': 1}
    fully_parenthesize = False  # affects self.str()

    def __init__(self, f: Callable[..., B], name: Optional[str] = None,
                 r: Optional[int] = None, top: str = '') -> None:
        """Wrap f in Func.
        * self.name is how it prints in math notation.
        * self.r is minimum number of required arguments
          (None means: attempt to determine r from f, defaulting to 1)
        * self.top encodes top-level operator in f's construction
        """
        if r is None:
            try:
                r = utils.count_required_args(f)
            except ValueError as e:
                r = 1  # default for functions that cannot be inspected
        self.required_args_count = r
        self.func = f
        self.top = top  # top-level operator, used to suppress unneeded parentheses
        update_wrapper(self, f, updated={})
        self.name = name or (f.__name__ if hasattr(f, '__name__') else str(f))

    @override
    def __repr__(self) -> str:
        return f"Func({self}, r={self.required_args_count}, top={self.top!r})"

    @override
    def __str__(self) -> str:
        return self.name

    def str(self, op: str) -> str:
        """Return name in the context of operator op, adding parentheses if needed.
        """
        if Func.fully_parenthesize:
            if self.top not in ('', '^') or op == '':
                return f"({self})"
        if Func.PRIORITIES[self.top] > Func.PRIORITIES[op]:
            return str(self)
        elif self.top == op and op in ('^', '@'):
            return str(self)
        else:
            return f"({self})"

    def show_top(self) -> str:
        """Show top-level function for motivation of reduction.
        """
        if self.top == '':
            if self.name.startswith('(λ'):
                return self.name[1]
            return self.name
        elif self.top == '^':
            if self.name.endswith(('°', '?')):
                return self.name[-1]
            return '^'
        else:
            return Func.COMBINATORS[self.top]

    def rename(self, name: str, top: Optional[str] = None) -> "Func[A, B]":
        """Rename f.
        """
        self.name = name
        if top is not None:
            self.top = top
        return self

    def define_as(self, name: str) -> "Func[A, B]":
        """Define name as self.
        """
        tr.trace_step(lambda: DefinitionStep(f"{name}"))
        return Func(self, name=name, top='')

    def doc(self, docstring: str) -> "Func[A, B]":
        """Add docstring to self.
        """
        self.__doc__ = docstring
        return self

    def __call__(self, *args: A, **kwargs) -> B:
        """Apply self to args.
        """
        # TODO: Should keyword arguments be passed as well?
        actual_args_count = len(args)
        # print(f"{self} requires {self.required_args_count} args; provided args: {args}")
        # print(f"call entry: {self.str('^')}{args!r}")
        # Cases to distinguish
        # R = self.required_args_count
        # R == 0 and args == (): treat as unit; new_args = args; show as (unit)
        #        and args == (x,): check that x == unit or x == (); new_args = (); show as args
        #        and args == (x, y, ...): TypeError
        # R == 1 and args == (): new_args = (unit,); show as new_args
        #        and args == (x,): new_args = args; show as either, but when isinstance(x, tuple), show as x
        #        and args == (x, y, ...): new_args = (args,); auto pack; show as args
        # R >= 2 and args == (): TypeError
        #        and args == (x,): new_args = x; auto unpack; show as x
        #        and args == (x, y, ...): new_args = args; show as either
        comment = ""
        if self.required_args_count == 1:  # pass required one argument
            if actual_args_count == 1:  # "normal" 1-from-1: pass on as is
                new_args = args
                if isinstance(args[0], tuple):
                    show_args_as = args[0]  # avoid double parentheses around arguments
                else:
                    show_args_as = args
            elif not actual_args_count:  # the 1-from-0 case
                new_args = (unit,)
                show_args_as = new_args
                comment = "; auto-provide unit argument"
            else:  # 1-from-2+: pass as tuple (auto-pack)
                new_args = (args,)
                show_args_as = args
                comment = "; auto-pack arguments in tuple"
        else:  # f requires zero or more than one argument
            if actual_args_count == 1:  # x-from 1 where x != 1: auto-unpack the 1 argument
                new_args = args[0]  # it must be iterable and of matching length (checked below)
                if not self.required_args_count:  # 0-from-1: auto convert unit
                    if new_args is not unit and new_args != ():
                        raise TypeError(f"{self.func!r} requires no argument, but actual argument {new_args!r} is not unit")
                    show_args_as = (unit,)
                    comment = "; auto-provide unit argument"
                else:  # self.required_args_count >= 2
                    if not isinstance(new_args, tuple):
                        raise TypeError(f"{self.func!r} requires {self.required_args_count} arguments, "
                                        f"but actual argument {new_args!r} is not a tuple")
                    show_args_as = new_args
                    comment = "; auto-unpack arguments from tuple"
            else:  # x-from-y where y != 1: pass on as is (numbers must match; checked below)
                new_args = args
                show_args_as = args
        # print(f"  passed args: {new_args}")

        # TODO: in trace step, mention whether evaluation is lazy
        tr.trace_step(lambda: ApplicationStep(f"{self.str('.')}.{utils.show_args(show_args_as)}"))
        tr.trace_step(lambda: MotivationStep(f"def. of {self.show_top()}{comment}"))

        actual_args_count = len(tuple(new_args))
        if self.required_args_count != actual_args_count:
            raise TypeError(f"{self.func!r} argument mismatch: {self.required_args_count} required, "
                            f"but {actual_args_count} given")
        tr.inc_depth()
        # TODO: full laziness; but this approach does not work.
        # from FuPy.laziness import Lazy, evaluate
        # if (Lazy.full_regime and
        #         (isinstance(arg, Lazy) for arg in new_args) and
        #         self.show_top() != 'λ' and
        #         self is not evaluate
        #     ):
        #     print("PROPAGATING LAZINESS")
        #     result = Lazy(la(': self.func(*(evaluate(arg) for arg in args), **kwargs)'),
        #                   name=f"(λ: {self.name}{utils.show_args(new_args)})")
        # else:
        result = self.func(*new_args, **kwargs)
        # print(f"  result: {result}")
        # print(f"call exit: {self.str('^')}{new_args!r} ~> {result!r}")
        tr.dec_depth()
        tr.trace_step(lambda: ResultStep(f"{utils.show_value(result)}"))
        return result

    def __matmul__[Z](self, g: Callable[[Z], A]) -> "Func[Z, B]":
        """Return self o g.

        If g is not an instance of Func, then it is wrapped as Func.
        The typing is difficulty to express:
        * if g expects no or more than one argument,
          then the composition has a single tuple argument.
        """
        if not isinstance(g, abc.Callable):
            return NotImplemented
        g = func(g)
        op = " ⚬ " if self.required_args_count == 1 else "* ⚬ "
        name = f"{self.str('@')}{op}{g.str('@')}"
        # return Func(lambda z: self(g(z)),
        #             name=f"{self.str('@')}{op}{g.str('@')}", top='@')
        # print(f"constructing {name}")
        tr.trace_step(lambda: DefinitionStep(f"{name}"))
        return Func(lambda z: self(g(z)), name, top='@')
        # return la('z: self(g(z))').rename(name, top='@')

    def __rmatmul__[C](self, g: Callable[..., C]) -> "Func[A, C]":
        """Return g o self.
        """
        if not isinstance(g, abc.Callable):
            return NotImplemented
        return func(g) @ self

    def __and__[C](self, g: Callable[[A], C]) -> "Func[A, Both[B, C]]":
        """Return self split g.
        """
        if not isinstance(g, abc.Callable):
            return NotImplemented
        g = func(g)
        name = f"{self.str('&')} △ {g.str('&')}"
        # print(f"constructing {name}")
        tr.trace_step(lambda: DefinitionStep(f"{name}"))
        return Func(lambda a: (self(a), g(a)), name=name, top='&')

    def __rand__[C](self, g: Callable[[A], C]) -> "Func[A, Both[C, B]]":
        """Return g split self.
        """
        if not isinstance(g, abc.Callable):
            return NotImplemented
        return func(g) & self

    def __or__[Z](self, g: Callable[[Z], B]) -> "Func[Either[A, Z], B]":
        """Return self case g.
        """
        if not isinstance(g, abc.Callable):
            return NotImplemented
        g = func(g)
        name = f"{self.str('|')} ▽ {g.str('|')}"
        tr.trace_step(lambda: DefinitionStep(f"{name}"))

        @func(name=name, top="|")
        def case_(x: Either[A, Z]) -> B:
            match x:
                case Left(value=a):
                    return self(a)
                case Right(value=z):
                    return g(z)
                case _:
                    raise TypeError(f"type of argument {x!r} of {name} is neither Left nor Right")

        return case_

    def __ror__[Z](self, g: Callable[[Z], B]) -> "Func[Either[Z, A], B]":
        """Return g case self.
        """
        if not isinstance(g, abc.Callable):
            return NotImplemented
        return func(g) | self

    def __mul__[C, D](self, g: Callable[[C], D]) -> "Func[Both[A, C], Both[B, D]]":
        """Return self x g.
        """
        if not isinstance(g, abc.Callable):
            return NotImplemented
        g = func(g)
        name = f"{self.str('*')} ⨯ {g.str('*')}"
        tr.trace_step(lambda: DefinitionStep(f"{name}"))
        return Func(lambda a, c: (self(a), g(c)),  # alternative: self @ first & g @ second
                    name=name, top='*')

    def __rmul__[C, D](self, g: Callable[[C], D]) -> "Func[Both[C, A], Both[D, B]]":
        """Return g x self.
        """
        if not isinstance(g, abc.Callable):
            return NotImplemented
        return func(g) * self

    def __add__[C, D](self, g: Callable[[C], D]) -> "Func[Either[A, C], Either[B, D]]":
        """Return self + g.
        """
        if not isinstance(g, abc.Callable):
            return NotImplemented
        g = func(g)
        name = f"{self.str('+')} + {g.str('+')}"
        tr.trace_step(lambda: DefinitionStep(f"{name}"))
        return (left @ self | right @ g).rename(name, top='+')

    def __radd__[C, D](self, g: Callable[[C], D]) -> "Func[Either[C, A], Either[D, B]]":
        """Return g + self.
        """
        if not isinstance(g, abc.Callable):
            return NotImplemented
        return func(g) + self

    def __pow__(self: "Func[A, A]", n: Any) -> "Func[A, A]":
        """Repeated composition.
        A.k.a. as function exponentiation.
        This is fold-right over nat.

        Assumptions: A == B and n >= 0.
        """
        if not isinstance(n, int):
            return NotImplemented
        if n == 0:
            return id_
        elif n == 1:  # optimization
            return self
        else:
            return (self @ self ** (n - 1)).rename(
                f"{self.str('^')}^{n}", top='^')
            # N.B. f ** -1 does not terminate
            # We can make f ** -1 = fix(f)
            # return (lazy(self ** _)(n - 1) @ self).rename(f"{self}^{n}")  # fold-left over nat
            # TODO: which is better:  self @ self ** (n - 1)  or  self ** (n - 1) @ self


def func(obj: Optional[Callable] = None, **kwargs) -> Callable:
    """Decorate obj by wrapping it in Func.

    When obj is None, it returns a wrapping function.
    Avoids double wrapping.
    When f is a class, it wraps obj.__init__ (though such functions cannot be used with `|`).
    """
    @wraps(func)
    def func_decorator(obj: Callable) -> Callable:
        if inspect.isclass(obj):
            if isinstance(obj.__init__, Func):  # don't decorate again
                return obj
            obj.__init__ = Func(obj.__init__, **kwargs)
            return obj
        else:  # a regular function
            if isinstance(obj, Func):  # don't decorate again
                return obj
            return Func(obj, **kwargs)

    if obj is None:
        return func_decorator
    else:
        return func_decorator(obj)


def la(la_expr: str) -> Func[Any, Any]:
    """Define a lambda abstraction with zero or more variables.
    Returns a curried or uncurried function.

    Argument :code:`la_expr` must have the shape:
        :code:`variables: expr`
    where variables are comma separated: variable, ..., variable,
    where each variable can be
    * empty (no name/tuple)
    * a single name
    * a tuple of zero or more names

    Empty or an empty tuple results in a constant function with unit as argument.
    A tuple of 2 or more names results in an uncurried function.
    Multiple variables result in a curried function.

    :code:`la('a, (b, c), , d: (a, b, c, d, e, f)')` where :code:`e == 42` locally and :code:`f` is global,
    results (roughly) in:
    .. code-block:: python

        Func(lambda a:
             Func(lambda b, c:  # this is an uncurried function
                  Func(lambda:  # this is a constant function
                       Func(lambda d: (a, b, c, d, e),
                            name=...),
                       name=...),
                  name=...),
             name=...)

    Recursive approach, with auto capturing of locals.
    """
    # TODO: investigate performance loss, due to parsing and eval
    # from pprint import pprint
    # pprint(f"la_expr: {la_expr}")
    try:
        parameters, body = la_expr.split(':', 1)
    except ValueError:
        raise SyntaxError(f"la({la_expr!r}) has no `:`")
    parameters, body = parameters.strip(), body.strip()
    # find first parameter (could be more robust?)
    if parameters.startswith('('):  # tuple of parameters
        try:
            parameter, rest = parameters.lstrip('(').split(')', 1)  # rest is empty if ')' not present
        except ValueError:
            raise SyntaxError(f"la({la_expr!r}) has `(` without `)`")
        rest = rest.split(',', 1)[1:]
    else:  # single parameter
        parameter, *rest = parameters.split(',', 1)
    # N.B. parameter can be empty
    # len(rest) is 1 or 0, depending on whether there was a comma or not

    parent_frame = inspect.currentframe().f_back
    parent_globals = parent_frame.f_globals
    parent_locals = parent_frame.f_locals
    # pprint(f"parent_locals: {parent_locals}")
    try:
        lambda_body = eval(f"lambda: {body}")
    except SyntaxError as excinfo:
        raise SyntaxError(f"la({la_expr!r}) body `{body}`: {excinfo}")
    # pprint(f"names: {lambda_body.__code__.co_names}")
    if parent_locals is parent_globals:
        custom_locals = {}
    else:
        custom_locals = {key: parent_locals[key]
                         for key in lambda_body.__code__.co_names
                         if key in parent_locals}
    # pprint(f"custom_locals: {custom_locals}")
    bindings = '\n'.join(utils.indent_lines(f"{var} = {utils.show_value(value)}", '  ')
                         for var, value in custom_locals.items())
    # pprint(bindings)
    where_clause = f" where {{\n{bindings}\n}}" if bindings else ''
    closure = ','.join(f" {var}={var}"
                       for var in custom_locals)
    # pprint(closure)
    new_body = f"la('{rest[-1].strip()}: {body}')" if rest else body  # TODO: what if body contains quotes?
    la_expr_new = f"lambda{' ' if parameter else ''}{parameter}{',' if closure and parameter else ''}{closure}: {new_body}"
    # pprint(f"la_expr_new: {la_expr_new}")
    name=f'''(λ {parameters}: `{body}`){where_clause}'''
    tr.trace_step(lambda: DefinitionStep(f"{name}"))
    try:
        new_func = eval(la_expr_new, parent_globals, custom_locals)
    except SyntaxError as excinfo:
        raise SyntaxError(f"la({la_expr!r}) has bad parameter `{parameter}`: {excinfo}")
    return Func(new_func, name=name)


@func(name="⊥", r=1)
def undefined[A](a: A = unit) -> Empty:
    """Abort evaluation.
    """
    raise ValueError(f"undefined({'' if a is unit else repr(a)})")


@func
def eq[A](a: A, b: A) -> bool:
    """Uncurried equality test.
    """
    return a == b


@func(name="id")
def id_[A](a: A) -> A:
    """Polymorphic identity function.
    """
    return a


@func(name="(°)")
def const[A, B](b: B) -> Func[A, B]:
    """Construct the constant function always returning b.
    """
    return Func(lambda a: b, name=f"{b.str('^') if isinstance(b, Func) else b}°", top='^')


@func(name="↪︎")
def left[A, B](a: A) -> Either[A, B]:
    """Inject left into sum type.
    """
    return Left(a)


@func(name="↩︎")
def right[A, B](b: B) -> Either[A, B]:
    """Inject right into sum type.
    """
    return Right(b)


@func(name="(?)")
def guard[A](p: Callable[[A], bool]) -> Callable[[A], Either[A, A]]:
    """For predicate p, construct function p? in (A -> bool) -> A -> Either[A, A].
    """
    @func(name=f"{p.str('^')}?", top='^')
    def aux(a: A) -> Either[A, A]:
        """p?(a)"""
        if p(a):
            return Left(a)
        else:
            return Right(a)

    return aux


@func(name="≪")
def first[A, B](t: Both[A, B]) -> A:
    """Project left out of product type.
    """
    return t[0]


@func(name="≫")
def second[A, B](t: Both[A, B]) -> B:
    """Project right out of product type.
    """
    return t[1]


def _parenth(a: Any) -> str:
    """Parenthesize a if needed.
    """
    if isinstance(a, Func):
        return a.str('^')
    else:
        return a


@dataclass
class OperatorSection:
    """Support for operator sectioning.
    OperatorSection() is used as dummy argument to implicitly create lambda expressions.
    It must not implement __call__, because otherwise an OperatorSection object will not work
    with Func function combinators as expected.
    """
    name: Final[str] = ''

    @override
    def __repr__(self) -> str:
        """Prints nothing, which is needed when both operands are omitted.
        """
        return f"OperatorSection(name={self.name!r})"

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other):
        name = f"(={other})"
        tr.trace_step(lambda: DefinitionStep(f"{name}"))
        return Func(lambda x: x == other, name=name)

    def __ne__(self, other):
        name = f"(≠{other})"
        tr.trace_step(lambda: DefinitionStep(f"{name}"))
        return Func(lambda x: x != other, name=name)

    def __ge__(self, other):
        name = f"(≥{other})"
        tr.trace_step(lambda: DefinitionStep(f"{name}"))
        return Func(lambda x: x >= other, name=name)

    def __gt__(self, other):
        name = f"(>{other})"
        tr.trace_step(lambda: DefinitionStep(f"{name}"))
        return Func(lambda x: x > other, name=name)

    def __le__(self, other):
        name = f"(≤{other})"
        tr.trace_step(lambda: DefinitionStep(f"{name}"))
        return Func(lambda x: x <= other, name=name)

    def __lt__(self, other):
        name = f"(<{other})"
        tr.trace_step(lambda: DefinitionStep(f"{name}"))
        return Func(lambda x: x < other, name=name)

    def __add__(self, other):
        name = f"(+{' ' if callable(other) else ''}{_parenth(other)})"
        tr.trace_step(lambda: DefinitionStep(f"{name}"))
        return Func(lambda x: x + other, name=name)
        # return la('x: x + other').rename(name)  # TODO: consider

    def __radd__(self, other):
        name = f"({_parenth(other)}{' ' if callable(other) else ''}+)"
        tr.trace_step(lambda: DefinitionStep(f"{name}"))
        return Func(lambda x: other + x, name=name)

    def __sub__(self, other):
        name = f"(-{other})"
        tr.trace_step(lambda: DefinitionStep(f"{name}"))
        return Func(lambda x: x - other, name=name)

    def __rsub__(self, other):
        name = f"({other}-)"
        tr.trace_step(lambda: DefinitionStep(f"{name}"))
        return Func(lambda x: other - x, name=name)

    def __mul__(self, other):
        name = f"(*{' ' if callable(other) else ''}{_parenth(other)})"
        tr.trace_step(lambda: DefinitionStep(f"{name}"))
        return Func(lambda x: x * other, name=name)

    def __rmul__(self, other):
        name = f"({_parenth(other)}{' ' if callable(other) else ''}*)"
        tr.trace_step(lambda: DefinitionStep(f"{name}"))
        return Func(lambda x: other * x, name=name)

    def __matmul__(self, other):
        name = f"(⚬{' ' if callable(other) else ''}{_parenth(other)})"
        tr.trace_step(lambda: DefinitionStep(f"{name}"))
        return Func(lambda x: x @ other, name=name)

    def __rmatmul__(self, other):
        name = f"({_parenth(other)}{' ' if callable(other) else ''}⚬)"
        tr.trace_step(lambda: DefinitionStep(f"{name}"))
        return Func(lambda x: other @ x, name=name)

    def __truediv__(self, other):
        name = f"(/{other})"
        tr.trace_step(lambda: DefinitionStep(f"{name}"))
        return Func(lambda x: x / other, name=name)

    def __rtruediv__(self, other):
        name = f"({other}/)"
        tr.trace_step(lambda: DefinitionStep(f"{name}"))
        return Func(lambda x: other / x, name=name)

    def __floordiv__(self, other):
        name = f"(div {other})"
        tr.trace_step(lambda: DefinitionStep(f"{name}"))
        return Func(lambda x: x // other, name=name)

    def __rfloordiv__(self, other):
        name = f"({other} div)"
        tr.trace_step(lambda: DefinitionStep(f"{name}"))
        return Func(lambda x: other // x, name=name)

    def __mod__(self, other):
        name = f"(mod {other})"
        tr.trace_step(lambda: DefinitionStep(f"{name}"))
        return Func(lambda x: x % other, name=name)

    def __rmod__(self, other):
        name = f"({other} mod)"
        tr.trace_step(lambda: DefinitionStep(f"{name}"))
        return Func(lambda x: other % x, name=name)

    def __pow__(self, other):
        name = f"(**{other})"
        tr.trace_step(lambda: DefinitionStep(f"{name}"))
        return Func(lambda x: x ** other, name=name)

    def __rpow__(self, other):
        name = f"({other}**)"
        tr.trace_step(lambda: DefinitionStep(f"{name}"))
        return Func(lambda x: other ** x, name=name)

    def __and__(self, other):
        name = f"({'△ ' if callable(other) else '&'}{_parenth(other)}"
        tr.trace_step(lambda: DefinitionStep(f"{name}"))
        return Func(lambda x: x & other, name=name)

    def __rand__(self, other):
        name = f"({_parenth(other)}{' △' if callable(other) else '&'})"
        tr.trace_step(lambda: DefinitionStep(f"{name}"))
        return Func(lambda x: other & x, name=name)

    def __or__(self, other):
        name = f"({'▽ ' if callable(other) else '&'}{_parenth(other)})"
        tr.trace_step(lambda: DefinitionStep(f"{name}"))
        return Func(lambda x: x | other, name=name)

    def __ror__(self, other):
        name = f"({_parenth(other)}{' ▽' if callable(other) else '&'})"
        tr.trace_step(lambda: DefinitionStep(f"{name}"))
        return Func(lambda x: other | x, name=name)

    def __divmod__(self, other):
        name = f"divmod( , {other})"
        tr.trace_step(lambda: DefinitionStep(f"{name}"))
        return Func(lambda x: divmod(x, other), name=name)

    def __rdivmod__(self, other):
        name = f"divmod({other}, )"
        tr.trace_step(lambda: DefinitionStep(f"{name}"))
        return Func(lambda x: divmod(other, x), name=name)


# object.__divmod__(self, other)
# object.__lshift__(self, other)
# object.__rshift__(self, other)
# object.__xor__(self, other)
#
# object.__rdivmod__(self, other)
# object.__rlshift__(self, other)
# object.__rrshift__(self, other)
# object.__rxor__(self, other)


# Client code may want to define `_ = x_` to simplify operator section notation.
# This is not done here, because `_` has a special meaning in some REPLs.
x_ = OperatorSection()


@func
def curry[A, B, C](f: "Callable[[Both[A, B]], C]") -> "Func[A, Func[B, C]]":
    """Curry f.
    """
    return Func(lambda a: Func(lambda b: f((a, b)),
                               name=f"curry({f})({a})"),
                name=f"curry({f})")


@func
def uncurry[A, B, C](f: Callable[[A], Callable[[B], C]]) -> Func[Both[A, B], C]:
    """Uncurry f.
    """
    return Func(lambda t: f(first(t))(second(t)),
                name=f"uncurry({f})")


@func
def flip[A, B, C](f: Callable[[A], Callable[[B], C]]) -> Func[B, Func[A, C]]:
    """Flip f.  Swaps arguments on curried functions.
    """
    return Func(lambda b: Func(lambda a: f(a)(b), name=f"flip({f})({b})"), name=f"flip({f})")


# function operators as uncurried functions
ap = Func(lambda f, x: f(x), name="ap")

compose = Func(lambda f, g: f @ g, name="compose")  # composition
split = Func(lambda f, g: f & g, name="split")
# split = la('(f, g): f & g').rename("split")
case_ = Func(lambda f, g: f | g, name="case")
ftimes = Func(lambda f, g: f * g, name="ftimes")
fplus = Func(lambda f, g: f + g, name="fplus")
fpower = Func(lambda f, n: f ** n, name="fpower")


@func
def fpower_left[A](f: Func[A, A], n: int) -> Func[int, A]:
    """Repeated composition.
    This is fold-left over nat.
    It is tail recursive.
    See FuPy.laziness.fpower_lazy for a version that does not use the stack.

    Assumption: n >= 0
    """
    return id_ if n == 0 else fpower_left(f, n - 1) @ f
