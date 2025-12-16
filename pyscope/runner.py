import runpy
import threading
import time

from pyscope.timer import ExecutionTimer
from pyscope.profiler import ProcessProfiler
from pyscope.hotspots import HotspotProfiler

def run(script_path):
    timer = ExecutionTimer()
    process_profiler = ProcessProfiler()
    hotspot_profiler = HotspotProfiler()

    running = True

    def sampler():
        while running:
            process_profiler.sample()
            time.sleep(0.1)

    sampler_thread = threading.Thread(target=sampler)

    timer.start()
    hotspot_profiler.start()
    sampler_thread.start()

    runpy.run_path(script_path, run_name="__main__")

    running = False
    sampler_thread.join()
    hotspot_profiler.stop()
    timer.stop()

    return {
        "execution_time": timer.elapsed(),
        "avg_cpu_percent": process_profiler.average_cpu(),
        "peak_memory_mb": process_profiler.peak_memory(),
        "hotspots": hotspot_profiler.top_hotspots()
    }
