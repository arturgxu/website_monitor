"""
Checker module using 'requests'

Responsibilities:
    - Perform HTTP request to a given URL;
    - If HEAD fails to produce a status (network error or no status),
optionally perform a fallback GET;
    - Normalize result into a dataclass 'URLCheckResult' for downstream
processing;
    - Do not perform any logging to mail or sending. Just return the result.

Usage(example):
    from monitor.checker import check_url, URLCheckResult
    result = check_url('https://example.com/', timeout=10, fallback_get=True)
"""

from dataclasses import dataclass
from typing import Optional, Dict
import requests
import time

@dataclass
class URLCheckResult:
    url: str
    status_code: Optional[int] = None
    error: Optional[str] = None
    method: Optional[str] = None
    elapsed: Optional[float] = None
    headers: Optional[Dict[str, str]] = None

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
}

def _perform_request(url: str, method: str, timeout: float, verify_ssl: bool) -> URLCheckResult:
    result = URLCheckResult(url=url)
    start = time.time()

    try:
        resp = requests.request(
            method,
            url,
            headers=DEFAULT_HEADERS,
            timeout=timeout,
            verify=verify_ssl,
            allow_redirects=True
        )
        elapsed = time.time() - start
        result.status_code = resp.status_code
        result.headers = dict(resp.headers)
        result.method = method
        result.elapsed = elapsed
        result.error = None
        return result

    except requests.exceptions.Timeout:
        result.elapsed = time.time() - start
        result.error = f"timeout after {timeout} seconds"
        result.method = method
        return result

    except requests.exceptions.SSLError as e:
        result.elapsed = time.time() - start
        result.error = f"SSL error: {e}"
        result.method = method
        return result

    except requests.exceptions.ConnectionError as e:
        result.elapsed = time.time() - start
        result.error = f"connection error: {e}"
        result.method = method
        return result

    except requests.exceptions.RequestException as e:
        result.elapsed = time.time() - start
        result.error = f"unknown error: {e}"
        result.method = method
        return result

def check_url(url: str, timeout: float = 5.0, verify_ssl: bool = True, fallback_get: bool = True) -> URLCheckResult:
    head_result = _perform_request(url, method="HEAD", timeout=timeout, verify_ssl=verify_ssl)
    if head_result.status_code is not None:
        return head_result
    if fallback_get:
        get_result = _perform_request(url, method="GET", timeout=timeout, verify_ssl=verify_ssl)
        return get_result
    return head_result