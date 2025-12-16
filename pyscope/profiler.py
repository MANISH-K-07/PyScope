import psutil
import os
import time

class ProcessProfiler:
    def __init__(self):
        self.process = psutil.Process(os.getpid())
        self.cpu_samples = []
        self.memory_samples = []

    def sample(self):
        cpu = self.process.cpu_percent(interval=None)
        memory = self.process.memory_info().rss / (1024 * 1024)  # MB

        self.cpu_samples.append(cpu)
        self.memory_samples.append(memory)

    def average_cpu(self):
        return sum(self.cpu_samples) / len(self.cpu_samples) if self.cpu_samples else 0.0

    def peak_memory(self):
        return max(self.memory_samples) if self.memory_samples else 0.0
