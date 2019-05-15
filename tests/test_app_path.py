#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "cnheider"
__doc__ = ""
import app_path

_app_name = "MyApp"
_app_author = "MyCompany"

props = (
    "user_data_dir",
    "user_config_dir",
    "user_cache_dir",
    "user_state_dir",
    "user_log_dir",
    "site_data_dir",
    "site_config_dir",
)


def test_all():
    print("-- app dirs (with optional 'version')")
    dirs = app_path.AppPath(_app_name, _app_author, version="1.0")
    for prop in props:
        print("%s: %s" % (prop, getattr(dirs, prop)))


def test_no_ver():
    print("\n-- app dirs (without optional 'version')")
    dirs = app_path.AppPath(_app_name, _app_author)
    for prop in props:
        print("%s: %s" % (prop, getattr(dirs, prop)))


def test_author():
    print("\n-- app dirs (without optional '_app_author')")
    dirs = app_path.AppPath(_app_name)
    for prop in props:
        print("%s: %s" % (prop, getattr(dirs, prop)))


def test_no_author():
    print("\n-- app dirs (with disabled '_app_author')")
    dirs = app_path.AppPath(_app_name, app_author=False)
    for prop in props:
        print("%s: %s" % (prop, getattr(dirs, prop)))
