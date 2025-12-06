# Website Status Monitor (HEAD/GET)

This project provides a lightweight monitoring script that checks multiple websites for availability using `HEAD` (with optional fallback to `GET`).  
It is designed to run on a server via **cron**, which captures the script output and delivers status reports by email through the server’s mail system.

The project does **not** send emails by itself.  
All notifications are handled externally by cron + the server’s MTA (Postfix, Exim, Mailcow, etc.).

---

## File Descriptions

### checker.py
Handles all HTTP logic:

- Sends `HEAD` requests  
- If `HEAD` fails or returns no status → optionally sends `GET`  
- Handles timeouts, SSL errors, and network exceptions  
- Returns a normalized `URLCheckResult` object

### reporter.py
Formats results into human-readable output:

- Adds unique messages for  
  - **4xx client errors**  
  - **5xx server errors**  
- Marks network errors (timeouts, DNS, SSL, connection issues)  
- Returns a complete multi-line report string

### runner.py
The orchestrator:

- Loads URL list  
- Runs checks for each URL via `checker.py`  
- Passes results to `reporter.py`  
- Returns the final report as a string (no printing)

### main.py
The execution entry point:

- Loads URLs from `urls.txt`  
- Runs the monitoring process  
- Prints the final report to stdout  
- Cron captures this output and emails it

---

## URL List

You must provide a file named `urls.txt`.

Format:  
One URL per line.

Example (see `urls_example.txt`):


---

## Installation & Activation (Server)

1. **Clone the project** onto the server:
   ```bash
   git clone <repo-url>
   cd website-monitor

2. **Install dependencies (Python 3.8+)**:
    ```bash
   pip3 install -r requirements.txt

3. **Create your URL list**:
    ```bash
   cp urls_example.txt urls.txt

4. **Test manually on the server**:
    ```bash
   python3 main.py 
   # or python main.py

5. **Configure cron (not included in this README)**:
    ```bash
   Cron should execute main.py, capture its stdout, and email it via the server’s configured mail system.
