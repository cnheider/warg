#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 17/03/2020
           """
__all__ = ["PlaybackShell", "ConfigShell"]

import cmd
from pathlib import Path
from typing import MutableMapping, Optional

from warg import passes_kws_to, PropertySettings


class PlaybackShell(cmd.Cmd):
    """description"""

    intro = "Type help or ? to list commands.\n"
    default_file_path = Path("playback.cmd")
    file = None

    # ----- record and playback -----
    def do_record(self, file: Path) -> None:
        """Save future commands to filename:  RECORD file.cmd"""
        if not file:
            file = self.default_file_path
        self.file = open(file, "w")

    def do_playback(self, file: Path) -> None:
        """Playback commands from a file:  PLAYBACK file.cmd"""
        self.close()
        if not file:
            file = self.default_file_path
        with open(file) as f:
            self.cmdqueue.extend(f.read().splitlines())

    def precmd(self, line: str) -> str:
        """

        :param line:
        :return:
        """
        line = line.lower()
        if self.file and "playback" not in line:
            print(line, file=self.file)
        return line

    def close(self) -> None:
        """Close file"""
        if self.file:
            self.file.close()
            self.file = None

    def do_exit(self, arg) -> bool:
        """If recording, stop, close file, close window, and exit:"""
        print("Exiting")
        self.close()
        return True

    def do_close(self, arg) -> None:
        """If recording, stop, close file, close window, and exit:"""
        self.do_exit(arg)


class ConfigShell(PlaybackShell):
    """description"""

    def get_names(self):  # Override!
        """

        :return:
        :rtype:
        """
        return dir(self)

    def onecmd(self, line):  # Override!
        """

        :param line:
        :type line:
        :return:
        :rtype:
        """
        try:
            return super().onecmd(line)
        except Exception as e:
            print(e)
            return False  # don't stop

    @passes_kws_to(cmd.Cmd.__init__)
    def __init__(self, name: str = "config", **kwargs: MutableMapping):
        super().__init__(**kwargs)
        ConfigShell.prompt = f"({name}) "

    def add_property_options(self, ps: PropertySettings) -> None:
        """

        :param ps:
        :type ps:
        """
        for p in ps.__iter_keys__():
            prop = getattr(ps.__class__, p)
            if isinstance(prop, property):
                getter = lambda *e: print(prop.fget(ps))
                getter.__doc__ = prop.fget.__doc__
                setter = lambda *e: prop.fset(ps, *e)
                setter.__doc__ = prop.fset.__doc__
                if prop.fdel:
                    deleter = lambda *e: prop.fdel(ps)
                    deleter.__doc__ = prop.fdel.__doc__
                else:
                    deleter = None
                self.add_option(p, getter=getter, setter=setter, deleter=deleter)

    def add_option(
        self,
        key: str,
        *,
        getter: callable,
        setter: callable,
        deleter: Optional[callable] = None,
    ) -> None:
        """

        :param key:
        :type key:
        :param getter:
        :type getter:
        :param setter:
        :type setter:
        :param deleter:
        :type deleter:
        """
        self.add_func(f"get_{key}", getter)
        self.add_func(f"set_{key}", setter)
        if deleter:
            self.add_func(f"del_{key}", deleter)

    def add_func(self, key: str, func: callable) -> None:
        """

        :param key:
        :type key:
        :param func:
        :type func:
        """
        k = f"do_{key}"
        assert k not in self.get_names()
        self.__setattr__(k, func)


if __name__ == "__main__":

    def ujsd():
        """

        :return:
        :rtype:
        """
        global A
        global SOME
        A = 99
        SOME = 99

        class Aconfig(PropertySettings):
            @property
            def some(self):
                """
                return SOME
                :return:
                :rtype:
                """
                global SOME
                return SOME

            @some.setter
            def some(self, i):
                """
                set SOME
                :return:
                :rtype:
                """
                global SOME
                SOME = i

            @some.deleter
            def some(self):
                """
                del SOME
                :return:
                :rtype:
                """
                global SOME
                del SOME

            @property
            def other(self):
                """
                return A
                :return:
                :rtype:
                """
                global A
                return A

            @other.setter
            def other(self, i):
                """
                set A
                :return:
                :rtype:
                """
                global A
                A = i

        ac = Aconfig()

        def set_A(e):
            """

            :param e:
            :type e:
            """
            global A
            A = e

        def get_A(e):
            """

            :param e:
            :type e:
            """
            global A
            print(A)

        cs = ConfigShell()
        cs.add_option("a", getter=get_A, setter=set_A)

        cs.add_property_options(ac)

        cs.cmdloop()

    ujsd()
