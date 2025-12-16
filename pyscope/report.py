import json
from datetime import datetime


class ProfilingReport:
    def __init__(self, execution_time, avg_cpu, peak_memory, hotspots):
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

    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "execution_time": self.execution_time,
            "avg_cpu_percent": self.avg_cpu_percent,
            "peak_memory_mb": self.peak_memory_mb,
            "hotspots": self.hotspots
        }

    def save(self, output_dir="reports"):
        filename = f"pyscope_report_{self.timestamp.replace(':', '-')}.json"
        path = f"{output_dir}/{filename}"

        with open(path, "w") as f:
            json.dump(self.to_dict(), f, indent=4)

        return path
