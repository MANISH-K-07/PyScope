from pyscope.optimizer import OptimizationEngine


def generate_html_report(report, output_path, regression=None):
    # ---------------- Optimization Suggestions ----------------
    engine = OptimizationEngine(report)
    suggestions = engine.generate()

    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>PyScope Performance Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
            background-color: #f8f9fa;
        }}
        h1, h2 {{
            color: #333;
        }}
        .section {{
            margin-bottom: 30px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th, td {{
            border: 1px solid #ccc;
            padding: 8px;
            text-align: left;
        }}
        th {{
            background-color: #e9ecef;
        }}
        .suggestion {{
            background: #fff3cd;
            padding: 10px;
            border-left: 5px solid #ffc107;
            margin-bottom: 10px;
        }}
        .regression {{
            padding: 10px;
            margin-bottom: 10px;
            border-left: 5px solid #f59e0b;
            background-color: #fffbeb;
            font-weight: bold;
        }}
        .ok {{
            padding: 10px;
            margin-bottom: 10px;
            border-left: 5px solid #16a34a;
            background-color: #ecfdf5;
            font-weight: bold;
        }}
    </style>
</head>
<body>

<h1>PyScope Performance Report</h1>

<div class="section">
    <h2>Summary</h2>
    <p><strong>Execution Time:</strong> {report.execution_time:.4f} seconds</p>
    <p><strong>Average CPU:</strong> {report.avg_cpu_percent:.2f}%</p>
    <p><strong>Peak Memory:</strong> {report.peak_memory_mb:.2f} MB</p>
</div>

<div class="section">
    <h2>Top Hotspots</h2>
    <table>
        <tr>
            <th>Function</th>
            <th>Calls</th>
            <th>Total Time (s)</th>
        </tr>
"""

    for h in report.hotspots:
        html += f"""
        <tr>
            <td>{h['function']}</td>
            <td>{h['calls']}</td>
            <td>{h['total_time']:.4f}</td>
        </tr>
        """

    html += """
    </table>
</div>
"""

    # ---------------- Regression Section ----------------
    if regression:
        html += """
<div class="section">
    <h2>Performance Regression Check</h2>
"""
        if regression["status"] == "insufficient":
            html += f"""
    <div class="ok">
        {regression["messages"][0]}
    </div>
"""
        elif regression["status"] == "ok":
            html += f"""
    <div class="ok">
        {regression["messages"][0]}
    </div>
"""
        else:
            for msg in regression["messages"]:
                html += f"""
    <div class="regression">
        ⚠️ {msg["text"]}
    </div>
"""
        html += """
</div>
"""

    # ---------------- Optimization Section ----------------
    html += """
<div class="section">
    <h2>Optimization Suggestions</h2>
"""

    for s in suggestions:
        html += f"""
    <div class="suggestion">
        {s}
    </div>
"""

    html += """
</div>

</body>
</html>
"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
