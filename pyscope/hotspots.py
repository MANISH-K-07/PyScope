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
        # Track only Python-level function calls
        if event == "call":
            code = frame.f_code
            func_name = f"{code.co_filename}:{code.co_name}"
            self.call_stack.append((func_name, time.perf_counter()))

        elif event == "return":
            if not self.call_stack:
                return  # Safety guard against mismatched events

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

            # Ignore non-file-backed code objects (e.g. <string>)
            if not filename.endswith(".py"):
                continue

            # Ignore frozen modules and interpreter internals
            if filename.startswith("<frozen"):
                continue

            # Ignore standard library code
            if self.stdlib_path in filename:
                continue

            filtered.append((func, data))

        return sorted(
            filtered,
            key=lambda item: item[1]["total_time"],
            reverse=True
        )[:limit]
