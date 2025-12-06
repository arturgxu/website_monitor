"""
- Accepts a list of URLs;
- Checks each URL using check_url();
- Collects the results and returns build_report();
- Returns the finished report text.
"""

from monitor.checker import check_url, URLCheckResult
from monitor.reporter import build_report
from typing import List

def run_checks(urls: List[str]) -> str:
    results: List[URLCheckResult] = []
    for url in urls:
        url = url.strip()
        if not url:
            continue
        result = check_url(url)
        results.append(result)
    return build_report(results)