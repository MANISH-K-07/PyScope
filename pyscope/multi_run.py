import os
import json
from glob import glob

class MultiRunAnalyzer:
    def __init__(self, reports_dir="reports/json"):
        self.reports_dir = reports_dir

    def load_reports(self, script_name=None):
        files = sorted(glob(os.path.join(self.reports_dir, "*.json")))
        reports = []

        for f in files:
            with open(f, "r", encoding="utf-8") as fp:
                data = json.load(fp)
                if script_name is None or os.path.basename(data.get("script", "")) == os.path.basename(script_name):
                    reports.append(data)
        return reports

    def compare_latest(self, script_name=None, threshold=0.001):
        reports = self.load_reports(script_name)

        if len(reports) < 2:
            return "Not enough runs to compare."

        previous = reports[-2]
        latest = reports[-1]

        regressions = []

        # Compare execution time
        prev_time = previous["execution_time"]
        latest_time = latest["execution_time"]
        if latest_time > prev_time * (1 + threshold):
            regressions.append(
                f"Execution time increased from {prev_time:.4f}s → {latest_time:.4f}s (+{((latest_time-prev_time)/prev_time)*100:.4f}%)"
            )

        # Compare peak memory
        prev_mem = previous["peak_memory_mb"]
        latest_mem = latest["peak_memory_mb"]
        if latest_mem > prev_mem * (1 + threshold):
            regressions.append(
                f"Peak memory increased from {prev_mem:.3f}MB → {latest_mem:.4f}MB (+{((latest_mem-prev_mem)/prev_mem)*100:.4f}%)"
            )

        # Compare top hotspot
        if previous["hotspots"] and latest["hotspots"]:
            prev_top = previous["hotspots"][0]
            latest_top = latest["hotspots"][0]
            if latest_top["total_time"] > prev_top["total_time"] * (1 + threshold):
                regressions.append(
                    f"Top hotspot '{latest_top['function']}' increased from {prev_top['total_time']:.4f}s → {latest_top['total_time']:.4f}s"
                )

        if not regressions:
            return "No significant performance regressions detected."

        return regressions
