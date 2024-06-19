from ._dag import (
    DAG,
)
from ._dag_map import (
    DagMap,
)
from arch_lint import (
    _utils,
)
from arch_lint.graph import (
    FullPathModule,
    ImportGraph,
)
from pathlib import (
    Path,
)
from typing import (
    Callable,
    FrozenSet,
    NoReturn,
    Optional,
    Tuple,
    Union,
)


def _chain_exist(
    graph: ImportGraph,
    importer: FrozenSet[FullPathModule],
    imported: FrozenSet[FullPathModule],
) -> Optional[Tuple[FullPathModule, FullPathModule]]:
    for s in importer:
        for t in imported:
            if graph.chain_exists(s, t, True):
                return (s, t)
    return None


def _independence(
    graph: ImportGraph, modules: FrozenSet[FullPathModule]
) -> Optional[Tuple[FullPathModule, FullPathModule]]:
    for m in modules:
        checks = modules - frozenset([m])
        for c in checks:
            if graph.chain_exists(m, c, True):
                return (m, c)
    return None


def _check_independence(
    graph: ImportGraph, modules: FrozenSet[FullPathModule]
) -> Union[None, NoReturn]:
    result = _independence(graph, modules)
    if result:
        raise Exception(
            f"Broken DAG same lvl modules should be independent {result[0].module} -> {result[1].module}"
        )
    return None


def _check_dag_over_modules(
    graph: ImportGraph,
    lower: FrozenSet[FullPathModule],
    upper: FrozenSet[FullPathModule],
) -> Union[None, NoReturn]:
    _chain = _chain_exist(graph, lower, upper)
    if _chain:
        importer = _chain[0]
        imported = _chain[1]
        specific = graph.find_shortest_chain(importer, imported)
        raise Exception(
            f"Broken DAG with illegal import {importer.module} -> {imported.module} i.e. chain {specific}"
        )
    return None


def dag_completeness(
    dag: DAG, graph: ImportGraph, parent: FullPathModule
) -> Union[None, NoReturn]:
    children = graph.find_children(parent)
    missing = children - dag.all_modules
    if len(children) > 1 and missing:
        relative = ",".join(d.name for d in missing)
        raise Exception(
            f"Missing children modules of `{parent}` at DAG i.e. {relative}"
        )
    return None


def dag_completeness_from_set(
    dag: DAG, expected: FrozenSet[FullPathModule], raise_if_excess: bool
) -> Union[None, NoReturn]:
    diff = expected - dag.all_modules
    if diff:
        relative = ",".join(d.name for d in diff)
        raise Exception(f"Missing root modules i.e. {relative}")
    diff_2 = dag.all_modules - expected
    if diff_2 and raise_if_excess:
        relative_2 = ",".join(d.name for d in diff_2)
        raise Exception(f"Not listed modules i.e. {relative_2}")
    return None


def dag_completeness_from_dir(
    dag: DAG,
    dir_path: Path,
    raise_if_excess: bool,
    parent: Optional[FullPathModule],
    path_filter: Callable[[Path], bool] = lambda _: True,
) -> Union[None, NoReturn]:
    """
    Check a DAG object completeness taking the elements of
    `dir_path` as the complete expected list of modules.

    - `dir_path` children are transformed into FullPathModule
    using children name as the module name.
    - if `parent` is provided then the FullPathModule object from
    `dir_path` children will be expected to be children of `parent`
    - `path_filter` used to filter the children of `dir_path` that
    will be transformed
    """

    def _to_module(raw: str) -> Union[FullPathModule, Exception]:
        if parent:
            _parent = parent.assert_child(raw)
            return _parent
        return FullPathModule.from_raw(raw)

    if dir_path.is_dir():
        expected = _utils.transform_sets(
            frozenset(p.name for p in filter(path_filter, dir_path.iterdir())),
            _to_module,
        )
        if isinstance(expected, Exception):
            raise expected
        return dag_completeness_from_set(dag, expected, raise_if_excess)
    raise Exception("Expected a dir path")


def dag_map_completeness(
    dag_map: DagMap, graph: ImportGraph, parent: FullPathModule
) -> Union[None, NoReturn]:
    """
    Check a DagMap object completeness taking the children of
    `parent` as the complete expected list of modules.
    """
    parent_dag = dag_map.get(parent)
    children = graph.find_children(parent)
    if not parent_dag and len(children) > 1:
        raise Exception(f"Missing module at DagMap i.e. {parent}")
    if parent_dag:
        dag_completeness(parent_dag, graph, parent)
    for c in children:
        dag = dag_map.get(c)
        if not dag and len(graph.find_children(c)) > 1:
            raise Exception(f"Missing module at DagMap i.e. {c}")
        if dag:
            dag_completeness(dag, graph, c)
        dag_map_completeness(dag_map, graph, c)
    return None


def check_dag(
    dag: DAG,
    graph: ImportGraph,
) -> Union[None, NoReturn]:
    """
    Check a DAG object completeness taking the children of
    `parent` as the complete expected list of modules.
    """
    for n, c in enumerate(dag.layers):
        _check_independence(graph, c)
        for lower_modules in dag.layers[n + 1 :]:
            _check_dag_over_modules(
                graph,
                lower_modules,
                c,
            )

    return None


def check_dag_map(
    dag_map: DagMap,
    graph: ImportGraph,
) -> Union[None, NoReturn]:
    for d in dag_map.all_dags():
        check_dag(d, graph)
    return None
