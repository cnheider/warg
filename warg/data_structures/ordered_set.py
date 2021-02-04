#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""
Modified for all import

An OrderedSet is a custom MutableSet that remembers its order, so that every
entry has an index that can be looked up. It can also act like a Sequence.

Based on a recipe originally posted to ActiveState Recipes by Raymond Hettiger,
and released under the MIT license.

           Created on 06-11-2020
           """

__all__ = ["OrderedSet"]

from typing import (
    Any,
    Dict,
    Iterable,
    Iterator,
    List,
    MutableSet,
    Optional,
    Sequence,
    Set,
    TypeVar,
    Union,
    overload,
)

SLICE_ALL = slice(None)
__version__ = "4.0.2"

T = TypeVar("T")


# When Python 3.6 is the minimum version, we can define a type like this,
# parameterizing the types that an OrderedSet can interoperate with:
#
# SetLike = Union[Sequence[T], Set[T]]


def _is_atomic(obj: Any) -> bool:
    """
    Returns True for objects which are iterable but should not be iterated in
    the context of indexing an OrderedSet.

    When we index by an iterable, usually that means we're being asked to look
    up a list of things.

    However, in the case of the .index() method, we shouldn't handle strings
    and tuples like other iterables. They're not sequences of things to look
    up, they're the single, atomic thing we're trying to find.

    As an example, oset.index('hello') should give the index of 'hello' in an
    OrderedSet of strings. It shouldn't give the indexes of each individual
    character.
    """
    return isinstance(obj, str) or isinstance(obj, tuple)


class OrderedSet(MutableSet[T], Sequence[T]):
    """
    An OrderedSet is a custom MutableSet that remembers its order, so that
    every entry has an index that can be looked up.

    Example:
        >>> OrderedSet([1, 1, 2, 3, 2])
        OrderedSet([1, 2, 3])
    """

    def __init__(self, iterable: Optional[Iterable[T]] = None):
        self.items = []  # type: List[T]
        self.map = {}  # type: Dict[T, int]
        if iterable is not None:
            self |= iterable

    def __len__(self):
        """
        Returns the number of unique elements in the ordered set

        Example:
            >>> len(OrderedSet([]))
            0
            >>> len(OrderedSet([1, 2]))
            2
        """
        return len(self.items)

    @overload
    def __getitem__(self, index: Sequence[int]) -> List[T]:
        ...

    @overload
    def __getitem__(self, index: slice) -> "OrderedSet[T]":
        ...

    def __getitem__(self, index: int) -> T:
        """
        Get the item at a given index.

        If `index` is a slice, you will get back that slice of items, as a
        new OrderedSet.

        If `index` is a list or a similar iterable, you'll get a list of
        items corresponding to those indices. This is similar to NumPy's
        "fancy indexing". The result is not an OrderedSet because you may ask
        for duplicate indices, and the number of elements returned should be
        the number of elements asked for.

        Example:
            >>> oset = OrderedSet([1, 2, 3])
            >>> oset[1]
            2
        """
        if isinstance(index, slice) and index == SLICE_ALL:
            return self.copy()
        elif isinstance(index, Iterable):
            return [self.items[i] for i in index]
        elif isinstance(index, slice) or hasattr(index, "__index__"):
            result = self.items[index]
            if isinstance(result, list):
                return self.__class__(result)
            else:
                return result
        else:
            raise TypeError("Don't know how to index an OrderedSet by %r" % index)

    def copy(self) -> "OrderedSet[T]":
        """
        Return a shallow copy of this object.

        Example:
            >>> this = OrderedSet([1, 2, 3])
            >>> other = this.copy()
            >>> this == other
            True
            >>> this is other
            False
        """
        return self.__class__(self)

    # Define the gritty details of how an OrderedSet is serialized as a pickle.
    # We leave off type annotations, because the only code that should interact
    # with these is a generalized tool such as pickle.
    def __getstate__(self):
        if len(self) == 0:
            # In pickle, the state can't be an empty list.
            # We need to return a truthy value, or else __setstate__ won't be run.
            #
            # This could have been done more gracefully by always putting the state
            # in a tuple, but this way is backwards- and forwards- compatible with
            # previous versions of OrderedSet.
            return (None,)
        else:
            return list(self)

    def __setstate__(self, state):
        if state == (None,):
            self.__init__([])
        else:
            self.__init__(state)

    def __contains__(self, key: Any) -> bool:
        """
        Test if the item is in this ordered set.

        Example:
            >>> 1 in OrderedSet([1, 3, 2])
            True
            >>> 5 in OrderedSet([1, 3, 2])
            False
        """
        return key in self.map

    def add(self, key: T) -> int:
        """
        Add `key` as an item to this OrderedSet, then return its index.

        If `key` is already in the OrderedSet, return the index it already
        had.

        Example:
            >>> oset = OrderedSet()
            >>> oset.append(3)
            0
            >>> print(oset)
            OrderedSet([3])
        """
        if key not in self.map:
            self.map[key] = len(self.items)
            self.items.append(key)
        return self.map[key]

    append = add

    def update(self, sequence: Union[Sequence[T], Set[T]]) -> int:
        """
        Update the set with the given iterable sequence, then return the index
        of the last element inserted.

        Example:
            >>> oset = OrderedSet([1, 2, 3])
            >>> oset.update([3, 1, 5, 1, 4])
            4
            >>> print(oset)
            OrderedSet([1, 2, 3, 5, 4])
        """
        item_index = 0
        try:
            for item in sequence:
                item_index = self.add(item)
        except TypeError:
            raise ValueError(
                "Argument needs to be an iterable, got %s" % type(sequence)
            )
        return item_index

    @overload
    def index(self, key: T) -> int:
        ...

    def index(self, key: Sequence[T]) -> List[int]:
        """
        Get the index of a given entry, raising an IndexError if it's not
        present.

        `key` can be an iterable of entries that is not a string, in which case
        this returns a list of indices.

        Example:
            >>> oset = OrderedSet([1, 2, 3])
            >>> oset.index(2)
            1
        """
        if isinstance(key, Iterable) and not _is_atomic(key):
            return [self.index(subkey) for subkey in key]
        return self.map[key]

    # Provide some compatibility with pd.Index
    get_loc = index
    get_indexer = index

    def pop(self) -> T:
        """
        Remove and return the last element from the set.

        Raises KeyError if the set is empty.

        Example:
            >>> oset = OrderedSet([1, 2, 3])
            >>> oset.pop()
            3
        """
        if not self.items:
            raise KeyError("Set is empty")

        elem = self.items[-1]
        del self.items[-1]
        del self.map[elem]
        return elem

    def discard(self, key: T) -> None:
        """
        Remove an element.  Do not raise an exception if absent.

        The MutableSet mixin uses this to implement the .remove() method, which
        *does* raise an error when asked to remove a non-existent item.

        Example:
            >>> oset = OrderedSet([1, 2, 3])
            >>> oset.discard(2)
            >>> print(oset)
            OrderedSet([1, 3])
            >>> oset.discard(2)
            >>> print(oset)
            OrderedSet([1, 3])
        """
        if key in self:
            i = self.map[key]
            del self.items[i]
            del self.map[key]
            for k, v in self.map.items():
                if v >= i:
                    self.map[k] = v - 1

    def clear(self) -> None:
        """
        Remove all items from this OrderedSet.
        """
        del self.items[:]
        self.map.clear()

    def __iter__(self) -> Iterator[T]:
        """
        Example:
            >>> list(iter(OrderedSet([1, 2, 3])))
            [1, 2, 3]
        """
        return iter(self.items)

    def __reversed__(self) -> Iterator[T]:
        """
        Example:
            >>> list(reversed(OrderedSet([1, 2, 3])))
            [3, 2, 1]
        """
        return reversed(self.items)

    def __repr__(self) -> str:
        if not self:
            return "%s()" % (self.__class__.__name__,)
        return "%s(%r)" % (self.__class__.__name__, list(self))

    def __eq__(self, other: Any) -> bool:
        """
        Returns true if the containers have the same items. If `other` is a
        Sequence, then order is checked, otherwise it is ignored.

        Example:
            >>> oset = OrderedSet([1, 3, 2])
            >>> oset == [1, 3, 2]
            True
            >>> oset == [1, 2, 3]
            False
            >>> oset == [2, 3]
            False
            >>> oset == OrderedSet([3, 2, 1])
            False
        """
        if isinstance(other, Sequence):
            # Check that this OrderedSet contains the same elements, in the
            # same order, as the other object.
            return list(self) == list(other)
        try:
            other_as_set = set(other)
        except TypeError:
            # If `other` can't be converted into a set, it's not equal.
            return False
        else:
            return set(self) == other_as_set

    def union(self, *sets: Union[Sequence[T], Set[T]]) -> "OrderedSet[T]":
        """
        Combines all unique items.
        Each items order is defined by its first appearance.

        Example:
            >>> oset = OrderedSet.union(OrderedSet([3, 1, 4, 1, 5]), [1, 3], [2, 0])
            >>> print(oset)
            OrderedSet([3, 1, 4, 5, 2, 0])
            >>> oset.union([8, 9])
            OrderedSet([3, 1, 4, 5, 2, 0, 8, 9])
            >>> oset | {10}
            OrderedSet([3, 1, 4, 5, 2, 0, 10])
        """
        cls = self.__class__ if isinstance(self, OrderedSet) else OrderedSet
        containers = map(list, it.chain([self], sets))
        items = it.chain.from_iterable(containers)
        return cls(items)

    def __and__(self, other: Union[Sequence[T], Set[T]]) -> "OrderedSet[T]":
        # the parent implementation of this is backwards
        return self.intersection(other)

    def intersection(self, *sets: Union[Sequence[T], Set[T]]) -> "OrderedSet[T]":
        """
        Returns elements in common between all sets. Order is defined only
        by the first set.

        Example:
            >>> oset = OrderedSet.intersection(OrderedSet([0, 1, 2, 3]), [1, 2, 3])
            >>> print(oset)
            OrderedSet([1, 2, 3])
            >>> oset.intersection([2, 4, 5], [1, 2, 3, 4])
            OrderedSet([2])
            >>> oset.intersection()
            OrderedSet([1, 2, 3])
        """
        cls = self.__class__ if isinstance(self, OrderedSet) else OrderedSet
        if sets:
            common = set.intersection(*map(set, sets))
            items = (item for item in self if item in common)
        else:
            items = self
        return cls(items)

    def difference(self, *sets: Union[Sequence[T], Set[T]]) -> "OrderedSet[T]":
        """
        Returns all elements that are in this set but not the others.

        Example:
            >>> OrderedSet([1, 2, 3]).difference(OrderedSet([2]))
            OrderedSet([1, 3])
            >>> OrderedSet([1, 2, 3]).difference(OrderedSet([2]), OrderedSet([3]))
            OrderedSet([1])
            >>> OrderedSet([1, 2, 3]) - OrderedSet([2])
            OrderedSet([1, 3])
            >>> OrderedSet([1, 2, 3]).difference()
            OrderedSet([1, 2, 3])
        """
        cls = self.__class__
        if sets:
            other = set.union(*map(set, sets))
            items = (item for item in self if item not in other)
        else:
            items = self
        return cls(items)

    def issubset(self, other: Union[Sequence[T], Set[T]]) -> bool:
        """
        Report whether another set contains this set.

        Example:
            >>> OrderedSet([1, 2, 3]).issubset({1, 2})
            False
            >>> OrderedSet([1, 2, 3]).issubset({1, 2, 3, 4})
            True
            >>> OrderedSet([1, 2, 3]).issubset({1, 4, 3, 5})
            False
        """
        if len(self) > len(other):  # Fast check for obvious cases
            return False
        return all(item in other for item in self)

    def issuperset(self, other: Union[Sequence[T], Set[T]]) -> bool:
        """
        Report whether this set contains another set.

        Example:
            >>> OrderedSet([1, 2]).issuperset([1, 2, 3])
            False
            >>> OrderedSet([1, 2, 3, 4]).issuperset({1, 2, 3})
            True
            >>> OrderedSet([1, 4, 3, 5]).issuperset({1, 2, 3})
            False
        """
        if len(self) < len(other):  # Fast check for obvious cases
            return False
        return all(item in self for item in other)

    def symmetric_difference(
        self, other: Union[Sequence[T], Set[T]]
    ) -> "OrderedSet[T]":
        """
        Return the symmetric difference of two OrderedSets as a new set.
        That is, the new set will contain all elements that are in exactly
        one of the sets.

        Their order will be preserved, with elements from `self` preceding
        elements from `other`.

        Example:
            >>> this = OrderedSet([1, 4, 3, 5, 7])
            >>> other = OrderedSet([9, 7, 1, 3, 2])
            >>> this.symmetric_difference(other)
            OrderedSet([4, 5, 9, 2])
        """
        cls = self.__class__ if isinstance(self, OrderedSet) else OrderedSet
        diff1 = cls(self).difference(other)
        diff2 = cls(other).difference(self)
        return diff1.union(diff2)

    def _update_items(self, items: list) -> None:
        """
        Replace the 'items' list of this OrderedSet with a new one, updating
        self.map accordingly.
        """
        self.items = items
        self.map = {item: idx for (idx, item) in enumerate(items)}

    def difference_update(self, *sets: Union[Sequence[T], Set[T]]) -> None:
        """
        Update this OrderedSet to remove items from one or more other sets.

        Example:
            >>> this = OrderedSet([1, 2, 3])
            >>> this.difference_update(OrderedSet([2, 4]))
            >>> print(this)
            OrderedSet([1, 3])

            >>> this = OrderedSet([1, 2, 3, 4, 5])
            >>> this.difference_update(OrderedSet([2, 4]), OrderedSet([1, 4, 6]))
            >>> print(this)
            OrderedSet([3, 5])
        """
        items_to_remove = set()  # type: Set[T]
        for other in sets:
            items_as_set = set(other)  # type: Set[T]
            items_to_remove |= items_as_set
        self._update_items([item for item in self.items if item not in items_to_remove])

    def intersection_update(self, other: Union[Sequence[T], Set[T]]) -> None:
        """
        Update this OrderedSet to keep only items in another set, preserving
        their order in this set.

        Example:
            >>> this = OrderedSet([1, 4, 3, 5, 7])
            >>> other = OrderedSet([9, 7, 1, 3, 2])
            >>> this.intersection_update(other)
            >>> print(this)
            OrderedSet([1, 3, 7])
        """
        other = set(other)
        self._update_items([item for item in self.items if item in other])

    def symmetric_difference_update(self, other: Union[Sequence[T], Set[T]]) -> None:
        """
        Update this OrderedSet to remove items from another set, then
        add items from the other set that were not present in this set.

        Example:
            >>> this = OrderedSet([1, 4, 3, 5, 7])
            >>> other = OrderedSet([9, 7, 1, 3, 2])
            >>> this.symmetric_difference_update(other)
            >>> print(this)
            OrderedSet([4, 5, 9, 2])
        """
        items_to_add = [item for item in other if item not in self]
        items_to_remove = set(other)
        self._update_items(
            [item for item in self.items if item not in items_to_remove] + items_to_add
        )


if __name__ == "__main__":
    import collections
    import itertools as it
    import operator
    import pickle
    import random
    import sys

    import pytest

    def test_pickle():
        set1 = OrderedSet("abracadabra")
        roundtrip = pickle.loads(pickle.dumps(set1))
        assert roundtrip == set1

    def test_empty_pickle():
        empty_oset = OrderedSet()
        empty_roundtrip = pickle.loads(pickle.dumps(empty_oset))
        assert empty_roundtrip == empty_oset

    def test_order():
        set1 = OrderedSet("abracadabra")
        assert len(set1) == 5
        assert set1 == OrderedSet(["a", "b", "r", "c", "d"])
        assert list(reversed(set1)) == ["d", "c", "r", "b", "a"]

    def test_binary_operations():
        set1 = OrderedSet("abracadabra")
        set2 = OrderedSet("simsalabim")
        assert set1 != set2

        assert set1 & set2 == OrderedSet(["a", "b"])
        assert set1 | set2 == OrderedSet(["a", "b", "r", "c", "d", "s", "i", "m", "l"])
        assert set1 - set2 == OrderedSet(["r", "c", "d"])

    def test_indexing():
        set1 = OrderedSet("abracadabra")
        assert set1[:] == set1
        assert set1.copy() == set1
        assert set1 is set1
        assert set1[:] is not set1
        assert set1.copy() is not set1

        assert set1[[1, 2]] == OrderedSet(["b", "r"])
        assert set1[1:3] == OrderedSet(["b", "r"])
        assert set1.index("b") == 1
        assert set1.index(["b", "r"]) == [1, 2]
        with pytest.raises(KeyError):
            set1.index("br")

    class FancyIndexTester:
        """
        Make sure we can index by a NumPy ndarray, without having to import
        NumPy.
        """

        def __init__(self, indices):
            self.indices = indices

        def __iter__(self):
            return iter(self.indices)

        def __index__(self):
            raise TypeError("NumPy arrays have weird __index__ methods")

        def __eq__(self, other):
            # Emulate NumPy being fussy about the == operator
            raise TypeError

    def test_fancy_index_class():
        set1 = OrderedSet("abracadabra")
        indexer = FancyIndexTester([1, 0, 4, 3, 0, 2])
        assert "".join(set1[indexer]) == "badcar"

    def test_pandas_compat():
        set1 = OrderedSet("abracadabra")
        assert set1.get_loc("b") == 1
        assert set1.get_indexer(["b", "r"]) == [1, 2]

    def test_tuples():
        set1 = OrderedSet()
        tup = ("tuple", 1)
        set1.add(tup)
        assert set1.index(tup) == 0
        assert set1[0] == tup

    def test_remove():
        set1 = OrderedSet("abracadabra")

        set1.remove("a")
        set1.remove("b")

        assert set1 == OrderedSet("rcd")
        assert set1[0] == "r"
        assert set1[1] == "c"
        assert set1[2] == "d"

        assert set1.index("r") == 0
        assert set1.index("c") == 1
        assert set1.index("d") == 2

        assert "a" not in set1
        assert "b" not in set1
        assert "r" in set1

        # Make sure we can .discard() something that's already gone, plus
        # something that was never there
        set1.discard("a")
        set1.discard("a")

    def test_remove_error():
        # If we .remove() an element that's not there, we get a KeyError
        set1 = OrderedSet("abracadabra")
        with pytest.raises(KeyError):
            set1.remove("z")

    def test_clear():
        set1 = OrderedSet("abracadabra")
        set1.clear()

        assert len(set1) == 0
        assert set1 == OrderedSet()

    def test_update():
        set1 = OrderedSet("abcd")
        result = set1.update("efgh")

        assert result == 7
        assert len(set1) == 8
        assert "".join(set1) == "abcdefgh"

        set2 = OrderedSet("abcd")
        result = set2.update("cdef")
        assert result == 5
        assert len(set2) == 6
        assert "".join(set2) == "abcdef"

    def test_pop():
        set1 = OrderedSet("ab")
        elem = set1.pop()

        assert elem == "b"
        elem = set1.pop()

        assert elem == "a"

        pytest.raises(KeyError, set1.pop)

    def test_getitem_type_error():
        set1 = OrderedSet("ab")
        with pytest.raises(TypeError):
            set1["a"]

    def test_update_value_error():
        set1 = OrderedSet("ab")
        with pytest.raises(ValueError):
            # noinspection PyTypeChecker
            set1.update(3)

    def test_empty_repr():
        set1 = OrderedSet()
        assert repr(set1) == "OrderedSet()"

    def test_eq_wrong_type():
        set1 = OrderedSet()
        assert set1 != 2

    def test_ordered_equality():
        # Ordered set checks order against sequences.
        assert OrderedSet([1, 2]) == OrderedSet([1, 2])
        assert OrderedSet([1, 2]) == [1, 2]
        assert OrderedSet([1, 2]) == (1, 2)
        assert OrderedSet([1, 2]) == collections.deque([1, 2])

    def test_ordered_inequality():
        # Ordered set checks order against sequences.
        assert OrderedSet([1, 2]) != OrderedSet([2, 1])

        assert OrderedSet([1, 2]) != [2, 1]
        assert OrderedSet([1, 2]) != [2, 1, 1]

        assert OrderedSet([1, 2]) != (2, 1)
        assert OrderedSet([1, 2]) != (2, 1, 1)

        # Note: in Python 2.7 deque does not inherit from Sequence, but __eq__
        # contains an explicit check for this case for python 2/3 compatibility.
        assert OrderedSet([1, 2]) != collections.deque([2, 1])
        assert OrderedSet([1, 2]) != collections.deque([2, 2, 1])

    def test_comparisons():
        # Comparison operators on sets actually test for subset and superset.
        assert OrderedSet([1, 2]) < OrderedSet([1, 2, 3])
        assert OrderedSet([1, 2]) > OrderedSet([1])

        # MutableSet subclasses aren't comparable to set on 3.3.
        if tuple(sys.version_info) >= (3, 4):
            assert OrderedSet([1, 2]) > {1}

    def test_unordered_equality():
        # Unordered set checks order against non-sequences.
        assert OrderedSet([1, 2]) == {1, 2}
        assert OrderedSet([1, 2]) == frozenset([2, 1])

        assert OrderedSet([1, 2]) == {1: "a", 2: "b"}
        assert OrderedSet([1, 2]) == {1: 1, 2: 2}.keys()
        assert OrderedSet([1, 2]) == {1: 1, 2: 2}.values()

        # Corner case: OrderedDict is not a Sequence, so we don't check for order,
        # even though it does have the concept of order.
        assert OrderedSet([1, 2]) == collections.OrderedDict([(2, 2), (1, 1)])

        # Corner case: We have to treat iterators as unordered because there
        # is nothing to distinguish an ordered and unordered iterator
        assert OrderedSet([1, 2]) == iter([1, 2])
        assert OrderedSet([1, 2]) == iter([2, 1])
        assert OrderedSet([1, 2]) == iter([2, 1, 1])

    def test_unordered_inequality():
        assert OrderedSet([1, 2]) != set([])
        assert OrderedSet([1, 2]) != frozenset([2, 1, 3])

        assert OrderedSet([1, 2]) != {2: "b"}
        assert OrderedSet([1, 2]) != {1: 1, 4: 2}.keys()
        assert OrderedSet([1, 2]) != {1: 1, 2: 3}.values()

        # Corner case: OrderedDict is not a Sequence, so we don't check for order,
        # even though it does have the concept of order.
        assert OrderedSet([1, 2]) != collections.OrderedDict([(2, 2), (3, 1)])

    def allsame_(iterable, eq=operator.eq):
        """ returns True of all items in iterable equal each other """
        iter_ = iter(iterable)
        try:
            first = next(iter_)
        except StopIteration:
            return True
        return all(eq(first, item) for item in iter_)

    def check_results_(results, datas, name):
        """
        helper for binary operator tests.

        check that all results have the same value, but are different items.
        data and name are used to indicate what sort of tests is run.
        """
        if not allsame_(results):
            raise AssertionError(
                "Not all same {} for {} with datas={}".format(results, name, datas)
            )
        for a, b in it.combinations(results, 2):
            if not isinstance(a, (bool, int)):
                assert a is not b, name + " should all be different items"

    def _operator_consistency_testdata():
        """
        Predefined and random data used to test operator consistency.
        """
        # test case 1
        data1 = OrderedSet([5, 3, 1, 4])
        data2 = OrderedSet([1, 4])
        yield data1, data2

        # first set is empty
        data1 = OrderedSet([])
        data2 = OrderedSet([3, 1, 2])
        yield data1, data2

        # second set is empty
        data1 = OrderedSet([3, 1, 2])
        data2 = OrderedSet([])
        yield data1, data2

        # both sets are empty
        data1 = OrderedSet([])
        data2 = OrderedSet([])
        yield data1, data2

        # random test cases
        rng = random.Random(0)
        a, b = 20, 20
        for _ in range(10):
            data1 = OrderedSet(rng.randint(0, a) for _ in range(b))
            data2 = OrderedSet(rng.randint(0, a) for _ in range(b))
            yield data1, data2
            yield data2, data1

    def test_operator_consistency_isect():
        for data1, data2 in _operator_consistency_testdata():
            result1 = data1.copy()
            result1.intersection_update(data2)
            result2 = data1 & data2
            result3 = data1.intersection(data2)
            check_results_(
                [result1, result2, result3], datas=(data1, data2), name="isect"
            )

    def test_operator_consistency_difference():
        for data1, data2 in _operator_consistency_testdata():
            result1 = data1.copy()
            result1.difference_update(data2)
            result2 = data1 - data2
            result3 = data1.difference(data2)
            check_results_(
                [result1, result2, result3], datas=(data1, data2), name="difference"
            )

    def test_operator_consistency_xor():
        for data1, data2 in _operator_consistency_testdata():
            result1 = data1.copy()
            result1.symmetric_difference_update(data2)
            result2 = data1 ^ data2
            result3 = data1.symmetric_difference(data2)
            check_results_(
                [result1, result2, result3], datas=(data1, data2), name="xor"
            )

    def test_operator_consistency_union():
        for data1, data2 in _operator_consistency_testdata():
            result1 = data1.copy()
            result1.update(data2)
            result2 = data1 | data2
            result3 = data1.union(data2)
            check_results_(
                [result1, result2, result3], datas=(data1, data2), name="union"
            )

    def test_operator_consistency_subset():
        for data1, data2 in _operator_consistency_testdata():
            result1 = data1 <= data2
            result2 = data1.issubset(data2)
            result3 = set(data1).issubset(set(data2))
            check_results_(
                [result1, result2, result3], datas=(data1, data2), name="subset"
            )

    def test_operator_consistency_superset():
        for data1, data2 in _operator_consistency_testdata():
            result1 = data1 >= data2
            result2 = data1.issuperset(data2)
            result3 = set(data1).issuperset(set(data2))
            check_results_(
                [result1, result2, result3], datas=(data1, data2), name="superset"
            )

    def test_operator_consistency_disjoint():
        for data1, data2 in _operator_consistency_testdata():
            result1 = data1.isdisjoint(data2)
            result2 = len(data1.intersection(data2)) == 0
            check_results_([result1, result2], datas=(data1, data2), name="disjoint")

    def test_bitwise_and_consistency():
        # Specific case that was failing without explicit __and__ definition
        data1 = OrderedSet([12, 13, 1, 8, 16, 15, 9, 11, 18, 6, 4, 3, 19, 17])
        data2 = OrderedSet([19, 4, 9, 3, 2, 10, 15, 17, 11, 13, 20, 6, 14, 16, 8])
        result1 = data1.copy()
        result1.intersection_update(data2)
        # This requires a custom & operation apparently
        result2 = data1 & data2
        result3 = data1.intersection(data2)
        check_results_([result1, result2, result3], datas=(data1, data2), name="isect")
