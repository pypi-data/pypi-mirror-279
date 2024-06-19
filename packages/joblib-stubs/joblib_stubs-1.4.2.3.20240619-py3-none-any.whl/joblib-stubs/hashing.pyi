import io
import pickle
import types
import typing

import typing_extensions
from joblib._typeshed import HashType

Pickler = pickle.Pickler

class _ConsistentSet:
    def __init__(self, set_sequence: typing.Iterable[typing.Hashable]) -> None: ...

class _MyHash:
    args: tuple[typing.Any]
    def __init__(self, *args: typing.Any) -> None: ...

class Hasher(Pickler):
    stream: io.BytesIO
    def __init__(self, hash_name: HashType = ...) -> None: ...
    def hash(self, obj: typing.Any, return_digest: bool = ...) -> str: ...
    def save(self, obj: typing.Any) -> None: ...
    def memoize(self, obj: typing.Any) -> None: ...
    def save_global(
        self,
        obj: typing.Any,
        name: str | None = ...,
        pack: typing.Callable[
            typing_extensions.Concatenate[str | bytes, ...], bytes
        ] = ...,
    ) -> None: ...
    # dispatch: dict[type[typing.Any], _Dispatch[typing.Any]]  # noqa: ERA001
    def save_set(self, set_items: typing.Iterable[typing.Hashable]) -> None: ...

class NumpyHasher(Hasher):
    coerce_mmap: bool
    np: types.ModuleType
    def __init__(self, hash_name: HashType = ..., coerce_mmap: bool = ...) -> None: ...
    def save(self, obj: typing.Any) -> None: ...

def hash(  # noqa: A001
    obj: typing.Any, hash_name: HashType = ..., coerce_mmap: bool = ...
) -> str: ...
