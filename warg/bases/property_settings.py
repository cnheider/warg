#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 17/03/2020
           """
__all__ = ["PropertySettings"]

from collections.abc import Mapping
from typing import Dict

from warg import NOD


class PropertySettings(
    # Mapping
):
    """ """

    # def __getitem__(self, k):
    #  return  self.__getattribute__(k)

    # def __len__(self) -> int:
    #  return len(self.__crystallise__())

    # raise_exception_on_none = False

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__setattr__(k, v)

        for setting in dir(self):
            if not setting.startswith("_"):
                try:
                    self.__getattr__(setting)
                except KeyError:
                    self.__setattr__(setting, None)

    def __clear__(self):
        for setting in dir(self):
            if not setting.startswith("_"):
                self.__setattr__(setting, None)

    def __setattr__(self, key, value):
        assert not key.startswith("_"), f"{key} is not allowed"
        # self.__getattr__(key)
        super().__setattr__(key, value)

    def __getattr__(self, item):
        assert not item.startswith("_"), f"{item} is not allowed"
        try:
            val = super().__getattribute__(item)
            # if PropertySettings.raise_exception_on_none and not val:
            #  raise ValueError(f'Property {item} is {val}')
            return val
        except AttributeError as a:
            a = type(a)(str(a) + f", available settings {self}")
            raise a

    def __iter_keys__(self):
        for setting in dir(self):
            if not setting.startswith("_"):
                yield setting

    def __str__(self) -> str:
        return self.__repr__()

    def __contains__(self, item):
        return hasattr(self, item)

    # def __dir__(self) -> Iterable[str]:
    #  return self.__crystallise__().keys()

    def __repr__(self) -> str:
        settings_dict = {}
        for setting in dir(self):
            if not setting.startswith("_"):
                try:
                    settings_dict[setting] = self.__getattr__(setting)
                except KeyError:
                    settings_dict[setting] = None

        return str(settings_dict)

    def __iter__(self):
        available_settings = []
        for setting in dir(self):
            if not setting.startswith("_"):
                available_settings.append(setting)

        return iter(available_settings)

    def __getitem__(self, item):
        return self.__getattr__(item)

    def __to_dict__(self) -> dict:
        return self.__crystallise__().as_dict()

    def __crystallise__(self) -> NOD:
        return NOD({k: getattr(self, k) for k in self})

    def __from_mapping__(self, mapping: Mapping) -> None:
        for k, v in mapping.items():
            setattr(self, k, v)

    def __from_dict__(self, dict: Dict) -> None:
        self.__from_mapping__(dict)


if __name__ == "__main__":
    a = PropertySettings()

    print({**a.__crystallise__()})
    assert not "h" in a
