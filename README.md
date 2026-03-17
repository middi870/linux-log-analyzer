# Linux Log Analyzer

A modular, high-performance log analysis tool for Linux systems, designed to detect anomalies, monitor activity, and process logs in real time.

Built with a pipeline architecture inspired by modern observability systems, this project demonstrates practical systems engineering concepts including streaming data processing, rule-based detection, and parallel execution.

---

## 🚀 Features

* 🔍 Multi-format log parsing

  * SSH authentication logs
  * Nginx access logs
  * Generic syslog support

* ⚡ Parallel log processing

  * Multi-threaded pipeline (`--workers`)
  * Efficient handling of large log files

* 📡 Real-time monitoring

  * Live log streaming (`--follow`)
  * Systemd journal integration (`--journal`)

* 🚨 Rule-based anomaly detection

  * YAML-configurable rules
  * Brute force detection
  * Error spike detection

* 📊 Real-time analytics

  * Event counters
  * Top attacking IPs
  * Summary reporting

* 🖥️ Live terminal dashboard

  * Auto-refreshing metrics
  * Inspired by tools like htop

---

## 🧱 Architecture

```
Log Sources
 ├─ File logs
 ├─ Directory logs
 ├─ Stream logs
 └─ systemd journal
        ↓
Readers (File / Directory / Stream / Journal)
        ↓
Parallel Processing Pipeline
        ↓
Parser Layer (SSH / Nginx / Syslog)
        ↓
Event Normalization
        ↓
Rule Engine (YAML-based)
        ↓
Alert System
        ↓
Statistics Engine
        ↓
Live Dashboard / Reports
```

---

## 📦 Project Structure

```
linux-log-analyser
│
├── analyzer
│   ├── event.py
│   ├── rule_engine.py
│   ├── statistics.py
│   ├── dashboard.py
│   └── parallel_pipeline.py
│
├── parser
│   ├── base_parser.py
│   ├── auth_parser.py
│   ├── nginx_parser.py
│   └── syslog_parser.py
│
├── reader
│   ├── file_reader.py
│   ├── stream_reader.py
│   ├── directory_reader.py
│   └── journal_reader.py
│
├── cli
│   └── main.py
│
├── rules
│   └── rules.yaml
│
├── examples_test_log
│   ├── auth.log
│   └── nginx.log
│
└── README.md
```

---

## ⚙️ Installation

```bash
git clone https://github.com/your-username/linux-log-analyser.git
cd linux-log-analyser

python -m venv venv
source venv/bin/activate

pip install pyyaml
```

---

## ▶️ Usage

### Analyze a file

```bash
python -m cli.main --file examples_test_log/auth.log
```

---

### Analyze a directory

```bash
python -m cli.main --dir /var/log
```

---

### Follow logs in real time

```bash
python -m cli.main --follow /var/log/pacman.log
```

---

### Read from systemd journal

```bash
python -m cli.main --journal ssh
```

---

### Enable dashboard

```bash
python -m cli.main --file examples_test_log/auth.log --dashboard
```

---

### Use parallel processing

```bash
python -m cli.main --file huge.log --workers 8
```

---

## 📊 Example Output

### Alerts

```
[ALERT] Possible SSH brute force attack
Rule: ssh_bruteforce
IP: 192.168.1.22
Attempts: 34
Window: 60 seconds
```

---

### Summary Report

```
===== Log Analysis Summary =====

Total Events: 1000

Event Types
-------------------
AUTH_FAIL        800
AUTH_SUCCESS     200

Top Source IPs
-------------------
192.168.1.22     800
```

---

### Live Dashboard

```
===== Live Log Analyzer Dashboard =====

Total Events: 1200

Event Types
-------------------
AUTH_FAIL        950
HTTP_ERROR       120

Top Source IPs
-------------------
192.168.1.22     700
10.0.0.5         200
```

---

## 🧠 Design Highlights

* Stream-based processing (no full file loading)
* Sliding window anomaly detection
* Rule-based detection engine (extensible)
* Modular parser architecture
* Concurrent execution using thread pools
* Clean separation of concerns

---

## 🔧 Rules Configuration

Rules are defined in YAML:

```yaml
ssh_bruteforce:
  event_type: AUTH_FAIL
  threshold: 5
  window: 60
  alert: "Possible SSH brute force attack"

nginx_error_spike:
  event_type: HTTP_ERROR
  threshold: 10
  window: 30
  alert: "Possible nginx error spike"
```

---

## 📈 Benchmark (Example)

```
1,000,000 log lines
Workers: 8
Processing time: ~2–4 seconds
```

---

## 🎯 Use Cases

* Linux system monitoring
* Security analysis (SSH brute force detection)
* DevOps log inspection
* Backend infrastructure debugging
* Learning observability systems

---

## 🛣️ Future Improvements

* JSON output mode for integration
* Plugin-based parser system
* Persistent storage (SQLite / indexing)
* Web-based dashboard
* Distributed log processing

---

## 📜 License

MIT License

---

## 👨‍💻 Author

Built as a systems engineering project focusing on:

* Linux internals
* log processing pipelines
* real-time analytics
* performance-oriented design

---

