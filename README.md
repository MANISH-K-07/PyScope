# PyScope 
### Python Performance Profiler — with Multi-Run Regression Detection & Optimization Suggestions

---

PyScope is a **lightweight, script-level performance profiler for Python** that combines **runtime measurement, CPU/memory profiling, hotspot analysis, optimization suggestions, and historical regression detection**.

Unlike traditional profilers that focus on a single execution, PyScope is designed to **track performance over time**, detect **statistically significant regressions**, and surface **function-level bottlenecks** automatically.

> **Core idea:** *Performance is not a single number — it’s a trend.*

---

## ✨ Key Features

### 🔍 Runtime Profiling
- Wall-clock execution time
- Average CPU utilization
- Peak memory usage

### 🔥 Hotspot Detection
- Function-level execution tracking
- Call counts and cumulative execution time
- Identifies dominant runtime contributors

### 💡 Optimization Suggestions
- Detects functions dominating total runtime
- Surfaces actionable optimization hints
- Rule-based (extensible to ML/LLM-based analysis)

### 📊 Report Generation
- **JSON reports** for programmatic analysis
- **HTML reports** for human-readable visualization
- Clean separation of:
  - `reports/json/`
  - `reports/html/`

### ⏱️ Multi-Run Performance Regression Detection (Advanced)
- Compares latest run against historical runs
- Script-aware and OS-safe (path normalization)
- Configurable regression thresholds

**Detects:**
- Execution time regressions
- Memory regressions
- Hotspot regressions

---

## 🧠 Why PyScope?

Most Python profilers answer:
> *“Where is my code slow right now?”*

PyScope answers:
> **“Did my code get slower than before — and why?”**

This makes PyScope suitable for:
- Continuous performance monitoring
- Algorithmic experimentation
- Research benchmarking
- Performance-sensitive refactors

---

## 🏗️ Architecture Overview
```
PyScope/
├── main.py # CLI entry point
├── pyscope/
│   ├── runner.py           # Orchestrates profiling lifecycle
│   ├── timer.py            # Wall-clock timing
│   ├── profiler.py         # CPU & memory sampling (psutil)
│   ├── hotspots.py         # Function-level execution tracking
│   ├── optimizer.py        # Optimization suggestion engine
│   ├── report.py           # JSON report generation
│   ├── html_report.py      # HTML report rendering
│   └── multi_run.py        # Historical regression analysis
├── examples/
│   └── slow_script.py      # Sample workload
└── reports/
    ├── json/
    └── html/
```


---

## 🔄 How Multi-Run Regression Detection Works

1. **Each run produces a timestamped JSON report**
   - Stored in `reports/json/`
   - Includes execution time, memory, hotspots, script path

2. **Script-aware matching**
   - Only compares runs of the *same script*
   - Uses OS-normalized absolute paths to avoid Windows/Linux mismatches

3. **Latest-vs-Previous comparison**
   - Execution time
   - Peak memory usage
   - Top hotspot cumulative time

4. **Threshold-based decision**
   - Default: **10% increase = regression**
   - Fully configurable

5. **Noise-aware**
   - Small runtime fluctuations are ignored
   - Prevents false positives caused by OS scheduling variance

### ⚙️ Configuration
Adjust regression sensitivity
In `pyscope/multi_run.py`:
```
def compare_latest(self, script_name=None, threshold=0.001):
```
- Lower threshold → more sensitive detection
- Higher threshold → more conservative detection

---

## 📌 Example: Regression Detection
```
Performance Regression Check
----------------------------------------
⚠️ Execution time increased from 1.5424s → 1.5462s (+0.2476%)
⚠️ Peak memory increased from 19.004MB → 19.1055MB (+0.5344%)
```


---

## 🧪 Usage

### Run PyScope on any Python script

```
python main.py examples/slow_script.py
```
### Demo Output
```
PyScope Performance Report
----------------------------------------
Execution Time : 1.5494 seconds
Average CPU    : 28.32 %
Peak Memory   : 18.80 MB

Top Hotspots
----------------------------------------
examples/slow_script.py:<module>
  Calls      : 1
  Total Time : 1.4540 seconds

examples/slow_script.py:slow
  Calls      : 1
  Total Time : 1.4540 seconds

Optimization Suggestions
----------------------------------------
• Function 'examples/slow_script.py:<module>' dominates runtime (94%).
Consider optimizing its algorithm or reducing repeated work.

JSON report saved to : reports\json\pyscope_report_2025-12-16T08-23-14.567350.json
HTML report saved to : reports\html\pyscope_report_2025-12-16T08-23-14.567350.html

Performance Regression Check
----------------------------------------
⚠️ Execution time increased from 1.4520s → 1.5494s (+6.7106%)
⚠️ Top hotspot 'examples/slow_script.py:<module>' increased from 1.4471s → 1.4540s
```
### What You Get

- CLI performance summary
- JSON report saved to reports/json/
- HTML report saved to reports/html/
- Automatic regression check against previous runs

## 🚧 Current Limitations
- Single-process Python scripts
- No multiprocessing or thread attribution (yet)
- Rule-based optimization suggestions

## 🛣️ Future Extensions
- Statistical confidence intervals over multiple baseline runs
- CI/CD integration (fail builds on regression)
- Flamegraph visualization
- ML-assisted optimization recommendations
- Language-agnostic profiling backend

## 🎓 Academic & Research Relevance
### PyScope demonstrates:
- Systems-level performance engineering
- Runtime instrumentation
- Historical performance analysis
- Noise-aware regression detection
- Clean, extensible software architecture
