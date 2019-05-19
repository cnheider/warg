#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pathlib

__author__ = "cnheider"
__doc__ = "Application data directories extension for pathlib"

import os
from warg.app_path_utilities import get_win_folder, SYSTEM


class AppPath(object):
    r"""
AppPath class for easing cross platform access to proper app data directories
"""

    def __init__(
        self,
        app_name=None,
        app_author=None,
        app_version=None,
        roaming=False,
        multi_path=False,
        ensure_existence=True,
    ):
        self._app_name = app_name
        self._app_author = app_author
        self._app_version = app_version
        self._roaming = roaming
        self._multi_path = multi_path
        self._ensure_existence = ensure_existence

    @staticmethod
    def ensure_existence(enabled, out):
        if enabled:
            if not out.exists():
                out.mkdir(parents=True)

    @property
    def user_data(self) -> pathlib.Path:
        out = self.user_data_path(
            self._app_name, self._app_author, version=self._app_version, roaming=self._roaming
        )

        self.ensure_existence(self._ensure_existence, out)
        return out

    @property
    def site_data(self) -> pathlib.Path:
        out = self.site_data_path(
            self._app_name, self._app_author, version=self._app_version, multi_path=self._multi_path
        )

        self.ensure_existence(self._ensure_existence, out)

        return out

    @property
    def user_config(self) -> pathlib.Path:
        out = self.user_config_path(
            self._app_name, self._app_author, version=self._app_version, roaming=self._roaming
        )
        self.ensure_existence(self._ensure_existence, out)
        return out

    @property
    def site_config(self) -> pathlib.Path:
        out = self.site_config_path(
            self._app_name, self._app_author, version=self._app_version, multi_path=self._multi_path
        )
        self.ensure_existence(self._ensure_existence, out)
        return out

    @property
    def user_cache(self) -> pathlib.Path:
        out = self.user_cache_path(self._app_name, self._app_author, version=self._app_version)
        self.ensure_existence(self._ensure_existence, out)
        return out

    @property
    def user_state(self) -> pathlib.Path:
        out = self.user_state_path(self._app_name, self._app_author, version=self._app_version)
        self.ensure_existence(self._ensure_existence, out)
        return out

    @property
    def user_log(self) -> pathlib.Path:
        out = self.user_log_path(self._app_name, self._app_author, version=self._app_version)
        self.ensure_existence(self._ensure_existence, out)
        return out

    @staticmethod
    def user_data_path(app_name=None, app_author=None, version=None, roaming=False) -> pathlib.Path:
        r"""Return full path to the user-specific data dir for this application.

    "app_name" is the name of application.
        If None, just the system directory is returned.
    "app_author" (only used on Windows) is the name of the
        app_author or distributing body for this application. Typically
        it is the owning company name. This falls back to app_name. You may
        pass False to disable it.
    "version" is an optional version path element to append to the
        path. You might want to use this if you want multiple versions
        of your app to be able to run independently. If used, this
        would typically be "<major>.<minor>".
        Only applied when app_name is present.
    "roaming" (boolean, default False) can be set True to use the Windows
        roaming appdata directory. That means that for users on a Windows
        network setup for roaming profiles, this user data will be
        sync'd on login. See
        <http://technet.microsoft.com/en-us/library/cc766489(WS.10).aspx>
        for a discussion of issues.


  Notes:
  - MSDN on where to store app data files:
  http://support.microsoft.com/default.aspx?scid=kb;en-us;310294#XSLTH3194121123120121120120
  - Mac OS X: http://developer.apple.com/documentation/MacOSX/Conceptual/BPFileSystem/index.html
  - XDG spec for Un*x: https://standards.freedesktop.org/basedir-spec/basedir-spec-latest.html

Typical user data directories are:
    Mac OS X:               ~/Library/Application Support/<AppName>
    Unix:                   ~/.local/share/<AppName>    # or in $XDG_DATA_HOME, if defined
    Win XP (not roaming):   C:\Documents and Settings\<username>\Application Data\<AppAuthor>\<AppName>
    Win XP (roaming):       C:\Documents and Settings\<username>\Local Settings\Application
    Data\<AppAuthor>\<AppName>
    Win 7  (not roaming):   C:\Users\<username>\AppData\Local\<AppAuthor>\<AppName>
    Win 7  (roaming):       C:\Users\<username>\AppData\Roaming\<AppAuthor>\<AppName>

For Unix, we follow the XDG spec and support $XDG_DATA_HOME.
That means, by default "~/.local/share/<AppName>".
"""

        if SYSTEM == "win32":
            if app_author is None:
                app_author = app_name
            const = roaming and "CSIDL_APPDATA" or "CSIDL_LOCAL_APPDATA"
            path = pathlib.Path(os.path.normpath(get_win_folder(const)))
            if app_name:
                if app_author is not False:
                    path = path / app_author / app_name
                else:
                    path = path / app_name
        elif SYSTEM == "darwin":
            path = pathlib.Path(os.path.expanduser("~/Library/Application Support/"))
            if app_name:
                path = path / app_name
        else:
            path = pathlib.Path(os.getenv("XDG_DATA_HOME", os.path.expanduser("~/.local/share")))
            if app_name:
                path = path / app_name
        if app_name and version:
            path = path / version
        return path

    @staticmethod
    def site_data_path(app_name=None, app_author=None, version=None, multi_path=False) -> pathlib.Path:
        r"""Return full path to the user-shared data dir for this application.

    "app_name" is the name of application.
        If None, just the system directory is returned.
    "app_author" (only used on Windows) is the name of the
        app_author or distributing body for this application. Typically
        it is the owning company name. This falls back to app_name. You may
        pass False to disable it.
    "version" is an optional version path element to append to the
        path. You might want to use this if you want multiple versions
        of your app to be able to run independently. If used, this
        would typically be "<major>.<minor>".
        Only applied when app_name is present.
    "multi_path" is an optional parameter only applicable to *nix
        which indicates that the entire list of data dirs should be
        returned. By default, the first item from XDG_DATA_DIRS is
        returned, or '/usr/local/share/<AppName>',
        if XDG_DATA_DIRS is not set

Typical site data directories are:
    Mac OS X:   /Library/Application Support/<AppName>
    Unix:       /usr/local/share/<AppName> or /usr/share/<AppName>
    Win XP:     C:\Documents and Settings\All Users\Application Data\<AppAuthor>\<AppName>
    Vista:      (Fail! "C:\ProgramData" is a hidden *system* directory on Vista.)
    Win 7:      C:\ProgramData\<AppAuthor>\<AppName>   # Hidden, but writeable on Win 7.

For Unix, this is using the $XDG_DATA_DIRS[0] default.

WARNING: Do not use this on Windows. See the Vista-Fail note above for why.
"""
        if SYSTEM == "win32":
            if app_author is None:
                app_author = app_name
            path = pathlib.Path(os.path.normpath(get_win_folder("CSIDL_COMMON_APPDATA")))
            if app_name:
                if app_author is not False:
                    path = path / app_author / app_name
                else:
                    path = path / app_name
        elif SYSTEM == "darwin":
            path = pathlib.Path(os.path.expanduser("/Library/Application Support"))
            if app_name:
                path = path / app_name
        else:
            # XDG default for $XDG_DATA_DIRS
            # only first, if multipath is False
            path = os.getenv("XDG_DATA_DIRS", os.pathsep.join(["/usr/local/share", "/usr/share"]))
            path_list = [os.path.expanduser(x.rstrip(os.sep)) for x in path.split(os.pathsep)]
            if app_name:
                if version:
                    app_name = os.path.join(app_name, version)
                path_list = [os.sep.join([x, app_name]) for x in path_list]

            path_list = [pathlib.Path(a) for a in path_list]

            if multi_path:
                path = os.pathsep.join(path_list)
            else:
                path = path_list[0]
            return path

        if app_name and version:
            path = path / version
        return path

    @staticmethod
    def user_config_path(app_name=None, app_author=None, version=None, roaming=False) -> pathlib.Path:
        r"""Return full path to the user-specific config dir for this application.

    "app_name" is the name of application.
        If None, just the system directory is returned.
    "app_author" (only used on Windows) is the name of the
        app_author or distributing body for this application. Typically
        it is the owning company name. This falls back to app_name. You may
        pass False to disable it.
    "version" is an optional version path element to append to the
        path. You might want to use this if you want multiple versions
        of your app to be able to run independently. If used, this
        would typically be "<major>.<minor>".
        Only applied when app_name is present.
    "roaming" (boolean, default False) can be set True to use the Windows
        roaming appdata directory. That means that for users on a Windows
        network setup for roaming profiles, this user data will be
        sync'd on login. See
        <http://technet.microsoft.com/en-us/library/cc766489(WS.10).aspx>
        for a discussion of issues.

Typical user config directories are:
    Mac OS X:               ~/Library/Preferences/<AppName>
    Unix:                   ~/.config/<AppName>     # or in $XDG_CONFIG_HOME, if defined
    Win *:                  same as user_data_dir

For Unix, we follow the XDG spec and support $XDG_CONFIG_HOME.
That means, by default "~/.config/<AppName>".
"""
        if SYSTEM == "win32":
            path = AppPath.user_data_path(app_name, app_author, None, roaming)
        elif SYSTEM == "darwin":
            path = pathlib.Path(os.path.expanduser("~/Library/Preferences/"))
            if app_name:
                path = path / app_name
        else:
            path = pathlib.Path(os.getenv("XDG_CONFIG_HOME", os.path.expanduser("~/.config")))
            if app_name:
                path = path / app_name
        if app_name and version:
            path = path / version
        return path

    @staticmethod
    def site_config_path(app_name=None, app_author=None, version=None, multi_path=False) -> pathlib.Path:
        r"""Return full path to the user-shared data dir for this application.

    "app_name" is the name of application.
        If None, just the system directory is returned.
    "app_author" (only used on Windows) is the name of the
        app_author or distributing body for this application. Typically
        it is the owning company name. This falls back to appname. You may
        pass False to disable it.
    "version" is an optional version path element to append to the
        path. You might want to use this if you want multiple versions
        of your app to be able to run independently. If used, this
        would typically be "<major>.<minor>".
        Only applied when app_name is present.
    "multi_path" is an optional parameter only applicable to *nix
        which indicates that the entire list of config dirs should be
        returned. By default, the first item from XDG_CONFIG_DIRS is
        returned, or '/etc/xdg/<AppName>', if XDG_CONFIG_DIRS is not set

Typical site config directories are:
    Mac OS X:   same as site_data_dir
    Unix:       /etc/xdg/<AppName> or $XDG_CONFIG_DIRS[i]/<AppName> for each value in
                $XDG_CONFIG_DIRS
    Win *:      same as site_data_dir
    Vista:      (Fail! "C:\ProgramData" is a hidden *system* directory on Vista.)

For Unix, this is using the $XDG_CONFIG_DIRS[0] default, if multipath=False

WARNING: Do not use this on Windows. See the Vista-Fail note above for why.
"""
        if SYSTEM == "win32":
            path = AppPath.site_data_path(app_name, app_author)
            if app_name and version:
                path = path / version
        elif SYSTEM == "darwin":
            path = pathlib.Path(os.path.expanduser("/Library/Preferences"))
            if app_name:
                path = path / app_name
        else:
            # XDG default for $XDG_CONFIG_DIRS
            # only first, if multi_path is False
            path = os.getenv("XDG_CONFIG_DIRS", "/etc/xdg")
            path_list = [os.path.expanduser(x.rstrip(os.sep)) for x in path.split(os.pathsep)]
            if app_name:
                if version:
                    app_name = os.path.join(app_name, version)
                path_list = [os.sep.join([x, app_name]) for x in path_list]

            path_list = [pathlib.Path(a) for a in path_list]

            if multi_path:
                path = os.pathsep.join(path_list)
            else:
                path = path_list[0]
        return path

    @staticmethod
    def user_cache_path(app_name=None, app_author=None, version=None, opinion=True) -> pathlib.Path:
        r"""Return full path to the user-specific cache dir for this application.

    "appname" is the name of application.
        If None, just the system directory is returned.
    "appauthor" (only used on Windows) is the name of the
        appauthor or distributing body for this application. Typically
        it is the owning company name. This falls back to appname. You may
        pass False to disable it.
    "version" is an optional version path element to append to the
        path. You might want to use this if you want multiple versions
        of your app to be able to run independently. If used, this
        would typically be "<major>.<minor>".
        Only applied when appname is present.
    "opinion" (boolean) can be False to disable the appending of
        "Cache" to the base app data dir for Windows. See
        discussion below.

Typical user cache directories are:
    Mac OS X:   ~/Library/Caches/<AppName>
    Unix:       ~/.cache/<AppName> (XDG default)
    Win XP:     C:\Documents and Settings\<username>\Local Settings\Application
    Data\<AppAuthor>\<AppName>\Cache
    Vista:      C:\Users\<username>\AppData\Local\<AppAuthor>\<AppName>\Cache

On Windows the only suggestion in the MSDN docs is that local settings go in
the `CSIDL_LOCAL_APPDATA` directory. This is identical to the non-roaming
app data dir (the default returned by `user_data_dir` above). Apps typically
put cache data somewhere *under* the given dir here. Some examples:
    ...\Mozilla\Firefox\Profiles\<ProfileName>\Cache
    ...\Acme\SuperApp\Cache\1.0
OPINION: This function appends "Cache" to the `CSIDL_LOCAL_APPDATA` value.
This can be disabled with the `opinion=False` option.
"""
        if SYSTEM == "win32":
            if app_author is None:
                app_author = app_name
            path = pathlib.Path(os.path.normpath(get_win_folder("CSIDL_LOCAL_APPDATA")))
            if app_name:
                if app_author is not False:
                    path = path / app_author / app_name
                else:
                    path = path / app_name
                if opinion:
                    path = path / "Cache"
        elif SYSTEM == "darwin":
            path = pathlib.Path(os.path.expanduser("~/Library/Caches"))
            if app_name:
                path = path / app_name
        else:
            path = pathlib.Path(os.getenv("XDG_CACHE_HOME", os.path.expanduser("~/.cache")))
            if app_name:
                path = path / app_name
        if app_name and version:
            path = path / version
        return path

    @staticmethod
    def user_state_path(app_name=None, app_author=None, version=None, roaming=False) -> pathlib.Path:
        r"""Return full path to the user-specific state dir for this application.

    "app_name" is the name of application.
        If None, just the system directory is returned.
    "app_author" (only used on Windows) is the name of the
        app_author or distributing body for this application. Typically
        it is the owning company name. This falls back to appname. You may
        pass False to disable it.
    "version" is an optional version path element to append to the
        path. You might want to use this if you want multiple versions
        of your app to be able to run independently. If used, this
        would typically be "<major>.<minor>".
        Only applied when app_name is present.
    "roaming" (boolean, default False) can be set True to use the Windows
        roaming appdata directory. That means that for users on a Windows
        network setup for roaming profiles, this user data will be
        sync'd on login. See
        <http://technet.microsoft.com/en-us/library/cc766489(WS.10).aspx>
        for a discussion of issues.

Typical user state directories are:
    Mac OS X:  same as user_data_dir
    Unix:      ~/.local/state/<AppName>   # or in $XDG_STATE_HOME, if defined
    Win *:     same as user_data_dir

For Unix, we follow this Debian proposal <https://wiki.debian.org/XDGBaseDirectorySpecification#state>
to extend the XDG spec and support $XDG_STATE_HOME.

That means, by default "~/.local/state/<AppName>".
"""
        if SYSTEM in ["win32", "darwin"]:
            path = AppPath.user_data_path(app_name, app_author, None, roaming)
        else:
            path = pathlib.Path(os.getenv("XDG_STATE_HOME", os.path.expanduser("~/.local/state")))
            if app_name:
                path = path / app_name
        if app_name and version:
            path = path / version
        return path

    @staticmethod
    def user_log_path(app_name=None, app_author=None, version=None, opinion=True) -> pathlib.Path:
        r"""Return full path to the user-specific log dir for this application.

    "app_name" is the name of application.
        If None, just the system directory is returned.
    "app_author" (only used on Windows) is the name of the
        app_author or distributing body for this application. Typically
        it is the owning company name. This falls back to appname. You may
        pass False to disable it.
    "version" is an optional version path element to append to the
        path. You might want to use this if you want multiple versions
        of your app to be able to run independently. If used, this
        would typically be "<major>.<minor>".
        Only applied when app_name is present.
    "opinion" (boolean) can be False to disable the appending of
        "Logs" to the base app data dir for Windows, and "log" to the
        base cache dir for Unix. See discussion below.

Typical user log directories are:
    Mac OS X:   ~/Library/Logs/<AppName>
    Unix:       ~/.cache/<AppName>/log  # or under $XDG_CACHE_HOME if defined
    Win XP:     C:\Documents and Settings\<username>\Local Settings\Application
    Data\<AppAuthor>\<AppName>\Logs
    Vista:      C:\Users\<username>\AppData\Local\<AppAuthor>\<AppName>\Logs

On Windows the only suggestion in the MSDN docs is that local settings
go in the `CSIDL_LOCAL_APPDATA` directory. (Note: I'm interested in
examples of what some windows apps use for a logs dir.)

OPINION: This function appends "Logs" to the `CSIDL_LOCAL_APPDATA`
value for Windows and appends "log" to the user cache dir for Unix.
This can be disabled with the `opinion=False` option.
"""
        if SYSTEM == "darwin":
            path = pathlib.Path.joinpath(pathlib.Path(os.path.expanduser("~/Library/Logs")), app_name)
        elif SYSTEM == "win32":
            path = AppPath.user_data_path(app_name, app_author, version)
            version = False
            if opinion:
                path = path / "Logs"
        else:
            path = AppPath.user_cache_path(app_name, app_author, version)
            version = False
            if opinion:
                path = path / "log"
        if app_name and version:
            path = path / version
        return path


if __name__ == "__main__":
    _app_name = "MyApp"
    _app_author = __author__

    props = ("user_data", "user_config", "user_cache", "user_state", "user_log", "site_data", "site_config")

    print("-- app dirs (with optional 'version')")
    dirs = AppPath(_app_name, _app_author, app_version="1.0", ensure_existence=False)
    for prop in props:
        print("%s: %s" % (prop, getattr(dirs, prop)))

    print("\n-- app dirs (without optional 'version')")
    dirs = AppPath(_app_name, _app_author, ensure_existence=False)
    for prop in props:
        print("%s: %s" % (prop, getattr(dirs, prop)))

    print("\n-- app dirs (without optional '_app_author')")
    dirs = AppPath(_app_name, ensure_existence=False)
    for prop in props:
        print("%s: %s" % (prop, getattr(dirs, prop)))

    print("\n-- app dirs (with disabled '_app_author')")
    dirs = AppPath(_app_name, app_author=False, ensure_existence=False)
    for prop in props:
        print("%s: %s" % (prop, getattr(dirs, prop)))
