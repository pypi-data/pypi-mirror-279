"""
Definitions of basic functions for natural numbers and (potentially infinite) lists.

Copyright (c) 2024 - Eindhoven University of Technology, The Netherlands

This software is made available under the terms of the MIT License.
"""
from typing import Any, Final, Callable
from FuPy.core import *

_ = x_  # even shorter name for the dummy argument


__all__ = [
    "not_", "and_", "or_",
    "swap", "coswap", "assoc_left", "assoc_right",
    "Maybe", "nothing", "just",
    "NatF", "natf", "Nat",
    "zero", "succ", "one",
    "NatF_Algebra", "NatF_CoAlgebra",
    "cataNat", "anaNat",
    "is_zero", "pred", "eqNat", "less",
    "intNat", "nat",
    "add", "mul", "sub", "div",
    "in_nat", "out_nat", "cata_nat", "ana_nat",
    "infinite",
    "ListF", "listf", "List_",
    "nil", "cons",
    "ListF_Alg", "ListF_CoAlg",
    "cataList", "anaList",
    "null", "head_tail", "head", "tail",
    "eqList",
    "strList", "listList", "list_",
    "length", "length_nat", "cat",
    "map_", "filter_",
    "concat",
    "take_drop", "take", "drop",
    "unzip", "zip", "zip_with",
    "from_",
    "null_", "cons_", "head_", "tail_", "cata_list", "ana_list",
]

# Functions on booleans

not_ = Func(lambda x: not x, name="¬")
and_ = Func(lambda x, y: x and y, name="∧")
or_ = Func(lambda x, y: x or y, name="∨")


# type: Func[Both[A, B], Both[B, A]]
swap = (second & first).rename("swap")

# type: Func[Either[A, B], Either[B, A]]
coswap = (right | left).rename("coswap")

# type: Func[Both[A, Both[B, C]], Both[Both[A, B], C]]
assoc_left = ((id_ * first) & second @ second).rename("assoc_left")  # (a, (b, c)) -> ((a, b), c)

# type: Func[Both[Both[A, B], C], Both[A, Both[B, C]]]
assoc_right = (first @ first & (second * id_)).rename("assoc_right")  # ((a, b), c) -> (a, (b, c))


type Maybe[X] = Either[Unit, X]  # 1 + X

nothing: Maybe[Any] = left(unit)  # inject left in Maybe[A]


@func
def just[A](a: A) -> Maybe[A]:
    """Inject right into Maybe[A]
    """
    return right(a)


@func
def maybef[X, Y](f: Callable[[X], Y]) -> Callable[[Maybe[X]], Maybe[Y]]:
    """Map f over a Maybe value.
    """
    return id_ + f


# (co)inductive type of natural numbers

type NatF[X] = Maybe[X]  # 1 + X


@func
def natf[X, Y](f: Callable[[X], Y]) -> Callable[[NatF[X]], NatF[Y]]:
    """Functor for type of natural numbers.
    """
    return id_ + f  # maybef(f)


# Alternative, defining NatF as instance of Functor
# @dataclass
# class NatF_[X](Functor[X]):
#     unNatF: Maybe[X]
#
#     @override
#     def __fmap__[Y](self, f: Callable[[X], Y]) -> "Functor[Y]":
#         return maybef(f)
#         return id_ + f  # natf(f), but the latter would add another indirection

# TODO: How to make a dataclass an instance of a protocol, afterwards?
# i.e., implement the required operations


# @func  # used in cataNat_
# def unNatF_[X](nfx: NatF_[X]) -> Maybe[X]:
#     return nfx.unNatF


type Nat = Fix[NatF]
# type Nat_ = Fix[NatF_]


zero: Final[Nat] = in_(left(unit))


@func(name="(+1)")
def succ(n: Nat) -> Nat:
    return in_(right(n))


one: Final[Nat] = succ(zero)


type NatF_Algebra[X] = F_Algebra[NatF, X]
type NatF_CoAlgebra[X] = F_CoAlgebra[NatF, X]


# TODO: Why not just define cataNat = cata(natf)?
@func(name=f"⦇ … ⦈_ℕ")
def cataNat[X](alg: NatF_Algebra[X]) -> Callable[[Nat], X]:
    """Catamorphism from NatF-algebra.
    """
    # return cata(natf)(alg)
    return cata(natf)(alg).rename(f"⦇ {alg} ⦈_ℕ")


# TODO: Why not just define cataNat_ = cata_ @ (_ @ unNatF_)?
# @func(name=f"⦇ … ⦈_ℕ_")
# def cataNat_[X](alg: F_Algebra[NatF_, X]) -> Callable[[Nat], X]:
#     """Catamorphism from NatF-algebra.
#     """
#     return cata_(alg @ unNatF_).rename(f"⦇ {alg} ⦈_ℕ_")


# TODO: Why not just define anaNat = ana(natf)?
@func(name=f"〖 … 〗_ℕ")
def anaNat[X](coalg: NatF_CoAlgebra[X]) -> Callable[[X], Nat]:
    """Anamorphism from NatF-coalgebra.
    """
    return ana(natf)(coalg).rename(f"〖 {coalg} 〗_ℕ")


# TODO: Why not just define anaNat_ = ana_ @ (NatF_ @ _)?
# @func(name=f"〖 … 〗_ℕ_")
# def anaNat_[X](coalg: F_CoAlgebra[X, NatF_]) -> Callable[[X], Nat]:
#     """Anamorphism from NatF-coalgebra.
#     """
#     return ana_(NatF_ @ coalg).rename(f"〖 {coalg} 〗_ℕ_")


# type: Callable[[Nat], bool]
# is_zero = (( const(True) | const(False) ) @ out).rename("is_zero")
is_zero = cataNat( const(True) | const(False) ).rename("is_zero")

# type: Callable[[Nat], Nat]  # partial function
pred = (( undefined | id_ ) @ out).rename("pred")
# tuple with identity
# pred = first @ cataNat( const(undefined, 0) | second & succ )

# type: Callable[[Nat], Callable[[Nat], bool]]
eqNat = cataNat( const(is_zero) | (lambda eq_n: (const(False) | eq_n @ pred) @ guard(is_zero)) ).rename("eqNat")
less = cataNat( const(not_ @ is_zero) | (lambda less_n: (const(False) | less_n @ pred) @ guard(is_zero)) ).rename("less")

# convert Nat to int

# type: Callable[[Nat], int]
intNat = cataNat( const(0) | (_ + 1) ).rename("intNat")

# convert int >= 0 to Nat
# type: Callable[[int], Nat]
nat = anaNat( (const(unit) + (_ - 1)) @ guard((_ == 0)) ).rename("nat")

#  various binary operators on Nat
# type: Callable[[Nat], Callable[[Nat], Nat]]
add = Func(lambda m: cataNat( const(m) | succ ), name="add")
mul = Func(lambda m: cataNat( const(zero) | add(m) ), name="mul")
sub = Func(lambda m: cataNat( const(m) | pred ), name="sub")
div = Func(lambda m: lambda n: anaNat( ( const(unit) + flip(sub)(n) ) @ guard(flip(less)(n)) )(m),
           name="div")

infinite: Final[Nat] = div(one)(zero)

# (co)inductive nat type based on native int

# TODO: use these in intNat and nat (?)
in_nat = (const(0) | (_ + 1)).rename("in_nat")
out_nat = ((const(unit) + (_ - 1)) @ guard((_ == 0))).rename("out_nat")


@func
def cata_nat[X](alg: Callable[[NatF[X]], X]) -> Func[int, X]:
    return fix(lambda rec: alg @ natf(rec) @ out_nat).rename(f"⦇ {alg} ⦈_nat")


@func
def ana_nat[X](coalg: Callable[[X], NatF[X]]) -> Func[X, int]:
    return fix(lambda rec: in_nat @ natf(rec) @ coalg).rename(f"〖 {coalg} 〗_nat")


# (co)inductive list type

type ListF[X] = Either[Unit, Both[Any, X]]  # 1 + A x X


@func
def listf[X, Y](f: Callable[[X], Y]) -> Callable[[ListF[X]], ListF[Y]]:
    """Functor for list type.
    """
    return id_ + id_ * f


type List_ = Fix[ListF]


nil: Final[List_] = in_(left(unit))


@func
def cons(x: Any, xs: List_) -> List_:
    """Uncurried operator to combine head and tail.
    """
    return in_(right((x, xs)))


type ListF_Alg[X] = F_Algebra[ListF, X]
type ListF_CoAlg[X] = F_CoAlgebra[ListF, X]


@func
def cataList[X](alg: ListF_Alg[X]) -> Callable[[List_], X]:
    """Catamorphism from ListF-algebra.
    """
    return cata(listf)(alg).rename(f"⦇ {alg} ⦈_𝕃")


@func
def anaList[X](coalg: ListF_CoAlg[X]) -> Callable[[X], List_]:
    """Anamorphism from ListF-algebra.
    """
    return ana(listf)(coalg).rename(f"〖 {coalg} 〗_𝕃")


# type: Callable[[List_], bool]
null = cataList( const(True) | const(False) ).rename("null")
# null = ( const(True) | const(False) ) @ out

# type: Callable[[List_], Any]
head_tail = (( undefined | id_ ) @ out).rename("head_tail")

# type: Callable[[List_], Any]
head = (first @ head_tail).rename("head")

# type: Callable[[List_], List_]
tail = (second @ head_tail).rename("tail")

# check whether two List_'s are equal (curried)
# type: Callable[[Nat], Callable[[Nat], bool]]
eqList = cataList( const(null)
                 | Func(lambda x, r:  # r = eqList(xs)
                              ( const(False)
                              | and_ @ (Func(lambda y: x == y) * r) @ head_tail
                              ) @ guard(null))
                 )

# represent a List_ as a string
# type: Callable[[List_], str]
strList = cataList(const("[]") | Func(lambda x, xs: f"{x} ⊢ {evaluate(xs)}"))

# convert a List_ to a regular Python list
# type: Callable[[List_], list]
listList = cataList(const([]) | Func(lambda x, xs: [x] + xs))

# convert regular Python list to a List_
# type: Callable[[list], List_]
list_ = anaList( (const(unit) + (Func(lambda xs: xs[0]) & (lambda xs: xs[1:]))) @ guard(not_) )

length = cataList(const(zero) | succ @ second).rename("length")
length_nat = cataList(const(0) | (1 + _) @ second).rename("length_nat")


@func
def cat(xs: List_, ys: List_) -> List_:
    """Uncurried catenation on List_.
    """
    return cataList( const(ys) | cons )(xs)


# map function over list
# type: Callable[[Callable[[X], Y]], Callable[[List_], List_]]
map_ = Func(lambda f: cataList( const(nil) | cons @ (f * id_) ).rename(f"map({f}"),
            name="map")

# filter list by predicate
# type: Callable[[Callable[[X], bool]], Callable[[List_], List_]]
filter_ = Func(lambda p: cataList(const(nil) | (cons | second) @ guard(p @ first)).rename(f"filter({p})"),
               name="filter")

concat = cataList( const(nil) | cat ).rename("concat")

take_drop = cata_nat( const(const(nil) & id_) |
                      Func(lambda tdn: (const(nil, nil) | (cons * id_) @ assoc_left @ (id_ * tdn) @ head_tail) @ guard(null))
                      ).rename("take_drop")
take = Func(lambda n: first @ take_drop(n)).rename("take")
drop = Func(lambda n: second @ take_drop(n)).rename("drop")
# drop = cata_nat( const(id_) | (lambda r: (const(nil) | r @ tail) @ guard(null))
#                  ).rename("drop")
# take = cata_nat( const(const(nil)) | (lambda r: (const(nil) | cons @ (id_ * r) @ head_tail) @ guard(null))
#                  ).rename(f"take")

unzip = cataList(const(nil, nil) | Func(lambda xy, ts: (cons(first(xy), first(ts)), cons(second(xy), second(ts))))).rename("unzip")
zip = anaList( (const(unit) + ((head * head) & (tail * tail))) @ guard(Func(lambda xs, ys: null(xs) or null(ys))) ).rename("zip")
zip_with = Func(lambda op: anaList( (const(unit) + (op @ (head * head) & (tail * tail))) @ guard(Func(lambda xs, ys: null(xs) or null(ys))) )
                ).rename("unzip_with")

from_ = anaList( right @ (id_ & (_ + 1)) ).rename("from")

# (co)inductive list_ type based on native list (as snoc lists)

null_ = la('xs: not xs').rename("null_")
cons_ = la('(x, xs): [x] + xs').rename("cons_")
head_ = la('xs: xs[0]').rename("head_")
tail_ = la('xs: xs[1:]').rename("tail_")
in_list = (const([]) | cons_).rename("in_list")
out_list = ((const(unit) + (head_ & tail_)) @ guard(null_)).rename("out_list")


@func
def cata_list[X](alg: Callable[[ListF[X]], X]) -> Func[list, X]:
    # return fix(lambda rec: alg @ listf(rec) @ out_list).rename(f"⦇ {alg} ⦈_list")
    return fix(la('rec: alg @ listf(rec) @ out_list')).rename(f"⦇ {alg} ⦈_list")
    # for infinite arguments, use lazy(rec)


@func
def ana_list[X](coalg: Callable[[X], ListF[X]]) -> Func[X, list]:
    return fix(lambda rec: in_list @ listf(rec) @ coalg).rename(f"〖 {coalg} 〗_list")
    # for infinite results, use lazy(rec)
