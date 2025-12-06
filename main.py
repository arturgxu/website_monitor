from monitor.runner import run_checks

def load_urls(path: str) -> list:
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def main():
    urls = load_urls("urls.txt")
    report_text = run_checks(urls)
    print(report_text)

if __name__ == "__main__":
    main()