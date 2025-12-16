import sys
import time
import os
from collections import defaultdict


class HotspotProfiler:
    """
    Function-level hotspot profiler using sys.setprofile.

    Tracks:
    - Number of calls per function
    - Total execution time per function

    Filters out:
    - Python interpreter internals (<frozen ...>)
    - Standard library code
    - Non-file-backed code objects (e.g. <string>)

    Also collapses redundant <module> entries when a single function dominates.
    """

    def __init__(self):
        self.call_stack = []
        self.stats = defaultdict(lambda: {
            "calls": 0,
            "total_time": 0.0
        })

        # Path to Python standard library (used for filtering)
        self.stdlib_path = os.path.dirname(os.__file__)

    def profiler(self, frame, event, arg):
        if event == "call":
            code = frame.f_code
            func_name = f"{code.co_filename}:{code.co_name}"
            self.call_stack.append((func_name, time.perf_counter()))

        elif event == "return":
            if not self.call_stack:
                return  # Safety guard

            func_name, start_time = self.call_stack.pop()
            elapsed = time.perf_counter() - start_time

            self.stats[func_name]["calls"] += 1
            self.stats[func_name]["total_time"] += elapsed

    def start(self):
        sys.setprofile(self.profiler)

    def stop(self):
        sys.setprofile(None)

    def top_hotspots(self, limit=10):
        filtered = []

        for func, data in self.stats.items():
            filename = func.split(":")[0]

            # Ignore non-file-backed code (e.g. <string>)
            if not filename.endswith(".py"):
                continue

            # Ignore frozen modules / interpreter internals
            if filename.startswith("<frozen"):
                continue

            # Ignore standard library
            if self.stdlib_path in filename:
                continue

            filtered.append((func, data))

        # Sort by total execution time (descending)
        filtered.sort(key=lambda item: item[1]["total_time"], reverse=True)

        # ---------------- Collapse redundant <module> ----------------
        # <module> represents the file-level execution frame
        # PyScope collapses the module frame — similar to how production profilers prioritize actionable hotspots

        if len(filtered) >= 2:
            top_func, top_data = filtered[0]
            second_func, second_data = filtered[1]

            if (
                "<module>" in top_func
                and top_data["calls"] == second_data["calls"]
                and abs(top_data["total_time"] - second_data["total_time"]) < 0.001
            ):
                # Drop the <module> entry as it adds no actionable insight
                filtered = filtered[1:]

        return filtered[:limit]
