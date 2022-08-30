#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "heider"
__doc__ = r"""

           Created on 8/30/22
           """

__all__ = ["has_x_server"]


import os
from warg.os.os_platform import is_nix


def windows_display_test():
    import subprocess, os

    if os.name == "nt":  # Windows
        import wmi

        try:
            wmi.WMI().computer.Win32_VideoController()[0]  # Tested on Windows 10
            return 1
        except:
            pass

    elif os.name == "posix":  # Linux
        out = subprocess.getoutput("sudo lshw -c video | grep configuration")  # Tested on CENTOS 7 and Ubuntu
        if out:
            return 1


def has_x_server() -> bool:
    """
    test if display is available, if other than linux system atm it returns true

    :return:
    :rtype:
    """
    if is_nix():
        return os.environ["DISPLAY"] != ""
    return True


if __name__ == "__main__":
    print(has_x_server())
