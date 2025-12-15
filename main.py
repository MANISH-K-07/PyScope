import sys
from pyscope.runner import run

if len(sys.argv) < 2:
    print("Usage: python main.py <script.py>")
    sys.exit(1)

script_path = sys.argv[1]
time_taken = run(script_path)

print(f"Execution Time: {time_taken:.4f} seconds")
