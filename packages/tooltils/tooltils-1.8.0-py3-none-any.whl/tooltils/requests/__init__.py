"""HTTP/1.1 simple interface"""


class _bm:
    from typing import Union, Dict, List, Callable

    from ..info import _logger, _loadConfig, _editCache, _deleteCacheKey, version
    from ._helpers import tooltilsResponse
    from ..errors import StatusCodeError
    from ..os import info

    class FileDescriptorOrPath:
        pass

    # fake type hints to avoid importing the real libraries
    # to help optimise slightly
    class HTTPResponse:
        pass

    class SSLContext:
        pass

    def propertyTest(value, types: tuple, name: str):
        if value is None:
            return types[0]()
        elif not isinstance(value, types):
            raise TypeError(name + " must be a valid '" + types[0].__name__ + "' instance")
        else:
            return value
    
    states: dict = {0: "Closed", 1: "Connected", 2: "Request in Progress"}

    logger = _logger("requests")

#_cachedConnections: dict = {}
#_pooling:           bool = bool(_bm._loadConfig('requests')['connectionCaching'])

import tooltils.requests.urllib as urllib


status_codes: _bm.Dict[int, str] = _bm.StatusCodeError.status_codes
"""List of official HTTP response status codes"""
defaultVerificationMethod:  bool = bool(_bm._loadConfig("requests")["defaultVerificationMethod"])
redirectLimit:               int = int(_bm._loadConfig("requests")["redirectLimit"])
StatusCodeError:       Exception = _bm.StatusCodeError

# to confuse the Python linter so that it registers advancedContext as a seperate
# class instead of an alias, looks nicer in code
class advancedContext():
    """Create an advanced context intended to be used for extended functionality with requesting"""

    def __init__(self, 
                 redirectLimit: int=redirectLimit, 
                 extraLogs: bool=False, 
                 SSLContext: _bm.SSLContext=None):
        """
        Create an advanced context intended to be used for extended functionality with requesting
        
        :param redirectLimit: How many times a request can be redirected before raising an error
        :param extraLogs: Whether to log extra information
        :param SSLContext: A custom SSLContext instance to override the request one
        """

        self.redirectLimit: int = redirectLimit
        self.extraLogs:    bool = extraLogs
        self.SSLContext         = SSLContext

advancedContext = urllib.advancedContext

def where() -> tuple:
    """Return default certificate file and path locations used by Python"""

    from ._helpers import where

    return where()

def connected() -> bool:
    """Get the connectivity status of the currently connected wifi network"""

    _bm.logger.debug("A blocking function was called and the cache may be updated", "connected()")

    from ._helpers import connected
    
    return connected()

def ctx(verify: bool=True, cert: str=None) -> _bm.SSLContext:
    """
    Create a custom SSLContext instance
    
    :param verify: Whether to apply setting to make the SSLContext instance verify with SSL
    :param cert: A custom certificate file to use in the SSLContext instance
    """

    from ._helpers import ctx

    return ctx(verify, cert)

def prep_url(url: str, 
             data: dict=None,
             https: bool=True,
             order: bool=False
             ) -> str:
    """
    Configure a URL making it viable for requests
    
    :param url: The URL to configure
    :param data: Data to add to the URL
    :param https: Whether to use a https or http schema in the URL
    :param order: Whether to order any data items added to the URL alphabetically
    """

    from ._helpers import prep_url

    return prep_url(url, data, https, order)

def verifiable() -> bool:
    """Determine whether requests can be verified with a valid ssl certificate on the current connection"""

    _bm.logger.debug("A blocking function was called and the cache may be updated", "verifiable()")

    from ..info import _loadCache, _loadConfig
    from ..os import getCurrentWifiName

    caching: bool = bool(_loadConfig("requests")["verifiableCaching"])
    wifiName: str = getCurrentWifiName()

    if wifiName == None:
        return False
    
    if caching:
        configData: dict = _loadConfig("requests")
        cacheData:  dict = _loadCache("requests")

        if cacheData["verifiableTimesChecked"] >= configData["verifiableCachingCheck"]:
            _bm._editCache("requests", {"verifiableTimesChecked": 0})
            _bm._deleteCacheKey("requests", wifiName, "verifiableNetworkList")
        else:
            if wifiName in list(cacheData["verifiableNetworkList"].keys()):
                _bm._editCache("requests", 
                  {"verifiableTimesChecked": cacheData["verifiableTimesChecked"] + 1})

                return cacheData["verifiableNetworkList"][wifiName]

    try:
        head("httpbin.org/get", mask=True, redirects=False)

        result: bool = True
    except Exception:
        result: bool = False

    if caching:
        _bm._editCache("requests", {wifiName: result}, "verifiableNetworkList")
        _bm._editCache("requests", {"verifiableTimesChecked": 1})

    return result

class tooltilsResponse(_bm.tooltilsResponse):
    """
    Create a tooltils style response class from the `http.client.HTTPResponse` attribute \n
    This class is not intended to be called directly because there is other data that requires
    attributes from the actual connection reference, but exists to allow Python text highlighters
    to show the return properties
    """

    def __init__(self, data: _bm.HTTPResponse, url: str, method: str, 
                 encoding: _bm.Union[str, tuple]=("utf-8", "ISO-8859-1"), 
                 _agent: str=None, _headers: dict=None, 
                 _clog: bool=None, _rID: int=-1,
                 _log: bool=True, _extra: bool=False):
        super().__init__(data, url, method, encoding, _agent, _headers, _clog, _rID,
                         _bm.logger if _log else None, _extra)

def _splitUrl(host: str, page: str, https: bool) -> tuple:
    error       = None
    url = _host = prep_url(host + (('/' + page) if page else ""), https=https)

    if page:
        _host: str = url.split('/')[2]
    
    _host = _host.replace("http" + ('s' if https else "") + "://", "")

    if '/' in _host:
        error = _bm.InvalidRequestURL("The host should only contain the website name and extension (etc httpbin.org)")
    elif '.' not in _host:
        error = _bm.InvalidRequestURL("The host should contain the website name and extension (etc httpbin.org)")

    if ':' in _host:
        error = _bm.InvalidRequestURL("You may not include a colon in the URL (this includes ports)")

    if error:
        raise error

    return (_host, '/'.join(url.split('/')[3:]) if page else "")

class openConnection():
    """Open a re-usable connection to a URL"""

    def __init__(self, 
                 host: str, 
                 port: int=(80, 443),
                 https: bool=True,
                 verify: bool=defaultVerificationMethod,
                 redirects: bool=True,
                 redirect_loops: bool=False,
                 auth: tuple=None,
                 data: dict=None,
                 headers: dict=None,
                 cookies: dict=None,
                 cert: str=None,
                 file_name: str=None,
                 write_binary: bool=False,
                 override: bool=False,
                 timeout: _bm.Union[int, float]=15,
                 encoding: _bm.Union[str, tuple]=("utf-8", "ISO-8859-1"),
                 mask: bool=False,
                 agent: str=None,
                 onStatusError: _bm.Union[_bm.Callable[..., Exception], Exception]=StatusCodeError,
                 proxy: str=None,
                 advContext: advancedContext=None,
                 _clog: bool=True,
                 _redirect: bool=False):
        """
        Open a re-usable connection to a URL

        :param host: The host to open the connection on
        :param port: The port to make the connection on
        :param https: Whether to use https
        :param verify: Whether to verify the request with SSL
        :param redirects: Whether the request can redirect
        :param redirect_loops: Whether the request can enter a redirect loop
        :param auth: Basic authentication in a tuple user-pass pair
        :param data: Data to send to the url as a dictionary
        :param headers: Headers to send to the url as a dictionary
        :param cookies: Cookies to send to the url in the headers as a dictionary
        :param cert: The certificate to verify the request's SSL connection
        :param file_name: The file name and or path to use if the request was a download
        :param write_binary: Whether to write the request file as a binary file
        :param override: Whether to override an existing file with the request file
        :param timeout: How long the request should last before being terminated
        :param encoding: The codec(s) to use to decode the request response
        :param mask: Whether to make the user-agent header that of a browser's to anonymise the request
        :param agent: Overwrite for the user-agent header
        :param onStatusError: A custom exception that can be passed to be raised instead of the default one when the request's status is >= 400
        :param proxy: The proxy to use for the request in the format '{host}:{port}'
        :param advContext: A tooltils.requests.advancedContext instance to provide advanced parameters
        """

        # this is for logging to help differentiate requests
        self.rID      = urllib._bm.newestID
        urllib._bm.newestID += 1

        if _redirect:
            self.rID     -= 1
            urllib._bm.newestID -= 1
        
        self._redirect = _redirect
        #self._cached   = False

        # variables that are defined once and never changed
        self._setStartVariables(host, port, https, verify, cert, timeout, proxy, advContext)

        # variables that may change
        self._setVariables(redirects, redirect_loops, auth, data, headers, cookies, 
                           file_name, write_binary, override, encoding, mask, agent,
                           onStatusError)

        self._setState(0)

        self._clog:  bool = bool(_clog)
        self._caller: str = "openConnection()" if _clog else "request()"

        if _clog and not _redirect:
            _bm.logger.debug(f"Setting up http{'s' if self.https else ''}/1.1 "
                             f"connection to <{self._host}:{self.port}", 
                             "openConnection()", self.rID)
        
        if self.port != 80 and self.port != 443 and not _redirect:
            _bm.logger.debug("Connection is not using port 80 or 443, it may fail", 
                             self._caller, self.rID)
        
        # create connection reference
        self._setup()

        # start the connection
        self.open()

    def __str__(self):
        return f"<Connection {self._host} [{self.state}]>"
    
    def __repr__(self):
        return self.__str__()
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type == None:
            self._setState(1)
            self.close()

            return True
    
    def _setStartVariables(self, host: str, port: int, https: bool, verify: bool,
                           cert: str, timeout: _bm.Union[int, float], proxy: str, 
                           advContext: advancedContext):
        from os.path import exists

        from ..errors import InvalidRequestURL

        error = None

        self.verify: bool = bool(verify)
        self.https:  bool = bool(https)
        self.host:    str = _splitUrl(host, "", https)[0]
        self._host:   str = self.host.replace("http" + ('s' if self.https else "") + "://", "")

        if '/' in self._host:
            error = InvalidRequestURL("The host should only contain the website name and extension (etc httpbin.org)")
        elif '.' not in self._host:
            error = InvalidRequestURL("The host should contain the website name and extension (etc httpbin.org)")

        if ':' in self._host:
            error = InvalidRequestURL("You may not include a colon in the URL (this includes ports)")

        if self.https and self.verify:
            if cert is None:
                self.cert: str = where()[1]
            else:
                if not isinstance(cert, str):
                    error = TypeError("Certificate must be a valid 'str' instance")
                elif cert.split('.')[-1] != "pem":
                    error = FileNotFoundError("Invalid certificate file path")
                elif not exists(cert) and cert != where()[1]:
                    error = FileNotFoundError("The certificate file does not exist")
                else:
                    self.cert = cert
        else:
            self.cert = None

        if not isinstance(timeout, (int, float)):
            error = TypeError("Timeout must be a valid 'int' or 'float' instance")
        else:
            self.timeout: _bm.Union[int, float] = timeout

        if port == (80, 443):
            self.port: int = int(443 if self.https else 80)
        elif not isinstance(port, int):
            error = TypeError("Port must be a valid 'int' instance")
        else:
            self.port: int = port
        
        if proxy is None:
            self.proxy = None
        elif not isinstance(proxy, str):
            error = TypeError("Proxy must be a valid 'str' instance")
        else:
            if ':' not in proxy:
                error = ValueError("Proxy must have the format 'host:port'")
            else:
                self.proxy: str = proxy

        if advContext is None:
            self.advContext         = None
            self.redirectLimit: int = redirectLimit
            self.extraLogs:    bool = False
            self.SSLContext         = None
        elif not isinstance(advContext, advancedContext):
            error = TypeError("AdvContext must be a valid 'tooltils.requests.advancedContext' instance")
        else:
            self.advContext         = advContext
            self.redirectLimit: int = advContext.redirectLimit
            self.extraLogs:    bool = advContext.extraLogs
            self.SSLContext         = advContext.SSLContext

        if error:
            raise error

    def _setVariables(self, redirects: bool, redirect_loops: bool, auth: tuple, 
                      data: dict, headers: dict, cookies: dict, file_name: str,
                      write_binary: bool, override: bool, 
                      encoding: _bm.Union[str, tuple], mask: bool, agent: str,
                      onStatusError: Exception=StatusCodeError, set: bool=True):
        error = None

        if auth and not isinstance(auth, tuple):
            error = TypeError("Authentiction must be a valid 'tuple' instance")
        elif auth and len(auth) != 2:
            error = ValueError("Invalid authentication details")

        if file_name and not isinstance(file_name, str):
            error = TypeError("File_name must be a valid 'str' instance")

        if agent and not isinstance(agent, str):
            error = TypeError("Agent must be a valid 'str' instance")

        if not isinstance(encoding, (str, tuple)):
            error = TypeError("Encoding must be a valid 'str' or 'tuple' instance")
        
        if onStatusError and onStatusError != StatusCodeError and Exception not in StatusCodeError.__bases__:
            error = TypeError("OnStatusError must be a valid 'Exception' or 'NoneType' instance")
        
        if error:
            raise error
        
        if set:
            self.redirects:      bool = bool(redirects)
            self.redirect_loops: bool = bool(redirect_loops)
            self.write_binary:   bool = bool(write_binary)
            self.redirects:      bool = bool(redirects)
            self.override:       bool = bool(override)
            self.mask:           bool = bool(mask)
            self.cookies:        dict = dict(_bm.propertyTest(cookies, (dict,), "Cookies"))
            self.headers:        dict = dict(_bm.propertyTest(headers, (dict,), "Headers"))
            self.data:           dict = dict(_bm.propertyTest(data, (dict, ), "Data"))
            self.agent:           str = agent
            self.file_name:       str = file_name
            self.auth:     tuple[str] = auth
            self.onStatusError:        Exception = onStatusError
            self.encoding: _bm.Union[str, tuple] = encoding
        else:
            return {"redirects": bool(redirects), "redirect_loops": bool(redirect_loops), 
                    "auth": auth, "data": data, 
                    "headers": dict(_bm.propertyTest(headers, (dict,), "Headers")), 
                    "cookies": dict(_bm.propertyTest(cookies, (dict,), "Cookies")), 
                    "file_name": file_name, "write_binary": bool(write_binary), 
                    "override": bool(override), "encoding": encoding, 
                    "mask": bool(mask), "agent": agent, "onStatusError": onStatusError}
    
    def _setup(self) -> None:
        from http.client import HTTPSConnection, HTTPConnection

        #global _cachedConnections

        #key: tuple = (self._host, self.port, self.proxy, self.https, 
        #              self.verify, self.cert, self.timeout, str(self.advContext))

        #if _pooling and key in _cachedConnections:
        #    # if existing conn is open and also free to make a request
        #    if _cachedConnections[key]._tooltilsState == 1:
        #        print(True)
        #        self._req          = _cachedConnections[key]
        #        self._cached: bool = True
        #
        #        self._setState(1)
        #
        #        return

        if self.proxy:
            self._req = HTTPConnection(self.proxy.split(':')[0], 
                                       self.proxy.split(':')[1], 
                                       timeout=self.timeout)

            self._req.set_tunnel(self._host, self.port)
        elif self.https:
            if self.SSLContext:
                _ctx = self.SSLContext

                if self.extraLogs and not self._redirect:
                    caller: str = (self._caller + ".open()") if "openConnection" in self._caller else self._caller

                    _bm.logger.debug("Using custom SSLContext instance", caller, self.rID)
            else:
                _ctx = ctx(self.verify, self.cert)

                if self.extraLogs and not self._redirect:
                    caller: str = (self._caller + ".open()") if "openConnection" in self._caller else self._caller

                    _bm.logger.debug("Using request created SSLContext instance", caller, self.rID)

            self._req = HTTPSConnection(self._host, self.port, 
                                        timeout=self.timeout, 
                                        context=_ctx)
        else:
            self._req = HTTPConnection(self._host, self.port, 
                                       timeout=self.timeout)
        
        #self._req._tooltilsState = 0

        #if _pooling:
        #    _cachedConnections[key] = self._req
    
    def _setState(self, state: int) -> None:
        if "state" not in (i for i in dir(self) if "__" not in i):
            self._state: int = 0
            self.state:  str = str("Defined")
        else:
            #self._req._tootlilsState = state

            self._state: int = state
            self.state:  str = str(_bm.states[state])
    
    def _prepare(self, method: str, auth: tuple, data: dict, headers: dict, 
                 cookies: dict, mask: str, agent: str, close: bool,
                 _redirect: bool) -> None:
        from json import dumps

        _headers = {}
        _data    = None

        if not close:
            connection: str = "keep-alive"
        else:
            connection: str = "close"
        
        if agent is None:
            agent: str = f"Python-tooltils/{_bm.version}"

        if mask:
            if _bm.info.platform.lower() == "windows":
                agent: str = "Windows NT 10.0; Win64; x64"
            elif _bm.info.platform.lower() == "macos":
                agent: str = "Macintosh; Intel Mac OS X 14.2"
            else:
                agent: str = "X11; Ubuntu; Linux i686"
            
            agent: str = str("Mozilla/5.0 (" + agent + "; rv:109.0) Gecko/20100101 Firefox/121.0")

        if (method == "POST" or method == "PUT") and data:
            _data: dict = dumps(data).encode()

            _headers.update({"Content-Length": str(len(_data))})

            if self.extraLogs and not _redirect:
                _bm.logger.debug("Adding 'Content-Length' to headers because the method is POST or PUT", 
                                 f"{self._caller}.send()", self.rID)

        elif method == "TRACE":
            _headers.update({"Content-Type": "message/http"})

            if self.extraLogs and not _redirect:
                _bm.logger.debug("Adding 'Content-Type': 'message/http' to headers because the method is TRACE", 
                                 f"{self._caller}.send()", self.rID)

        _headers.update({"Connection": connection, "User-Agent": agent, 
                         "Accept": "*/*", "Accept-Encoding": "gzip, deflate"})
        
        for i in cookies.keys():
            _headers.update({"Cookie", f"{str(i)}={str(cookies[i])}"})
        
        if auth:
            _headers.update({"Authorization": _bm.basicAuth(auth[0], auth[1])})

        if self.extraLogs and not _redirect:
            _bm.logger.debug("Adding necessary request headers", 
                             f"{self._caller}.send()", self.rID)

            if cookies:
                _bm.logger.debug("Adding cookies to request headers", 
                                 f"{self._caller}.send()", self.rID)
            
            if auth:
                _bm.logger.debug("Adding authorisation to request headers", 
                                 f"{self._caller}.send()", self.rID)
        
        _headers.update(headers)

        return (_data, _headers)
    
    def close(self, _err: bool=False) -> None:
        """Close the connection to the host"""

        from ..errors import ConnectionError

        error = None

        if self._state == 0:
            error = ConnectionError("The connection to the host has not been opened yet", self.host)
        elif self._state == 2:
            error = ConnectionError("A request is currently in progress", self.host)
        
        if error:
            raise error
        
        self._req.close()
        
        self._setState(0)

        caller: str = "close()" if self._clog else "send()"

        if not self._redirect and not _err:
            _bm.logger.debug("The connection was closed", f"{self._caller}.{caller}", self.rID)

    def open(self) -> None:
        """Open the connection to the host"""

        from ssl import SSLCertVerificationError
        from http.client import InvalidURL
        from socket import gaierror

        from ..errors import (ConnectionError, InvalidRequestURL,
                              ActiveRequestError, SSLCertificateFailed,
                              InvalidWifiConnection, ConnectionTimeoutExpired)

        error = None

        if self._state == 1:
            error = ConnectionError("The connection to the host is already active", self.host)
        elif self._state == 2:
            error = ConnectionError("A request is currently in progress", self.host)

        caller: str = "open()" if self._clog else "send()"

        try:
            self._req.connect()
        except InvalidURL as err:
            if "nonnumeric port" in str(err):
                error = InvalidRequestURL("You may not include a colon in the URL (this includes ports)")
            elif "control characters" in str(err):
                error = InvalidRequestURL("URL contains intransmissible characters")
            else:
                error = InvalidRequestURL("An unknown url related error occured, check the above stack trace for more info")
        except ConnectionResetError:
            error = ActiveRequestError("The host ended the connection without a response", self.host)
        except SSLCertVerificationError:
            error = SSLCertificateFailed()
        except gaierror:
            # call the _helpers.py version because it doesn't have the different logging call

            from ._helpers import connected

            if connected():
                error = _bm.StatusCodeError(404)
            else:
                error = InvalidWifiConnection()

            if not self._redirect:
                _bm.logger.debug("tooltils.requests.connected() was called and may update the cache", 
                                 f"{self._caller}.{caller}", self.rID)
        except TimeoutError:
            error = ConnectionTimeoutExpired(timeout=self.timeout)
        except OSError as err:
            if "[WinError 10051]" in str(err):
                error = ActiveRequestError("The host ended the connection without a response", self.host)
            else:
                error = ConnectionError("An unknown error occured, check the above stack trace for more info")

        if error:
            raise error

        self._setState(1)

        if not self._redirect:
            _bm.logger.debug("The connection was opened",
                             f"{self._caller}.{caller}", self.rID)

    def change(self, **params: object) -> None:
        """
        Change the data being sent for requests made to this host \n
        You may pass the parameters `redirects`, `redirect_loops`, `auth`, `data`, `headers`, `cookies`, `cert`,
        `file_name`, `write_binary`, `override`, `encoding`, `mask`, `agent` and `onStatusError` as seen 
        in the `openConnection` class definition
        """

        self._setVariables(
            params.get("redirects", self.redirects), params.get("redirect_loops", self.redirect_loops),
            params.get("auth", self.auth), params.get("date", self.data),
            params.get("headers", self.headers), params.get("cookies", self.cookies),
            params.get("file_name", self.file_name), params.get("write_binary", self.write_binary),
            params.get("override", self.override), params.get("encoding", self.encoding),
            params.get("mask", self.mask), params.get("agent", self.agent),
            params.get("onStatusError", self.onStatusError)
        )

    def send(self,
             method: str="GET",
             page: str="",
             close: bool=False,
             **params: object
             ) -> tooltilsResponse:
        """
        Send the request to the host \n
        You may pass any kwarg parameters from the `.change()` method as kwargs for single use request data

        :param method: The method to use in the request
        :param page: The page of the host to request
        :param close: Whether to close the connection after the request
        """

        from ssl import SSLError, SSLCertVerificationError
        from os.path import exists, abspath
        from os import remove

        from ..errors import ConnectionError, ActiveRequestError, SSLCertificateFailed, ConnectionTimeoutExpired

        error = None

        if self._state == 0:
            error = ConnectionError("The connection is currently closed")
        elif self._state == 2:
            error = ConnectionError("There is currently a request in progress")

        if error:
            raise error

        self._setState(2)

        newData = self._setVariables(
            params.get("redirects", self.redirects), params.get("redirect_loops", self.redirect_loops),
            params.get("auth", self.auth), params.get("date", self.data), 
            params.get("headers", self.headers), params.get("cookies", self.cookies), 
            params.get("file_name", self.file_name), params.get("write_binary", self.write_binary), 
            params.get("override", self.override), params.get("encoding", self.encoding), 
            params.get("mask", self.mask), params.get("agent", self.agent), 
            params.get("onStatusError", self.onStatusError), set=False
        )

        redirects:          bool = newData["redirects"]
        redirect_loops:     bool = newData["redirect_loops"]
        auth:              tuple = newData["auth"]
        data:               dict = newData["data"]
        headers:            dict = newData["headers"]
        cookies:            dict = newData["cookies"]
        file_name:           str = newData["file_name"]
        write_binary:       bool = newData["write_binary"]
        override:           bool = newData["override"]
        encoding:          tuple = newData["encoding"]
        mask:               bool = newData["mask"]
        agent:               str = newData["agent"]
        onStatusError: Exception = newData["onStatusError"]

        rData: dict = params.get("_redirectData", {})

        if isinstance(method, str):
            from ._helpers import httpMethods

            if method.upper() not in httpMethods:
                error = ValueError(f"Unknown http method '{method}'")
            else:
                _method = method = method.upper()

            if method == "DOWNLOAD":
                _method: str = "GET"
        else:
            error = TypeError("Method must be a valid 'str' instance")

        if isinstance(page, str):
            if page and '/' not in page:
                page = '/' + page

            try:
                if page[-1] == '/':
                    page = page[:-1]
            except IndexError:
                pass
        else:
            error = TypeError("Page must be a valid 'str' instance")

        if error:
            raise error

        try:
            _data, _headers = self._prepare(method, auth, data, headers, cookies,
                                            mask, agent, close, bool(rData))

            if not rData:
                _bm.logger.debug(f"Sending {method} request", f"{self._caller}.send()", self.rID)

            self._req.putrequest(_method, page)

            if not rData and self.extraLogs:
                _bm.logger.debug(f"Sending headers: {_headers}",
                                 f"{self._caller}.send()", self.rID)

            for k, v in _headers.items():
                self._req.putheader(k, v)

            if _data and self.extraLogs:
                _bm.logger.debug(f"Sending data with length: {len(_data)}",
                                 f"{self._caller}.send()", self.rID)

            self._req.endheaders(_data if _data else None)
    
            rdata = self._req.getresponse()

            redirectDir = rdata.getheader("location")

            if not rData and not (rdata.status >= 400 and onStatusError):
                _bm.logger.debug("Obtained request response",
                                 f"{self._caller}.send()", self.rID)

            resp = tooltilsResponse(rdata, self.host + page, method, encoding,
                                    _headers["User-Agent"], _headers, self._clog,
                                    self.rID, not bool(redirectDir))

            self.state:  str = str("Connected")
            self._state: int = int(1)

            if rdata.status >= 400 and onStatusError:
                if onStatusError == StatusCodeError:
                    error = _bm.StatusCodeError(rdata.status, rdata.reason)
                else:
                    # check if the custom exception has been passed as an object or name
                    if hasattr(onStatusError, "__name__"):
                        error = onStatusError()
                    else:
                        error = onStatusError
            elif redirects and redirectDir:
                from ._helpers import validateRedirect

                rHost, rPage, rData = validateRedirect(redirectDir, rData, redirect_loops,
                                                       self.redirectLimit, self.https)

                _bm.logger.debug(f"Redirected: {rHost + rPage}",
                                 f"{self._caller}.send()", self.rID)

                if rHost == self.host:
                    return self.send(method, rPage, close, _redirectData=rData,
                                     redirects=redirects, redirect_loops=redirect_loops,
                                     auth=auth, data=data, headers=headers, cookies=cookies,
                                     file_name=file_name, write_binary=write_binary,
                                     override=override, encoding=encoding, mask=mask,
                                     agent=agent, onStatusError=onStatusError)
                else:
                    return openConnection(rHost, self.port, self.https, self.verify, redirects,
                                          redirect_loops, auth, data, headers, cookies, self.cert, 
                                          file_name, write_binary, override, self.timeout, 
                                          encoding, mask, agent, onStatusError, self.proxy,
                                          self.advContext, self._clog, True).send(method, rPage, True,
                                                                                  _redirectData=rData)
        except ConnectionResetError:
            error = ActiveRequestError("The host or client ended the connection without a response", self.host + page)
        except TimeoutError:
            error = ConnectionTimeoutExpired(timeout=self.timeout)
        except SSLCertVerificationError:
            error = SSLCertificateFailed()
        except SSLError:
            from ._helpers import connected

            if connected():
                error = SSLCertificateFailed()
            else:
                error = ConnectionError("The connection was forcibly closed by the client")
            
            if not rData:
                _bm.logger.debug("tooltils.requests.connected() was called and may update the cache", 
                                 f"{self._caller}.send()", self.rID)
        except OSError:
            error = ConnectionError("An unknown error occured, check the above stack trace for more info")
        
        self._setState(1)
    
        if close:
            self.close(True)

        if error:
            _bm.logger.debug(f"Request failed due to: {type(error).__name__}",
                             f"{self._caller}.send()", self.rID)

            if self.port != 80 and self.port != 443:
                _bm.logger.debug("Request may have failed due to the port not being set to 80 or 443",
                                 f"{self._caller}.send()", self.rID)

            raise error

        resp.redirected = bool(rData)

        if method == "DOWNLOAD":
            if file_name == None:
                try:
                    file_name = page.split('/')[-1]
                except IndexError:
                    file_name = self._host + ".downloadfile"

            if override and exists(file_name):
                remove(file_name)
            elif exists(file_name):
                raise FileExistsError("The requested file already exists on the disk")
                
            # test if the file_name is sanitary
                
            try:
                with open(file_name, "a+") as _f:
                    pass

                remove(file_name)
            except OSError:
                raise FileNotFoundError("Unable to locate valid file_name descriptor from request url")

            if write_binary:
                with open(file_name, "wb+") as _f:
                    _f.write(resp.raw)
            else:
                with open(file_name, "a+") as _f:
                    _f.write(resp.text)

            resp.path = abspath(file_name)
            
        return resp

class request():
    """Open a single-use connection to a URL"""

    def __init__(self, 
                 url: str,
                 method: str,
                 port: int=(80, 443),
                 https: bool=True,
                 verify: bool=defaultVerificationMethod,
                 redirects: bool=True,
                 redirect_loops: bool=False,
                 auth: tuple=None,
                 data: dict=None,
                 headers: dict=None,
                 cookies: dict=None,
                 cert: str=None, 
                 file_name: str=None,
                 write_binary: bool=False,
                 override: bool=False,
                 timeout: _bm.Union[int, float]=15, 
                 encoding: _bm.Union[str, tuple]=("utf-8", "ISO-8859-1"),
                 mask: bool=False,
                 agent: str=None,
                 onStatusError: _bm.Union[_bm.Callable[..., Exception], Exception]=StatusCodeError,
                 proxy: str=None,
                 advContext: advancedContext=None):
        """
        Open a single-use connection to a URL

        :param url: The URL to request
        :param method: The http method to use
        :param port: The port to make the connection on
        :param https: Whether to use https
        :param verify: Whether to verify the request with SSL
        :param redirects: Whether the request can redirect
        :param redirect_loops: Whether the request can enter a redirect loop
        :param auth: Basic authentication in a tuple user-pass pair
        :param data: Data to send to the url as a dictionary
        :param headers: Headers to send to the url as a dictionary
        :param cookies: Cookies to send to the url in the headers as a dictionary
        :param cert: The certificate to verify the request's SSL connection
        :param file_name: The file name and or path to use if the request was a download
        :param write_binary: Whether to write the request file as a binary file
        :param override: Whether to override an existing file with the request file
        :param timeout: How long the request should last before being terminated
        :param encoding: The codec(s) to use to decode the request response
        :param mask: Whether to make the user-agent header that of a browser's to anonymise the request
        :param agent: Overwrite for the user-agent header
        :param onStatusError: A custom exception that can be passed to be raised instead of the default one when the request's status is >= 400
        :param proxy: The proxy to use for the request in the format '{host}:{port}'
        :param advContext: A tooltils.requests.advancedContext instance to provide advanced parameters
        """
        
        if isinstance(method, str):
            from ._helpers import httpMethods

            if method.upper() not in httpMethods:
                raise ValueError(f"Unknown http method '{method}'")
            else:
                self.method = method.upper()
        else:
            raise TypeError("Method must be a valid 'str' instance")
        
        if port == (80, 443):
            port = 443 if https else 80
        
        url = url.replace("https://", "").replace("http://", "")

        host, self._page = _splitUrl(url.split('/')[0] if '/' in url else url, 
                                     '/'.join(url.split('/')[1:]) if '/' in url else "", https)

        sch = "http" + ('s' if https else "")
        url = sch + "://" + host + '/' + self._page

        _bm.logger.debug(f"Setting up http{sch}/1.1 {self.method} request to "
                         f"<{url.replace(sch + '://', '')}:{port}>", "request()", urllib._bm.newestID)

        self._req = openConnection(host, port, https, verify, redirects, redirect_loops,
                                   auth, data, headers, cookies, cert, file_name,
                                   write_binary, override, timeout, encoding, mask, agent,
                                   onStatusError, proxy, advContext, _clog=False)

        self.redirected: bool = False
        self.sent:       bool = False
        self.rID:         int = self._req.rID

        self.url:             str = url
        self.port:            int = port
        self.https:          bool = https
        self.verify:         bool = verify
        self.redirects:      bool = redirects
        self.redirect_loops: bool = redirect_loops
        self.auth:          tuple = auth
        self.data:           dict = data
        self.headers:        dict = headers
        self.cookies:        dict = cookies
        self.cert:            str = cert
        self.file_name:       str = file_name
        self.write_binary:   bool = write_binary
        self.override:       bool = override
        self.mask:           bool = mask
        self.agent:           str = agent
        self.proxy:           str = proxy
        self.timeout:  _bm.Union[int, float] = timeout
        self.encoding: _bm.Union[str, tuple] = encoding
        self.advContext:     advancedContext = advContext
        self.onStatusError:        Exception = onStatusError

    def __str__(self):
        return "<{} {} {}>".format(
            self.method,
            self._host if self.method != "DOWNLOAD" else self.file_name,
            "[Unsent]" if not self.sent else f"[{self._code}]"
        )
    
    def __repr__(self):
        return self.__str__()
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type == None:
            self._req._state = 1
            self._req.close()

            return True

    def send(self) -> tooltilsResponse:
        """Send the request"""

        resp = self._req.send(self.method, ('/' + self._page) if self._page else "", True)

        self._code:       int = resp.code
        self.redirected: bool = True if resp.redirected else False

        return resp

def get(url: str,
        port: int=(80, 443),
        https: bool=True,
        verify: bool=defaultVerificationMethod,
        redirects: bool=True,
        redirect_loops: bool=False,
        auth: tuple=None,
        data: dict=None,
        headers: dict=None,
        cookies: dict=None,
        cert: _bm.FileDescriptorOrPath=None, 
        timeout: _bm.Union[int, float]=15, 
        encoding: _bm.Union[str, tuple]=("utf-8", "ISO-8859-1"),
        mask: bool=False,
        agent: str=None,
        onStatusError: _bm.Union[_bm.Callable[..., Exception], Exception]=StatusCodeError,
        proxy: str=None,
        advContext: advancedContext=None
        ) -> tooltilsResponse:
    """
    Send a GET request

    :param url: The URL to request
    :param port: The port to make the connection on
    :param https: Whether to use https
    :param verify: Whether to verify the request with SSL
    :param redirects: Whether the request can redirect
    :param redirect_loops: Whether the request can enter a redirect loop
    :param auth: Basic authentication in a tuple user-pass pair
    :param data: Data to send to the url as a dictionary
    :param headers: Headers to send to the url as a dictionary
    :param cookies: Cookies to send to the url in the headers as a dictionary
    :param cert: The certificate to verify the request's SSL connection
    :param timeout: How long the request should last before being terminated
    :param encoding: The codec(s) to use to decode the request response
    :param mask: Whether to make the user-agent header that of a browser's to anonymise the request
    :param agent: Overwrite for the user-agent header
    :param onStatusError: A custom exception that can be passed to be raised instead of the default one when the request's status is >= 400
    :param proxy: The proxy to use for the request in the format '{host}:{port}'
    :param advContext: A tooltils.requests.advancedContext instance to provide advanced parameters
    """

    return request(url, "GET", port, https, verify, redirects,
                   redirect_loops, auth, data, headers, cookies, 
                   cert, None, None, None, timeout, encoding, 
                   mask, agent, onStatusError, proxy, advContext).send()

def post(url: str,
         port: int=(80, 443),
         https: bool=True,
         verify: bool=defaultVerificationMethod,
         redirects: bool=True,
         redirect_loops: bool=False,
         auth: tuple=None,
         data: dict=None,
         headers: dict=None,
         cookies: dict=None,
         cert: str=None, 
         timeout: _bm.Union[int, float]=15, 
         encoding: _bm.Union[str, tuple]=("utf-8", "ISO-8859-1"),
         mask: bool=False,
         agent: str=None,
         onStatusError: _bm.Union[_bm.Callable[..., Exception], Exception]=StatusCodeError,
         proxy: str=None,
         advContext: advancedContext=None
         ) -> tooltilsResponse:
    """
    Send a POST request

    :param url: The URL to request
    :param port: The port to make the connection on
    :param https: Whether to use https
    :param verify: Whether to verify the request with SSL
    :param redirects: Whether the request can redirect
    :param redirect_loops: Whether the request can enter a redirect loop
    :param auth: Basic authentication in a tuple user-pass pair
    :param data: Data to send to the url as a dictionary
    :param headers: Headers to send to the url as a dictionary
    :param cookies: Cookies to send to the url in the headers as a dictionary
    :param cert: The certificate to verify the request's SSL connection
    :param timeout: How long the request should last before being terminated
    :param encoding: The codec(s) to use to decode the request response
    :param mask: Whether to make the user-agent header that of a browser's to anonymise the request
    :param agent: Overwrite for the user-agent header
    :param onStatusError: A custom exception that can be passed to be raised instead of the default one when the request's status is >= 400
    :param proxy: The proxy to use for the request in the format '{host}:{port}'
    :param advContext: A tooltils.requests.advancedContext instance to provide advanced parameters
    """

    return request(url, "POST", port, https, verify, redirects,
                   redirect_loops, auth, data, headers, cookies, 
                   cert, None, None, None, timeout, encoding, 
                   mask, agent, onStatusError, proxy, advContext).send()

def download(url: str,
             port: int=(80, 443),
             https: bool=True,
             verify: bool=defaultVerificationMethod,
             redirects: bool=True,
             redirect_loops: bool=False,
             auth: tuple=None,
             data: dict=None,
             headers: dict=None,
             cookies: dict=None,
             cert: str=None, 
             file_name: str=None,
             write_binary: bool=False,
             override: bool=False,
             timeout: _bm.Union[int, float]=15, 
             encoding: _bm.Union[str, tuple]=("utf-8", "ISO-8859-1"),
             mask: bool=False,
             agent: str=None,
             onStatusError: _bm.Union[_bm.Callable[..., Exception], Exception]=StatusCodeError,
             proxy: str=None,
             advContext: advancedContext=None
             ) -> tooltilsResponse:
    """
    Download a file onto the disk

    :param url: The URL to request
    :param port: The port to make the connection on
    :param https: Whether to use https
    :param verify: Whether to verify the request with SSL
    :param redirects: Whether the request can redirect
    :param redirect_loops: Whether the request can enter a redirect loop
    :param auth: Basic authentication in a tuple user-pass pair
    :param data: Data to send to the url as a dictionary
    :param headers: Headers to send to the url as a dictionary
    :param cookies: Cookies to send to the url in the headers as a dictionary
    :param cert: The certificate to verify the request's SSL connection
    :param file_name: The file name and or path to use if the request was a download
    :param write_binary: Whether to write the request file as a binary file
    :param override: Whether to override an existing file with the request file
    :param timeout: How long the request should last before being terminated
    :param encoding: The codec(s) to use to decode the request response
    :param mask: Whether to make the user-agent header that of a browser's to anonymise the request
    :param agent: Overwrite for the user-agent header
    :param onStatusError: A custom exception that can be passed to be raised instead of the default one when the request's status is >= 400
    :param proxy: The proxy to use for the request in the format '{host}:{port}'
    :param advContext: A tooltils.requests.advancedContext instance to provide advanced parameters
    """

    return request(url, "DOWNLOAD", port, https, verify, redirects,
                   redirect_loops, auth, data, headers, cookies, cert, 
                   file_name, write_binary, override, timeout, encoding, 
                   mask, agent, onStatusError, proxy, advContext).send()

def head(url: str,
         port: int=(80, 443),
         https: bool=True,
         verify: bool=defaultVerificationMethod,
         redirects: bool=True,
         redirect_loops: bool=False,
         auth: tuple=None,
         data: dict=None,
         headers: dict=None,
         cookies: dict=None,
         cert: str=None, 
         timeout: _bm.Union[int, float]=15, 
         encoding: _bm.Union[str, tuple]=("utf-8", "ISO-8859-1"),
         mask: bool=False,
         agent: str=None,
         onStatusError: _bm.Union[_bm.Callable[..., Exception], Exception]=StatusCodeError,
         proxy: str=None,
         advContext: advancedContext=None
         ) -> tooltilsResponse:
    """
    Send a HEAD request

    :param url: The URL to request
    :param port: The port to make the connection on
    :param https: Whether to use https
    :param verify: Whether to verify the request with SSL
    :param redirects: Whether the request can redirect
    :param redirect_loops: Whether the request can enter a redirect loop
    :param auth: Basic authentication in a tuple user-pass pair
    :param data: Data to send to the url as a dictionary
    :param headers: Headers to send to the url as a dictionary
    :param cookies: Cookies to send to the url in the headers as a dictionary
    :param cert: The certificate to verify the request's SSL connection
    :param timeout: How long the request should last before being terminated
    :param encoding: The codec(s) to use to decode the request response
    :param mask: Whether to make the user-agent header that of a browser's to anonymise the request
    :param agent: Overwrite for the user-agent header
    :param onStatusError: A custom exception that can be passed to be raised instead of the default one when the request's status is >= 400
    :param proxy: The proxy to use for the request in the format '{host}:{port}'
    :param advContext: A tooltils.requests.advancedContext instance to provide advanced parameters
    """

    return request(url, "HEAD", port, https, verify, redirects,
                   redirect_loops, auth, data, headers, cookies, 
                   cert, None, None, None, timeout, encoding, 
                   mask, agent, onStatusError, proxy, advContext).send()

def put(url: str,
        port: int=(80, 443),
        https: bool=True,
        verify: bool=defaultVerificationMethod,
        redirects: bool=True,
        redirect_loops: bool=False,
        auth: tuple=None,
        data: dict=None,
        headers: dict=None,
        cookies: dict=None,
        cert: str=None,
        timeout: _bm.Union[int, float]=15, 
        encoding: _bm.Union[str, tuple]=("utf-8", "ISO-8859-1"),
        mask: bool=False,
        agent: str=None,
        onStatusError: _bm.Union[_bm.Callable[..., Exception], Exception]=StatusCodeError,
        proxy: str=None,
        advContext: advancedContext=None
        ) -> tooltilsResponse:
    """
    Send a PUT request

    :param url: The URL to request
    :param port: The port to make the connection on
    :param https: Whether to use https
    :param verify: Whether to verify the request with SSL
    :param redirects: Whether the request can redirect
    :param redirect_loops: Whether the request can enter a redirect loop
    :param auth: Basic authentication in a tuple user-pass pair
    :param data: Data to send to the url as a dictionary
    :param headers: Headers to send to the url as a dictionary
    :param cookies: Cookies to send to the url in the headers as a dictionary
    :param cert: The certificate to verify the request's SSL connection
    :param timeout: How long the request should last before being terminated
    :param encoding: The codec(s) to use to decode the request response
    :param mask: Whether to make the user-agent header that of a browser's to anonymise the request
    :param agent: Overwrite for the user-agent header
    :param onStatusError: A custom exception that can be passed to be raised instead of the default one when the request's status is >= 400
    :param proxy: The proxy to use for the request in the format '{host}:{port}'
    :param advContext: A tooltils.requests.advancedContext instance to provide advanced parameters
    """

    return request(url, "PUT", port, https, verify, redirects,
                   redirect_loops, auth, data, headers, cookies, 
                   cert, None, None, None, timeout, encoding, 
                   mask, agent, onStatusError, proxy, advContext).send()

def patch(url: str,
          port: int=(80, 443),
          https: bool=True,
          verify: bool=defaultVerificationMethod,
          redirects: bool=True,
          redirect_loops: bool=False,
          auth: tuple=None,
          data: dict=None,
          headers: dict=None,
          cookies: dict=None,
          cert: str=None, 
          timeout: _bm.Union[int, float]=15, 
          encoding: _bm.Union[str, tuple]=("utf-8", "ISO-8859-1"),
          mask: bool=False,
          agent: str=None,
          onStatusError: _bm.Union[_bm.Callable[..., Exception], Exception]=StatusCodeError,
          proxy: str=None,
          advContext: advancedContext=None
          ) -> tooltilsResponse:
    """
    Send a PATCH request

    :param url: The URL to request
    :param port: The port to make the connection on
    :param https: Whether to use https
    :param verify: Whether to verify the request with SSL
    :param redirects: Whether the request can redirect
    :param redirect_loops: Whether the request can enter a redirect loop
    :param auth: Basic authentication in a tuple user-pass pair
    :param data: Data to send to the url as a dictionary
    :param headers: Headers to send to the url as a dictionary
    :param cookies: Cookies to send to the url in the headers as a dictionary
    :param cert: The certificate to verify the request's SSL connection
    :param timeout: How long the request should last before being terminated
    :param encoding: The codec(s) to use to decode the request response
    :param mask: Whether to make the user-agent header that of a browser's to anonymise the request
    :param agent: Overwrite for the user-agent header
    :param onStatusError: A custom exception that can be passed to be raised instead of the default one when the request's status is >= 400
    :param proxy: The proxy to use for the request in the format '{host}:{port}'
    :param advContext: A tooltils.requests.advancedContext instance to provide advanced parameters
    """

    return request(url, "PATCH", port, https, verify, redirects,
                   redirect_loops, auth, data, headers, cookies, 
                   cert, None, None, None, timeout, encoding, 
                   mask, agent, onStatusError, proxy, advContext).send()

def options(url: str,
            port: int=(80, 443),
            https: bool=True,
            verify: bool=defaultVerificationMethod,
            redirects: bool=True,
            redirect_loops: bool=False,
            auth: tuple=None,
            data: dict=None,
            headers: dict=None,
            cookies: dict=None,
            cert: str=None, 
            timeout: _bm.Union[int, float]=15, 
            encoding: _bm.Union[str, tuple]=("utf-8", "ISO-8859-1"),
            mask: bool=False,
            agent: str=None,
            onStatusError: _bm.Union[_bm.Callable[..., Exception], Exception]=StatusCodeError,
            proxy: str=None,
            advContext: advancedContext=None
            ) -> tooltilsResponse:
    """
    Send an OPTIONS request

    :param url: The URL to request
    :param port: The port to make the connection on
    :param https: Whether to use https
    :param verify: Whether to verify the request with SSL
    :param redirects: Whether the request can redirect
    :param redirect_loops: Whether the request can enter a redirect loop
    :param auth: Basic authentication in a tuple user-pass pair
    :param data: Data to send to the url as a dictionary
    :param headers: Headers to send to the url as a dictionary
    :param cookies: Cookies to send to the url in the headers as a dictionary
    :param cert: The certificate to verify the request's SSL connection
    :param timeout: How long the request should last before being terminated
    :param encoding: The codec(s) to use to decode the request response
    :param mask: Whether to make the user-agent header that of a browser's to anonymise the request
    :param agent: Overwrite for the user-agent header
    :param onStatusError: A custom exception that can be passed to be raised instead of the default one when the request's status is >= 400
    :param proxy: The proxy to use for the request in the format '{host}:{port}'
    :param advContext: A tooltils.requests.advancedContext instance to provide advanced parameters
    """

    return request(url, "OPTIONS", port, https, verify, redirects,
                   redirect_loops, auth, data, headers, cookies, 
                   cert, None, None, None, timeout, encoding, 
                   mask, agent, onStatusError, proxy, advContext).send()

def trace(url: str,
          port: int=(80, 443),
          https: bool=True,
          verify: bool=defaultVerificationMethod,
          redirects: bool=True,
          redirect_loops: bool=False,
          auth: tuple=None,
          headers: dict=None,
          cert: str=None, 
          timeout: _bm.Union[int, float]=15, 
          encoding: _bm.Union[str, tuple]=("utf-8", "ISO-8859-1"),
          mask: bool=False,
          agent: str=None,
          onStatusError: _bm.Union[_bm.Callable[..., Exception], Exception]=StatusCodeError,
          proxy: str=None,
          advContext: advancedContext=None
          ) -> tooltilsResponse:
    """
    Send a TRACE request

    :param url: The URL to request
    :param port: The port to make the connection on
    :param https: Whether to use https
    :param verify: Whether to verify the request with SSL
    :param redirects: Whether the request can redirect
    :param redirect_loops: Whether the request can enter a redirect loop
    :param auth: Basic authentication in a tuple user-pass pair
    :param data: Data to send to the url as a dictionary
    :param headers: Headers to send to the url as a dictionary
    :param cookies: Cookies to send to the url in the headers as a dictionary
    :param cert: The certificate to verify the request's SSL connection
    :param timeout: How long the request should last before being terminated
    :param encoding: The codec(s) to use to decode the request response
    :param mask: Whether to make the user-agent header that of a browser's to anonymise the request
    :param agent: Overwrite for the user-agent header
    :param onStatusError: A custom exception that can be passed to be raised instead of the default one when the request's status is >= 400
    :param proxy: The proxy to use for the request in the format '{host}:{port}'
    :param advContext: A tooltils.requests.advancedContext instance to provide advanced parameters
    """

    return request(url, "TRACE", port, https, verify, redirects,
                   redirect_loops, auth, None, headers, None, 
                   cert, None, None, None, timeout, encoding, 
                   mask, agent, onStatusError, proxy, advContext).send()

def delete(url: str,
           port: int=(80, 443),
           https: bool=True,
           verify: bool=defaultVerificationMethod,
           redirects: bool=True,
           redirect_loops: bool=False,
           auth: tuple=None,
           data: dict=None,
           headers: dict=None,
           cookies: dict=None,
           cert: str=None, 
           timeout: _bm.Union[int, float]=15, 
           encoding: _bm.Union[str, tuple]=("utf-8", "ISO-8859-1"),
           mask: bool=False,
           agent: str=None,
           onStatusError: _bm.Union[_bm.Callable[..., Exception], Exception]=StatusCodeError,
           proxy: str=None,
           advContext: advancedContext=None
           ) -> tooltilsResponse:
    """
    Send a DELETE request

    :param url: The URL to request
    :param port: The port to make the connection on
    :param https: Whether to use https
    :param verify: Whether to verify the request with SSL
    :param redirects: Whether the request can redirect
    :param redirect_loops: Whether the request can enter a redirect loop
    :param auth: Basic authentication in a tuple user-pass pair
    :param data: Data to send to the url as a dictionary
    :param headers: Headers to send to the url as a dictionary
    :param cookies: Cookies to send to the url in the headers as a dictionary
    :param cert: The certificate to verify the request's SSL connection
    :param timeout: How long the request should last before being terminated
    :param encoding: The codec(s) to use to decode the request response
    :param mask: Whether to make the user-agent header that of a browser's to anonymise the request
    :param agent: Overwrite for the user-agent header
    :param onStatusError: A custom exception that can be passed to be raised instead of the default one when the request's status is >= 400
    :param proxy: The proxy to use for the request in the format '{host}:{port}'
    :param advContext: A tooltils.requests.advancedContext instance to provide advanced parameters
    """

    return request(url, "DELETE", port, https, verify, redirects,
                   redirect_loops, auth, data, headers, cookies, 
                   cert, None, None, None, timeout, encoding, 
                   mask, agent, onStatusError, proxy, advContext).send()
