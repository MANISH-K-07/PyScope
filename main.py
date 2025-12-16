import sys
import os

from pyscope.runner import run
from pyscope.html_report import generate_html_report
from pyscope.optimizer import OptimizationEngine
from pyscope.multi_run import MultiRunAnalyzer


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <script.py>")
        sys.exit(1)

    script_path = sys.argv[1]

    # Run profiler
    report = run(script_path)

    # Attach script path for multi-run comparison
    report.script = script_path

    # Generate optimization suggestions
    engine = OptimizationEngine(report)
    report.suggestions = engine.generate()

    # Save JSON report
    report_path = report.save()

    # Save HTML report
    html_dir = os.path.join("reports", "html")
    os.makedirs(html_dir, exist_ok=True)
    html_filename = os.path.basename(report_path).replace(".json", ".html")
    html_path = os.path.join(html_dir, html_filename)
    generate_html_report(report, html_path)

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

    print("Optimization Suggestions")
    print("-" * 40)
    for s in report.suggestions:
        print(f"• {s}")

    print(f"\nJSON report saved to : {report_path}")
    print(f"HTML report saved to : {html_path}")

    # Multi-run comparison
    analyzer = MultiRunAnalyzer()
    regression_summary = analyzer.compare_latest(script_path)

    print("\nPerformance Regression Check")
    print("-" * 40)
    if isinstance(regression_summary, list):
        for r in regression_summary:
            print(f"⚠️ {r}")
    else:
        print(regression_summary)

    print("")

if __name__ == "__main__":
    main()
