class OptimizationEngine:
    def __init__(self, report):
        self.report = report

    def generate(self):
        suggestions = []

        total_time = self.report.execution_time
        hotspots = self.report.hotspots

        # Rule 1: Dominant hotspot
        if hotspots:
            top = hotspots[0]
            share = top["total_time"] / total_time if total_time > 0 else 0

            if share > 0.6:
                suggestions.append(
                    f"Function '{top['function']}' dominates runtime "
                    f"({share:.0%}).\nConsider optimizing its algorithm "
                    "or reducing repeated work."
                )

        # Rule 2: High CPU usage
        if self.report.avg_cpu_percent > 80:
            suggestions.append(
                "High average CPU usage detected.\nThe workload appears CPU-bound.\n"
                "Consider multiprocessing or algorithmic optimizations."
            )

        # Rule 3: High memory usage
        if self.report.peak_memory_mb > 500:
            suggestions.append(
                "High peak memory usage detected.\n"
                "Investigate large in-memory data structures or streaming approaches."
            )

        # Rule 4: Many hotspot calls
        for h in hotspots:
            if h["calls"] > 1000:
                suggestions.append(
                    f"Function '{h['function']}' is called frequently "
                    f"({h['calls']} calls).\nConsider caching or batching operations."
                )

        if not suggestions:
            suggestions.append(
                "No obvious performance bottlenecks detected.\n"
                "The program appears well-balanced."
            )

        return suggestions
