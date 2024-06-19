from typing import (
    Callable,
    FrozenSet,
    List,
    NoReturn,
    Set,
    Tuple,
    TypeVar,
    Union,
)

_T = TypeVar("_T")
_R = TypeVar("_R")


def chain_items(
    items: Tuple[Union[FrozenSet[_T], Tuple[_T, ...]], ...]
) -> Tuple[_T, ...]:
    all_items: List[_T] = []
    for item_set in items:
        for item in item_set:
            all_items.append(item)
    return tuple(all_items)


def assert_set(
    items: Tuple[_T, ...], encode: Callable[[_T], str]
) -> Union[FrozenSet[_T], Exception]:
    item_set: Set[_T] = set([])
    for i in items:
        if i in item_set:
            return Exception(f"Duplicated item i.e. {encode(i)}")
        item_set.add(i)
    return frozenset(item_set)


def transform_items(
    items: Tuple[_T, ...], transform: Callable[[_T], Union[_R, Exception]]
) -> Union[Tuple[_R, ...], Exception]:
    result: List[_R] = []
    for i in items:
        item = transform(i)
        if isinstance(item, Exception):
            return item
        result.append(item)
    return tuple(result)


def transform_sets(
    items: FrozenSet[_T], transform: Callable[[_T], Union[_R, Exception]]
) -> Union[FrozenSet[_R], Exception]:
    _items: Tuple[_T, ...] = tuple(items)
    result = transform_items(_items, transform)
    if isinstance(result, Exception):
        return result
    return frozenset(result)


def to_tuple(item: Union[Tuple[str, ...], str]) -> Tuple[str, ...]:
    if isinstance(item, tuple):
        return item
    return (item,)


def raise_or_value(item: Union[_T, Exception]) -> Union[_T, NoReturn]:
    if isinstance(item, Exception):
        raise item
    return item
