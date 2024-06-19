from .mock_arch import (
    forbidden_allowlist,
    project_dag,
)
from arch_lint.dag.check import (
    check_dag_map,
)
from arch_lint.forbidden import (
    check_forbidden,
)
from arch_lint.graph import (
    FullPathModule,
    ImportGraph,
)
from arch_lint.private import (
    check_private,
)
import pytest

root = "mock_module"


def test_dag_creation() -> None:
    project_dag()


def test_dag() -> None:
    graph = ImportGraph.build_graph(root, True)
    print(graph)
    check_dag_map(project_dag(), graph)


def test_forbidden_creation() -> None:
    forbidden_allowlist()


def test_forbidden() -> None:
    graph = ImportGraph.build_graph(root, True)
    allowlist_map = forbidden_allowlist()
    check_forbidden(allowlist_map, graph)


def test_private_check_case_1() -> None:
    graph = ImportGraph.build_graph(root, False)
    with pytest.raises(Exception) as err:
        check_private(
            graph, FullPathModule.assert_module("mock_module.illegal_import")
        )
    assert (
        str(err.value)
        == "Illegal import of private module mock_module.illegal_import -> mock_module.illegal_import.layer1._private_module"
    )


def test_private_check_case_2() -> None:
    graph = ImportGraph.build_graph(root, False)
    with pytest.raises(Exception) as err:
        check_private(
            graph, FullPathModule.assert_module("mock_module.illegal_import_2")
        )
    assert (
        str(err.value)
        == "Illegal import of private module mock_module.illegal_import_2.foo -> mock_module.illegal_import_2.layer1._private_module"
    )


def test_private_check_case_3() -> None:
    graph = ImportGraph.build_graph(root, False)
    with pytest.raises(Exception) as err:
        check_private(
            graph, FullPathModule.assert_module("mock_module.illegal_import_3")
        )
    assert (
        str(err.value)
        == "Illegal import of private module mock_module.illegal_import_3.foo -> mock_module.illegal_import_3.layer1._private_module"
    )
