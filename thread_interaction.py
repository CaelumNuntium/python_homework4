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
                for s in self.senders:
                    if s.is_alive():
                        self.flag = True
                if (not self.flag) and time.time() > self.start_time + self.timeout:
                    return
                if not qu.empty():
                    val = qu.get(False)
                    print(f"Receiver: f({val}) = {f(val)}")

        super().__init__(target=iterfunc, args=(self.func, self.queue))

    def add_sender(self, sender):
        self.senders.append(sender)


class Sender(threading.Thread):
    def __init__(self, q, n, rec):
        self.queue = q
        self.receiver = rec

        def iterfunc(qu):
            for i in range(n):
                val = random.randint(0, 1000)
                qu.put(val, block=False)
                print(f"Sender: send value {val}")
                time.sleep(random.randint(0, 10))

        super().__init__(target=iterfunc, args=(self.queue, ))
        self.receiver.add_sender(self)


q = queue.Queue(1024)
receiver = Receiver(q, math.sin, 10)
for i in range(10):
    s = Sender(q, 5, receiver)
    s.start()
receiver.start()
