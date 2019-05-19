#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "cnheider"
__doc__ = ""
from warg import app_path

_app_name = "MyApp"
_app_author = __author__

props = ("user_data", "user_config", "user_cache", "user_state", "user_log", "site_data", "site_config")


def test_all():
    print("-- app dirs (with optional 'version')")
    dirs = app_path.AppPath(_app_name, _app_author, app_version="1.0", ensure_existence=False)
    for prop in props:
        print("%s: %s" % (prop, getattr(dirs, prop)))


def test_no_ver():
    print("\n-- app dirs (without optional 'version')")
    dirs = app_path.AppPath(_app_name, _app_author, ensure_existence=False)
    for prop in props:
        print("%s: %s" % (prop, getattr(dirs, prop)))


def test_author():
    print("\n-- app dirs (without optional '_app_author')")
    dirs = app_path.AppPath(_app_name, ensure_existence=False)
    for prop in props:
        print("%s: %s" % (prop, getattr(dirs, prop)))


def test_no_author():
    print("\n-- app dirs (with disabled '_app_author')")
    dirs = app_path.AppPath(_app_name, app_author=False, ensure_existence=False)
    for prop in props:
        print("%s: %s" % (prop, getattr(dirs, prop)))
