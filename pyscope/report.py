import os
import json
from datetime import datetime


class ProfilingReport:
    def __init__(self, execution_time, avg_cpu, peak_memory, hotspots, script_path=None):
        self.timestamp = datetime.utcnow().isoformat()
        self.execution_time = execution_time
        self.avg_cpu_percent = avg_cpu
        self.peak_memory_mb = peak_memory
        self.hotspots = [
            {
                "function": func,
                "calls": data["calls"],
                "total_time": data["total_time"]
            }
            for func, data in hotspots
        ]
        self.suggestions = []
        self.script = script_path  # <-- store script path for multi-run comparison

    def to_dict(self):
        data = {
            "timestamp": self.timestamp,
            "script": self.script,  # <-- include script path in JSON
            "execution_time": self.execution_time,
            "avg_cpu_percent": self.avg_cpu_percent,
            "peak_memory_mb": self.peak_memory_mb,
            "hotspots": self.hotspots,
        }
        if self.suggestions:
            data["suggestions"] = self.suggestions
        return data

    def save(self, base_dir="reports"):
        json_dir = os.path.join(base_dir, "json")
        os.makedirs(json_dir, exist_ok=True)

        filename = f"pyscope_report_{self.timestamp.replace(':', '-')}.json"
        path = os.path.join(json_dir, filename)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=4)

        return path
