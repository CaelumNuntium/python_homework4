from multiprocessing import Process
import time
import math


def slow_func(a, b):
    s = 0
    for i in range(math.floor(a), math.ceil(b)):
        s += 1
    return s


if __name__ == '__main__':
    size = 39916800
    res = 1
    times = []
    while True:
        processes = []
        for i in range(res):
            p = Process(target=slow_func, args=(i * size / res, (i + 1) * size / res))
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
    print(f"Your CPU has {res - 1} cores")
