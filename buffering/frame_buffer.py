from queue import Queue

class FrameBuffer:
    def __init__(self, maxsize: int = 100):
        self.queue = Queue(maxsize=maxsize)

    def put(self, frame):
        if not self.queue.full():
            self.queue.put(frame)

    def get(self):
        return self.queue.get()

    def empty(self) -> bool:
        return self.queue.empty()