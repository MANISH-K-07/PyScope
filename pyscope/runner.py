import runpy
from pyscope.timer import ExecutionTimer

def run(script_path):
    timer = ExecutionTimer()
    timer.start()

    runpy.run_path(script_path, run_name="__main__")

    timer.stop()
    return timer.elapsed()
