import sys
from pyscope.runner import run


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <script.py>")
        sys.exit(1)

    script_path = sys.argv[1]

    # Run profiler
    report = run(script_path)

    # Persist report
    report_path = report.save()

    # CLI output
    print("\nPyScope Performance Report")
    print("-" * 40)
    print(f"Execution Time : {report.execution_time:.4f} seconds")
    print(f"Average CPU    : {report.avg_cpu_percent:.2f} %")
    print(f"Peak Memory   : {report.peak_memory_mb:.2f} MB")

    print("\nTop Hotspots")
    print("-" * 40)
    for h in report.hotspots:
        print(f"{h['function']}")
        print(f"  Calls      : {h['calls']}")
        print(f"  Total Time : {h['total_time']:.4f} seconds\n")

    print(f"Report saved to: {report_path}")


if __name__ == "__main__":
    main()
