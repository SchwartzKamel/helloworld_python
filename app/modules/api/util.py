"""util.py
================================================
Collection of utilities to use in an application
"""
from typing import Optional
import httpx

def GET_page(url:str, api_key: Optional[str] = None) -> str:
    """Send a GET request to a URL and return the response as text

    Args:
        url (str): URL to send a GET request to
        api_key (Optional[str], optional): Randommer.io API key. Defaults to None.

    Returns:
        str: HTTP GET response as text
    """
    if api_key is None:
        resp = httpx.get(f"{url}")
    else:
        params = {"X-Api-Key": api_key}
        resp = httpx.get(f"{url}", params)

    return resp.text