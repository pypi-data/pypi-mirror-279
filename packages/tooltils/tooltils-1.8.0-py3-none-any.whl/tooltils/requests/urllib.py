"""HTTP/1.1 simple interface - `urllib.request`"""


class _bm:
    from typing import Any, Dict, Union, Callable

    from ..errors import (ActiveRequestError, InvalidRequestURL, ConnectionError,
                          ConnectionTimeoutExpired, InvalidWifiConnection,
                          StatusCodeError, SSLCertificateFailed,
                          RequestRedirectError, RequestCodecError)
    from ._helpers import tooltilsResponse, httpMethods
    from ..info import _logger, _loadConfig, version
    from ..os import info

    class FileDescriptorOrPath:
        pass

    class HTTPResponse:
        pass

    class SSLContext:
        pass
    
    noRedirects = None
    newestID    = 1
    
    def propertyTest(value, types: tuple, name: str):
        if value is None:
            return types[0]()
        elif not isinstance(value, types):
            raise TypeError(name + " must be a valid '" + types[0].__name__ + "' instance")
        else:
            return value

    logger = _logger("requests.urllib")


StatusCodeError                 = _bm.StatusCodeError
redirectLimit:              int = _bm._loadConfig("requests")["redirectLimit"]
defaultVerificationMethod: bool = bool(_bm._loadConfig("requests")["defaultVerificationMethod"])

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

        if type(redirectLimit) is not int:
            raise TypeError("RedirectLimit must be a valid 'int' instance")
        elif redirectLimit < 1:
            raise ValueError("RedirectLimit must be bigger than 1")
        if type(SSLContext).__name__ != "SSLContext" and SSLContext is not None:
            raise TypeError("SSLContext must be a valid 'ssl.SSLContext' instance")
    
        self.redirectLimit: int = redirectLimit
        self.extraLogs:    bool = extraLogs
        self.SSLContext         = SSLContext
    
    def __eq__(self, advCtx) -> bool:
        if not isinstance(advCtx, advancedContext):
            raise TypeError("Expression value two should be of type 'advancedContext'")

        return (self.redirectLimit, self.extraLogs, self.SSLContext
                ) == (advCtx.redirectLimit, advCtx.extraLogs, advCtx.SSLContext)

    
    def __str__(self) -> str:
        values = (f"{i}={repr(getattr(self, i))}" for i in (i2 for i2 in dir(self) if "__" not in i2))

        return f"advancedContext({', '.join(values)})"
    
    def __repr__(self) -> str:
        return self.__str__()

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
                 advContext: advancedContext=None,
                 _redirect: bool=False):
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

        self.rID      = _bm.newestID
        _bm.newestID += 1

        if _redirect:
            self.rID     -= 1
            _bm.newestID -= 1

        self._redirect: bool = _redirect

        self._setVariables(url, method, port, https, verify, redirects, 
                           redirect_loops, auth, data, headers, cookies, 
                           cert, file_name, write_binary, override, timeout,
                           encoding, mask, agent, onStatusError, proxy, 
                           advContext)

        if not _redirect:
            _bm.logger.debug("Setting up http{}/1.1 {} request to {} on port {}".format(
                             's' if self.https else "", self.method,
                             '/'.join(self.url.split('/')[2:]), self.port),
                             "request()", self.rID)

        self._setup()

    def __str__(self):
        if self.state:
            code: str = f"[{self._code}]"
        else:
            code: str = "[Unsent]"

        return "<{} {} {}>".format(self.method, '/'.join(self.url.split('/')[2:]), code)

    def __repr__(self):
        return self.__str__()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type == None:
            self._state = True

            return True

    def _setVariables(self, url: str, method: str,
                      port: int, https: bool, verify: bool,
                      redirects: bool, redirect_loops: bool,
                      auth: tuple, data: dict, headers: dict,
                      cookies: dict, cert: str, file_name: str,
                      write_binary: bool, override: bool,
                      timeout: int, encoding: str, mask: bool,
                      agent: str, onStatusError: Exception,
                      proxy: str, advContext: advancedContext):
        from os.path import exists

        from ._helpers import prep_url, httpMethods, where

        error = None

        self.redirect_loops  = bool(redirect_loops)
        self.redirects: bool = bool(redirects)
        self.write_binary    = bool(write_binary)
        self.verify:    bool = bool(verify)
        self.https:     bool = bool(https)
        self.override:  bool = bool(override)
        self.mask:      bool = bool(mask)
        self.state:      str = "Prepared"
        self.url:        str = prep_url(url, None, self.https)
        self.cookies:   dict = dict(_bm.propertyTest(cookies, (dict,), "Cookies"))
        self.data:      dict = dict(_bm.propertyTest(data, (dict,), "Data"))
        self.headers:   dict = dict(_bm.propertyTest(headers, (dict,), "Headers"))

        self._url   = self.url.replace("https://", "").replace("http://", "")
        self._state = False

        if ':' in self.url.replace("https://", "").replace("http://", ""):
            error = _bm.InvalidRequestURL("You may not include a colon in the URL (this includes ports)")

        if type(method) is str:
            if method.upper() not in httpMethods:
                error = ValueError(f"Invalid http method '{method}'")
            else:
                self.method = self._method = method.upper()
            
            if self.method == "DOWNLOAD":
                self._method: str = "GET"
        else:
            error = TypeError("Method must be a valid 'str' instance")

        if port == (80, 443):
            self.port: int = int(443 if self.https else 80)
        elif type(port) is not int:
            error = TypeError("Port must be a valid 'int' instance")
        else:
            self.port: int = port

        if proxy is None:
            self.proxy = None
        elif type(proxy) is not str:
            error = TypeError("Proxy must be a valid 'str' instance")
        else:
            if ':' not in proxy:
                error = ValueError("Proxy must have the format 'host:port'")
            else:
                self.proxy: str = proxy

        if self.https and self.verify:
            if cert is None:
                self.cert: str = where()[1]
            else:
                if type(cert) is not str:
                    error = TypeError("Certificate must be a valid 'str' instance")
                elif cert.split('.')[-1] != "pem":
                    error = FileNotFoundError("Invalid certificate file path")
                elif not exists(cert) and cert != where()[1]:
                    error = FileNotFoundError("The certificate file does not exist")
                else:
                    self.cert = cert
        else:
            self.cert = None

        if auth is None:
            self.auth = None
        elif type(auth) is not tuple and type(auth) is not list:
            raise TypeError("Authentiction must be a valid 'tuple' instance")
        elif len(auth) != 2:
            raise ValueError("Invalid authentication details")
        else:
            self.auth: tuple = tuple(auth)

        if type(timeout) is not int and type(timeout) is not float:
            raise TypeError("Timeout must be a valid 'int' instance")
        else:
            self.timeout: int = int(timeout)

        if file_name and type(file_name) is not str:
            error = TypeError("File_name must be a valid 'str' instance")
        else:
            self.file_name: str = file_name

        if agent and type(agent) is not str:
            error = TypeError("Agent must be a valid 'str' instance")
        else:
            self.agent: str = agent

        if type(encoding) is not str and type(encoding) is not tuple:
            error =  TypeError("Encoding must be a valid 'str' or 'tuple' instance")
        else:
            self.encoding: _bm.Union[str, tuple] = encoding
        
        if onStatusError and onStatusError != StatusCodeError and Exception not in StatusCodeError.__bases__:
            error = TypeError("OnStatusError must be a valid 'Exception' or 'NoneType' instance")
        else:
            self.onStatusError = onStatusError
        
        if advContext is None:
            self.advContext         = None
            self.redirectLimit: int = redirectLimit
            self.extraLogs:    bool = False
            self.SSLContext         = None
        elif type(advContext) is not advancedContext:
            error = TypeError("AdvContext must be a valid 'tooltils.requests.advancedContext' instance")
        else:
            self.advContext         = advContext
            self.redirectLimit: int = advContext.redirectLimit
            self.extraLogs:    bool = advContext.extraLogs
            self.SSLContext         = advContext.SSLContext

        if error:
            raise error
    
    def _setup(self):
        from urllib.request import HTTPSHandler, HTTPHandler, ProxyHandler, OpenerDirector, Request

        from ._helpers import ctx

        if self.https:
            if self.SSLContext:
                openers = [HTTPSHandler(context=self.SSLContext)]

                if self.extraLogs and not self._redirect:
                    _bm.logger.debug("Using custom SSLContext instance", "request()", self.rID)
            else:
                openers = [HTTPSHandler(context=ctx(self.verify, self.cert))]

                if self.extraLogs and not self._redirect:
                    _bm.logger.debug("Using request created SSLContext instance", "request()", self.rID)
        else:
            openers = [HTTPHandler()]

        if self.proxy:
            openers.append(ProxyHandler(
                {"http" + 's' if self.https else "": self.proxy}
            ))

        self._opener = OpenerDirector()

        for i in openers:
            self._opener.add_handler(i)

        self._data, self._headers = self._prepare(self.method, self.auth,
                                                  self.data, self.headers,
                                                  self.cookies, self.mask,
                                                  self.agent)

        self._req = Request(self.url, headers=self._headers,
                            method=self._method)

    def _prepare(self, method: str, auth: tuple, data: dict, headers: dict, 
                 cookies: dict, mask: str, agent: str) -> None:
        from json import dumps

        from ._helpers import basicAuth
        from ..info import version

        _headers = {}
        _data    = None
        
        if agent is None:
            agent: str = f"Python-tooltils/{version}"

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

            if self.extraLogs and not self._redirect:
                _bm.logger.debug("Adding 'Content-Length' to headers because the " +
                                 "method is POST or PUT", "request()", self.rID)

        elif method == "TRACE":
            _headers.update({"Content-Type": "message/http"})

            if self.extraLogs and not self._redirect:
                _bm.logger.debug("Adding 'Content-Type': 'message/http' to " +
                                 "headers because the method is TRACE", "request()", self.rID)

        _headers.update({"Connection": "close", "User-Agent": agent, 
                         "Accept": "*/*", "Accept-Encoding": "gzip, deflate"})
        
        for i in list(cookies.keys()): 
            _headers.update({"Cookie", f"{str(i)}={str(cookies[i])}"})
        
        if auth:
            _headers.update({"Authorization": basicAuth(auth[0], auth[1])})

        if not self._redirect and self.extraLogs:
            _bm.logger.debug("Adding necessary request headers", "request()", self.rID)

            if cookies:
                _bm.logger.debug("Adding cookies to request headers", "request()", self.rID)
            
            if auth:
                _bm.logger.debug("Adding authorisation to request headers", "request()", self.rID)
        
        _headers.update(headers)

        return (_data, _headers)

    def send(self, **shared: object) -> _bm.tooltilsResponse:
        """Send the request to the URL"""

        from ssl import SSLCertVerificationError, SSLError
        from urllib.error import HTTPError, URLError
        from os.path import exists, abspath
        from socket import gaierror
        from os import remove

        from ._helpers import connected, validateRedirect

        error = None

        if self._state:
            raise _bm.ConnectionError("The request has already been sent")
        
        if not self._redirect:
            _bm.logger.debug("Sending request", "request().send()", self.rID)

            if self.extraLogs:
                _bm.logger.debug(f"Sending headers: {self._headers}", "request().send()", self.rID)

                if self._data:
                    _bm.logger.debug(f"Sending data with length: {len(self._data)}", 
                                     "request().send()", self.rID)

        try:
            rdata = self._opener.open(self._req, data=self._data, timeout=self.timeout)

            if not self._redirect and not (rdata.status >= 400 and self.onStatusError):
                _bm.logger.debug("Obtained request response", "request().send()", self.rID)

            resp = tooltilsResponse(rdata, self.url, self.method, self.encoding,
                                    self._headers['User-Agent'], self._headers,
                                    False, self.rID, not bool(rdata.getheader('location', None)))
            
            if rdata.status >= 400 and self.onStatusError:
                if self.onStatusError == StatusCodeError:
                    error = _bm.StatusCodeError(rdata.status, rdata.reason)
                else:
                    # check if the custom exception has been passed as an object or name
                    if hasattr(self.onStatusError, "__name__"):
                        error = self.onStatusError()
                    else:
                        error = self.onStatusError
        except ConnectionResetError:
            error = _bm.ActiveRequestError("The host or client ended the connection without a response", self.url)
        except SSLCertVerificationError:
            error = _bm.SSLCertificateFailed()
        except SSLError:
            if connected():
                error = _bm.SSLCertificateFailed()
            else:
                error = _bm.ConnectionError("The connection was forcibly closed by the client")
            
            _bm.logger.debug("tooltils.requests.connected() was called and may update the cache", 
                             "request().send()", self.rID)
        except HTTPError as err:
            if self.onStatusError:
                if self.onStatusError == StatusCodeError:
                    error = _bm.StatusCodeError(err.code, err.reason)
                else:
                    error = self.onStatusError()
        except URLError as err:
            if "[Errno 8]" in str(err) or "[Errno 11001]" in str(err):
                if connected():
                    error = _bm.StatusCodeError(404)
                else:
                    error = _bm.InvalidWifiConnection()

                _bm.logger.debug("tooltils.requests.connected() was called and may update the cache", 
                                 "request().send()")
            elif "timed out" in str(err):
                error = _bm.ConnectionTimeoutExpired("The request connection operation timed out", self.timeout)
            elif "ssl" in str(err):
                error = _bm.SSLCertificateFailed()
            else:
                error = err
        except gaierror:
            if connected():
                if self.onStatusError:
                    if self.onStatusError == StatusCodeError:
                        error = _bm.StatusCodeError(err.code, err.reason)
                    else:
                        if hasattr(self.onStatusError, "__name__"):
                            error = self.onStatusError()
                        else:
                            error = self.onStatusError
                else:
                    rdata.status = 404
                    rdata.reason = "Not Found"
            else:
                error = _bm.InvalidWifiConnection()
            
            _bm.logger.debug("tooltils.requests.connected() was called and may update the cache", 
                             "request().send()", self.rID)
        except TimeoutError:
            error = _bm.ConnectionTimeoutExpired("The request connection operation timed out", self.timeout)
        except ValueError:
            error = _bm.InvalidRequestURL("Invalid URL", self.url)
        except OSError:
            error = _bm.ConnectionError("An unknown error occured, check the above stack trace for more info")

        self.state:   str = "Sent"
        self._state: bool = True

        if error:
            _bm.logger.debug("Request to <{}:{}> failed due to: {}".format(
                             '/'.join(self.url.split('/')[2:]), self.port, 
                             type(error).__name__),
                             "request().send()", self.rID)
            
            if self.port != 80 and self.port != 443:
                _bm.logger.debug("Request may have failed due to the port not being set to 80 or 443",
                                 "request().send()", self.rID)

            raise error
        
        redirectDir = rdata.getheader("location", None)
        rData       = shared.get("_redirectData", {})

        if self.redirects and redirectDir:
            rHost, rPage, rData = validateRedirect(redirectDir, rData,
                                                   self.redirect_loops, 
                                                   self.redirectLimit, 
                                                   self.https)
            
            _bm.logger.debug(f"Redirected: {rHost + rPage}", "request().send()", 
                             self.rID)
            
            return request(rHost + rPage, self.method, self.port, self.https,
                           self.verify, self.redirects, self.redirect_loops, self.auth,
                           self.data, self.headers, self.cookies, self.cert, self.file_name,
                           self.write_binary, self.override, self.timeout, self.encoding,
                           self.mask, self.agent, self.onStatusError, self.proxy, 
                           self.advContext, True).send(_redirectData=rData)

        resp.redirected = bool(rData)
        
        self._code = resp.status_code

        if self.method == "DOWNLOAD":
            if self.file_name == None:
                try:
                    self.file_name = self.url.split('/')[-1]
                except IndexError:
                    self.file_name = self._url + ".downloadfile"

            if self.override and exists(self.file_name):
                remove(self.file_name)
            else:
                raise FileExistsError("The requested file already exists on the disk")
                
            # test if the file_name is sanitary
                
            try:
                with open(self.file_name, "a+") as _f:
                    pass

                remove(self.file_name)
            except OSError:
                raise FileNotFoundError("Unable to locate valid file_name descriptor from request url")

            if self.write_binary:
                with open(self.file_name, "wb+") as _f:
                    _f.write(resp.raw)
            else:
                with open(self.file_name, "a+") as _f:
                    _f.write(resp.text)

            resp.path = abspath(self.file_name)
        
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
        cert: str=None,
        timeout: _bm.Union[int, float]=15,
        encoding: _bm.Union[str, tuple]=("utf-8", "ISO-8859-1"),
        mask: bool=False,
        agent: str=None,
        onStatusError: _bm.Union[_bm.Callable[..., Exception], Exception]=StatusCodeError,
        proxy: str=None,
        advContext: advancedContext=None
        ) -> _bm.tooltilsResponse:
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

    return request(url, "GET", port, https, 
                   verify, redirects, redirect_loops, 
                   auth, data, headers, cookies, cert, 
                   None, None, None, timeout, encoding, 
                   mask, agent, onStatusError, proxy, 
                   advContext).send()

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
         ) -> _bm.tooltilsResponse:
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

    return request(url, "POST", port, https, 
                   verify, redirects, redirect_loops, 
                   auth, data, headers, cookies, cert, 
                   None, None, None, timeout, encoding, 
                   mask, agent, onStatusError, proxy, 
                   advContext).send()

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
             ) -> _bm.tooltilsResponse:
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

    return request(url, "DOWNLAOD", port, https, 
                   verify, redirects, redirect_loops, 
                   auth, data, headers, cookies, cert, 
                   file_name, write_binary, override, 
                   timeout, encoding, mask, agent, 
                   onStatusError, proxy, advContext).send()

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
         ) -> _bm.tooltilsResponse:
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

    return request(url, "HEAD", port, https, 
                   verify, redirects, redirect_loops, 
                   auth, data, headers, cookies, cert, 
                   None, None, None, timeout, encoding, 
                   mask, agent, onStatusError, proxy, 
                   advContext).send()

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
        ) -> _bm.tooltilsResponse:
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

    return request(url, "PUT", port, https, 
                   verify, redirects, redirect_loops, 
                   auth, data, headers, cookies, cert, 
                   None, None, None, timeout, encoding, 
                   mask, agent, onStatusError, proxy, 
                   advContext).send()

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
          ) -> _bm.tooltilsResponse:
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

    return request(url, "PATCH", port, https, 
                   verify, redirects, redirect_loops, 
                   auth, data, headers, cookies, cert, 
                   None, None, None, timeout, encoding, 
                   mask, agent, onStatusError, proxy, 
                   advContext).send()

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
        ) -> _bm.tooltilsResponse:
    """
    Send a OPTIONS request
        
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

    return request(url, "OPTIONS", port, https, 
                   verify, redirects, redirect_loops, 
                   auth, data, headers, cookies, cert, 
                   None, None, None, timeout, encoding, 
                   mask, agent, onStatusError, proxy, 
                   advContext).send()

def trace(url: str,
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
          ) -> _bm.tooltilsResponse:
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

    return request(url, "TRACE", port, https, 
                   verify, redirects, redirect_loops, 
                   auth, data, headers, cookies, cert, 
                   None, None, None, timeout, encoding, 
                   mask, agent, onStatusError, proxy, 
                   advContext).send()

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
           ) -> _bm.tooltilsResponse:
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

    return request(url, "DELETE", port, https, 
                   verify, redirects, redirect_loops, 
                   auth, data, headers, cookies, cert, 
                   None, None, None, timeout, encoding, 
                   mask, agent, onStatusError, proxy, 
                   advContext).send()
