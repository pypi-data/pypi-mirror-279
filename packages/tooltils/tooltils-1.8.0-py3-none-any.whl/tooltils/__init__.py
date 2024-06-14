"""
# tooltils | v1.8.0

A lightweight python utility package built on the standard library

```py
>>> import tooltils
>>> data = tooltils.requests.get('httpbin.org/get')
>>> data.status_code
'200 OK'
>>> data.end_data.url
'https:/httpbin.org/get'
>>> data.end_data.sent_headers
{'User-Agent': 'Python-tooltils/1.8.0', 'Accept-Encoding': 'gzip, deflate', ...}
>>> data.headers
{'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Host': 'httpbin.org', ...}
```

## API

Read the full documentation within `API.md` included in the github project directory
"""

import tooltils.requests as requests
import tooltils.errors as errors
import tooltils.info as info
import tooltils.os as os

class _bm:
    from typing import Union, Any, Dict, List, Callable, Iterable, Generator
    from functools import lru_cache
    from types import GeneratorType
    # Note: The lru_cache decorator cannot be used on functions that take any mutable objects
    #       as the arguments are hashed and then cached, and mutable objects are not hashable
    
    class EPOCH_seconds:
        pass

    months: tuple = (
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    )
    ends:  tuple = ("th", "st", "nd", "rd", "th", "th", "th", "th", "th", "th")

    def fv(*values):
        return (str(i) if i > 9 else f"0{i}" for i in values)

    logger = info._logger("")


ANSI_colours: _bm.Dict[str, int] = {
    "white":  97,
    "cyan":   36,
    "pink":   35,
    "blue":   34,
    "yellow": 33,
    "green":  32,
    "red":    31,
    "gray":   30,
}
"""List of major colours as ANSI integer codes"""

def waveLength(file: str) -> _bm.Union[int, float]:
    """
    Get the length of a wave file in seconds
    
    :param file: The WAVE file
    :param dcp: The decimal places to round the length of the WAVE file
    """

    if not isinstance(file, str):
        raise TypeError("File must be a valid 'str' instance")

    if not info._bm.exists(file):
        raise FileNotFoundError("Could not locate WAVE file")

    try:
        with open(file, encoding="latin-1") as _f:
            _f.seek(28)

            sdata = _f.read(4)
    except OSError:
        raise FileNotFoundError("The WAVE file was unable to be read or located")

    rate: int = 0

    for i in (0, 1, 2, 3):
        rate += ord(sdata[i]) * pow(256, i)

    #return round((_bm.ospath().getsize(file) - 44) * 1000 / rate / 1000, dcp)
    # * 1000 and / 1000 cancel each other out
    return (info._bm.getsize(file) - 44) / rate

@_bm.lru_cache(maxsize=None)
def style(text: str, 
          colour: str="",
          bold: bool=False,
          italic: bool=False,
          fill: bool=False,
          crossed: bool=False,
          underline: bool=False,
          double_underline: bool=False,
          clear: bool=True
          ) -> str:
    """
    Create text in the specified colour and or style

    :param text: The text to style
    :param colour: The colour to style the text with
    :param bold: Whether to make the text bold
    :param italic: Whether to make the text italic
    :param fill: Whether to make the text colour fill in the background of the character
    :param crossed: Whether to make the text crossed out
    :param underline: Whether to make the text underline
    :param double_underline: Whether to make the text double underline
    :param clear: Whether to append an empty escape sequence after the string to clear any formatting
    """

    if not isinstance(text, str):
        raise TypeError("Text must be a valid 'str' instance")

    if not isinstance(colour, (str, int)):
        raise TypeError("Colour must be a valid 'str' instance")

    if not colour:
        code = 0
    else:
        code = ANSI_colours.get(colour.lower(), colour)

    style: str = ''

    for k, v in (('1', bold), ('3', italic), ('9', crossed), 
                 ('4', underline), ("21", double_underline)):
        if v:
            style += ';' + k

    return "\u001b[{}{}m{}{}".format((code + 10) if fill else code, style, text,
                                     "\u001b[0m" if clear else "")

def halve(array: _bm.Union[str, list, tuple, set, dict]) -> list:
    """
    Return the halves of a string or array

    :param array: The iterable to halve
    """

    if not isinstance(array, (str, list, tuple, set, dict)):
        raise TypeError("Array must be a valid 'str' or array instance")

    i: int = len(array)

    if i % 2 == 0:
        return [array[:i // 2], array[i // 2:]]
    else:
        return [array[:(i // 2 + 1)], array[(i // 2 + 1):]]

@_bm.lru_cache(maxsize=None)
def cipher(text: str, shift: int) -> str:
    """
    A simple caeser cipher

    :param text: The text to shift
    :param shift: How many places in the alphabet to shift the text
    """

    if not isinstance(text, str):
        raise TypeError('Text must be a valid \'str\' instance')
    elif len(text) < 1:
        raise ValueError('Invalid text')

    if not isinstance(shift, int):
        raise TypeError('Shift must be a valid \'int\' instance')
    elif shift == 0:
        raise ValueError('Shift must not be equal to zero')

    result: str = ""

    for i in text:
        start: int = 65 if i.isupper() else 97
        result    += chr((ord(i) + shift - start) % 26 + start)

    return result

def cstrip(text: str, values: _bm.Union[str, dict], strict: bool=True) -> str:
    """
    Change text based off a dictionary of values or a string of individual characters

    :param text: Text to change
    :param values: Values to change the string from
    """

    if isinstance(values, str):
        for i in values:
            if strict:
                text = text.replace(i, '')
            else:
                text = text.replace(i.upper() if not strict else i, '').replace(i.lower() if strict else '', '')
    elif isinstance(values, dict):
        for k, v in values.items():
            if strict:
                text = text.replace(k, v)
            else:
                # first replace to make sure k is upper, then replace with one statement

                text = text.replace(k.lower(), k.upper()).replace(k.upper(), v)
    else:
        raise TypeError("Values must be a valid 'str' or 'dict' instance")

    return text

def date(epoch: _bm.EPOCH_seconds=...,
         timezone: str=None,
         format: int=0
         ) -> str:
    """
    Convert the current date timestamp to a readable format

    #### Format:
    - `0:` "2024/03/08 17:29:46"
    - `1:` "5:30 PM on the 8th of March, 2024"
    - `2:` "Mar 8 2024, 17:30:23"

    :param epoch: The EPOCH date in seconds
    :param timezone: The timezone specifier (+-99:99)
    :param format: The format to output the date in
    """

    from datetime import datetime, timedelta, timezone as dtTimezone
    from time import localtime, gmtime, time

    if not isinstance(epoch, (int, float)) and epoch != ...:
        raise TypeError("Epoch must be a valid 'int' or 'float' instance")

    if not isinstance(timezone, str) and timezone:
        raise TypeError("Timezone must be a valid 'str' instance")

    if not isinstance(format, int):
        raise TypeError("Format must be a valid 'int' instance")

    try:
        if epoch == ...:
            epoch = time()

        if timezone == None:
            sdate = localtime(epoch)
        elif "00:00" in timezone:
            sdate = gmtime(epoch)
        elif timezone.startswith('+') or timezone.startswith('-'):
            timezone = dtTimezone(timedelta(
                       hours=int(timezone[:3]),
                       minutes=int(timezone[4:])))

            sdate = datetime.fromtimestamp(epoch, tz=timezone).timetuple()
        else:
            raise ValueError("Invalid timezone")
    except (ValueError, IndexError):
        raise TypeError("Timezone not found")
    except OverflowError:
        raise OverflowError("Epoch timestamp too large")

    if format == 0:
        return "{}/{}/{} {}:{}:{}".format(sdate.tm_year,
               *_bm.fv(sdate.tm_mon, sdate.tm_mday, sdate.tm_hour,
               sdate.tm_min, sdate.tm_sec))

    elif format == 1:
        hour: int = sdate.tm_hour % 12 if sdate.tm_hour % 12 != 0 else 12

        if sdate.tm_mday in (11, 12, 13):
            end: str = "th"
        else:
            end: str = _bm.ends[int(str(sdate.tm_mday)[-1])]

        return "{}:{} {} on the {}{} of {}, {}".format(hour, *_bm.fv(sdate.tm_min),
               "PM" if sdate.tm_hour >= 12 else "AM", sdate.tm_mday, end,
               _bm.months[sdate.tm_mon - 1], sdate.tm_year)

    elif format == 2:
        return "{} {} {}, {}:{}:{}".format(_bm.months[sdate.tm_mon - 1][:3], sdate.tm_mday,
                                          sdate.tm_year, *_bm.fv(sdate.tm_hour, sdate.tm_min, 
                                          sdate.tm_sec))

    else:
        raise ValueError(f"Format '{format}' not found")

@_bm.lru_cache(maxsize=None)
def epoch(date: str) -> int:
    """
    Get the epoch timestamp from a formatted date
    
    :param date: The formatted date to get the EPOCH in seconds from
    """

    from datetime import datetime

    if not isinstance(date, str):
        raise TypeError("Date must be a valid 'str' instance")

    if '/' in date:
        splitDate: list = str(date).split(' ')
    elif '-' in date:
        splitDate: list = str(date).replace('-', '/').split(' ')
    elif ',' in date:
        try:
            # Remove '1st' to avoid stripping Augu[st]
            sdate: list = cstrip(date, {':': ' ', " on the": "", " of": "", ',': "", 
                                        "th": "", "1st": "", "nd": "", "rd": ""}).split(' ')
            hours, minutes, meridan, days, month, year = sdate

            if "1st" in date:
                days = '1'
            if meridan == "PM":
                hours = str(int(hours) + 12)

            splitDate: tuple = (year + '/' + str(int(_bm.months.index(month)) + 1)
                                + '/' + days, hours + ':' + minutes + ":00")
        except (IndexError, ValueError):
            try:
                month, days, year, hours, minutes, seconds = cstrip(
                    date, {':': ' ', ',': ""}).split(' ')
            
                month = [i for i, it in enumerate(_bm.months) if month == it[:3]][0] + 1

                splitDate: tuple = (year + '/' + str(month) + '/' + days, 
                                    hours + ':' + minutes + ':' + seconds)
            except (IndexError, ValueError):
                raise ValueError("Invalid date")
    else:
        raise ValueError("Unknown date format")

    try:
        sdate = datetime(*[int(i) for i in splitDate[0].split(
                         '/') + splitDate[1].split(':')])
    except IndexError:
        raise ValueError("Invalid date")

    days: int = datetime(sdate.year, sdate.month, 
                         sdate.day, sdate.hour,
                         sdate.minute, sdate.second).toordinal(
                         ) - datetime(1970, 1, 1).toordinal() - 1

    # Add 13 hours because of obscure glitch
    # it is not a timezone thing!! 
    hours = days * 24 + sdate.hour + 13
    minutes = hours * 60 + sdate.minute
    epoch = minutes * 60 + sdate.second

    return epoch

def squeeze(array: _bm.Union[list, tuple, set, dict],
            item: _bm.Any=None
            ) -> _bm.Union[list, tuple, set, dict]:
    """
    Remove empty or the specified item(s) from an array
    
    :param array: The iterable to search through and remove the item from
    :param item: The item to remove from the iterable
    """
    
    if not isinstance(array, (list, tuple, set, dict)):
        raise TypeError("Array must be a valid iterable container")

    op = type(array)
    if op is not dict:
        array = list(array)

    if item is None:
        if op is dict:
            for i in tuple(array.keys()):
                if not array[i]:
                    array.pop(i)
        
            return array
        else:
            return op(filter(None, array))
    else:
        if op is dict:
            for i in tuple(array.keys()):
                if array[i] == item:
                    array.pop(i)
        else:
            for i, it in enumerate(array):
                if it == item:
                    array.pop(i)

        return op(array)

def reverseDictSearch(array: dict, value: _bm.Any) -> tuple:
    """
    Find the unknown key(s) of a value in a dictionary
    
    :param array: The dictionary to search
    :param value: The value to find the keys for
    """

    if not isinstance(array, dict):
        raise TypeError("Array must be a valid dictionary instance")

    # Create an isolated dict inside of the list to avoid
    # duplicate values getting merged/deleted
    swappedDict: list = [{v: k} for (k, v) in array.items()]
    results:     list = []

    for i in range(len(swappedDict)):
        try:
            results.append(swappedDict[i][value])
        except KeyError:
            continue
    
    if results == []:
        raise IndexError("There was no key matching the specified value")
    else:
        return tuple(results)

def getArrayValues(array: _bm.Union[list, tuple, dict]) -> tuple:
    """
    Recursively obtain all of the values of any keys or items within an array
    
    :param array: The iterable to get the values for
    """

    if not isinstance(array, (list, tuple, dict)):
        raise TypeError("Array must be a valid 'list', 'tuple' or 'dict' instance")

    values: list = []

    if isinstance(array, dict):
        items: list = [i[1] for i in array.items()]
    else:
        items: list = list(array)

    for i in items:
        if isinstance(i, dict):
            for ii in getArrayValues(i):
                values.append(ii) 
        elif isinstance(i, (list, tuple)):
            for ii in i:
                if isinstance(ii, (dict, list, tuple)):
                    for iii in getArrayValues(ii):
                        values.append(iii)
                else:
                    values.append(ii)
        else:
            values.append(i)

    return tuple(values)

def timeTest(method: _bm.Callable,
             accuracy: int=10,
             *args,
             **kwargs,
             ) -> float:
    """
    Run a method with optional kwargs {accuracy} amount of times, 
    sum then divide by {accuracy} for precise run time

    :param method: The method to test
    :param accuracy: How many times to run the method
    :param *args: Optional args to pass to the method
    :param **kwargs: Optional kwargs to pass to the method
    """

    from time import perf_counter

    avg: float = 0.0

    if not isinstance(accuracy, int):
        raise TypeError("Accuracy must be a valid 'int' instance")
    elif accuracy < 1:
        raise ValueError("Accuracy must be 1 or bigger")

    if not hasattr(method, "__call__"):
        raise TypeError("Method must be a callable instance")

    for i in range(accuracy):
        start = perf_counter()
        method(*args, **kwargs)
        avg += perf_counter() - start

    return avg / accuracy

def tgzOpen(file: str, 
            output: str=None,
            ) -> str:
    """
    Open a gzipped tar file
    
    :param file: The .tgz file to open
    :param output: The name and file path of the output file/folder
    """

    from tarfile import open as tOpen
    from gzip import open as gOpen
    from shutil import copyfileobj
    from os.path import abspath
    from os import remove

    if type(file) is not str:
        raise TypeError("File must be a valid 'str' instance")
    elif not _bm.exists(file):
        raise FileNotFoundError("Could not locate the specified gzipped tar file")
    else:
        file: str = abspath(file)

    if file.endswith(".tar.gz"):
        tfile: str = '.'.join(file.split('.')[:-1])
    else:
        tfile: str = '.'.join(file.split('.')[:-1]) + ".tar"

    if output is None:
        output: str = '.'.join(tfile.split('.')[:-1])
    elif not isinstance(output, str):
        raise TypeError("Output must be a valid 'str' instance")
    else:
        output: str = abspath(output)

    if _bm.exists(output) or _bm.exists(tfile):
        raise FileExistsError("Output file/folder already file exists")

    with gOpen(file, "rb") as _f, open(tfile, "wb") as _f2:
        copyfileobj(_f, _f2)

    with tOpen(tfile) as _f:
        _f.extractall(output)

    remove(tfile)

    return output

def lengthSort(array: _bm.Union[list, tuple, set, dict],
               fromLowest: bool=True,
               sortByKey: bool=False
               ) -> _bm.Union[list, tuple, set, dict]:
    """
    Sort an array by it's length
    
    :param array: The iterable to sort
    :param fromLowest: Whether to sort in ascending order
    :param sortByKey: Whether to instead sort by keys if the iterable is a dictionary
    """

    if not isinstance(array, (list, tuple, set, dict)):
        raise TypeError("Array must be a valid 'list', 'tuple', 'set' or 'dict' instance")
    elif len(array) == 0:
        raise ValueError("Array cannot be empty")
    
    if isinstance(array, (list, tuple, set)):
        return sorted(array, key=lambda l: len(l), reverse=not fromLowest)
    elif isinstance(array, dict):
        return dict(sorted(array.items(), key=lambda l: len(l[1 if sortByKey else 0]),
                           reverse=fromLowest)) # sorted() isn't flipped here for some reason,
                                                # that's why fromLowest is being passed as is

def dirVars(object: object, output: bool=True, 
            includePythonFuncs: bool=False, 
            format: str="%(name)s: %(value)s\n"
            ) -> _bm.Union[str, None]:
    """
    Get all of the attributes of an object and store/print them formatted
    
    :param object: The object to get the attributes for
    :param output: Whether to print the attributes formatted as they are obtained
    :param includePythonFuncs: Whether to include attributes prefixed and suffixed with a double underscore
    :param format: The format to use for each attribute in the object
    """

    if not isinstance(format, str):
        raise TypeError("Format must be a valid 'str' instance")

    if includePythonFuncs:
        objs = dir(object)
    else:
        objs = (i for i in dir(object) if not i.startswith("__") and not i.endswith("__"))

    if not output:
        text: str = ""

    for i in objs:
        v = format % {"name": i, "value": getattr(object, i)}

        if output:
            print(v, end="")
        else:
            text += v
    
    if not output:
        return text[:-1]

class subtractableList(list):
    """To create a list that can be subtracted from using an iterable that isn't a string or dictionary"""

    def __sub__(self, iterable: _bm.Iterable) -> list:
        if not isinstance(iterable, (list, set, tuple)):
            raise TypeError("Second argument of list subtraction operation must be a 'list', 'tuple' or 'set'")

        iterable: set = set(iterable)

        return [i for i in self.copy() if i not in iterable]
    
        # implementation 2
        # return set(self.copy()) - set(iterable)
        # does not preserve order of list though
        # and also removes duplicates from first list
        # even if they're not present in the second
        # unwanted behaviour...

class duplicateKeysDict():
    """
    Create a dictionary that allows for duplicate keys
    
    This class also implements some dunder and custom methods not present in the normal Python dict 
    """

    def __init__(self, iterable: _bm.Union[_bm.Iterable, _bm.GeneratorType]=None) -> None:
        """:param iterable: An iterable to be converted to a dict"""

        if iterable == None:
            self._dict: subtractableList = subtractableList()

            return

        if isinstance(iterable, (set, list, tuple)):
            try:
                dict(iterable)

                self._dict: subtractableList = subtractableList(iterable)
            except ValueError as err: 
                raise err
        elif isinstance(iterable, dict):
            self._dict: subtractableList = subtractableList(iterable.items())
        else:
            iterable = subtractableList(iterable)

            try:
                dict(iterable)

                self._dict: subtractableList = iterable
            except ValueError: 
                raise TypeError("Second argument of addition operation must be an iterable that is not a string")
    
    def __str__(self) -> str:
        return '{' + ", ".join(f"{repr(i[0])}: {repr(i[1])}" for i in self._dict) + '}'
    
    def __repr__(self) -> str:
        return self.__str__()

    def __add__(self, iterable: _bm.Iterable):
        if isinstance(iterable, (set, list, tuple)):
            try:
                dict(iterable)

                iterable = self._dict + list(iterable)
            except ValueError as err: 
                raise err
        elif isinstance(iterable, dict):
            iterable = self._dict + list(iterable.items())
        else:
            iterable = list(iterable)

            try:
                dict(iterable)

                iterable += self._dict
            except ValueError as err: 
                raise TypeError("Second argument of addition operation must be an iterable that is not a string")

        return duplicateKeysDict(iterable)

    def __sub__(self, iterable: _bm.Iterable):
        if isinstance(iterable, (set, list, tuple)):
            try:
                dict(iterable)

                iterable = self._dict - list(iterable)
            except ValueError as err: 
                raise err
        elif isinstance(iterable, dict):
            iterable = self._dict - list(iterable.items())
        else:
            try:
                iterable = subtractableList(iterable)

                dict(iterable)

                iterable -= self._dict
            except (ValueError, TypeError): 
                raise TypeError("Second argument of subtraction operation must be an iterable that is not a string")

        return duplicateKeysDict(iterable)
    
    def __mul__(self, value: int):
        if not isinstance(value, int):
            raise TypeError("Second argument of multiplication operation must be an integer")

        return duplicateKeysDict(self._dict * value)
    
    def __eq__(self, obj) -> bool:
        if self._dict == obj:
            return True
        else:
            return False

    def __len__(self) -> int:
        return len(self._dict)
    
    def __reversed__(self) -> _bm.Generator:
        return (i for i in self._dict[::-1])

    def __getitem__(self, key: _bm.Any) -> _bm.Union[tuple, _bm.Any]:
        items: tuple = tuple(i[1] for i in self._dict if key == i[0])

        if not items:
            raise KeyError(f"Key {repr(key)} not in dictionary")
        
        if len(items) > 1:
            return items
        else:
            return items[0]

    def __iter__(self) -> _bm.Generator:
        """
        By default, looping through the dictionary will return the result of `.keys()` 
        to maintain consistency with a normal Python dict and to also make checking 
        if a key is in the dictionary easier
        """

        return self.keys()

    def update(self, dictionary: dict) -> None:
        """Update the dictionary from the elements of another dictionary or duplicate key dictionary"""

        if not isinstance(dictionary, (dict, duplicateKeysDict)):
            raise TypeError("Dictionary must be a valid 'dict' instance")

        for k, v in dictionary.items():
            self._dict.append((k, v))
    
    def pop(self, key: _bm.Any, amount: int=-1) -> None:
        """Remove instances of the specified key"""

        if not isinstance(amount, int):
            raise TypeError("Amount must be a valid 'int' instance")

        if amount < 1 and amount != -1:
            raise ValueError("Amount must be -1 or greater than 0")
        
        # copy the internal list because removing items from the list 
        # while looping through it causes buggy behaviour
        for i in self._dict.copy():
            if amount == 0:
                break

            if amount != -1:
                amount -= 1
            
            if i[0] == key:
                self._dict.remove(i)

        # implementation 2
        # also loads the whole internal list into memory as I cannot find a solution that doesn't
        #
        # removedBefore: bool = False
        #
        # for i, it in tuple(enumerate(self._dict)):
        #     print(i, it, removedBefore)
        #
        #     if removedBefore:
        #         i -= 1
        #         it = self._dict[i]
        #
        #         removedBefore = False
        #
        #     if it[0] == key:
        #         self._dict.remove(it)
        #
        #         removedBefore = True
        #
        #     if amount == 0:
        #         break
        #
        #     if amount != -1:
        #         amount -= 1
    
    def items(self) -> _bm.Generator:
        """Return the dictionary as a key value tuple pair iterable"""

        return (i for i in self._dict)

    def keys(self) -> _bm.Generator:
        """Return the keys of the dictionary"""

        return (i[0] for i in self._dict)
    
    def values(self) -> _bm.Generator:
        """Return the values of the dictionary"""

        return (i[1] for i in self._dict)

    def copy(self):
        """Shallow copy the dictionary"""

        return self.shallow_copy()

    def shallow_copy(self):
        """Shallow copy the dictionary"""

        return duplicateKeysDict(self._dict.copy())
    
    def deep_copy(self):
        """Deep copy the dictionary (not thread safe and consumes more memory)"""

        from copy import deepcopy

        return duplicateKeysDict(deepcopy(self._dict))
    
    def clear(self) -> None:
        """Empty the dictionary"""

        self._dict = subtractableList()
    
    def get(self, key: _bm.Any, default: _bm.Any=None) -> _bm.Union[tuple, _bm.Any]:
        """Return the value(s) of the key in the dictionary, if not found, return default"""

        try:
            return self.__getitem__(key)
        except KeyError:
            return default
    
    def reverse(self) -> None:
        """Reverse the dictionary"""

        self._dict = subtractableList(self.__reversed__())

    def flip(self) -> None:
        """Flip the dictionary key and value pairs (k, v -> v, k)"""

        self._dict = subtractableList((v, k) for k, v in self.items())

class interpreter():
    """Custom top-level Python interpreter to add useful typing features"""

    def __init__(self, 
                 file: str,
                 output: str="%(name)s.interpreted.py",
                 override: bool=False,
                 ternary: bool=True,
                 comments: bool=True):
        """
        Custom top-level Python interpreter to add useful typing features
        
        :param file: The file to parse
        :param output: The name of the output file
        :param override: Whether to override an existing output file
        :param ternary: Whether to convert ternary statements
        :param comments: Whether to convert comments
        """

        from os.path import exists, abspath

        if not isinstance(file, str):
            raise TypeError("File must be a valid 'str' instance")

        if not exists(file):
            raise FileNotFoundError("Could not locate Python file")

        if not isinstance(output, str):
            raise TypeError("Output must be a valid 'str' instance")

        self.file: str = file

        if '.' in file:
            file: str = '.'.join(file.split('.')[0:-1])
        else:
            file: str = file

        self.output:        str = output % {"name": file}
        self.override:     bool = bool(override)
        self.ternary:      bool = bool(ternary)
        self.comments:     bool = bool(comments)
        self._interpreted: list = []

        if not self.override and exists(self.output):
            raise FileExistsError("Output file already present")

        try:
            with open(self.file) as _f:
                _content = _f.readlines()
        except IsADirectoryError:
            raise FileNotFoundError("There was a problem locating the file")

        for i in _content:
            if i.strip() == '\n' or i.strip() == "":
                self._interpreted.append(i)
            elif self.comments and i.lstrip()[:2] == "//":
                self._interpreted.append(self._convertComment(i))
            elif self.ternary and i.lstrip()[0] != '#' and len(i.split('=')) != 1 and \
                 len(i.split('=')[1].split('?')) != 1:
                self._interpreted.append(self._convertTernary(i))
            else:
                self._interpreted.append(i)

        with open(self.output, "a+") as _f:
            _f.truncate(0)
            _f.writelines(self._interpreted)
        
        self.file:   str = abspath(self.file)
        self.output: str = abspath(self.output)

    def __str__(self):
        return f"<Interpreter instance [{self.file.split(info._bm.split)[-1]}]>"
    
    def __repr__(self):
        return self.__str__()

    def _getIndent(self, line: str) -> str:
        return "".join([' ' for i in range(len(line) - len(line.lstrip()))])

    def _convertTernary(self, line: str) -> _bm.Union[str, None]:
        statement: list = line.split('=')

        try:
            condition: str = statement[1].split('?')[0][1:-1]
            values:   list = statement[1].split('?')[1].split(':')

            return "{} = {} if {} else {}\n".format(statement[0][:-1], values[0].strip(), condition, 
                                                    values[1].strip().replace('\n', ""))
        except Exception as error:
            raise error

    def _convertComment(self, line: str) -> _bm.Union[str, None]:
        return self._getIndent(line) + '#' + line.lstrip()[2:]

    def read(self) -> str:
        """Read the output file and return the content as a string"""

        if "".join(self._interpreted)[-1:] == '\n':
            return "".join(self._interpreted)[:-1]
        else:
            return "".join(self._interpreted)
    
    def readlines(self) -> list:
        """Read the output file and return the content as a list containing strings split at every newline"""

        return self._interpreted
