import threading
import math
import queue
import random
import time


class Receiver(threading.Thread):
    def __init__(self, q, func, timeout):
        self.func = func
        self.queue = q
        self.senders = []
        self.flag = True
        self.start_time = time.time()
        self.timeout = timeout

        def iterfunc(f, qu):
            while self.flag:
                self.flag = False
                for s in senders:
                    if s.is_alive():
                        self.flag = True
                if time.time() > self.start_time + self.timeout:
                    return
                print(f(qu.get(False)))

        super().__init__(target=iterfunc, args=(self.queue, self.queue))


class Sender(threading.Thread):
    def __init__(self, q, n, rec):
        self.queue = q
        self.receiver = rec

        def iterfunc(qu):
            for i in range(n):
                qu.put(random.randint(0, 1000))
                time.sleep(random.randint(0, 20))

        super().__init__(target=iterfunc, args=(self.queue, ))


q = queue.Queue(1024)
receiver = Receiver(q, math.sin, 10)
receiver.start()
for i in range(10):
    Sender(q, random.randint(1, 10), receiver).start()
