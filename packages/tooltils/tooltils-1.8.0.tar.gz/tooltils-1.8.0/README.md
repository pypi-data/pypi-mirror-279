# tooltils | v1.8.0

[![python](https://img.shields.io/badge/python-3.7+-teal)](https://pypi.org/project/tooltils/)
[![downloads](https://static.pepy.tech/personalized-badge/tooltils?period=total&units=international_system&left_color=grey&right_color=red&left_text=downloads)](https://pepy.tech/project/tooltils)

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

## Installation

Get the latest version from PyPi

```console
python -m pip install tooltils
```

OR install using the source code

```console
git clone https://github.com/feetbots/tooltils.git
cd tooltils
python -m pip install setup.py --user
```

## API

The full API is available to read in the project files at [**API.md**](API.md)

## Best Features

Tooltils is built completely on the Python standard library, but still implementing advanced features like:
- Automatic or specified timezone conversion for date and time methods
- A command line interface to manage the installation
- Obtaining thorough operating system information
- Keep-alive connection re-use for requesting
- High optimisation
