# 🔎 Python Network Scanner

A lightweight, multithreaded **Python network reconnaissance tool** developed to understand the fundamentals of TCP/IP networking, host discovery, port scanning, service identification, and security-oriented reporting.

> ⚠️ **Authorized Use Only:** This project is intended for educational purposes and authorized security testing. Only scan systems and networks that you own or have explicit permission to assess.

---

## 📌 Overview

Network reconnaissance is an important part of cybersecurity because it helps security professionals understand what systems and services are exposed on a network.

This project implements a basic network scanner from scratch using Python's standard library. It focuses on learning how TCP connections, ports, IPv4 subnets, concurrency, and service identification work without relying on external scanning frameworks.

---

## ✨ Features

* 🔹 Single IPv4 host scanning
* 🔹 IPv4 subnet discovery
* 🔹 TCP port scanning
* 🔹 Multithreaded scanning
* 🔹 Configurable connection timeout
* 🔹 Common service identification
* 🔹 Optional HTTP metadata detection
* 🔹 CLI-based interface
* 🔹 CSV report generation
* 🔹 JSON report generation
* 🔹 Input validation
* 🔹 Logging
* 🔹 Unit tests

---

## 🛠️ Technologies

| Technology           | Purpose                   |
| -------------------- | ------------------------- |
| Python 3.10+         | Core programming language |
| `socket`             | TCP networking            |
| `ipaddress`          | IPv4/subnet handling      |
| `concurrent.futures` | Multithreaded scanning    |
| `http.client`        | Basic HTTP metadata       |
| `csv`                | CSV reporting             |
| `json`               | JSON reporting            |
| `unittest`           | Testing                   |

No third-party Python packages are required for Version 1.

---

## 🏗️ Project Architecture

```text
                         ┌──────────────────┐
                         │   CLI Interface  │
                         │     cli.py       │
                         └────────┬─────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                    ▼                           ▼
             Single Target                IPv4 Network
                    │                           │
                    │                           ▼
                    │                    Host Discovery
                    │                    discovery.py
                    │                           │
                    └─────────────┬─────────────┘
                                  ▼
                           TCP Port Scanner
                              ports.py
                                  │
                                  ▼
                         Service Identification
                             services.py
                                  │
                     ┌────────────┴────────────┐
                     ▼                         ▼
                 Terminal                 Reporting
                                             │
                                      ┌──────┴──────┐
                                      ▼             ▼
                                    JSON           CSV
```

---

## 📂 Project Structure

```text
python-network-scanner/
│
├── scanner/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py
│   ├── config.py
│   ├── discovery.py
│   ├── models.py
│   ├── ports.py
│   ├── reporting.py
│   ├── services.py
│   └── utils.py
│
├── tests/
│   ├── test_ports.py
│   └── test_utils.py
│
├── reports/
├── screenshots/
│
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

---

# 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/python-network-scanner.git
cd python-network-scanner
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

Version 1 uses only the Python standard library:

```bash
pip install -r requirements.txt
```

---

# ▶️ Usage

## Scan your own computer

The safest way to test the project is against localhost:

```bash
python -m scanner --target 192.168.x.x --ports 1-100
```

---

## Scan common ports

```bash
python -m scanner --target 192.168.x.x --profile common
```

Available profiles:

```text
quick
common
web
full
```

---

## Scan selected ports

```bash
python -m scanner --target 192.168.x.x --ports 22,80,443
```

---

## Scan a port range

```bash
python -m scanner --target 192.168.x.x --ports 1-1024
```

---

## Multithreaded scanning

```bash
python -m scanner \
    --target 192.168.x.x \
    --ports 1-1024 \
    --workers 100
```

---

## Authorized subnet discovery

```bash
python -m scanner --network 192.168.1.0/24
```

The scanner first attempts to identify reachable hosts using a small set of TCP discovery ports and then scans the configured ports on discovered hosts.

> A host may be online even if it does not respond on the discovery ports used by this Version 1 implementation.

---

# 🌐 HTTP Metadata

For HTTP/HTTPS services, basic metadata can optionally be collected:

```bash
python -m scanner \
    --target 192.168.x.x \
    --ports 80,443 \
    --http
```

The scanner can report:

* HTTP status
* `Server` header when provided

It does **not** attempt exploitation or vulnerability testing.

---

# 📊 Reporting

## JSON

```bash
python -m scanner \
    --target 192.168.x.x \
    --profile common \
    --json reports/scan.json
```

## CSV

```bash
python -m scanner \
    --target 192.168.x.x \
    --profile common \
    --csv reports/scan.csv
```

## Both

```bash
python -m scanner \
    --target 192.168.x.x \
    --profile common \
    --json reports/scan.json \
    --csv reports/scan.csv
```

---

# 🧪 Testing

Run the automated tests:

```bash
python -m unittest discover -s tests -v
```

The test suite covers:

* Port parsing
* IPv4 validation
* CIDR validation
* TCP port scanning

---

# ⚙️ CLI Options

```text
--target IP
    Scan a single IPv4 host.

--network CIDR
    Discover hosts in an IPv4 subnet.

--ports PORTS
    Specify ports such as:
    22,80,443
    or
    1-1024

--profile PROFILE
    quick | common | web | full

--workers N
    Maximum concurrent workers.

--timeout SECONDS
    TCP connection timeout.

--json FILE
    Save results as JSON.

--csv FILE
    Save results as CSV.

--http
    Collect basic HTTP metadata.

--log-level LEVEL
    DEBUG | INFO | WARNING | ERROR
```

---

# 🔐 Security & Ethical Use

This project is designed for:

* Cybersecurity education
* Networking education
* Authorized penetration-testing labs
* Personal/home lab reconnaissance
* Learning Python socket programming

Do **not** use this tool to scan systems without authorization.

The project intentionally does not include:

* Exploitation
* Credential attacks
* Authentication bypass
* Malware
* Stealth/evasion mechanisms
* Destructive actions

---

# 🔮 Future Improvements

### Version 2

* [ ] Async scanning with `asyncio`
* [ ] Better service identification
* [ ] Scan history
* [ ] SQLite database
* [ ] HTML reports
* [ ] GUI/dashboard
* [ ] Improved logging
* [ ] Configurable scan profiles

### Version 3

* [ ] IPv6 support
* [ ] Advanced protocol identification
* [ ] Visualization dashboard
* [ ] Historical comparison
* [ ] Performance benchmarking
* [ ] Expanded automated testing

---

# 👨‍💻 Author

**Darsh Baheti**

B.Tech — Electronics & Communication Engineering

Interested in:

* Cybersecurity
* Ethical Hacking
* Python
* Network Security
* Linux
* AI/ML

---

## ⭐ If you found this project useful

Feel free to explore the code, suggest improvements, or use the project as a learning reference.

**Built for learning. Built responsibly.**
