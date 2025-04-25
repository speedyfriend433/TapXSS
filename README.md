# TapXSS - XSS Vulnerability Scanner

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)

TapXSS is a powerful XSS (Cross-Site Scripting) vulnerability scanner that helps identify potential security flaws in web applications by testing URL parameters with various payloads.

## Features

- Multi-threaded scanning for efficient testing
- Payload reflection detection
- Executable pattern validation
- Comprehensive reporting
- Easy-to-use command line interface

## Installation

1. Clone this repository:
```bash
git clone https://github.com/speedyfriend433/TapXSS.git
cd TapXSS
```

2. Install required dependencies:
```bash
pip3 install -r requirements.txt
```

## Usage

```bash
python3 tapxss.py "https://example.com/search?q=test" payloads.txt
```

Where:
- `https://example.com/search?q=test` is the target URL with parameters to test
- `payloads.txt` is a text file containing XSS payloads (one per line)

## Sample Payloads File

Create a `payloads.txt` file with content like:
```
<script>alert(1)</script>
"><script>alert(1)</script>
'onmouseover=alert(1)
```

## Output

The tool will:
1. Print reflected payloads during scanning
2. Save confirmed vulnerabilities to `results/report.txt`

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
