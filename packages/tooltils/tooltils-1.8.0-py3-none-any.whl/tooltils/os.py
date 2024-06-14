"""Operating system specific methods, information and interaction"""


class _bm:
    from typing import NoReturn, Union, List, Dict, Tuple
    from sys import platform

    from .errors import (SubprocessExecutionError, SubprocessCodeError, 
                         SubprocessTimeoutExpired, SubprocessLookupNotFound, 
                         SubprocessPermissionError)
    from .info import _logger
    
    st = platform.lower().startswith

    if st("linux"):
        platform = dplatform = "Linux"
    elif st("win"):
        platform = dplatform = "Windows"
    elif st("cygwin"):
        platform, dplatform = "Cygwin", "Windows"
    elif st("msys"):
        platform, dplatform = "MSYS2", "Windows"
    elif st("darwin"):
        platform, dplatform = "MacOS", "Darwin"
    elif st("os2"):
        platform = dplatform = "OS2"
    elif st("risc"):
        platform, dplatform = "RiscOS", "Linux"
    elif st("athe"):
        platform, dplatform = "Atheos", "Linux"
    elif st("freebsd"):
        platform, dplatform = "FreeBSD", "BSD"
    elif st("openbsd"):
        platform, dplatform = "OpenBSD", "BSD"
    elif st("aix"):
        platform = dplatform = "AIX"
    else:
        dplatform = platform
    
    def check(cmd: str, shell: bool=False) -> list:
        from subprocess import run

        return run(cmd, shell=shell, capture_output=True
                   ).stdout.decode().splitlines()

    logger = _logger("os")

    k32 = None

    executableExts: tuple = ("bat", "bin", "cmd", "com", "cpl", "exe", "gadget", 
                             "inf1", "ins", "inx", "isu", "job", "jse", "lnk", 
                             "msc", "msi", "msp", "mst", "paf", "pif", "ps1", 
                             "reg", "rgs", "scr", "sct", "shb", "shs", "u3p", 
                             "vb", "vbe", "vbs", "vbscript", "ws", "wsf", "wsh")


def exit(details: str="", code: int=1) -> _bm.NoReturn:
    """
    Print some text and exit the current thread
    
    :param details: Text to print before exiting the current thread
    :param code: The exit code to use
    """

    from sys import exit

    if type(details) is not str:
        raise TypeError("Details must be a valid 'str' instance")

    if type(code) is not int:
        raise TypeError("Code must be a valid 'int' instance")

    if details == "":
        print("", end="")
    else:
        print(details)
    
    _bm.logger.info(f"Exiting the current thread with exit code {code}", "exit()")

    exit(code)

def clear() -> None:
    """Clear the terminal history"""

    from subprocess import run

    if _bm.platform.lower() == "windows":
        run("cls", shell=True)
    else:
        run("clear")

    _bm.logger.debug("Terminal history was cleared", "clear()")

class system():
    """Call a system program and return some information"""

    def __init__(self, 
                 cmds: _bm.Union[str, list, tuple], 
                 shell: bool=False,
                 timeout: _bm.Union[int, float]=10, 
                 check: bool=False,
                 capture: bool=True,
                 output: bool=True,
                 **shared: None):
        """
        Call a system program and return some information
        
        :param cmds: The arguments or program to run
        :param shell: Whether to use the shell as the input
        :param timeout: How long the child process should last before being terminated
        :param check: Whether to raise an error if the child process' exit code was not zero
        :param capture: Whether to capture the output of the child process
        :param output: Whether to allow the child process to output to stdout
        """

        from subprocess import run, CalledProcessError, TimeoutExpired, DEVNULL

        error = None

        if cmds == "" and not shell:
            raise ValueError("The call will fail because the input command is an invalid alias (no content)")

        if not isinstance(cmds, (str, list, tuple)):
            raise TypeError("Cmds must be a valid 'str', 'list' or 'tuple' instance")
        if not isinstance(timeout, (int, float)):
            raise TypeError("Timeout must be a valid 'int' or 'float' instance")
        
        name: str = cmds if type(cmds) is str else ' '.join(cmds)

        try:
            if output:
                self.rdata = run(cmds, shell=bool(shell), check=bool(check), 
                                 capture_output=bool(capture), timeout=timeout)
            else:
                self.rdata = run(cmds, shell=bool(shell), check=bool(check), 
                                 stdout=DEVNULL, timeout=timeout)
        except CalledProcessError as err:
            error = _bm.SubprocessCodeError(code=err.returncode)
        except TimeoutExpired:
            error = _bm.SubprocessTimeoutExpired(timeout=self.timeout)
        except FileNotFoundError:
            error = _bm.SubprocessLookupNotFound(name=name)
        except PermissionError:
            error = _bm.SubprocessPermissionError(name=name)
        except Exception:
            error = _bm.SubprocessExecutionError("An unknown process execution error occured, read the above stack trace for info")
        
        if shared.get("_call", False):
            caller: str = "call"
        elif shared.get("_check", False):
            caller: str = "check"
        else:
            caller: str = "system"

        _bm.logger.debug(f"Called child program/command with{' the' if shell else 'out'} shell", 
                         caller + "()")
        
        if error:
            raise error
        
        self.cmds: _bm.Union[list, str, tuple] = cmds
        self.timeout:    _bm.Union[int, float] = timeout
        self.list_text:              list[str] = []
        self.clean_list_text:        list[str] = []

        self.shell:   bool = bool(shell)
        self.check:   bool = bool(check)
        self.capture: bool = bool(capture)
        self.output:  bool = bool(output)
        self.code:     int = self.rdata.returncode
        self.raw:    bytes = b""
        self.text:     str = ""

        if capture:
            self.raw:                 bytes = self.rdata.stdout
            self.text:                  str = self.raw.decode()
            self.list_text:       list[str] = self.text.splitlines()
            self.clean_list_text: list[str] = list(filter(None, self.list_text))

    def __str__(self) -> str:
        return f"<System instance [Exit code {self.code}]>"
    
    def __repr__(self) -> str:
        return self.__str__()

def check(cmds: _bm.Union[str, list, tuple], 
          shell: bool=False,
          timeout: _bm.Union[int, float]=10,
          check: bool=False,
          clean: bool=False,
          listify: bool=True,
          raw: bool=False
          ) -> _bm.Union[str, bytes, _bm.List[str]]:
    """
    Call a system program and return the output
    
    :param cmds: The arguments or program to run
    :param shell: Whether to use the shell as the input
    :param timeout: How long the child process should last before being terminated
    :param check: Whether to raise an error if the child process' exit code was not zero
    :param clean: Whether to remove empty items if the output is a list
    :param listify: Whether to convert the string output of the process to a list seperated by newlines
    :param raw: Whether to return the bytes of the process output
    """

    data = system(cmds, shell, timeout, check, _check=True)

    if raw:
        return data.raw

    if listify and clean:
        return data.clean_list_text

    if listify:
        return data.list_text
    
    return data.text

def call(cmds: _bm.Union[str, list, tuple], 
         shell: bool=False, 
         timeout: _bm.Union[int, float]=10,
         check: bool=False,
         output: bool=True
         ) -> int:
    """
    Call a system program and return the exit code
    
    :param cmds: The arguments or program to run
    :param shell: Whether to use the shell as the input
    :param timeout: How long the child process should last before being terminated
    :param check: Whether to raise an error if the child process' exit code was not zero
    :param output: Whether to allow the child process to output to stdout
    """
    
    return system(cmds, shell, timeout, check, False, output, _call=True).code

def pID(name: str, strict: bool=False) -> _bm.Union[_bm.Tuple[int], None]:
    """
    Get the process ID of an app or binary by name
    
    :param name: The name of the process
    :param strict: Whether the name should be exactly the same to be considered a match
    """

    if type(name) is not str:
        raise TypeError("Name must be a valid 'str' instance")
    elif len(name) == 0:
        raise ValueError("Invalid name")

    if _bm.platform.lower() == "macos" or _bm.platform.lower() == "linux":
        ids: list = [int(i) for i in check(["pgrep", "-x" if strict else "-i", name])]
        #ids: list = [int(i) for i in check(f'ps -ax | awk \'/[{name[0]}]{name[1:]}/' + '{print $1}\'', True)]

    elif _bm.platform.lower() == "windows":
        from ctypes import sizeof, byref

        if _bm.k32 == None:
            from ctypes import windll, Structure, wintypes, POINTER, c_char

            _bm.k32 = windll.kernel32
            
            class _PROCESSENTRY32(Structure):
                _fields_: list = [
                    ("dwSize", wintypes.DWORD),
                    ("cntUsage", wintypes.DWORD),
                    ("th32ProcessID", wintypes.DWORD),
                    ("th32DefaultHeapID", POINTER(wintypes.ULONG)),
                    ("th32ModuleID", wintypes.DWORD),
                    ("cntThreads", wintypes.DWORD),
                    ("th32ParentProcessID", wintypes.DWORD),
                    ("pcPriClassBase", wintypes.LONG),
                    ("dwFlags", wintypes.DWORD),
                    ("szExeFile", c_char * 260)
                ]

            _bm.processEntry32 = _PROCESSENTRY32

        snapshot  = _bm.k32.CreateToolhelp32Snapshot(0x2, 0)
        ids: list = []

        if snapshot != -1:
            procEntry = _bm.processEntry32()
            procEntry.dwSize = sizeof(_bm.processEntry32)

            if _bm.k32.Process32First(snapshot, byref(procEntry)):
                while _bm.k32.Process32Next(snapshot, byref(procEntry)):
                    entryName: str = procEntry.szExeFile.decode("utf-8")

                    if strict:
                        for i in _bm.executableExts:
                            if name + '.' + i == entryName:
                                ids.append(int(procEntry.th32ProcessID))
                    elif name.lower() in entryName.lower():
                        ids.append(int(procEntry.th32ProcessID))
        
        _bm.k32.CloseHandle(snapshot)
    else:
        return None

    return tuple(ids)

def getCurrentWifiName() -> _bm.Union[str, None]:
    """Get the currently connected wifi name"""

    if _bm.platform.lower() == "macos":
        wifiName = check(["/System/Library/PrivateFrameworks/Apple80211." +
                          "framework/Versions/Current/Resources/airport", "-I"])
            
        if "AirPort: Off" in wifiName[0]:
            return None
        else:
            v: int = 0

            for i, it in enumerate(wifiName):
                if it.lstrip()[:4] == "SSID":
                    v = i

                    break
            
            return wifiName[v].lstrip()[6:]

    elif _bm.platform.lower() == "windows":
        data: list = check(["netsh", "wlan", "show", "interfaces"])
        v:     int = 0

        for i, it in enumerate(data):
            if it.lstrip()[:4] == "SSID":
                v = i

                break

        if v == 0:
            return None
        else:
            return data[v].lstrip()[4:].lstrip()[1:].lstrip()

    elif _bm.platform.lower() == "linux":
        data = check(["iwgetid", "-r"])

        return data if data else None

    else:
        return None


# info classes
class _info:
    """Operating system information"""

    def __init__(self):
        from sys import version, maxsize, executable
        from socket import gethostname

        self.python_version:    str = version.split(" (")[0].strip()
        """Current Python interpreter version"""
        self.name:              str = gethostname()
        """The network and user name of the current operating system/computer"""
        self.bitsize:           int = 64 if (maxsize > 2 ** 32) else 32
        """The bit limit of the current Python interpreter"""
        self.interpreter:       str = executable
        """Location of current Python interpreter"""
        self.platform:          str = _bm.platform
        """Name of current operating system"""
        self.detailed_platform: str = _bm.dplatform
        """Technical name of your computer's OS"""

        self.macOS_releases: _bm.Dict[str, str] = {
            "10.0":  "Cheetah",
            "10.1":  "Puma",
            "10.2":  "Jaguar",
            "10.3":  "Panther",
            "10.4":  "Tiger",
            "10.5":  "Leopard",
            "10.6":  "Snow Leopard",
            "10.7":  "Lion",
            "10.8":  "Mountain Lion",
            "10.9":  "Mavericks",
            "10.10": "Yosemite",
            "10.11": "El Capitan",
            "10.12": "Sierra",
            "10.13": "High Sierra",
            "10.14": "Mojave",
            "10.15": "Catalina",
            "11":    "Big Sur",
            "12":    "Monterey",
            "13":    "Ventura",
            "14":    "Sonoma"
        }
        """List of all current MacOS versions"""

        self._sysinfo: list = []

        self._cpu:   list = [False, ""]
        self._arch:  list = [False, ""]
        self._model: list = [False, ""]
        self._cores: list = [False, 0]
        self._ram:   list = [False, 0]
        self._manufacturer:     list = [False, ""]
        self._serial_number:    list = [False, ""]
        self._boot_drive:       list = [False, ""]
        self._platform_version: list = [False, ()]
    
    @property
    def cpu(self) -> str:
        """Name of the currently in use cpu of your computer"""

        return self._cpu[1]
    
    @cpu.setter
    def cpu(self, value: str):
        self._cpu[1] = value
    
    @property
    def arch(self) -> str:
        """Computer architecture"""

        return self._arch[1]

    @arch.setter
    def arch(self, value: str):
        self._arch[1] = value
    
    @property
    def model(self) -> str:
        """The model or manufacturer of your computer"""

        return self._model[1]
    
    @model.setter
    def model(self, value: str) -> str:
        self._model[1] = value

    @property
    def cores(self) -> int:
        """The amount of cores in your computer's cpu"""

        return self._cores[1]

    @cores.setter
    def cores(self, value: int):
        self._cores[1] = value
    
    @property
    def ram(self) -> int:
        """The amount of ram in megabytes in your computer"""

        return self._ram[1]
    
    @ram.setter
    def ram(self, value: int):
        self._ram[1] = value
    
    @property
    def manufacturer(self) -> str:
        """The creator of your computer"""

        return self._manufacturer[1]
    
    @manufacturer.setter
    def manufacturer(self, value: str):
        self._manufacturer[1] = value
    
    @property
    def serial_number(self) -> str:
        """The identifiable code or tag string of your computer (This is unobtainable on Linux)"""

        return self._serial_number[1]
    
    @serial_number.setter
    def serial_number(self, value: str) -> str:
        self._serial_number[1] = value
    
    @property
    def boot_drive(self) -> str:
        """The location of the disk currently being used on your computer"""

        return self._boot_drive[1]

    @boot_drive.setter
    def boot_drive(self, value: str):
        self._boot_drive[1] = value
    
    @property
    def platform_version(self) -> _bm.Tuple[str]:
        """Version number and or name of current OS"""

        return self._platform_version[1]
    
    @platform_version.setter
    def platform_version(self, value: tuple):
        self._platform_version[1] = value

class _info_macOS(_info):
    """Operating system information"""

    def _strip(self, value: str) -> str:
        return value.split(": ")[1]

    def __sysinfo(self) -> None:
        if not self._sysinfo:
            self._sysinfo = check(["system_profiler", "SPHardwareDataType"])
    
    @property
    def cpu(self) -> str:
        """Name of the currently in use cpu of your computer"""

        self.__sysinfo()

        if not self._cpu[0]:
            self._cpu[0] = True
            self._cpu[1] = self._strip(self._sysinfo[5])

        return self._cpu[1]

    @property
    def arch(self) -> str:
        """Computer architecture"""

        if not self._arch[0]:
            self._arch[0] = True
            self._arch[1] = _bm.check("arch")[0]

        return self._arch[1]
    
    @property
    def model(self) -> str:
        """The model or manufacturer of your computer"""

        self.__sysinfo()

        if not self._model[0]:
            self._model[0] = True
            self._model[1] = self._strip(self._sysinfo[2])

        return self._model[1]

    @property
    def cores(self) -> int:
        """The amount of cores in your computer's cpu"""

        self.__sysinfo()

        if not self._cores[0]:
            self._cores[0] = True
            self._cores[1] = int(self._strip(self._sysinfo[6]).split(" (")[0])

        return self._cores[1]

    @property
    def ram(self) -> str:
        """The amount of ram in megabytes in your computer"""

        self.__sysinfo()

        if not self._ram[0]:
            self._ram[1] = self._strip(self._sysinfo[7])
            self._ram[0] = True
    
            if "GB" in self._ram[1]:
                self._ram[1] = int(self._ram[1].split(' ')[0]) * 1024
            else:
                self._ram[1] = int(self._ram[1].split(' ')[0])

        return self._ram[1]

    @property
    def manufacturer(self) -> str:
        """The creator of your computer"""

        return "Apple Inc."

    @property
    def serial_number(self) -> str:
        """The identifiable code or tag string of your computer (This is unobtainable on Linux)"""

        self.__sysinfo()

        if not self._serial_number[0]:
            self._serial_number[0] = True
            self._serial_number[1] = self._strip(self._sysinfo[10])

        return self._serial_number[1]

    @property
    def boot_drive(self) -> str:
        """The location of the disk currently being used on your computer"""

        if not self._boot_drive[0]:
            self._boot_drive[0] = True
            self._boot_drive[1] = _bm.check(["bless", "--info", "--getBoot"])[0]

        return self._boot_drive[1]

    @property
    def platform_version(self) -> _bm.Tuple[str]:
        """Version number and or name of current OS"""

        if not self._platform_version[0]:
            pver: list = [_bm.check(["sw_vers", "-productVersion"])[0]]

            if len(pver[0].split('.')) > 1:
                if pver[0][:2] in (i for i in tuple(self.macOS_releases.keys()) if len(i) == 2):
                    pver.append(self.macOS_releases[pver[0][:2]])
                else:
                    pver.append(self.macOS_releases['.'.join(pver[0].split('.')[:2])])
            else:
                pver.append(self.macOS_releases[pver[0]])

            self._platform_version[0] = True
            self._platform_version[1] = tuple(pver)

        return self._platform_version[1]

class _info_windows(_info):
    """Operating system information"""

    def _wmic(self, *cmds: tuple) -> str: 
        return [i.strip() for i in _bm.check("wmic " + cmds[0] + " get " + cmds[1])][2]

    def _strip(self, value: str) -> str: 
        return value.split(": ")[1].strip()

    def __sysinfo(self) -> None:
        if not self._sysinfo:
            self._sysinfo = check("systeminfo")
    
    @property
    def cpu(self) -> str:
        """Name of the currently in use cpu of your computer"""

        if not self._cpu[0]:
            self._cpu[0] = True
            self._cpu[1] = self._wmic("cpu", "name")

        return self._cpu[1]

    @property
    def arch(self) -> str:
        """Computer architecture"""

        if not self._arch[0]:
            self._arch[0] = True
            self._arch[1] = self._wmic("os", "OSArchitecture").replace("Processor", "").strip()

        return self._arch[1]
    
    @property
    def model(self) -> str:
        """The model or manufacturer of your computer"""

        self.__sysinfo()

        if not self._model[0]:
            self._model[0] = True
            self._model[1] = self._strip(self._sysinfo[12])

        return self._model[1]

    @property
    def cores(self) -> int:
        """The amount of cores in your computer's cpu"""

        if not self._cores[0]:
            self._cores[0] = True
            self._cores[1] = self._wmic("cpu", "NumberOfCores")

        return self._cores[1]

    @property
    def ram(self) -> str:
        """The amount of ram in megabytes in your computer"""

        self.__sysinfo()

        if not self._ram[0]:
            self._ram[0] = True
            self._ram[1] = int(self._strip(self._sysinfo[23]).split(' ')[0].replace(',', ""))

        return self._ram[1]

    @property
    def manufacturer(self) -> str:
        """The creator of your computer"""

        self.__sysinfo()

        if not self._manufacturer[0]:
            self._manufacturer[0] = True
            self._manufacturer[1] = self._strip(self._sysinfo[11])

        return self._manufacturer[1]

    @property
    def serial_number(self) -> str:
        """The identifiable code or tag string of your computer (This is unobtainable on Linux)"""

        if not self._serial_number[0]:
            self._serial_number[0] = True
            self._serial_number[1] = self._wmic("bios", "SerialNumber")

        return self._serial_number[1]

    @property
    def boot_drive(self) -> str:
        """The location of the disk currently being used on your computer"""

        self.__sysinfo()

        if not self._boot_drive[0]:
            self._boot_drive[0] = True
            self._boot_drive[1] = self._strip(self._sysinfo[19])

        return self._boot_drive[1]

    @property
    def platform_version(self) -> _bm.Tuple[str]:
        """Version number and or name of current OS"""

        self.__sysinfo()

        if not self._platform_version[0]:
            self._platform_version[0] = True
            self._platform_version[1] = (self._strip(self._sysinfo[2]).split(' ')[0], 
                                         self._strip(self._sysinfo[1]).split(' ')[-1])

        return self._platform_version[1]

class _info_linux(_info):
    """Operating system information"""

    @property
    def cpu(self) -> str:
        """Name of the currently in use cpu of your computer"""

        if not self._cpu[0]:
            self._cpu[0] = True
            self._cpu[1] = _bm.check("lscpu | grep 'Model:'", True)[0].split(':')[1].strip()

        return self._cpu[1]

    @property
    def arch(self) -> str:
        """Computer architecture"""

        if not self._arch[0]:
            self._arch[0] = True
            self._arch[1] = _bm.check("arch")[0]

        return self._arch[1]
    
    @property
    def model(self) -> str:
        """The model or manufacturer of your computer"""

        if not self._model[0]:
            self._model[0] = True
            self._model[1] = _bm.check(["cat", "/sys/devices/virtual/dmi/id/product_name"])[0]

        return self._model[1]

    @property
    def cores(self) -> int:
        """The amount of cores in your computer's cpu"""

        if not self._cores[0]:
            self._cores[0] = True
            self._cores[1] = int(_bm.check("lscpu | grep 'Core(s) per socket:'", True)[0].split(':')[1].strip())

        return self._cores[1]

    @property
    def ram(self) -> str:
        """The amount of ram in megabytes in your computer"""

        if not self._ram[0]:
            self._ram[0] = True
            self._ram[1] = round(int(_bm.check("cat /proc/meminfo | grep 'MemTotal:'", True)[0].split(':')[1].strip().split(' ')[0]) / 1000)

        return self._ram[1]

    @property
    def manufacturer(self) -> str:
        """The creator of your computer"""

        if not self._manufacturer[0]:
            self._manufacturer[0] = True
            self._manufacturer[1] = _bm.check(["cat", "/sys/devices/virtual/dmi/id/sys_vendor"])[0]

        return self._manufacturer[1]

    @property
    def serial_number(self) -> str:
        """The identifiable code or tag string of your computer (This is unobtainable on Linux)"""

        _bm.logger.warning("Serial_number property is unobtainable on Linux systems", 
                           "info")

        return ""

    @property
    def boot_drive(self) -> str:
        """The location of the disk currently being used on your computer"""

        if not self._boot_drive[0]:
            self._boot_drive[0] = True
            self._boot_drive[1] = _bm.check("df /boot | grep -Eo '/dev/[^ ]+'", True)[0]

        return self._boot_drive[1]

    @property
    def platform_version(self) -> _bm.Tuple[str]:
        """Version number and or name of current OS"""

        if not self._platform_version[0]:
            sysinfo = _bm.check(["cat", "/etc/os-release"])

            self._platform_version[0] = True
            self._platform_version[1] = [sysinfo[3].split('"')[1].split(' ')[0], sysinfo[1].split('"')[1]]

        return self._platform_version[1]

if _bm.platform.lower() == "macos":
    info = _info_macOS()
elif _bm.platform.lower() == "windows":
    info = _info_windows()
elif _bm.dplatform.lower() == "linux":
    info = _info_linux()
else:
    info = _info()

info: _info = info
"""Operating system information"""


for _i in ("_info", "_info_macOS", "_info_windows", "_info_linux", "_i"):
    try:
        del locals()[_i]
    except NameError:
        continue
