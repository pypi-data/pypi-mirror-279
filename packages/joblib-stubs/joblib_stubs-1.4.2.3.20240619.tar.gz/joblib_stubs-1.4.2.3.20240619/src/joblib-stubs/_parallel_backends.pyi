import typing
from abc import ABCMeta, abstractmethod
from collections.abc import Generator
from concurrent import futures
from multiprocessing.pool import AsyncResult as AsyncResult

import typing_extensions
from joblib._multiprocessing_helpers import mp as mp
from joblib._typeshed import AnyContainer, Prefer, Require, ReturnAs
from joblib.executor import get_memmapping_executor as get_memmapping_executor
from joblib.externals.loky import cpu_count as cpu_count
from joblib.externals.loky import process_executor as process_executor
from joblib.externals.loky.process_executor import (
    ShutdownExecutorError as ShutdownExecutorError,
)
from joblib.parallel import Parallel as Parallel
from joblib.pool import MemmappingPool as MemmappingPool

_T = typing_extensions.TypeVar("_T")
_R = typing_extensions.TypeVar("_R", default=typing.Literal["list"], bound=ReturnAs)

class ParallelBackendBase(typing.Generic[_R], metaclass=ABCMeta):
    supports_inner_max_num_threads: typing.ClassVar[bool]
    supports_retrieve_callback: typing.ClassVar[bool]
    default_n_jobs: typing.ClassVar[int]
    @property
    def supports_return_generator(self) -> bool: ...
    @property
    def supports_timeout(self) -> bool: ...
    nesting_level: int | None
    inner_max_num_threads: int
    def __init__(
        self,
        nesting_level: int | None = ...,
        inner_max_num_threads: int | None = ...,
        **kwargs: typing.Any,
    ) -> None: ...
    MAX_NUM_THREADS_VARS: typing.ClassVar[list[str]]
    TBB_ENABLE_IPC_VAR: typing.ClassVar[str]
    @abstractmethod
    def effective_n_jobs(self, n_jobs: int) -> int: ...
    @abstractmethod
    def apply_async(
        self,
        func: typing.Callable[[], _T],
        callback: typing.Callable[[AnyContainer[_T]], typing.Any]  # FIXME: mypy error
        | None = ...,
    ) -> AnyContainer[_T]: ...
    def retrieve_result_callback(
        self, out: futures.Future[_T] | AsyncResult[_T]
    ) -> _T: ...
    parallel: Parallel[_R]
    def configure(
        self,
        n_jobs: int = ...,
        parallel: Parallel[_R] | None = ...,
        prefer: Prefer | None = ...,
        require: Require | None = ...,
        **backend_args: typing.Any,
    ) -> int: ...
    def start_call(self) -> None: ...
    def stop_call(self) -> None: ...
    def terminate(self) -> None: ...
    def compute_batch_size(self) -> int: ...
    def batch_completed(self, batch_size: int, duration: float) -> None: ...
    def get_exceptions(self) -> list[BaseException]: ...
    def abort_everything(self, ensure_ready: bool = ...) -> None: ...
    def get_nested_backend(
        self,
    ) -> tuple[
        SequentialBackend[typing.Any] | ThreadingBackend[typing.Any], int | None
    ]: ...
    def retrieval_context(self) -> Generator[None, None, None]: ...
    @staticmethod
    def in_main_thread() -> bool: ...

class SequentialBackend(ParallelBackendBase[_R], typing.Generic[_R]):
    uses_threads: typing.ClassVar[bool]
    supports_timeout: typing.ClassVar[bool]
    supports_retrieve_callback: typing.ClassVar[bool]
    supports_sharedmem: typing.ClassVar[bool]
    def apply_async(
        self,
        func: typing.Callable[[], typing.Any],
        callback: typing.Callable[..., typing.Any] | None = ...,
    ) -> typing.NoReturn: ...
    # mypy
    def effective_n_jobs(self, n_jobs: int) -> int: ...

class PoolManagerMixin:
    def effective_n_jobs(self, n_jobs: int) -> int: ...
    def terminate(self) -> None: ...
    def apply_async(
        self,
        func: typing.Callable[[], _T],
        callback: typing.Callable[[AsyncResult[_T]], typing.Any] | None = ...,
    ) -> AsyncResult[_T]: ...
    def retrieve_result_callback(self, out: typing.Any) -> typing.Any: ...
    def abort_everything(self, ensure_ready: bool = ...) -> None: ...

class AutoBatchingMixin(typing.Generic[_R]):
    MIN_IDEAL_BATCH_DURATION: typing.ClassVar[float]
    MAX_IDEAL_BATCH_DURATION: typing.ClassVar[int]
    parallel: Parallel[_R]
    def __init__(self, **kwargs: typing.Any) -> None: ...
    def compute_batch_size(self) -> int: ...
    def batch_completed(self, batch_size: int, duration: float) -> None: ...
    def reset_batch_stats(self) -> None: ...

class ThreadingBackend(PoolManagerMixin, ParallelBackendBase[_R], typing.Generic[_R]):
    supports_retrieve_callback: typing.ClassVar[bool]
    uses_threads: typing.ClassVar[bool]
    supports_sharedmem: typing.ClassVar[bool]
    def configure(  # type: ignore[override]
        self,
        n_jobs: int = ...,
        parallel: Parallel[_R] | None = ...,
        **backend_args: typing.Any,
    ) -> int: ...

class MultiprocessingBackend(  # type: ignore[misc] # FIXME
    PoolManagerMixin, AutoBatchingMixin[_R], ParallelBackendBase[_R], typing.Generic[_R]
):
    supports_retrieve_callback: typing.ClassVar[bool]
    supports_return_generator: typing.ClassVar[bool]
    def configure(
        self,
        n_jobs: int = ...,
        parallel: Parallel[_R] | None = ...,
        prefer: Prefer | None = ...,
        require: Require | None = ...,
        **memmappingpool_args: typing.Any,
    ) -> int: ...

class LokyBackend(AutoBatchingMixin[_R], ParallelBackendBase[_R], typing.Generic[_R]):  # type: ignore[misc] # FIXME
    supports_retrieve_callback: typing.ClassVar[bool]
    supports_inner_max_num_threads: typing.ClassVar[bool]
    def configure(
        self,
        n_jobs: int = ...,
        parallel: Parallel[_R] | None = ...,
        prefer: Prefer | None = ...,
        require: Require | None = ...,
        idle_worker_timeout: float = ...,
        **memmappingexecutor_args: typing.Any,
    ) -> int: ...
    def terminate(self) -> None: ...
    def abort_everything(self, ensure_ready: bool = ...) -> None: ...
    def apply_async(
        self,
        func: typing.Callable[[], _T],
        callback: typing.Callable[[futures.Future[_T]], typing.Any] | None = ...,
    ) -> futures.Future[_T]: ...
    # mypy
    def effective_n_jobs(self, n_jobs: int) -> int: ...

class FallbackToBackend(Exception):  # noqa: N818
    backend: ParallelBackendBase[typing.Any]
    def __init__(self, backend: ParallelBackendBase[typing.Any]) -> None: ...

def inside_dask_worker() -> bool: ...
