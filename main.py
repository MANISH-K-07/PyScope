import sys
from pyscope.runner import run

if len(sys.argv) < 2:
    print("Usage: python main.py <script.py>")
    sys.exit(1)

script_path = sys.argv[1]
report = run(script_path)

print("\nPyScope Performance Report")
print("-" * 30)
print(f"Execution Time : {report['execution_time']:.4f} seconds")
print(f"Average CPU    : {report['avg_cpu_percent']:.2f} %")
print(f"Peak Memory   : {report['peak_memory_mb']:.2f} MB")
