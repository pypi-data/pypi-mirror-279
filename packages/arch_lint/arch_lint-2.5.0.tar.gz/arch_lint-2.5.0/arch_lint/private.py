from __future__ import (
    annotations,
)

from arch_lint.graph import (
    FullPathModule,
    ImportGraph,
)
from dataclasses import (
    dataclass,
    field,
)
from typing import (
    NoReturn,
    Optional,
    Union,
)


@dataclass(frozen=True)
class _Private:
    pass


@dataclass(frozen=True)
class PrivateModule:
    _private: _Private = field(repr=False, hash=False, compare=False)
    module: FullPathModule

    @staticmethod
    def is_private(module: FullPathModule) -> Optional[PrivateModule]:
        if module.name.startswith("_"):
            return PrivateModule(_Private(), module)
        return None

    @classmethod
    def first_private_module_parent(
        cls, module: FullPathModule
    ) -> Optional[PrivateModule]:
        """Returns the first private module in the parent chain of a module (self inclusive)"""
        result = cls.is_private(module)
        if not result and module.parent:
            return cls.first_private_module_parent(module.parent)
        return result


def check_private(
    graph: ImportGraph, module: FullPathModule
) -> Union[None, NoReturn]:
    imports = graph.find_modules_directly_imported_by(module)
    _private_modules = frozenset(
        PrivateModule.first_private_module_parent(i) for i in imports
    )
    private_modules = frozenset(i for i in _private_modules if i is not None)

    def _validate_import(private: PrivateModule) -> bool:
        parent = private.module.parent
        if parent:
            return module.is_descendant_of(parent) or parent == module
        return True  # private root modules are global

    for p in private_modules:
        if not _validate_import(p):
            raise Exception(
                f"Illegal import of private module {module.module} -> {p.module.module}"
            )
    for c in graph.find_children(module):
        check_private(graph, c)
    return None
