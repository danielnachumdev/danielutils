import urllib.request
import urllib.parse
from urllib.parse import urlparse, urlencode
from typing import Tuple
import urllib
from .Decorators import validate


def prettify_html(html: str) -> str:
    return html


@validate(str)
def get_html(url: str) -> str:
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers = {'User-Agent': user_agent, }
    req = urllib.request.Request(url, headers=headers)
    html = urllib.request.urlopen(req).read().decode('UTF-8')
    # return bs4(html, 'html.parser').prettify()
    return html


@validate(str)
def get_url_details(url: str) -> Tuple[str, str, str, str, str]:
    scheme, netloc, path, params, query, fragment = urlparse(url)
    return scheme, netloc, path, params, query, fragment


@validate(str)
def url_encode(s: str) -> str:
    return urllib.parse.quote(s)


@validate(str)
def url_decode(s: str) -> str:
    return urllib.parse.unquote_plus(s)


def get_elements(html: str, tag: str) -> list[str]:
    from bs4 import BeautifulSoup as bs4
    return [str(v) for v in bs4(html, 'html.parser').find_all(tag)]
