import time

def slow():
    total = 0
    for i in range(20_000_000):  # increase this number
        total += i
    time.sleep(1)

slow()
