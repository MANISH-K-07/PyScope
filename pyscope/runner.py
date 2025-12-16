import runpy
import threading
import time

from pyscope.timer import ExecutionTimer
from pyscope.profiler import ProcessProfiler
from pyscope.hotspots import HotspotProfiler
from pyscope.report import ProfilingReport


def run(script_path):
    timer = ExecutionTimer()
    process_profiler = ProcessProfiler()
    hotspot_profiler = HotspotProfiler()

    running = True

    def sampler():
        while running:
            process_profiler.sample()
            time.sleep(0.1)  # 100ms sampling interval

    sampler_thread = threading.Thread(target=sampler, daemon=True)

    # Start profiling
    timer.start()
    hotspot_profiler.start()
    sampler_thread.start()

    # Execute target script
    runpy.run_path(script_path, run_name="__main__")

    # Stop profiling
    running = False
    sampler_thread.join()
    hotspot_profiler.stop()
    timer.stop()

    # Build structured report
    return ProfilingReport(
        execution_time=timer.elapsed(),
        avg_cpu=process_profiler.average_cpu(),
        peak_memory=process_profiler.peak_memory(),
        hotspots=hotspot_profiler.top_hotspots()
    )
