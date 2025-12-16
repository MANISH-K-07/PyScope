[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/github/license/MANISH-K-07/PyScope)](LICENSE)
[![GitHub Issues](https://img.shields.io/github/issues/MANISH-K-07/PyScope)](https://github.com/MANISH-K-07/PyScope/issues)

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

### 🏗️ Architecture & Design Decisions
```
Target Script
     │
     ▼
Runner (runner.py)
     │
     ├── ExecutionTimer        → wall-clock execution time
     ├── ProcessProfiler       → CPU & memory sampling
     ├── HotspotProfiler       → function-level hotspots
     │
     ▼
ProfilingReport
     │
     ├── JSON Report (machine-readable)
     ├── HTML Report (human-readable)
     │
     ├── OptimizationEngine   → rule-based suggestions
     └── MultiRunAnalyzer     → regression detection
```

### Folder Structure
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

## 🧪 Usage

### Run PyScope on any Python script

```
python main.py examples/slow_script.py
```
### Demo Output
- **CLI**
```
PyScope Performance Report
----------------------------------------
Execution Time : 1.8917 seconds
Average CPU    : 40.91 %
Peak Memory   : 19.15 MB

Top Hotspots
----------------------------------------
examples/slow_script.py:slow
  Calls      : 1
  Total Time : 1.8782 seconds

Optimization Suggestions
----------------------------------------
• Function 'examples/slow_script.py:slow' dominates runtime (99%).
Consider optimizing its algorithm or reducing repeated work.

JSON report saved to : reports\json\pyscope_report_2025-12-16T12-26-04.603376.json
HTML report saved to : reports\html\pyscope_report_2025-12-16T12-26-04.603376.html

Performance Regression Check
----------------------------------------
⚠️ Execution time increased from 1.5524s → 1.9941s (+28.4541%)
⚠️ Peak memory increased from 18.844MB → 19.2539MB (+2.1766%)
⚠️ Top hotspot 'examples/slow_script.py:<module>' increased from 1.4750s → 1.9084s
```

- **HTML**
<img width="1903" height="850" alt="image" src="https://github.com/user-attachments/assets/ccd55685-f101-461a-8b38-2acc3adf1f75" />

- **JSON**
```
{
    "timestamp": "2025-12-16T12:26:04.603376",
    "script": "examples/slow_script.py",
    "execution_time": 1.8917008000425994,
    "avg_cpu_percent": 40.90555555555555,
    "peak_memory_mb": 19.15234375,
    "hotspots": [
        {
            "function": "examples/slow_script.py:slow",
            "calls": 1,
            "total_time": 1.878245399799198
        }
    ],
    "suggestions": [
        "Function 'examples/slow_script.py:slow' dominates runtime (99%).\nConsider optimizing its algorithm or reducing repeated work."
    ],
    "regression": {
        "status": "regression",
        "messages": [
            {
                "level": "warning",
                "text": "Execution time increased from 1.5524s \u2192 1.9941s (+28.4541%)"
            },
            {
                "level": "warning",
                "text": "Peak memory increased from 18.844MB \u2192 19.2539MB (+2.1766%)"
            },
            {
                "level": "warning",
                "text": "Top hotspot 'examples/slow_script.py:<module>' increased from 1.4750s \u2192 1.9084s"
            }
        ]
    }
}
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
