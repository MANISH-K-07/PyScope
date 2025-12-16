from datetime import datetime


def generate_html_report(report, output_path):
    hotspots_rows = ""
    for h in report.hotspots:
        hotspots_rows += f"""
        <tr>
            <td>{h['function']}</td>
            <td>{h['calls']}</td>
            <td>{h['total_time']:.4f}</td>
        </tr>
        """

    html = f"""
    <html>
    <head>
        <title>PyScope Report</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
                background-color: #f8f9fa;
            }}
            h1 {{ color: #333; }}
            .card {{
                background: white;
                padding: 20px;
                margin-bottom: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
            }}
            th, td {{
                padding: 10px;
                border-bottom: 1px solid #ddd;
            }}
            th {{
                background-color: #f1f1f1;
            }}
        </style>
    </head>
    <body>

        <h1>PyScope Performance Report</h1>
        <p><strong>Generated:</strong> {datetime.utcnow().isoformat()}</p>

        <div class="card">
            <h2>Summary</h2>
            <p><strong>Execution Time:</strong> {report.execution_time:.4f} seconds</p>
            <p><strong>Average CPU:</strong> {report.avg_cpu_percent:.2f} %</p>
            <p><strong>Peak Memory:</strong> {report.peak_memory_mb:.2f} MB</p>
        </div>

        <div class="card">
            <h2>Hotspots</h2>
            <table>
                <tr>
                    <th>Function</th>
                    <th>Calls</th>
                    <th>Total Time (s)</th>
                </tr>
                {hotspots_rows}
            </table>
        </div>

    </body>
    </html>
    """

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
