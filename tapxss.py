import requests
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

def load_payloads(file_path):
    with open(file_path, "r") as f:
        return [line.strip() for line in f.readlines() if line.strip()]

def inject_payload(url, param, payload):
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    if param not in query:
        return None
    query[param] = payload
    new_query = urlencode(query, doseq=True)
    new_url = urlunparse(parsed._replace(query=new_query))
    return new_url

def is_xss_successful(url, payload):
    """
    Validate if the XSS payload was successfully reflected and executable.
    Returns True if the payload is both reflected and appears to be executable.
    """
    try:
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            return False
            
        # Check if payload is reflected in response
        if payload not in response.text:
            return False
            
        # Additional checks for executable patterns
        executable_patterns = [
            'onxxx=',
            'onxxx%3D',
            'OnXxx=',
            'OnXxx%3D'
        ]
        
        return any(pattern in response.text for pattern in executable_patterns)
    except:
        return False

def scan_url(test_url, param, payload, results):
    try:
        response = requests.get(test_url, timeout=5)
        if payload in response.text:
            print(f"[+] Reflected: {payload} → {param}")
            results.append((test_url, param, payload))
    except Exception as e:
        print(f"[!] Error: {e}")

def scan(url, payloads):
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    param_names = list(params.keys())
    results = []
    threads = []

    print(f"🧪 Scanning {url}")
    with ThreadPoolExecutor(max_workers=10) as executor:
        for param in param_names:
            for payload in payloads:
                test_url = inject_payload(url, param, payload)
                executor.submit(scan_url, test_url, param, payload, results)
    
    # Filter out unsuccessful reflections
    filtered_results = []
    for url, param, payload in results:
        if is_xss_successful(url, payload):
            filtered_results.append((url, param, payload))
    
    return filtered_results

def save_results(results):
    if not results:
        return
    with open("results/report.txt", "w") as f:
        for url, param, payload in results:
            f.write(f"URL: {url}\nParam: {param}\nPayload: {payload}\n\n")
    print("✅ Report saved to results/report.txt")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python tapxss.py <URL_WITH_FUZZ> <payloads.txt>")
        sys.exit(1)

    url = sys.argv[1]
    payload_file = sys.argv[2]

    payloads = load_payloads(payload_file)
    results = scan(url, payloads)
    save_results(results)