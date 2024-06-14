import enum
from typing import Iterable, Iterator, List, overload


class ADFun:
    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, arg0: advec, arg1: advec, /) -> None: ...

    def Dependent(self, arg0: advec, arg1: advec, /) -> None: ...

    def to_graph(self, arg: cpp_graph, /) -> None: ...

    def Domain(self) -> int: ...

    def Range(self) -> int: ...

    def size_dyn_ind(self) -> int: ...

    def optimize(self, arg: str, /) -> None: ...

    def function_name_set(self, arg: str, /) -> None: ...

class FunctionIndex:
    def __init__(self, arg: int, /) -> None: ...

    @property
    def index(self) -> int: ...

class HessianSparsityType(enum.Enum):
    Full = 0

    Upper = 1

    Lower = 2

@overload
def Independent(x: advec) -> None: ...

@overload
def Independent(x: advec, dynamic: advec) -> None: ...

@overload
def Independent(x: advec, abort_op_index: int, record_compare: bool) -> None: ...

@overload
def Independent(x: advec, abort_op_index: int, record_compare: bool, dynamic: advec) -> None: ...

class JacobianHessianSparsityPattern:
    @property
    def jacobian(self) -> sparsity_pattern_t: ...

    @property
    def hessian(self) -> sparsity_pattern_t: ...

    @property
    def reduced_hessian(self) -> sparsity_pattern_t: ...

class NLConstraintIndex:
    @property
    def index(self) -> int: ...

    @property
    def dim(self) -> int: ...

class NonlinearFunction:
    def __init__(self, arg0: ADFun, arg1: str, /) -> None: ...

    @property
    def name(self) -> str: ...

    @property
    def nx(self) -> int: ...

    @property
    def np(self) -> int: ...

    @property
    def ny(self) -> int: ...

    @property
    def f_graph(self) -> cpp_graph: ...

    @property
    def jacobian_graph(self) -> cpp_graph: ...

    @property
    def hessian_graph(self) -> cpp_graph: ...

    @property
    def m_jacobian_nnz(self) -> int: ...

    @property
    def m_hessian_nnz(self) -> int: ...

    @property
    def m_jacobian_rows(self) -> List[int]: ...

    @property
    def m_jacobian_cols(self) -> List[int]: ...

    @property
    def m_hessian_rows(self) -> List[int]: ...

    @property
    def m_hessian_cols(self) -> List[int]: ...

    def assign_evaluators(self, arg0: int, arg1: int, arg2: int, arg3: int, /) -> None: ...

class NonlinearFunctionModel:
    def __init__(self) -> None: ...

    @property
    def nl_functions(self) -> nlfunctionvec: ...

class ParameterIndex:
    def __init__(self, arg: int, /) -> None: ...

    @property
    def index(self) -> int: ...

class a_double:
    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, arg: float, /) -> None: ...

    def __neg__(self) -> a_double: ...

    @overload
    def __add__(self, arg: a_double, /) -> a_double: ...

    @overload
    def __add__(self, arg: float, /) -> a_double: ...

    @overload
    def __sub__(self, arg: a_double, /) -> a_double: ...

    @overload
    def __sub__(self, arg: float, /) -> a_double: ...

    @overload
    def __mul__(self, arg: a_double, /) -> a_double: ...

    @overload
    def __mul__(self, arg: float, /) -> a_double: ...

    @overload
    def __truediv__(self, arg: a_double, /) -> a_double: ...

    @overload
    def __truediv__(self, arg: float, /) -> a_double: ...

    @overload
    def __iadd__(self, arg: a_double, /) -> a_double: ...

    @overload
    def __iadd__(self, arg: float, /) -> a_double: ...

    @overload
    def __isub__(self, arg: a_double, /) -> a_double: ...

    @overload
    def __isub__(self, arg: float, /) -> a_double: ...

    @overload
    def __imul__(self, arg: a_double, /) -> a_double: ...

    @overload
    def __imul__(self, arg: float, /) -> a_double: ...

    @overload
    def __itruediv__(self, arg: a_double, /) -> a_double: ...

    @overload
    def __itruediv__(self, arg: float, /) -> a_double: ...

    def __radd__(self, arg: float, /) -> a_double: ...

    def __rsub__(self, arg: float, /) -> a_double: ...

    def __rmul__(self, arg: float, /) -> a_double: ...

    def __rtruediv__(self, arg: float, /) -> a_double: ...

def abs(arg: a_double, /) -> a_double: ...

def acos(arg: a_double, /) -> a_double: ...

def acosh(arg: a_double, /) -> a_double: ...

class advec:
    @overload
    def __init__(self) -> None:
        """Default constructor"""

    @overload
    def __init__(self, arg: advec) -> None:
        """Copy constructor"""

    @overload
    def __init__(self, arg: Iterable[a_double], /) -> None:
        """Construct from an iterable object"""

    def __len__(self) -> int: ...

    def __bool__(self) -> bool:
        """Check whether the vector is nonempty"""

    def __repr__(self) -> str: ...

    def __iter__(self) -> Iterator[a_double]: ...

    @overload
    def __getitem__(self, arg: int, /) -> a_double: ...

    @overload
    def __getitem__(self, arg: slice, /) -> advec: ...

    def clear(self) -> None:
        """Remove all items from list."""

    def append(self, arg: a_double, /) -> None:
        """Append `arg` to the end of the list."""

    def insert(self, arg0: int, arg1: a_double, /) -> None:
        """Insert object `arg1` before index `arg0`."""

    def pop(self, index: int = -1) -> a_double:
        """Remove and return item at `index` (default last)."""

    def extend(self, arg: advec, /) -> None:
        """Extend `self` by appending elements from `arg`."""

    @overload
    def __setitem__(self, arg0: int, arg1: a_double, /) -> None: ...

    @overload
    def __setitem__(self, arg0: slice, arg1: advec, /) -> None: ...

    @overload
    def __delitem__(self, arg: int, /) -> None: ...

    @overload
    def __delitem__(self, arg: slice, /) -> None: ...

    def __eq__(self, arg: advec, /) -> bool: ...

    def __ne__(self, arg: advec, /) -> bool: ...

    @overload
    def __contains__(self, arg: a_double, /) -> bool: ...

    @overload
    def __contains__(self, arg: object, /) -> bool: ...

    def count(self, arg: a_double, /) -> int:
        """Return number of occurrences of `arg`."""

    def remove(self, arg: a_double, /) -> None:
        """Remove first occurrence of `arg`."""

def asin(arg: a_double, /) -> a_double: ...

def asinh(arg: a_double, /) -> a_double: ...

def atan(arg: a_double, /) -> a_double: ...

def atanh(arg: a_double, /) -> a_double: ...

def cos(arg: a_double, /) -> a_double: ...

def cosh(arg: a_double, /) -> a_double: ...

class cpp_graph:
    def __init__(self) -> None: ...

    def __iter__(self) -> Iterator[cpp_graph_iter]: ...

    @property
    def n_dynamic_ind(self) -> int: ...

    @property
    def n_variable_ind(self) -> int: ...

    @property
    def n_constant(self) -> int: ...

    @property
    def n_dependent(self) -> int: ...

    @property
    def n_operator(self) -> int: ...

    def constant_vec_get(self, arg: int, /) -> float: ...

    def dependent_vec_get(self, arg: int, /) -> int: ...

class cpp_graph_iter:
    @property
    def op_enum(self) -> graph_op: ...

    @property
    def n_result(self) -> int: ...

    @property
    def arg_node(self) -> list: ...

def erf(arg: a_double, /) -> a_double: ...

def erfc(arg: a_double, /) -> a_double: ...

def exp(arg: a_double, /) -> a_double: ...

def expm1(arg: a_double, /) -> a_double: ...

class graph_op(enum.Enum):
    abs = 0

    acos = 1

    acosh = 2

    add = 3

    asin = 4

    asinh = 5

    atan = 6

    atanh = 7

    atom4 = 8

    atom = 9

    azmul = 10

    cexp_eq = 11

    cexp_le = 12

    cexp_lt = 13

    comp_eq = 14

    comp_le = 15

    comp_lt = 16

    comp_ne = 17

    cos = 18

    cosh = 19

    discrete = 20

    div = 21

    erf = 22

    erfc = 23

    exp = 24

    expm1 = 25

    log1p = 26

    log = 27

    mul = 28

    neg = 29

    pow = 30

    print = 31

    sign = 32

    sin = 33

    sinh = 34

    sqrt = 35

    sub = 36

    sum = 37

    tan = 38

    tanh = 39

def jacobian_hessian_sparsity(arg0: ADFun, arg1: HessianSparsityType, /) -> JacobianHessianSparsityPattern: ...

def log(arg: a_double, /) -> a_double: ...

def log1p(arg: a_double, /) -> a_double: ...

class nlfunctionvec:
    @overload
    def __init__(self) -> None:
        """Default constructor"""

    @overload
    def __init__(self, arg: nlfunctionvec) -> None:
        """Copy constructor"""

    @overload
    def __init__(self, arg: Iterable[NonlinearFunction], /) -> None:
        """Construct from an iterable object"""

    def __len__(self) -> int: ...

    def __bool__(self) -> bool:
        """Check whether the vector is nonempty"""

    def __repr__(self) -> str: ...

    def __iter__(self) -> Iterator[NonlinearFunction]: ...

    @overload
    def __getitem__(self, arg: int, /) -> NonlinearFunction: ...

    @overload
    def __getitem__(self, arg: slice, /) -> nlfunctionvec: ...

    def clear(self) -> None:
        """Remove all items from list."""

    def append(self, arg: NonlinearFunction, /) -> None:
        """Append `arg` to the end of the list."""

    def insert(self, arg0: int, arg1: NonlinearFunction, /) -> None:
        """Insert object `arg1` before index `arg0`."""

    def pop(self, index: int = -1) -> NonlinearFunction:
        """Remove and return item at `index` (default last)."""

    def extend(self, arg: nlfunctionvec, /) -> None:
        """Extend `self` by appending elements from `arg`."""

    @overload
    def __setitem__(self, arg0: int, arg1: NonlinearFunction, /) -> None: ...

    @overload
    def __setitem__(self, arg0: slice, arg1: nlfunctionvec, /) -> None: ...

    @overload
    def __delitem__(self, arg: int, /) -> None: ...

    @overload
    def __delitem__(self, arg: slice, /) -> None: ...

@overload
def pow(arg0: a_double, arg1: int, /) -> a_double: ...

@overload
def pow(arg0: a_double, arg1: float, /) -> a_double: ...

@overload
def pow(arg0: float, arg1: a_double, /) -> a_double: ...

@overload
def pow(arg0: a_double, arg1: a_double, /) -> a_double: ...

def sin(arg: a_double, /) -> a_double: ...

def sinh(arg: a_double, /) -> a_double: ...

def sparse_hessian(arg0: ADFun, arg1: sparsity_pattern_t, arg2: sparsity_pattern_t, /) -> ADFun: ...

def sparse_jacobian(arg0: ADFun, arg1: sparsity_pattern_t, /) -> ADFun: ...

class sparsity_pattern_t:
    def nnz(self) -> int: ...

    def to_list(self) -> tuple: ...

def sqrt(arg: a_double, /) -> a_double: ...

def tan(arg: a_double, /) -> a_double: ...

def tanh(arg: a_double, /) -> a_double: ...
