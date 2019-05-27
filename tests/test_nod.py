#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pytest

from warg.named_ordered_dictionary import NOD, IllegalAttributeKey

__author__ = "cnheider"


def test_attribute_assignment():
    nodict = NOD()
    nodict.paramA = "str_parameter"
    nodict.paramB = 10
    assert nodict.paramA == "str_parameter"
    assert nodict.paramB == 10


def test_dict_arg_construction():
    nodict = NOD({"paramA": "str_parameter", "paramB": 10})
    assert nodict.paramA == "str_parameter"
    assert nodict.paramB == 10


def test_update_and_set_attr_update():
    nodict = NOD()
    nodict.update({"paramA": 20, "paramB": "other_param", "paramC": 5.0})
    nodict.paramA = 10
    assert nodict.paramA == 10
    assert nodict.paramB == "other_param"


def test_set_item_update():
    nodict = NOD()
    nodict["paramA"] = 10
    assert nodict.paramA == 10


def test_as_list_args_and_kwargs():
    vals = [1, 3, 5]
    nodict = NOD(10, val2=2, *vals)
    nolist = nodict.as_list()
    assert nolist[0] == 10
    assert nodict.val2 == 2
    assert nolist[-2] == vals[-1]


def test_kv_unmap():
    nodict = NOD("str_parameter", 10)
    odict = {**nodict}
    assert nodict.as_list()[0] == list(odict.values())[0]


def test_update_attr_with_kwargs():
    nodict = NOD("str_parameter", 10)
    nodict.update(arg1=20, arg0="other_param")
    assert nodict.arg0 == "other_param"
    assert nodict.arg1 == 20


def test_update_attr_with_dict_arg():
    nodict = NOD("str_parameter", 10)
    nodict.update({"arg1": 20, "arg0": "other_param"})
    assert nodict.arg0 == "other_param"
    assert nodict.arg1 == 20


def test_no_existing_attr():
    nodict = NOD(paramA="str_parameter", paramB=10)
    nodict.update(20, "other_param")
    assert nodict.paramB == "other_param"
    assert nodict.paramA == 20
    assert nodict.get("paramC") is None


def test_existing_map_unpacking():
    nodict = NOD(paramA="str_parameter", paramB=10)
    nodict.update(20, "other_param")
    nodict = NOD(paramC="str_parameter", **nodict)
    assert nodict.paramB == "other_param"
    assert nodict.paramA == 20
    assert nodict.get("paramC") is not None


def test_as_list():
    arg0, arg1 = NOD("str_parameter", 10).as_list()
    assert arg0 == "str_parameter"
    assert arg1 == 10


def test_access_operators():
    arg0, arg1 = NOD("str_parameter", 10).as_list()
    columns = NOD.nod_of(arg1, dsa=arg0)
    assert columns["arg1"] == arg1
    assert columns.arg1 == arg1
    assert columns["dsa"] == arg0
    assert columns / "dsa" == arg0
    assert id(columns / "dsa") == id(columns["dsa"])


def test_new_attr_on_existing():
    a = NOD(4, 2)
    a.list = "a"
    assert a.list == "a"


def test_addition_arithmetic():
    a = NOD(4, 2)
    b = a + a
    assert b.as_list() == [8, 4]


def test_illegal_overwrite():
    with pytest.raises(IllegalAttributeKey) as exc_info:
        NOD(update=2)

    assert exc_info.type is IllegalAttributeKey


def test_slice_get():
    a = NOD(4, 2)
    b = a + a
    assert b[:1] == [8]
    assert b[-1:] == [4]


def test_slice_get_adv():
    a = NOD(4, 2)
    b = a[:1] + a[0:]
    assert b[:1] == [4]
    assert b[-1:] == [2]


def test_slice_set():
    a = NOD(4, 2)
    a[:1] = [8]
    assert a.as_list() == [8, 2]


def test_slice_all():
    a = NOD(4, 2)
    b = a + a + a
    b[:1] = [8]
    assert b.as_list() == [8, 6]
