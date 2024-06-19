import types
import typing
from concurrent import futures
from multiprocessing.context import BaseContext
from multiprocessing.pool import AsyncResult as AsyncResult

import typing_extensions
from joblib._multiprocessing_helpers import mp as mp
from joblib._parallel_backends import AutoBatchingMixin as AutoBatchingMixin
from joblib._parallel_backends import FallbackToBackend as FallbackToBackend
from joblib._parallel_backends import LokyBackend as LokyBackend
from joblib._parallel_backends import MultiprocessingBackend as MultiprocessingBackend
from joblib._parallel_backends import ParallelBackendBase as ParallelBackendBase
from joblib._parallel_backends import SequentialBackend as SequentialBackend
from joblib._parallel_backends import ThreadingBackend as ThreadingBackend
from joblib._typeshed import (
    BatchedCall,
    MmapMode,
    Prefer,
    Require,
    ReturnAs,
    ReturnGererator,
    ReturnGereratorUnordered,
    ReturnList,
    ReturnUnknown,
)
from joblib._utils import _Sentinel
from joblib._utils import eval_expr as eval_expr
from joblib.disk import memstr_to_bytes as memstr_to_bytes
from joblib.externals import loky as loky
from joblib.logger import Logger as Logger
from joblib.logger import short_format_time as short_format_time

_T = typing_extensions.TypeVar("_T")
_P = typing_extensions.ParamSpec("_P")
_R = typing_extensions.TypeVar("_R", default=typing.Literal["list"], bound=ReturnAs)

IS_PYPY: bool
BACKENDS: dict[str, type[ParallelBackendBase[typing.Any]]]
DEFAULT_BACKEND: str
MAYBE_AVAILABLE_BACKENDS: set[str]
DEFAULT_THREAD_BACKEND: str
EXTERNAL_BACKENDS: dict[str, typing.Callable[[], typing.Any]]
default_parallel_config: dict[str, _Sentinel[typing.Any]]
VALID_BACKEND_HINTS: tuple[str | None, ...]
VALID_BACKEND_CONSTRAINTS: tuple[str | None, ...]

def get_active_backend(
    prefer: Prefer | None = ..., require: Require | None = ..., verbose: int = ...
) -> tuple[ParallelBackendBase[typing.Any], int]: ...

class parallel_config:  # noqa: N801
    old_parallel_config: dict[str, typing.Any]
    parallel_config: dict[str, typing.Any]
    def __init__(
        self,
        backend: str | ParallelBackendBase[typing.Any] | None = ...,
        *,
        n_jobs: int | None = ...,
        verbose: int | None = ...,
        temp_folder: str | None = ...,
        max_nbytes: int | str | None = ...,
        mmap_mode: MmapMode | None = ...,
        prefer: Prefer | None = ...,
        require: Require | None = ...,
        inner_max_num_threads: int | None = ...,
        **backend_params: typing.Any,
    ) -> None: ...
    def __enter__(self) -> dict[str, typing.Any]: ...
    def __exit__(
        self,
        type: type[BaseException] | None,  # noqa: A002
        value: BaseException | None,
        traceback: types.TracebackType | None,
    ) -> None: ...
    def unregister(self) -> None: ...

class parallel_backend(parallel_config, typing.Generic[_R]):  # noqa: N801
    old_backend_and_jobs: tuple[ParallelBackendBase[typing.Any], int] | None
    new_backend_and_jobs: tuple[ParallelBackendBase[_R], int]
    def __init__(
        self,
        backend: ParallelBackendBase[_R],
        n_jobs: int = ...,
        inner_max_num_threads: int | None = ...,
        **backend_params: typing.Any,
    ) -> None: ...
    def __enter__(self) -> tuple[ParallelBackendBase[_R], int]: ...  # type: ignore[override]

DEFAULT_MP_CONTEXT: BaseContext | None
method: str | None

class BatchedCalls:
    items: list[BatchedCall[..., typing.Any]]
    def __init__(
        self,
        iterator_slice: typing.Iterable[BatchedCall[..., typing.Any]],
        backend_and_jobs: ParallelBackendBase[typing.Any]
        | tuple[ParallelBackendBase[typing.Any], int],
        reducer_callback: typing.Callable[[], typing.Any] | None = ...,
        pickle_cache: dict[typing.Any, typing.Any] | None = ...,
    ) -> None: ...
    def __call__(self) -> list[typing.Any]: ...
    def __reduce__(
        self,
    ) -> tuple[
        type[BatchedCalls],
        tuple[
            list[BatchedCall[..., typing.Any]],
            tuple[ParallelBackendBase[typing.Any], int | None],
            None,
            dict[typing.Any, typing.Any],
        ],
    ]: ...
    def __len__(self) -> int: ...

TASK_DONE: typing.Literal["Done"]
TASK_ERROR: typing.Literal["Error"]
TASK_PENDING: typing.Literal["Pending"]

def cpu_count(only_physical_cores: bool = ...) -> int: ...
def delayed(
    function: typing.Callable[_P, _T],
) -> typing.Callable[_P, BatchedCall[_P, _T]]: ...

class BatchCompletionCallBack(typing.Generic[_T]):
    dispatch_timestamp: float
    batch_size: int
    parallel: Parallel
    parallel_call_id: tuple[str, ...]
    job: futures.Future[_T] | AsyncResult[_T] | None
    status: str
    def __init__(
        self, dispatch_timestamp: float, batch_size: int, parallel: Parallel
    ) -> None: ...
    def register_job(self, job: futures.Future[_T] | AsyncResult[_T]) -> None: ...
    def get_result(self, timeout: float) -> typing.Any: ...
    def get_status(self, timeout: float) -> str: ...
    def __call__(self, out: futures.Future[_T] | AsyncResult[_T]) -> None: ...

def register_parallel_backend(
    name: str, factory: type[ParallelBackendBase[typing.Any]], make_default: bool = ...
) -> None: ...
def effective_n_jobs(n_jobs: int = ...) -> int: ...

class Parallel(Logger, typing.Generic[_R]):
    _backend: ParallelBackendBase[_R]
    _backend_args: dict[str, typing.Any]
    verbose: int
    timeout: float | None
    pre_dispatch: int | str
    return_as: _R
    return_generator: bool
    return_ordered: bool
    n_jobs: int
    batch_size: int | typing.Literal["auto"]
    def __init__(
        self,
        n_jobs: int | None = ...,
        backend: str | ParallelBackendBase[_R] | None = ...,
        return_as: ReturnAs = ...,
        verbose: int | None = ...,
        timeout: float | None = ...,
        pre_dispatch: int | str = ...,
        batch_size: int | typing.Literal["auto"] = ...,
        temp_folder: str | None = ...,
        max_nbytes: int | str | None = ...,
        mmap_mode: MmapMode | None = ...,
        prefer: Prefer | None = ...,
        require: Require | None = ...,
    ) -> None: ...
    #
    @typing.overload
    def __new__(
        cls,
        n_jobs: int | None = ...,
        backend: str | ParallelBackendBase[ReturnList] | None = ...,
        verbose: int | None = ...,
        timeout: float | None = ...,
        pre_dispatch: int | str = ...,
        batch_size: int | typing.Literal["auto"] = ...,
        temp_folder: str | None = ...,
        max_nbytes: int | str | None = ...,
        mmap_mode: MmapMode | None = ...,
        prefer: Prefer | None = ...,
        require: Require | None = ...,
    ) -> Parallel[ReturnList]: ...
    @typing.overload
    def __new__(
        cls,
        n_jobs: int | None = ...,
        backend: str | ParallelBackendBase[ReturnList] | None = ...,
        return_as: ReturnList = ...,
        verbose: int | None = ...,
        timeout: float | None = ...,
        pre_dispatch: int | str = ...,
        batch_size: int | typing.Literal["auto"] = ...,
        temp_folder: str | None = ...,
        max_nbytes: int | str | None = ...,
        mmap_mode: MmapMode | None = ...,
        prefer: Prefer | None = ...,
        require: Require | None = ...,
    ) -> Parallel[ReturnList]: ...
    @typing.overload
    def __new__(
        cls,
        n_jobs: int | None = ...,
        backend: str | ParallelBackendBase[ReturnGererator] | None = ...,
        return_as: ReturnGererator = ...,
        verbose: int | None = ...,
        timeout: float | None = ...,
        pre_dispatch: int | str = ...,
        batch_size: int | typing.Literal["auto"] = ...,
        temp_folder: str | None = ...,
        max_nbytes: int | str | None = ...,
        mmap_mode: MmapMode | None = ...,
        prefer: Prefer | None = ...,
        require: Require | None = ...,
    ) -> Parallel[ReturnGererator]: ...
    @typing.overload
    def __new__(
        cls,
        n_jobs: int | None = ...,
        backend: str | ParallelBackendBase[ReturnGereratorUnordered] | None = ...,
        return_as: ReturnGereratorUnordered = ...,
        verbose: int | None = ...,
        timeout: float | None = ...,
        pre_dispatch: int | str = ...,
        batch_size: int | typing.Literal["auto"] = ...,
        temp_folder: str | None = ...,
        max_nbytes: int | str | None = ...,
        mmap_mode: MmapMode | None = ...,
        prefer: Prefer | None = ...,
        require: Require | None = ...,
    ) -> Parallel[ReturnGereratorUnordered]: ...
    @typing.overload
    def __new__(
        cls,
        n_jobs: int | None = ...,
        backend: str | ParallelBackendBase[ReturnUnknown] | None = ...,
        return_as: ReturnUnknown = ...,
        verbose: int | None = ...,
        timeout: float | None = ...,
        pre_dispatch: int | str = ...,
        batch_size: int | typing.Literal["auto"] = ...,
        temp_folder: str | None = ...,
        max_nbytes: int | str | None = ...,
        mmap_mode: MmapMode | None = ...,
        prefer: Prefer | None = ...,
        require: Require | None = ...,
    ) -> Parallel[ReturnUnknown]: ...
    @typing.overload
    def __new__(
        cls,
        n_jobs: int | None = ...,
        backend: str | ParallelBackendBase[typing.Any] | None = ...,
        return_as: ReturnAs = ...,
        verbose: int | None = ...,
        timeout: float | None = ...,
        pre_dispatch: int | str = ...,
        batch_size: int | typing.Literal["auto"] = ...,
        temp_folder: str | None = ...,
        max_nbytes: int | str | None = ...,
        mmap_mode: MmapMode | None = ...,
        prefer: Prefer | None = ...,
        require: Require | None = ...,
    ) -> Parallel[typing.Any]: ...
    #
    def __enter__(self) -> typing_extensions.Self: ...
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: types.TracebackType | None,
    ) -> None: ...
    def dispatch_next(self) -> None: ...
    def dispatch_one_batch(
        self, iterator: typing.Iterable[BatchedCall[..., typing.Any]]
    ) -> bool: ...
    def print_progress(self) -> None: ...
    @typing.overload
    def __call__(
        self: Parallel[ReturnList], iterable: typing.Iterable[BatchedCall[..., _T]]
    ) -> list[_T]: ...
    @typing.overload
    def __call__(
        self: Parallel[ReturnGererator], iterable: typing.Iterable[BatchedCall[..., _T]]
    ) -> typing.Generator[_T, None, None]: ...
    @typing.overload
    def __call__(
        self: Parallel[ReturnGereratorUnordered],
        iterable: typing.Iterable[BatchedCall[..., _T]],
    ) -> typing.Generator[_T, None, None]: ...
    @typing.overload
    def __call__(
        self: Parallel[ReturnUnknown], iterable: typing.Iterable[BatchedCall[..., _T]]
    ) -> list[_T] | typing.Generator[_T, None, None]: ...
    @typing.overload
    def __call__(
        self: Parallel[typing.Any], iterable: typing.Iterable[BatchedCall[..., _T]]
    ) -> list[_T] | typing.Generator[_T, None, None]: ...
    @typing.overload
    def __call__(
        self, iterable: typing.Iterable[BatchedCall[..., _T]]
    ) -> list[_T] | typing.Generator[_T, None, None]: ...
