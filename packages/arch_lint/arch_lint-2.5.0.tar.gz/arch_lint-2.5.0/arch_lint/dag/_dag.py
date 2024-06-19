from __future__ import (
    annotations,
)

from arch_lint import (
    _utils,
)
from arch_lint._full_path import (
    FullPathModule,
)
from dataclasses import (
    dataclass,
)
from typing import (
    FrozenSet,
    Tuple,
    Union,
)


@dataclass(frozen=True)
class _Private:
    pass


@dataclass(frozen=True)
class DAG:
    """
    Defines a DAG between modules
    """

    _inner: _Private
    layers: Tuple[FrozenSet[FullPathModule], ...]
    all_modules: FrozenSet[FullPathModule]

    @staticmethod
    def new(
        dag: Tuple[Union[FrozenSet[str], Tuple[str, ...]], ...]
    ) -> Union[DAG, Exception]:
        """
        - each `str` is mapped into a `FullPathModule`
        - each mapped `FullPathModule` should be not duplicated
        """
        all_modules = _utils.assert_set(_utils.chain_items(dag), lambda x: x)
        if isinstance(all_modules, Exception):
            return all_modules
        all_modules_full = _utils.transform_sets(
            all_modules, FullPathModule.from_raw
        )
        if isinstance(all_modules_full, Exception):
            return all_modules_full
        _dag = tuple(frozenset(d) for d in dag)
        layers = _utils.transform_items(
            _dag,
            lambda layer: _utils.transform_sets(
                layer, FullPathModule.from_raw
            ),
        )
        if isinstance(layers, Exception):
            return layers
        return DAG(_Private(), layers, frozenset(all_modules_full))

    @staticmethod
    def from_full_paths(
        dag: Tuple[FrozenSet[FullPathModule], ...]
    ) -> Union[DAG, Exception]:
        all_modules = _utils.assert_set(
            _utils.chain_items(dag), lambda x: str(x)
        )
        if isinstance(all_modules, Exception):
            return all_modules
        return DAG(_Private(), dag, frozenset(all_modules))
