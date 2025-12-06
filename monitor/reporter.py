"""
Reporter module - formatting HTTP check results for output

Responsibilities:
    - Receive a list of URLCheckResult objects;
    - Convert each result into a human-readable line;
    - Add unique messages for 4xx and 5xx classes of errors;
    - Add messages for network errors (timeouts, DNS, SLL issues);
    - Return the final multiline text for stdout output.
"""

from typing import List
from monitor.checker import URLCheckResult

def _format_single_result(result: URLCheckResult) -> str:
    url = result.url
    if result.status_code is None:
        return f"[NETWORK ERROR] {url} - {result.error or 'unknown error'}"
    code = result.status_code
    if 400 <= code < 500:
        return f"[CLIENT ERROR {code}] {url} - Page not found or request invalid]"
    if code >= 500:
        return f"[SERVER ERROR {code}] {url} - Internal server error]"
    return f"[OK] {url}"

def build_report(results: List[URLCheckResult]) -> str:
    lines = [_format_single_result(r) for r in results]
    return "\n".join(lines)