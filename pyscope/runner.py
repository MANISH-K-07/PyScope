import runpy
import threading
import time

from pyscope.timer import ExecutionTimer
from pyscope.profiler import ProcessProfiler

def run(script_path):
    timer = ExecutionTimer()
    profiler = ProcessProfiler()
    running = True

    def sampler():
        while running:
            profiler.sample()
            time.sleep(0.1)  # sample every 100ms

    sampler_thread = threading.Thread(target=sampler)

    timer.start()
    sampler_thread.start()

    runpy.run_path(script_path, run_name="__main__")

    running = False
    sampler_thread.join()
    timer.stop()

    return {
        "execution_time": timer.elapsed(),
        "avg_cpu_percent": profiler.average_cpu(),
        "peak_memory_mb": profiler.peak_memory()
    }
