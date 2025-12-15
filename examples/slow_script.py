import time

total = 0
for i in range(8_000_000):
    total += i

time.sleep(1)
print("Finished execution")
