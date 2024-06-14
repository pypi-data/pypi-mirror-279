from sys import exit, argv

from .info import _bm, _loadConfig, license, long_description


keys: list = []

for k, v in _loadConfig().items():
    for k2 in v.keys():
        keys.append(k2)

infoVars: dict = dict((k, v) for k, v in _bm.info.__dict__.items() if "__" not in k)

infoVars.update({"license": license, "long_description": long_description})


class commands:
    _test:     dict = {}
    _cmds:     dict = {}
    _cmdNames: list = []

    def _register(*aliases: str, meth, desc: str, 
                  args: tuple) -> None:
        if args:
            args: tuple = (tuple([i[0] for i in args]), 
                           dict([(i[0], i[2]) for i in args]), args)
        else:
            args = None

        for i, it in enumerate(aliases): 
            commands._cmdNames.append(it)
            commands._cmds.update({it: (desc, meth, args, bool(i))})

    def _getCmdAliases() -> list:
        cmds: list = []

        # compile aliases with their respective commands
        # so there are no duplicate commands when printed
        for k, v in commands._cmds.items():
            if v[3]:
                cmds[-1][0].append(k)
            else:
                cmds.append([[k], v])
        
        return cmds

    def _stylePrintCommand(i: tuple) -> str:
        name: str = f"{i[0][0]}\u001b[0m"
        args: str = ""

        if i[1][2]:
            args = "\n\n" + '\n'.join([f"  {f'\u001b[1m-{i2[0]}\u001b[0m'} {i2[3]}, " +
                            f"{'required' if i2[2] else 'not required'}, must be type " +
                            f"{i2[1].__name__}" for i2 in i[1][2][2]])

        if len(i[0]) > 1:
            aliases: str = ', '.join([f"\u001b[1m{i2}\u001b[0m" for i2 in i[0][1:]])
            name:    str = f"{i[0][0]} \u001b[0m(also: {aliases})"
        
        return f"- \u001b[1m{name}:\n  {i[1][0]}{args}\n\n"

    def help(c: str=None) -> None:
        text: str = ""

        if c:
            for i in commands._getCmdAliases():
                if c in i[0]:
                    text += commands._stylePrintCommand(i)

                    break

            if not text:
                return error(f"help -c | Unknown command name")
        else:
            args: str = ""
            
            for i in commands._getCmdAliases():
                if len(i[0]) > 1:
                    args += '[' + " | ".join(i[0]) + "] "
                else:
                    args += f"[{i[0][0]}] "
                
                text += commands._stylePrintCommand(i)

            text = f"usage: python -m tooltils {args.rstrip()}\n\n\u001b[1mCommands List:\n\n\u001b[0m" + text
        
        print(text.rstrip())
    
    def info(v: str=None) -> None:
        if v:
            try:
                print(infoVars[v])
            except KeyError:
                return error("info -v | Unknown info variable")
        else:
            print("\u001b[1mInstallation information:\u001b[0m\n" + \
                  '\n'.join([f"- {k}: {repr(va)}" for k, va in infoVars.items()]))

    def cache() -> None:
        from json import dumps

        from .info import _loadCache

        print(dumps(_loadCache(), indent=4))

    def config() -> None:
        from json import dumps

        from .info import _loadConfig

        print(dumps(_loadConfig(), indent=4))

    def _checkLoaded() -> None:
        from .info import _checkLoaded

        try:
            _checkLoaded()
        except FileExistsError:
            return error("The tooltils data files have been deleted, please rerun the command" +
                         "to create them again")

    def clearCache() -> None:
        from .info import clearCache

        commands._checkLoaded()
        
        clearCache()
    
    def clearConfig() -> None:
        from .info import clearConfig

        commands._checkLoaded()
        
        clearConfig()
    
    def clearData() -> None:
        from .info import clearData

        commands._checkLoaded()
        
        clearData()
    
    def deleteData(psv: str=None, tsv: str=None) -> None:
        from .info import deleteData

        commands._checkLoaded()
        
        try:
            deleteData(psv, tsv)
        except FileNotFoundError as err:
            if "exist" in err.args[0]:
                return error("The tooltils data files have been deleted, please rerun " + 
                             "the command to create them again")
            else:
                return error(err.args[0])
        
        print("Deleted Tooltils data files successfully")
    
    def configEdit(**tables: str) -> None:
        from .info import _getConfig

        from json import dumps

        data: dict = _loadConfig()
        _f         = _getConfig()

        for k, v in data.items():
            for k2 in v.keys():
                for k3 in tables.keys():
                    if k2 == k3:
                        data[k][k2] = tables[k3]

        _f.truncate(0)
        _f.write(dumps(data, indent=4))
        _f.seek(0)

        print("\u001b[1mEdited successfully\u001b[0m")
    
    def request(url: str, method: str="GET", port: int=(80, 443), 
                https: bool=True, verify: bool=True, redirects: bool=True,
                redirect_loops: bool=False, cert: str=None,
                file_name: str=None, override: bool=False, 
                timeout: _bm.Union[int, float]=15,
                encoding: _bm.Union[str, tuple]=("utf-8", "ISO-8859-1"),
                mask: bool=False, agent: str=None, proxy: str=None):
        from .requests import request

        try:
            rData = request(url, method, port, https, verify, redirects,
                            redirect_loops, None, None, None, None, cert,
                            file_name, override, timeout, encoding,
                            mask, agent, proxy=proxy).send()
        except Exception as err:
            return error(str(err))

        print(f"Status: {rData.status_code}\nResponse Headers: {rData.headers}\n \
                Redirected: {rData.redirected}\nResponse: {rData.json if rData.json else rData.text}")


def pointToError(text: str, errIdx: int, offset: int=0) -> str:
    #width: int = os.get_terminal_size().columns

    width: int = len(text)

    text += f"\n{"".join([' ' for i in range(width)])}"
    text  = list(text)

    text[width + errIdx + 1] = f"{''.join([' ' for i in range(offset)])}\u001b[1m^\u001b[0m"

    return "".join(text)

def error(text: str, cmd: str=None, errIdx: int=None) -> None:
    from subprocess import run

    if cmd and errIdx:
        err:    str = "  " + pointToError(cmd, errIdx, 2) + '\n'
        errIdx: str = f", col {errIdx}"
    else:
        err:    str = ("  " + cmd + '\n') if cmd else ""
        errIdx: str = ""

    run("", shell=True)

    print(f"\u001b[1mException raised{errIdx}:\u001b[0m\n{err}\n\u001b[31;1m{text}\u001b[0m")

    exit(1)


def parseCommand(cmd: str) -> tuple:
    from ast import literal_eval

    fullcmd: str = cmd

    cmd:   list = cmd.split(' ')
    instr: bool = False
    inopt: bool = False
    items: list = [""]
    opts:  list = [""]
    icmd:   str = ""

    for i in commands._cmdNames:
        if icmd:
            break

        for i2 in cmd:
            if i == i2:
                icmd = i

                cmd.remove(i2)

                break

    cmd = ' '.join(cmd)

    for i, it in enumerate(cmd):
        if len(opts) == len(items) + 2:
            items.append("")
        
        if it == '"' or it == '\'':
            items[-1] += it

            instr = not instr
        elif it == '-' and not instr:
            inopt = True
        elif inopt and it != ' ':
            opts[-1] += it
            #return error('Expected command name with value', cmd, i)
        elif inopt and it == ' ':
            inopt = False

            opts.append("")
        elif instr:
            items[-1] += it
            #return error('Expected command name with string value', cmd, i)
        elif not (items[-1].startswith('"') or items[-1].startswith('\'')) and it != ' ':
            items[-1] += it
        elif items[-1] != "":
            items.append("")

        if commands._test["loopLog"] or commands._test["all"]:
            print('\n'.join([f"{k}: {v}" for k, v in {"loop": i, "instr": instr, "inopt": inopt,
                  "items": items, "opts": opts}.items()]) + '\n')

    icmdName: str = icmd

    for k, v in commands._cmds.items():
        if icmd == k:
            icmd = v[1]

            break

    if isinstance(icmd, str):
        return error("Unknown command name", fullcmd)

    for i, it in enumerate(items):
        if not ('"' in it or '\'' in it):
            try:
                it = literal_eval(it)
            except Exception:
                pass

        if isinstance(it, str):
            it = it.strip()
        
        items[i] = it
    
    opts = list(filter(None, opts))

    if len(items) > len(opts) and len(opts) == 0:
        items = []

    if any(opts):
        if len(opts) > len(items):
            args: dict = {}

            for i, it in enumerate(opts):
                try:
                    args.update({it: items[i]})
                except IndexError:
                    args.update({it: True})
        else:
            args: dict = dict(zip(opts, items))

        #if len(args) < (len(iopt) + len(item)) / 2:
        #    return error('Mismatched argument values found', cmd)
    elif any(items):
        return error("Mismatched argument values found (standalone values)", fullcmd)
    else:
        args: dict = {}
    
    for k, v in args.items():
        if v == '':
            args[k] = True

    params: tuple = commands._cmds[icmdName][2]

    if not params:
        params = (tuple(), {}, (tuple(), ))
    
    for k, v in params[1].items():
        if v and k not in list(args.keys()):
            return error(f"Required argument '{k}' for command '{icmdName}' missing", fullcmd)

    for i in opts:
        if i not in params[0]:
            return error(f"Unknown argument '{i}' for command '{icmdName}'", fullcmd)
        elif params[0]:
            for i2 in params[2]:
                if not isinstance(args[i], i2[1]):
                    return error(f"Type of argument '{i}' for command '{icmdName}' " +
                                 f"should be '{i2[1].__name__}', not '{type(args[i]).__name__}'", fullcmd)

    if commands._test["log"] or commands._test["all"]:
        print('\n'.join([f"{k}: {v}" for k, v in {"opts": opts, "items": items, 
                                                  "args": args, "result": (icmd, args)}.items()]))

    return (icmd, args)

def runCommand(cmd: str) -> None:
    if not cmd:
        return commands.help()
    
    result = parseCommand(cmd)

    result[0](**result[1])


def main() -> None:
    commands._register("help", "commands", meth=commands.help, 
                       desc="Show a list of commands or details of a specific command", 
                       args=(('c', str, False, "Show details for a specific command"), ))

    commands._register("info", meth=commands.info,
                       desc="Print installation information or a specific value",
                       args=(('v', str, False, "Print a specific information variable"), ))

    commands._register("cache", meth=commands.cache, desc="Show the cache data", args=None)
    commands._register("config", meth=commands.config, desc="Show the config data", args=None)

    commands._register("clearCache", meth=commands.clearCache, desc="Clear the cache data",
                       args=None)
    commands._register("clearConfig", meth=commands.clearConfig, desc="Clear the config data",
                       args=None)
    commands._register("clearData", meth=commands.clearData, desc="Clear the cache and config data",
                       args=None)
    
    commands._register("deleteData", meth=commands.deleteData, desc="Delete the data files",
                       args=(("pyv", str, False, "The Python version to delete the data for"), 
                             ("tsv", str, False, "The Tooltils version to delete the data for")))

    commands._register("configEdit", meth=commands.configEdit, desc="Edit a config table",
                       args=tuple((i, object, False, "Config table") for i in keys))

    if False:
        commands._register("request", "curl", meth=commands.request, desc="Send a request",
                           args=(("url", str, True, "The url to request"), 
                                ("method", str, False, "The method to use"),
                                ("port", int, False, "The request port"),
                                ("https", bool, False, "Whether to use https"),
                                ("verify", bool, False, "Whether to verify the request connection"),
                                ("redirects", bool, False, "Whether redirects are allowed"),
                                ("redirect_loops", bool, False, "Whether redirect looping is allowed"),
                                ("cert", str, False, "Certificate for the request"),
                                ("file_name", str, False, "Request download file name"),
                                ("write_binary", bool, False, "Whether to write request download file in binary"),
                                ("override", bool, False, "Whether to override an existing request download"),
                                ("timeout", int, False, "Request timeout length"),
                                ("encoding", str, False, "Request response decoder(s)"),
                                ("mask", bool, False, "Request user agent header mask"),
                                ("agent", str, False, "Request user agent override"),
                                ("proxy", str, False, "Request proxy")))

    if commands._test["cmd"] or commands._test["all"]:
        commands._register("test", "test2", "test3", meth=lambda testValue: print(testValue),
                           desc="Test command",
                           args=(("testValue", str, True, "Test argument"), 
                                 ("testValue2", int, False, "Test argument 2")))

    runCommand(' '.join(argv[1:]).strip())


# make testing buttery smooth
# cursed formatting go!!!
commands._test = {
      "all": False
,     "cmd": False
,     "log": False
, "loopLog": False
}

if any(commands._test.values()):
    main()
elif __name__ == "__main__":
    main()
