#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pytest

from warg.named_ordered_dictionary import IllegalAttributeKey, NOD

__author__ = "Christian Heider Nielsen"


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


def test_access_operators_NOD():
    arg0 = "str_parameter"
    arg1 = 10
    l = NOD(arg0, arg1)
    assert l[id(arg1)] == arg1
    assert l.__getattr__(id(arg1)) == arg1
    assert l[id(arg0)] == arg0
    assert l / id(arg0) == arg0
    assert l @ id(arg0) == arg0


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


def test_sorcery():
    from sorcery import dict_of

    def ret1():
        return 1

    arg1 = ret1()
    columns = dict_of(arg1)
    assert columns["arg1"] == arg1


def test_access_operators_NOD_of():
    list_rep = NOD("str_parameter", 10).as_list()
    arg0 = list_rep[0]
    arg1 = list_rep[1]
    columns = NOD.nod_of(arg1, dsa=arg0)
    assert columns["arg1"] == arg1
    assert columns.arg1 == arg1
    assert columns["dsa"] == arg0
    assert columns / "dsa" == arg0
    assert columns @ "dsa" == arg0
    assert id(columns / "dsa") == id(columns["dsa"])


def test_multiple_return_assignment_to_contstruction():
    arg0, arg1 = ("sta", 1)
    columns = NOD.nod_of(arg1, arg0)
    assert columns.arg1 == 1
    assert columns.arg0 == "sta"


def test_access_operators_single_explicit_naming():
    arg0 = "str_parameter"
    columns = NOD.nod_of(dsa=arg0)
    assert columns["dsa"] == arg0
    assert columns / "dsa" == arg0
    assert id(columns / "dsa") == id(columns["dsa"])


def test_access_operators_single_no_naming():
    dsa = "str_parameter"
    columns = NOD.nod_of(dsa)
    assert columns["dsa"] == dsa
    assert columns / "dsa" == dsa
    assert id(columns / "dsa") == id(columns["dsa"])


def test_access_operators_no_multi_return_no_variable_name_direct_inference():
    arg0 = "str_parameter"
    columns = NOD.nod_of("sas", dsa=arg0)
    print(columns)
    assert columns[:1] == ["sas"]
    assert columns.as_list()[0] == "sas"
    assert columns.as_list()[1] == arg0
    assert columns["dsa"] == arg0
    assert columns / "dsa" == arg0
    assert id(columns / "dsa") == id(columns["dsa"])


def test_nested():
    cfg = NOD()

    cfg.MODEL = NOD()

    cfg.MODEL.DEVICE = "cuda"
    # match default boxes to any ground truth with jaccard overlap higher than a threshold (0.5)
    cfg.MODEL.THRESHOLD = 0.5
    cfg.MODEL.NUM_CLASSES = 21
    # Hard negative mining
    cfg.MODEL.NEG_POS_RATIO = 3
    cfg.MODEL.CENTER_VARIANCE = 0.1
    cfg.MODEL.SIZE_VARIANCE = 0.2

    cfg.ADSA = 203182

    print(cfg)


def test_copy():
    from copy import deepcopy, copy

    nodict = NOD()
    nodict.paramA = "str_parameter"
    nodict.paramB = 10

    b = copy(nodict)
    print(b)
    assert b.paramB == 10
    assert b.paramB == nodict.paramB

    a = deepcopy(nodict)
    print(a)
    assert a.paramB == 10
    assert a.paramB == nodict.paramB


def test_distribute_keys_view():
    nodict = NOD()
    nodict.paramA = 2
    nodict.paramB = 10

    nodict.paramC = 5
    nodict[nodict.keys()] = 4

    assert nodict.paramA == 4
    assert nodict.paramB == 4
    assert nodict.paramC == 4


def test_distribute_slice():
    nodict = NOD()
    nodict.paramA = 2
    nodict.paramB = 10
    nodict.paramC = 5
    nodict.paramD = 5

    nodict[:3] = 4

    assert nodict.paramA == 4
    assert nodict.paramB == 4
    assert nodict.paramC == 4
    assert nodict.paramD == 5


def test_multi_key_index():
    nodict = NOD()
    nodict.paramA = 2
    nodict.paramB = 10
    nodict.paramC = 5
    nodict.paramD = 5

    nodict["paramA", "paramB"] = 4

    assert nodict.paramA == 2
    assert nodict.paramB == 10
    assert nodict.paramC == 5
    assert nodict.paramD == 5

    assert nodict["paramA", "paramB"] == 4


def test_call_index():
    nodict = NOD()
    nodict.paramA = 2
    nodict.paramB = 10
    nodict.paramC = 5
    nodict.paramD = 5
    nodict[6] = 1
    nodict[1] = 1
    nodict[2] = 11

    assert nodict.paramA == 2
    assert nodict.paramB == 10
    assert nodict.paramC == 5
    assert nodict.paramD == 5

    assert nodict("paramA", "paramB", 6) == [2, 10, 1]
    assert nodict("paramC") == [5]
    assert nodict(6, "paramD", 1) == [1, 5, 1]
    assert nodict(2) == [11]
