"""Installation information and management"""


class _bm:
    from sys import platform, version as pyv
    from os.path import exists, expanduser
    from typing import Union, List

    split: str = '\\' if "win" in platform.lower() and platform.lower() != "darwin" else '/'
    home:  str = expanduser('~')

    if not home:
        home: str = split.join(__file__.split(split)[:3])

        if not home:
            home: str = ""

    class info:
        from sys import platform as platform__

        split__: str = '\\' if "win" in platform__.lower() and platform__.lower() != "darwin" else '/'

        author:              str = "feetbots"
        author_email:        str = "pheetbots@gmail.com"
        maintainer:          str = "feetbots"
        maintainer_email:    str = "pheetbots@gmail.com"
        version:             str = "1.8.0"
        released:            str = "14/6/2024"
        release_description: str = "THE biggest update yet"
        description:         str = "A lightweight python utility package built on the standard library"
        homepage:            str = "https://github.com/feetbots/tooltils"
        homepage_issues:     str = "https://github.com/feetbots/tooltils/issues"
        location:            str = split__.join(__file__.split(split__)[:-1]) + split__
        releases:           list = ["1.0.0-beta", "1.1.0", "1.2.0", "1.3.0", "1.4.0", 
                                    "1.4.1", "1.4.2", "1.4.3", "1.4.4", "1.4.4-1", 
                                    "1.5.0", "1.5.1", "1.5.2", "1.5.3", "1.6.0", 
                                    "1.7.0", "1.7.1", "1.7.2", "1.8.0"]

    baseDir: str = home + split + '.tooltils' + split
    pyDir:   str = baseDir + 'py' + pyv.split('(')[0].strip() + split
    tDir:    str = pyDir + 'ts' + info.version + split

    modules: tuple = ("TOOLTILS", "TOOLTILS", "ERRORS", "INFO", 
                      "OS", "REQUESTS", "REQUESTS.URLLIB")

    levels:  dict = {10: "DEBUG", 20: "INFO", 30: "WARNING", 40: "ERROR", 50: "CRITICAL"}
    sLevels: dict = dict([(v, k) for k, v in levels.items()])

    _loggerInfo = {
        "tooltils": [False, False, False, False, False], 
        "tooltils.errors": [False, False, False, False, False],
        "tooltils.info": [False, False, False, False, False],
        "tooltils.os": [False, False, False, False, False],
        "tooltils.requests": [False, False, False, False, False],
        "tooltils.requests.urllib": [False, False, False, False, False]
    }

    defaultLogFormat: str = "[\u001b[3;1m%(time)s\u001b[0m] [\u001b[5;1m%(module)s.%(caller)s\u001b[0m | " + \
                            "\u001b[3;1m%(level)s\u001b[0m%(rID)s]: %(message)s"

    defaultCache:  dict = {
        "universal": {
            "configMethodValues": {}
        },
        "main": {},
        "info": {
            "licenseContent": None,
            "readmeContent": None
        },
        "os": {},
        "requests": {
            "verifiableTimesChecked": 0,
            "verifiableNetworkList": {},
            "connectedTimesChecked": 0,
            "connectedNetworkList": {}
        },
        "errors": {}
    }
    defaultConfig: dict = {
        "universal": {
            "loggingFormat": defaultLogFormat,
            "loggingTimeFormat": "%H:%M:%S",
            "disableOnlineContentFetch": False,
            "disableConfigMethodValues": True,
            "configMethodCheck": 20,
            "lazyLoading": True
        },
        "main": {},
        "info": {},
        "os": {},
        "requests": {
            "defaultVerificationMethod": True,
            "verifiableCachingCheck": 20,
            "connectedCachingCheck": 20,
    #       "connectionCaching": True,
            "verifiableCaching": True,
            "connectedCaching": False,
            "redirectLimit": 20
        },
        "errors": {}
    }

    openCache          = None
    openConfig         = None
    actualConfig: dict = {}
    
    def closeFiles() -> None:
        _bm.openCache.close()
        _bm.openConfig.close()

        _bm.openCache  = False
        _bm.openConfig = False

def _logger(module: str):
    return _loggerClass(module)

class _loggerClass:
    def __init__(self, module: str): 
        global _loggerInfo

        try:
            _loggerInfo
        except NameError:
            _loggerInfo = _bm._loggerInfo

        self.module: str = "tooltils" + ('.' if module else "") + module

    def log(self, level: int, message: str, caller: str, rID: int):
        from datetime import datetime
        from time import time

        global _loggerInfo

        format: str = _loadConfig("universal")['loggingFormat']
        timeFormat: str = _loadConfig("universal")['loggingTimeFormat']

        message = format % {"time": datetime.fromtimestamp(time()).strftime(timeFormat),
                            "module": self.module, "caller": caller, "level": _bm.levels[level],
                            "rID": f" | C{rID}" if rID != -1 else "", "message": message}

        # mysterious code go!!! job security forever!!!
        for k, v in _loggerInfo.items():
            if locals().get('i', 0) == None:
                break

            for i, it in enumerate(v):
                if it and (i * 10) == level and k == self.module:
                    print(message)

                    i = None

                    break

    def debug(self, message: str, caller: str, rID: int=-1):
        self.log(10, message, caller, rID)

    def info(self, message: str, caller: str, rID: int=-1):
        self.log(20, message, caller, rID)

    def warning(self, message: str, caller: str, rID: int=-1):
        self.log(30, message, caller, rID)

    def error(self, message: str, caller: str, rID: int=-1):
        self.log(40, message, caller, rID)

    def critical(self, message: str, caller: str, rID: int=-1):
        self.log(50, message, caller, rID)


author:              str = _bm.info.author
"""The current owner of tooltils"""
author_email:        str = _bm.info.author_email
"""The email of the current owner of tooltils"""
maintainer:          str = _bm.info.maintainer
"""The current sustainer of tooltils"""
maintainer_email:    str = _bm.info.maintainer_email
"""The email of the current sustainer of tooltils"""
version:             str = _bm.info.version
"""The current installation version"""
released:            str = _bm.info.released
"""The release date of the current version"""
release_description: str = _bm.info.release_description
"""The description of the current release version"""
description:         str = _bm.info.description
"""The short description of tooltils"""
homepage:            str = _bm.info.homepage
"""The current home website of tooltils"""
homepage_issues:     str = _bm.info.homepage_issues
"""The current issues directory of the home website of tooltils"""
location:            str = _bm.info.location
"""The path of the current installation of tooltils"""
releases:  _bm.List[str] = _bm.info.releases
"""All current versions of tooltils"""


def _checkLoaded():
    if not _bm.openCache and not _bm.openConfig:
        raise FileExistsError("The tooltils data files have been deleted, please rerun your program " +
                              "to create them again")

def _getCache():
    if not _bm.openCache:
        _bm.openCache = open(_bm.tDir + "cache.json", "r+")

    return _bm.openCache

def _getConfig():
    from json import load

    if _bm.openConfig:
        return _bm.openConfig

    _f  = _bm.openConfig = open(_bm.tDir + "config.json", "r+")
    _f2 = _getCache()

    # locate and config method values and convert them

    config: dict = load(_f)
    cache:  dict = load(_f2)
    funcs:  dict = cache["universal"]["configMethodValues"]

    _bm.actualConfig.update(config)

    _f.seek(0)
    _f2.seek(0)

    if config["universal"]["disableConfigMethodValues"]:
        return _f
 
    for k, v in config.items():
        for k2, v2 in v.items():
            if type(v2) is str and "$f " in v2:
                try:
                    statement: str = v2.split(' ')[1].split('(')
                    funcName:  str = statement[0]
                    args:      str = '[' + statement[1][:-1] + ']'

                    if funcName in funcs.keys() and funcs[funcName][1] < config["universal"]["configMethodCheck"]:
                        funcs[funcName] = (funcs[funcName][0], funcs[funcName][1] + 1)
                        _editCache("universal", {"configMethodValues": funcs})
                    else:
                        value = _bm.run(funcName, args)

                        funcs.update({funcName: (value, 1)})
                        _editCache("universal", {"configMethodValues": funcs})
                except Exception:
                    value = None
            else:
                value = v2

            _bm.actualConfig[k][k2] = value
    
    return _f

def _loadCache(module: str="") -> dict:
    from json import load

    if "logger" in dir(_bm):
        _checkLoaded()

    _f         = _getCache()
    data: dict = load(_f)

    _f.seek(0)

    if module == "":
        return data
    else:
        return data[module]

def _editCache(module: str, option: dict, subclass: str="") -> None:
    from json import load, dumps

    _checkLoaded()

    _f         = _getCache()
    data: dict = load(_f)

    if subclass:
        data[module][subclass].update(option)
    else:
        data[module].update(option)

    _f.seek(0)
    _f.truncate()
    _f.write(dumps(data, indent=4))
    _f.seek(0)

def _deleteCacheKey(module: str, key: str, subclass: str="") -> None:
    from json import load, dumps

    _checkLoaded()

    _f = _getCache()
    data = load(_f)

    if subclass:
        keys = data[module][subclass].keys()
    else:
        keys = data[module].keys()

    for i in list(keys):
        if key == i:
            if subclass:
                data[module][subclass].pop(i)
            else:
                data[module].pop(i)

    _f.seek(0)
    _f.truncate()
    _f.write(dumps(data, indent=4))
    _f.seek(0)

def _loadConfig(module: str="") -> dict:
    # make sure _getConfig() is called otherwise _bm.actualConfig will not be set

    if "logger" in dir(_bm):
        _checkLoaded()

    _getConfig()

    if module == "":
        return _bm.actualConfig
    else:
        return _bm.actualConfig[module]

def clearCache(module: str=None) -> None:
    """
    Clear the file cache of tooltils or a specific module within
    
    :param module: The name of the tooltils module to clear the cache for
    """

    from json import load, dumps

    _checkLoaded()

    module: str = str(module).lower()
    _f          = _getCache()
    data:  dict = load(_f)

    if module == "none":
        data: dict = _bm.defaultCache
    else:
        try:
            data.update(_bm.defaultCache[module])
        except KeyError:
            raise FileNotFoundError("Cache module not found")

    _f.seek(0)
    _f.truncate(0)
    _f.write(dumps(data, indent=4))
    _f.seek(0)

    _bm.logger.debug("User cache was cleared", "clearCache()")

def clearConfig(module: str=None) -> None:
    """
    Revert the config of tooltils or a specific module within

    :param module: The name of the tooltils module to clear the config for
    """

    from json import load, dumps

    _checkLoaded()

    module: str = str(module).lower()
    _f          = _getConfig()
    data:  dict = load(_f)

    if module == "none":
        data: dict = _bm.defaultConfig
    else:
        try:
            data.update(_bm.defaultConfig[module])
        except KeyError:
            raise FileNotFoundError("Config module not found")

    _f.seek(0)
    _f.truncate(0)
    _f.write(dumps(data, indent=4))
    _f.seek(0)

    _bm.logger.debug("User config was reset", "clearConfig()")

def clearData() -> None:
    """Clear the cache and config of tooltils"""

    from json import dumps

    _checkLoaded()

    _f  = _getCache()
    _f2 = _getConfig()

    _f.truncate(0)
    _f.write(dumps(_bm.defaultCache, indent=4))
    _f.seek(0)

    _f2.truncate(0)
    _f2.write(dumps(_bm.defaultConfig, indent=4))
    _f2.seek(0)

    _bm.logger.debug("User cache and config was cleared and reset", "clearData()")

def deleteData(pyv: str=None, tsv: str=None) -> None:
    """
    Delete the stored data for a specific python version of tooltils, a specific tooltils version, 
    a combination of these or the entire tooltils storage directory
    
    :param pyv: The python version to delete all the data for
    :param tsv: The tooltils version to delete all the data for
    """

    _checkLoaded()

    from shutil import rmtree
    from os import listdir

    if type(pyv) is not str and pyv:
        raise TypeError("Pyv must be a valid 'str' instance")
    if type(tsv) is not str and tsv:
        raise TypeError("Tsv must be a valid 'str' instance")

    if not _bm.exists(_bm.baseDir):
        raise FileNotFoundError("The tooltils storage directory does not exist")
    
    if not _bm.exists(_bm.tDir):
        raise FileNotFoundError("The current tooltils version storage directory does not exist")

    if not pyv and not tsv:
        _bm.closeFiles()

        rmtree(_bm.baseDir)

        logMsg: str = "User storage directory was deleted"
    elif pyv and tsv:
        if not ("py" + pyv) in listdir(_bm.baseDir):
            raise FileNotFoundError("Python version not found in tooltils data files")
        
        if not ("ts" + tsv) in listdir(_bm.pyDir):
            raise FileNotFoundError("Tooltils version not found in tooltils data files")

        _bm.closeFiles()

        rmtree(_bm.tDir)

        logMsg: str = f"User storage data for Python version {pyv} and Tooltils version {tsv} was deleted"
    elif pyv:
        if not ("py" + pyv) in listdir(_bm.baseDir):
            raise FileNotFoundError("Python version not found in tooltils data files")

        _bm.closeFiles()

        rmtree(_bm.pyDir)

        logMsg: str = f"User storage data for Python version {pyv} was deleted"
    elif tsv:
        for i in [i for i in listdir(_bm.baseDir) if "temp" not in i and
                                                     ".DS_Store" not in i]:
            for i2 in listdir(_bm.baseDir + i):
                try:
                    if ("ts" + tsv) in i2:
                        if _bm.openCache:
                            _bm.closeFiles()
                        
                        rmtree(_bm.baseDir + i + _bm.split + i2)
                except FileNotFoundError:
                    continue
                
        if _bm.openCache:
            raise FileNotFoundError("Tooltils version not found in tooltils data files")

        logMsg: str = f"User storage data for Tooltils version {tsv} was deleted"
    
    try:
        _checkLoaded()

        _bm.logger.debug(logMsg, "deleteData()")
    except FileExistsError:
        pass

class logger:
    """Initialise a specialised logger for Tooltils"""

    def __init__(self, 
                 module: str="ALL", 
                 level: _bm.Union[str, int]="ALL",
                 level2: _bm.Union[str, int]="ALL"
                 ) -> None:
        """
        Initialise a specialised logger for Tooltils

        :param module: The tooltil module to enable the logging for
        :param level: The starting level of the logging level range
        :param level2: The ending level of the logging level range
        """

        if type(level) is str: 
            level = level.upper()

        if type(level2) is str: 
            level2 = level2.upper()
        
        if type(module) is not str:
            raise TypeError("Module must be a valid 'str' instance")
        elif module.upper() not in ("", "ALL") + _bm.modules:
            raise ValueError(f"Unknown module '{module}'")
        else:
            if module.upper() == "ALL":
                self.module: str = "all"
            elif module.upper() == "" or module.upper() == "MAIN" or module.upper() == "TOOLTILS":
                self.module: str = "tooltils"
            else:
                # make sure 'tooltils.' is only in the string once
                self.module: str = "tooltils." + module.lower().replace("tooltils.", "")

        for i in (("level", level), ("level2", level2)):
            if i[1] not in ("ALL", "DEBUG", "INFO", "WARN", "ERROR", "CRITICAL", 10, 20, 30, 40, 50):
                raise ValueError(f"Invalid {i[0]} '{i[1]}'")
            else:
                if i[0] == "level":
                    if level == "ALL":
                        level: int = 10
                    elif type(level) is str:
                        level: int = _bm.sLevels[level]
                else:
                    if level2 == "ALL":
                        level2: int = 50
                    elif type(level2) is str:
                        level2: int = _bm.sLevels[level2]

        self.level:             int = int(level)
        self.level2:            int = int(level2)
        self.enabled:          bool = bool(False)
        self._levelRange: list[int] = list(range(int(self.level / 10) - 1, int(self.level2 / 10)))

        self.enable()

        _bm.logger.debug(f"Initiated logger for <{self.module}> with range " + 
                         f"{_bm.levels[self.level]} -> {_bm.levels[self.level2]}", 
                         "logger()")

    def __str__(self) -> str:
        return f"<Logger instance: [{'on' if self.enabled else 'off'}] -> [{self.module}]>"

    def __repr__(self) -> str:
        return self.__str__()
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type == None:
            self.disable()

            return True

    def enable(self) -> None:
        """Enable the logger instance"""

        if self.enabled:
            raise ValueError('The logger is already enabled')
        else:
            global _loggerInfo

            self.enabled: bool = bool(True)

            if self.module == "all":
                for i in _loggerInfo.keys():
                    for i2 in self._levelRange:
                        _loggerInfo[i][i2] = True
            else:
                for i in self._levelRange:
                    _loggerInfo[self.module][i] = True

    def disable(self) -> None:
        """Disable the logger instance"""

        if not self.enabled:
            raise ValueError('The logger is already disabled')
        else:
            global _loggerInfo

            self.enabled: bool = bool(False)

            if self.module == "all":
                for i in _loggerInfo.keys():
                    for i2 in self._levelRange:
                        _loggerInfo[i][i2] = False
            else:
                for i in self._levelRange:
                    _loggerInfo[self.module][i] = False


# necessary startup code

_cache = _config = True

if not _bm.exists(_bm.baseDir):
    from os import mkdir as _mkdir

    _mkdir(_bm.baseDir)
    _mkdir(_bm.baseDir + "temp")

if not _bm.exists(_bm.pyDir):
    from os import mkdir as _mkdir

    _mkdir(_bm.pyDir)

if not _bm.exists(_bm.tDir):
    from os import mkdir as _mkdir

    _mkdir(_bm.tDir)

if _bm.exists(_bm.tDir + "cache.json"):
    _cache: bool = False
if _bm.exists(_bm.tDir + "config.json"):
    _config: bool = False

if _cache:
    from json import dumps as _dumps

    with open(_bm.tDir + "cache.json", "a+") as _f:
        _f.write(_dumps(_bm.defaultCache, indent=4))

if _config:
    from json import dumps as _dumps

    with open(_bm.tDir + "config.json", "a+") as _f:
        _f.write(_dumps(_bm.defaultConfig, indent=4))

_data = _loadConfig()

for _i in (("universal", "configMethodCheck", int), ("requests", "verifiableCachingCheck", int), 
           ("requests", "connectedCachingCheck", int), ("requests", "redirectLimit", int),
           ("universal", "loggingFormat", str), ("universal", "loggingTimeFormat", str)):
    if type(_data[_i[0]][_i[1]]) is not _i[2]:
        raise RuntimeError(f"Config value {_i[0]}.{_i[1]} is not an instance of " + 
                           f"type '{_i[2].__name__}', please change it or " + 
                           "reset the config")

# try to get license and long_description

_check:              bool = not _data["universal"]["disableOnlineContentFetch"]
license, long_description = 0, 0

# check if it is already cached
if _check and _loadCache("info")["licenseContent"] == None:
    from ssl import create_default_context as _create_default_context, CERT_NONE as _CERT_NONE
    from http.client import HTTPSConnection as _HTTPSConnection
    from zipfile import ZipFile as _ZipFile

    try:
        # make testing easier
        verOverride = releases[-2] if len(version.split('.')) > 3 else version

        ctx = _create_default_context()

        ctx.check_hostname = False
        ctx.verify_mode    = _CERT_NONE
        ctx.set_ciphers("RSA")

        _req = _HTTPSConnection("codeload.github.com", context=ctx)
        _req.request("GET", "/feetbots/tooltils/zip/refs/tags/{}".format(
                     'v' + verOverride), body=None,
                     headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:10.0) " + 
                              "Gecko/20100101 Firefox/10.0"})

        with open(_bm.baseDir + f"temp{_bm.split}files.zip", "wb+") as _f:
            _f.write(_req.getresponse().read())
        
        with _ZipFile(_bm.baseDir + f"temp{_bm.split}files.zip") as _f:
            _f.extractall(_bm.baseDir + f"temp{_bm.split}files")
        
        with open(_bm.baseDir + f"temp{_bm.split}files{_bm.split}tooltils-{verOverride}{_bm.split}LICENSE") as _f, \
             open(_bm.baseDir + f"temp{_bm.split}files{_bm.split}tooltils-{verOverride}{_bm.split}README.md") as _f2:
            license, long_description = _f.read(), _f2.read()

        _editCache("info", {"licenseContent": license, 
                            "readmeContent": long_description})
    except Exception:
        pass
    finally:
        from shutil import rmtree as _rmtree
        from os import remove as _remove

        try:
            _remove(_bm.baseDir + f"temp{_bm.split}files.zip")
            _rmtree(_bm.baseDir + f"temp{_bm.split}files")
        except Exception:
            pass

        _req.close()
else:
    license          = _loadCache("info")["licenseContent"]
    long_description = _loadCache("info")["readmeContent"]

if not license and not long_description:
    _editCache("info", {"licenseContent": 0, "readmeContent": 0})

def _getLines():
    from os import listdir

    def getFiles(dir: str) -> list:
        fileList: list = []

        for i in listdir(location + dir):
            fileList.append(location + ("" if not dir else dir + _bm.split) + i)
        
        return fileList

    lines:  int = 0
    files: list = getFiles("") + getFiles("requests")

    for i in files:
        for x in ("README.md", "API.md", "CHANGELOG.md", "LICENSE", ".DS_Store",
                  "__pycache__", ".git"):
            if x in i:
                files.remove(i)

    for i in files:
        try:
            with open(i) as _f:
                lines += len(_f.readlines())
        except (IsADirectoryError, UnicodeDecodeError, PermissionError):
            # PermissionError catches exceptions that are raised when we try to open
            # a directory... for some reason... Windows moment!
            continue

    return lines

license:          str = str(license) if isinstance(license, str) else None
"""The content of the currently used license"""
long_description: str = str(long_description) if isinstance(long_description, str) else None
"""The long description of tooltils"""
lines:            int = int(_getLines())
"""The amount of lines of code in this tooltils installation"""

if _bm.exists(_bm.tDir + "config.json"):
    from json import load as _load

    with open(_bm.tDir + "config.json") as _f:
        if not _load(_f)["universal"]["lazyLoading"]:
            import ssl as _ssl
            import http.client as _httpclient
            import socket as _socket
            import subprocess as _subprocess
            import time as _time
            import urllib as _urllib
            import datetime as _datetime
            import gzip as _gzip
            import shutil as _shutil
            import os as _os
            import tarfile as _tarfile
            import base64 as _base64


for _i in ["ssl", "httpclient", "socket", "subprocess", "time", "urllib", "datetime",
           "gzip", "shutil", "os", "tarfile", "base64", "getLines", "cache", 
           "config", "check", "create_default_context", "CERT_NONE", "ctx",
            "HTTPSConnection", "ZipFile", "req", "date", "mkdir", "remove", 
            "rmtree", "load", "f", "f2", "i"]:
    try:
        del locals()['_' + _i]
    except KeyError:
        continue

# done down here because the check for config types is done after
# the logger instance would've been created
_bm.logger = _logger("info")
