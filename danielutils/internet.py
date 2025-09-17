import logging
import urllib.request
import urllib.parse
from urllib.parse import urlparse
import urllib
from typing import Tuple as Tuple
from .decorators import validate
from .reflection import get_python_version
from .logging_.utils import get_logger

logger = get_logger(__name__)

if get_python_version() >= (3, 9):
    from builtins import tuple as Tuple  # type:ignore

# def prettify_html(html: str) -> str:
#     return html


@validate  # type:ignore
def get_html(url: str) -> str:
    """returns the html for a given url

    Args:
        url (str): url

    Returns:
        str: the html as a string
    """
    logger.info("Fetching HTML from URL: %s", url)
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers = {'User-Agent': user_agent, }
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as f:
        html = f.read().decode('UTF-8')
    logger.info("Successfully fetched HTML, length: %d characters", len(html))
    # return bs4(html, 'html.parser').prettify()
    return html


@validate  # type:ignore
def get_url_details(url: str) -> "Tuple[str, str, str, str, str, str]":
    """returns details about a url

    Args:
        url (str): url

    Returns:
        tuple[str, str, str, str, str]: scheme, netloc, path, params, query, fragment
    """
    scheme, netloc, path, params, query, fragment = urlparse(url)
    return scheme, netloc, path, params, query, fragment


@validate  # type:ignore
def url_encode(s: str) -> str:
    """encodes a string for url

    Args:
        s (str): string to encode

    Returns:
        str: encoded string
    """
    return urllib.parse.quote(s)


@validate  # type:ignore
def url_decode(s: str) -> str:
    """decodes a url encoded string back to normal string

    Args:
        s (str): string to decode

    Returns:
        str: result string
    """
    return urllib.parse.unquote_plus(s)


# def get_elements(html: str, tag: str) -> list[str]:
#     return [str(v) for v in bs4(html, 'html.parser').find_all(tag)]


__all__ = [
    # "prettify_html",
    "get_html",
    "get_url_details",
    "url_encode",
    "url_decode",
    # "get_elements"
]
