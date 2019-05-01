#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "cnheider"
__doc__ = """
Created on 27/04/2019

@author: cnheider
"""


def action_callback(nid, action, notifications_registry):
    nid, action = int(nid), str(action)
    try:
        n = notifications_registry[nid]
    except KeyError:
        # this message was created through some other program.
        return
    n.action_callback(action, notifications_registry)


def closed_callback(nid, reason, notifications_registry):
    nid, reason = int(nid), int(reason)
    try:
        n = notifications_registry[nid]
    except KeyError:
        # this message was created through some other program.
        return
    n.closed_callback(n)
    del notifications_registry[nid]


def no_op(*args):
    """No-op function for callbacks.
  """
    pass
