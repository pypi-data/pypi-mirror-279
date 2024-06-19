from __future__ import (
    annotations,
)

from . import (
    _utils,
)
from ._full_path import (
    FullPathModule,
)
from dataclasses import (
    dataclass,
)
import grimp
from grimp.application.ports.graph import (
    AbstractImportGraph,
)
from typing import (
    FrozenSet,
    NoReturn,
    Optional,
    Tuple,
    TypeVar,
    Union,
)

_T = TypeVar("_T")


def _assert_bool(raw: _T) -> Union[bool, Exception]:
    if isinstance(raw, bool):
        return raw
    return TypeError(
        f"Expected `bool` but got `{type(raw)}`; This is a lib bug and should be reported."
    )


def _assert_str(raw: _T) -> Union[str, Exception]:
    if isinstance(raw, str):
        return raw
    return TypeError(
        f"Expected `str` but got `{type(raw)}`; This is a lib bug and should be reported."
    )


def _assert_opt_str_tuple(
    raw: Optional[_T],
) -> Union[Optional[Tuple[str, ...]], Exception]:
    if raw is None:
        return raw
    if isinstance(raw, tuple):
        return _utils.transform_items(raw, _assert_str)
    return TypeError(
        f"Expected `Optional[Tuple[str, ...]]` but got `{type(raw)}`; This is a lib bug and should be reported."
    )


@dataclass(frozen=True)  # type: ignore[misc]
class _ImportGraph:  # type: ignore[no-any-unimported]
    graph: AbstractImportGraph  # type: ignore[no-any-unimported]


@dataclass(frozen=True)
class ImportGraph:
    _inner: _ImportGraph
    roots: FrozenSet[FullPathModule]

    @staticmethod
    def from_modules(
        root_modules: Union[FullPathModule, FrozenSet[FullPathModule]],
        external_packages: bool,
    ) -> ImportGraph:
        _root_modules = (
            root_modules
            if isinstance(root_modules, frozenset)
            else frozenset([root_modules])
        )
        raw_modules = frozenset(r.module for r in _root_modules)
        graph = grimp.build_graph(*raw_modules, include_external_packages=external_packages)  # type: ignore[misc]
        return ImportGraph(_ImportGraph(graph), _root_modules)  # type: ignore[misc]

    @classmethod
    def build_graph(
        cls, raw_roots: Union[str, FrozenSet[str]], external_packages: bool
    ) -> Union[ImportGraph, NoReturn]:
        roots = (
            raw_roots
            if isinstance(raw_roots, frozenset)
            else frozenset([raw_roots])
        )
        modules = frozenset(FullPathModule.assert_module(r) for r in roots)
        return cls.from_modules(modules, external_packages)

    def chain_exists(
        self,
        importer: FullPathModule,
        imported: FullPathModule,
        as_packages: bool,
    ) -> bool:
        result = _assert_bool(
            self._inner.graph.chain_exists(importer.module, imported.module, as_packages),  # type: ignore[misc]
        )
        return _utils.raise_or_value(result)

    def find_shortest_chain(
        self,
        importer: FullPathModule,
        imported: FullPathModule,
    ) -> Optional[Tuple[FullPathModule, ...]]:
        _raw = _assert_opt_str_tuple(
            self._inner.graph.find_shortest_chain(importer.module, imported.module),  # type: ignore[misc]
        )
        raw = _utils.raise_or_value(_raw)
        if raw is None:
            return None
        return tuple(FullPathModule.assert_module(r) for r in raw)

    def find_children(
        self, module: FullPathModule
    ) -> FrozenSet[FullPathModule]:
        items: FrozenSet[str] = frozenset(self._inner.graph.find_children(module.module))  # type: ignore[misc]
        return frozenset(FullPathModule.assert_module(i) for i in items)

    def find_modules_that_directly_import(
        self, module: FullPathModule
    ) -> FrozenSet[FullPathModule]:
        items: FrozenSet[str] = frozenset(self._inner.graph.find_modules_that_directly_import(module.module))  # type: ignore[misc]
        return frozenset(FullPathModule.assert_module(i) for i in items)

    def find_modules_directly_imported_by(
        self, module: FullPathModule
    ) -> FrozenSet[FullPathModule]:
        items: FrozenSet[str] = frozenset(self._inner.graph.find_modules_directly_imported_by(module.module))  # type: ignore[misc]
        return frozenset(FullPathModule.assert_module(i) for i in items)

    def find_modules_that_import(
        self, module: FullPathModule, as_package: bool
    ) -> FrozenSet[FullPathModule]:
        """
        as_package: set true to include only external modules relative to the suplied one
        """
        items: FrozenSet[str] = frozenset(self._inner.graph.find_downstream_modules(module.module, as_package))  # type: ignore[misc]
        return frozenset(FullPathModule.assert_module(i) for i in items)


__all__ = [
    "FullPathModule",
]
