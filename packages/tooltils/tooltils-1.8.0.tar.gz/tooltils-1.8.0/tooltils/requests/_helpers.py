def where() -> tuple:
    # if get_default_verify_paths().cafile is None then it's using openssl

    from ssl import get_default_verify_paths

    data = get_default_verify_paths()

    if data.cafile == None:
        return (data.openssl_capath, data.openssl_cafile)
    else:
        return (data.capath, data.cafile)

def connected() -> bool:
    from socket import create_connection, gethostbyname

    from ..info import _loadConfig, _loadCache, _editCache, _deleteCacheKey
    from ..os import getCurrentWifiName

    caching: bool = bool(_loadConfig("requests")["connectedCaching"])
    wifiName: str = getCurrentWifiName()
    result:  bool = True

    if wifiName == None:
        return False

    if caching:
        configData: dict = _loadConfig("requests")
        cacheData:  dict = _loadCache("requests")

        if cacheData["connectedTimesChecked"] >= configData["connectedCachingCheck"]:
            _editCache("requests", {"connectedTimesChecked": 0})
            _deleteCacheKey("requests", wifiName, "connectedNetworkList")
        else:
            if wifiName in list(cacheData["connectedNetworkList"].keys()):
                _editCache("requests", {"connectedTimesChecked": cacheData["connectedTimesChecked"] + 1})

                return cacheData["connectedNetworkList"][wifiName]

    try:
        create_connection((gethostbyname("httpbin.org"), 80), 3).close()
    except (TimeoutError, OSError):
        result: bool = False

    if caching:
        _editCache("requests", {wifiName: result}, "connectedNetworkList")
        _editCache("requests", {"connectedTimesChecked": 1})

    return result

def ctx(verify: bool=True, cert: str=None):
    from ssl import get_default_verify_paths, create_default_context, SSLError

    try:
        if type(cert) is not str and cert is not None:
            raise TypeError("Certificate must be a valid file path")

        if not verify:
            cert = None
        
        if cert == get_default_verify_paths().openssl_cafile:
            cert = None

        ctx = create_default_context(cafile=cert)
        ctx.  set_alpn_protocols(["https/1.1"])
    except (FileNotFoundError, IsADirectoryError, SSLError):
        raise FileNotFoundError("Not a valid certificate file path")
        
    if not verify:         
        ctx.check_hostname = False
        ctx.verify_mode    = 0 # ssl.CERT_NONE
        ctx.                 set_ciphers("RSA")
        
    return ctx

def _check(url: str, https: bool) -> bool:
    from urllib.parse import urlparse

    # dont EVER touch this function, it will cause irreversible brain damage

    try:
        urls  = urlparse(url)
        valid = (all((urls.scheme, urls.netloc)), urls.scheme, urls.netloc, urls.path, urls)
    except Exception:
        valid = (False, None, None, None, None)

    if not valid[0]:
        if not all((valid[1], valid[2])):
            if valid[3]:
                if not url.startswith("https://") and not url.startswith("http://"):
                    url: str = "http" + ('s' if https else "") + "://" + url

                    return _check(url, https)

        return (0,) + valid
    elif valid[0]:
        if valid[1] != "http" and valid[1] != "https":
            return (1,) + valid

        if '.' not in valid[2]:
            return (2,) + valid

        return (3,) + valid

def prep_url(url: str, 
             data: dict=None,
             https: bool=True,
             order: bool=False
             ) -> str:
    from urllib.parse import urlunparse, urlencode

    from ..errors import InvalidRequestURL
    
    if type(url) is not str:
        raise TypeError("Url must be a valid 'str' instance")
    elif url == "":
        raise InvalidRequestURL("URL is empty")
    elif ' ' in url:
        url: str = url.replace(' ', "%20")

    if data is None:
        data = {}
    elif type(data) is not dict:
        raise TypeError("Data must be a valid 'dict' instance")

    if url[0] == '/' or url.startswith("file:///") or url.startswith("C:\\"):
        raise InvalidRequestURL("Url must be a http url instance, not a file path", url)
    
    valid = _check(url, https)

    if valid[0] == 0:
        if not valid[2] and valid[3]:
            if not url.startswith("https://") and not url.startswith("http://"):
                url: str = "http" + ('s' if https else "") + "://" + url
        else:
            raise InvalidRequestURL("URL does not contain either a scheme or host, or both", url)
    elif valid[0] == 1:
        raise InvalidRequestURL("An unknown protocol scheme was found", url)
    elif valid[0] == 2:
        raise InvalidRequestURL("URL does not contain a valid host", url)
    elif valid[0] == 3:
        url: str = urlunparse(valid[5])
    
    if url.startswith("https://") and not https:
        url: str = "http://" + "://".join(url.split("://")[1:])
    elif url.startswith("http://") and https:
        url: str = "https://" + "://".join(url.split("://")[1:])
    
    if url[-1] == '/':
        url: str = url[:-1]

    if data != {}:
        url += '?' + urlencode(data, doseq=order, safe='/')

    return url

def basicAuth(user: str, password: str) -> str:
    from base64 import b64encode

    key: str = "Basic {}".format(
        b64encode(f'{user}:{password}'.encode()).decode('ascii')
    )

    return key

class tooltilsResponse():
    def __init__(self, data, url: str, method: str, 
                 encoding: str=('utf-8', 'ISO-8859-1'), 
                 _agent: str=None, _headers: dict=None, 
                 _clog: bool=None, _rID: int=-1,
                 _logger=None, _extra=False):
        from json import loads, JSONDecodeError
        from gzip import decompress

        from ..errors import RequestCodecError

        # sneaky
        if type(data).__name__ != "HTTPResponse":
            raise TypeError("Data must be a valid 'http.client.HTTPResponse' instance")
        
        if type(url) is not str:
            raise TypeError("Url must be a valid 'str' instance")
        
        if type(method) is not str:
            raise TypeError("Method must be a valid 'str' instance")
        
        if type(encoding) is not str and type(encoding) is not tuple:
            raise TypeError("Encoding must be a valid 'str' or 'tuple' instance")

        if _clog:
            self._caller: str = "openConnection().send()"
        elif _clog == False:
            self._caller: str = "request().send()"
        else:
            self._caller: str = "tooltilsResponse()"

        self.data             = data
        self.code:        int = self.data.status
        self.reason:      str = self.data.reason
        self.status_code: str = f'{self.code} {self.reason}'
        self.headers:    dict = dict(self.data.getheaders())
        self.redirected: bool = bool(False)
        self.path:        str = None
        self.pos:         int = int(0)

        class end_data():
            def __init__(self, url, headers, agent):
                self.url          = url
                self.sent_headers = headers
                self.agent        = agent
        
        # do some weird inline comparisons to make sure the type is reported as str | None
        _agent = _agent if _agent else str(self.headers.get(
                 "User-Agent", None)) if self.headers.get(
                 "User-Agent", None) else None

        self.end_data = end_data(url, _headers, _agent)

        if method == "HEAD":
            self.raw  = None
            self.text = None
            self.json = None
            
            return

        self.raw: bytes = self.data.read()

        try:
            self.text = decompress(self.raw)
        except OSError as err:
            if "Not a gzipped file" in str(err) and _logger and _extra:
                _logger.debug("Request response body was not gzipped", self._caller, _rID)
                            
            self.text = self.raw

        if type(encoding) is str:
            try:
                self.text: str = str(self.text.decode(encoding))
            except UnicodeDecodeError:
                pass
        else:
            for i in encoding:
                try:
                    self.text: str = str(self.text.decode(i))

                    break
                except UnicodeDecodeError:
                    pass
                        
            if type(self.text) is not str:
                raise RequestCodecError("None of the specified encodings were able to decipher the " + 
                                        "request response body", encoding)
                        
            try:
                self.json: dict = loads(self.text)
            except JSONDecodeError:
                self.json = None

                if _logger and _extra:
                    _logger.debug('Request response body is not json', self._caller, _rID)
        
        self._method: str = method
                        
    def read(self, amt: int=None) -> bytes:
        """
        Read the request response body or up to amt bytes \n
        This method only exists for cross compatibility"""

        if self.raw == None:
            raise ValueError("The request response body was unable to be read")

        if type(amt) is not int and amt != None:
            raise TypeError("Amt must be a valid 'int' instance")
        elif amt:
            if self.pos + amt > len(self.raw):
                raise ValueError("Tried to read over the length of the request response body")
            elif amt < 0:
                raise ValueError("Amt must be bigger than 0")

        if amt:
            try:
                raw        = self.raw[self.pos:self.pos + amt]
                self.pos += amt

                return raw
            except IndexError:
                raise ValueError('Tried to read over the length of the request response body')
        else:
            return self.raw

    def readlines(self, amt: int=None) -> list:
        """
        Read the request response body or up to amt bytes and return as a list split at every newline \n
        This method only exists for cross compatibility
        """

        if self.raw == None:
            raise ValueError("The request response body was unable to be read")

        if type(amt) is not int and amt != None:
            raise TypeError("Amt must be a valid 'int' instance")
        
        if amt:
            if (self.pos + amt) > len(self.raw):
                raise ValueError("Tried to read over the length of the request response body")
            elif amt < 0:
                raise ValueError("Amt must be bigger than 0")

            try:
                text       = self.text[self.pos:self.pos + amt].splitlines()
                self.pos += amt

                return text
            except IndexError:
                raise ValueError("Tried to read over the length of the request response body")
        else:
            return self.text.splitlines()
    
    def seek(self, pos: int) -> None:
        """
        Seek to a position in the request response body \n
        This method only exists for cross compatibility
        """

        if self.raw == None:
            raise ValueError("The request response body text position was unable to be changed")

        if type(pos) is not int:
            raise TypeError("Pos must be a valid 'int' instance")

        if pos > len(self.text):
            raise ValueError("Tried to read over the length of the request response body")
        if pos < 0:
            raise ValueError("Pos must be bigger than 0")
        
        self.pos = pos
    
    def close(self) -> None:
        """This method does nothing and only exists for cross compatibility"""

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type == None:
            return True
    
    def __str__(self):
        return f"<{self._method.upper()} {self.end_data.url} [{self.status_code}]>"

    def __repr__(self):
        return self.__str__()

def validateRedirect(newurl: str, redirectData: dict, 
                     redirect_loops: bool, redirectLimit: int,
                     https: bool):
    from ..errors import RequestRedirectError, ActiveRequestError

    if redirectData:
        if redirectData["redirected"] >= redirectData["limit"]:
            raise RequestRedirectError(limit=redirectData["redirected"])
        else:
            redirectData["redirected"] += 1
                
        if not redirect_loops and newurl in redirectData["redirectList"]:
            raise RequestRedirectError("Redirect loop detected")
        else:
            redirectData["redirectList"].append(newurl)
    else:
        redirectData: dict = {"redirected": 1, "redirectList": [newurl],
                              "limit": redirectLimit}
                    
    try:
        try:
            newurl       = prep_url(newurl, https=https)
            redirectHost = newurl.split('/')[2]
            redirectPage = '/' + '/'.join(newurl.split('/')[3:])
        except IndexError:
            redirectHost = prep_url(newurl, https=https).split('/')[2]
            redirectPage = ""
    except Exception:
        raise ActiveRequestError("The request redirected but returned a malformed location header",
                                 newurl)

    redirectHost = "http" + ('s' if https else "") + "://" + redirectHost

    return (redirectHost, redirectPage, redirectData)

httpMethods: tuple = ("GET", "POST", "PUT", "DOWNLOAD", "HEAD", "PATCH", "OPTIONS", "TRACE", "DELETE")
