import os
from multiprocessing import Process
import time
import math


def slow_func(n):
    s = 0
    for i in range(math.floor(n)):
        s += 1
    return s


if __name__ == '__main__':
    size = 39916800
    results = [0, 0]
    for j in [0, 1]:
        res = 1
        times = []
        while True:
            processes = []
            for i in range(res):
                p = Process(target=slow_func, args=(size / res, ))
                processes.append(p)
            for p in processes:
                p.start()
            t1 = time.time()
            for p in processes:
                p.join()
            t2 = time.time()
            times.append(t2 - t1)
            print(f"{res} processes: {t2 - t1} s")
            if res > 1:
                if times[res - 2] / times[res - 1] < 1:
                    break
            res += 1
        results[j] = res
    if results[0] == results[1]:
        print(f"I think your CPU has {results[0] - 1} cores", end=" ")
        if results[0] == os.cpu_count():
            print("and I am right!")
        else:
            print(f"but it has {os.cpu_count()} cores...")
    else:
        print("I don't know how many cores do your CPU have because it is a very bad way to get this information!")
