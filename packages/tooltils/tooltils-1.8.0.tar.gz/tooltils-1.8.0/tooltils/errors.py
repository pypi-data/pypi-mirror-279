"""Package specific exceptions"""


class _bm:
    from typing import Union, Dict


class TooltilsError(Exception):
    """Base class for tooltils specific errors"""

    def __init__(self, message: str=''):
        """Base class for tooltils specific errors"""

        self.message: str = message
    
    def __str__(self):
        if self.message:
            return self.message
        else:
            return 'A Tooltils error occured'

class TooltilsMainError(TooltilsError):
    """Base class for tooltils main module specific errors"""

    def __init__(self, message: str=''):
        """Base class for tooltils main module specific errors"""

        self.message: str = message
    
    def __str__(self):
        if self.message:
            return self.message
        else:
            return 'A tooltils main module error occured'

class TooltilsInfoError(TooltilsError):
    """Base class for tooltils.info specific errors"""

    def __init__(self, message: str=''):
        """Base class for tooltils.info specific errors"""

        self.message: str = message
    
    def __str__(self):
        if self.message:
            return self.message
        else:
            return 'A tooltils.info error occured'

class TooltilsOSError(TooltilsError):
    """Base class for tooltils.os specific errors"""

    def __init__(self, message: str=''):
        """Base class for tooltils.os specific errors"""

        self.message: str = message
    
    def __str__(self):
        if self.message:
            return self.message
        else:
            return 'A tooltils.os error occured'

class SubprocessError(TooltilsOSError):
    """Base class for tooltils.os.system() specific errors"""

    def __init__(self, message: str=''):
        """Base class for tooltils.os.system() specific errors"""

        self.message: str = message
    
    def __str__(self):
        if self.message:
            return self.message
        else:
            return 'A tooltils.os.system() error occured'

class SubprocessExecutionError(SubprocessError):
    """Child process execution failed"""

    def __init__(self, message: str=''):
        """Child process execution failed"""

        self.message: str = message
    
    def __str__(self):
        if self.message:
            return self.message
        else:
            return 'Child process execution failed'

class SubprocessCodeError(SubprocessError):
    """Child process execution returned non-zero exit code"""

    def __init__(self, message: str='', code: int=0):
        """Child process execution returned non-zero exit code"""

        self.message: str = message
        self.code:    int = code
    
    def __str__(self):
        if self.message:
            return self.message
        elif self.code:
            return f'Child process execution returned non-zero exit code {self.code}'
        else:
            return 'Child process execution returned non-zero exit code'

class SubprocessTimeoutExpired(SubprocessError):
    """Child process execution timed out"""
    
    def __init__(self, message: str='', timeout: int=0):
        """Child process execution timed out"""

        self.message: str = message
        self.timeout: int = timeout
    
    def __str__(self):
        if self.message:
            return self.message
        elif self.timeout:
            return f'Child process execution timed out at {self.timeout} seconds'
        else:
            return 'Child process execution timed out'

class SubprocessLookupNotFound(SubprocessError):
    """Unable to locate program or shell command"""

    def __init__(self, message: str='', name: str=''):
        """Unable to locate program or shell command"""

        self.message: str = message
        self.name:    str = name
    
    def __str__(self):
        if self.message:
            return self.message
        elif self.name:
            return f'Unable to locate program or shell command \'{self.name}\''
        else:
            return 'Unable to locate program or shell command'

class SubprocessPermissionError(SubprocessError):
    """Denied access to program or shell command"""

    def __init__(self, message: str='', name: str=''):
        """Denied access to program or shell command"""

        self.message: str = message
        self.name:    str = name
    
    def __str__(self):
        if self.message:
            return self.message
        elif self.name:
            return f'Denied access to program or shell command \'{self.name}\''
        else:
            return 'Denied access to program or shell command'

class TooltilsRequestsError(TooltilsError):
    """Base class for tooltils.requests specific errors"""

    def __init__(self, message: str=''):
        """Base class for tooltils.requests specific errors"""

        self.message: str = message
    
    def __str__(self):
        if self.message:
            return self.message
        else:
            return 'A tooltils.requests error occured'

class RequestError(TooltilsRequestsError):
    """Base class for requesting specific errors"""

    def __init__(self, message: str=''):
        """Base class for requesting specific errors"""

        self.message: str = message
    
    def __str__(self):
        if self.message:
            return self.message
        else:
            return 'A request error occured'

class ActiveRequestError(RequestError):
    """The request to the URL failed"""

    def __init__(self, message: str='', url: str=''):
        """The request to the URL failed"""

        self.message: str = message
        self.url:     str = url

    def __str__(self):
        if self.message:
            return self.message
        elif self.url:
            return f'Request to \'{self.url}\' failed'
        else:
            return 'The request to the URL failed'

class InvalidRequestURL(RequestError):
    """URL cannot be used to make a valid request"""

    def __init__(self, message: str='', url: str=''):
        """URL cannot be used to make a valid request"""

        self.message: str = message
        self.url:     str = url
    
    def __str__(self):
        if self.message:
            return self.message
        elif self.url:
            return f'URL \'{self.url}\' cannot be used to make a valid request'
        else:
            return 'URL cannot be used to make a valid request'

class ConnectionError(RequestError):
    """Connection to URL failed"""

    def __init__(self, message: str='', url: str=''):
        """Connection to URL failed"""

        self.message: str = message
        self.url:     str = url
    
    def __str__(self):
        if self.message:
            return self.message
        elif self.url:
            return f'Connection to \'{self.url}\' failed'
        else:
            return 'Connection to URL failed'

class ConnectionTimeoutExpired(RequestError):
    """Request connection timeout expired"""

    def __init__(self, message: str='', timeout: int=0):
        """Request connection timeout expired"""

        self.message: str = message
        self.timeout: int = timeout
    
    def __str__(self):
        if self.message:
            return self.message
        elif self.timeout:
            return f'Request connection timeout expired at {self.timeout} seconds'
        else:
            return 'Request connection timeout expired'

class StatusCodeError(RequestError):
    """Status code of URL response is not 200"""

    status_codes: _bm.Dict[int, str] = {
        100: 'Continue',
        101: 'Switching Protocols',
        102: 'Processing',
        103: 'Early Hints',
        200: 'OK',
        201: 'Created',
        202: 'Accepted',
        203: 'Non-Authoritative Information',
        204: 'No Content',
        205: 'Reset Content',
        206: 'Partial Content',
        207: 'Multi-Status',
        208: 'Already Reported',
        226: 'I\'m Used',
        300: 'Multiple Choices',
        301: 'Moved Permanently',
        302: 'Found',
        303: 'See Other',
        304: 'Not Modified',
        305: 'Use Proxy',
        307: 'Temporary Redirect',
        308: 'Permanent Redirect',
        400: 'Bad Request',
        401: 'Unauthorized',
        402: 'Payment Required',
        403: 'Forbidden',
        404: 'Not Found',
        405: 'Method Not Allowed',
        406: 'Not Acceptable',
        407: 'Proxy Authentication Required',
        408: 'Request Timeout',
        409: 'Conflict',
        410: 'Gone',
        411: 'Content-Length Required',
        412: 'Precondition Failed',
        413: 'Request Entity Too Large',
        414: 'Request URI Too Long',
        415: 'Unsupported Media Type',
        416: 'Requested Range Not Satisfiable',
        417: 'Expectation Failed',
        421: 'Misdirected Request',
        422: 'Unprocessable Content',
        423: 'Locked',
        424: 'Failed Dependency',
        425: 'Too Early',
        426: 'Upgrade Required',
        428: 'Precondition Required',
        429: 'Too Many Requests',
        431: 'Request Header Fields Too Large',
        451: 'Unavailable For Legal Reasons',
        500: 'Internal Server Error',
        501: 'Not Implemented',
        502: 'Bad Gateway',
        503: 'Service Unavailable',
        504: 'Gateway Timeout',
        505: 'HTTP Version Not Supported',
        506: 'Variant Also Negotiates',
        507: 'Insufficient Storage',
        508: 'Loop Detected',
        510: 'Not Extended',
        511: 'Network Authorisation Required',
    }
    """List of official HTTP response status codes"""
    
    def __init__(self, code: int=0, reason: str=''):
        """Status code of URL response is not 200"""

        self.code:   int = code
        self.reason: str = reason

    def __str__(self):
        if self.code and self.reason:
            return f'{self.code} {self.reason}'
        elif self.code:
            try:
                return f'{self.code} {self.status_codes[self.code]}'
            except KeyError:
                pass
        elif self.reason:
            try:
                code: int = {v: k for k, v in self.status_codes.items()}[self.reason]

                return f'{code} {self.reason}'
            except KeyError:
                pass
        
        return 'The URL request response returned an impassable HTTP status code'

class SSLCertificateFailed(RequestError):
    """The currently used SSL certificate could not be used to verify requests"""

    def __init__(self, message: str=''):
        """The currently used SSL certificate could not be used to verify requests"""

        self.message: str = message
    
    def __str__(self):
        if self.message:
            return self.message
        else:
            return 'The currently used SSL certificate could not be used to verify requests'

class InvalidWifiConnection(RequestError):
    """No valid internet connection could be found for the request"""

    def __init__(self, message: str=''):
        """No valid internet connection could be found for the request"""

        self.message: str = message
    
    def __str__(self):
        if self.message:
            return self.message
        else:
            return 'No valid internet connection could be found for the request'

class RequestRedirectError(RequestError):
    """Request redirected too many times or entered a redirect loop"""

    def __init__(self, message: str='', limit: int=0):
        """Request redirected too many times or entered a redirect loop"""

        self.message: str = message
        self.limit:   int = limit
    
    def __str__(self):
        if self.message:
            return self.message
        elif self.limit:
            return f'Request redirected too many times at {self.limit} redirects'
        else:
            return 'Request redirected too many times or entered a redirect loop'

class RequestCodecError(RequestError):
    """Unable to decode request body"""

    def __init__(self, message: str='', 
                 encoding: _bm.Union[str, tuple]=('utf-8', 'ISO-8859-1')):
        """Unable to decode request body"""

        self.message:                    str = message
        self.encoding: _bm.Union[str, tuple] = encoding
    
    def __str__(self):
        if self.message:
            return self.message
        elif self.encoding:
            return 'Unable to decode request body from codec(s): {}'.format(
                   '\'' + self.encoding + '\'' if type(self.encoding) is str else self.encoding)
        else:
            return 'Unable to decode request body'
