import threading
from queue import Queue
from typing import Callable, Iterator

from openobd import OpenOBDSession


class ConnectionMonitorManager:

    sample_size = None              # type: int

    def __init__(self, stream_function: Callable, sample_size=None):
        self.incoming_messages = Queue()
        self.stream_thread = threading.Thread(target=self._stream, args=(stream_function,), daemon=True)
        self.stream_thread.start()
        self.sample_size = sample_size if sample_size is not None else 10

    def _stream(self, stream_function: Callable):
        try:
            responses = stream_function()
            for response in responses:
                # check if the current size of the queue is reached its limit
                if self.incoming_messages.qsize() >= self.sample_size:
                    # remove first element
                    self.incoming_messages.get()
                    self.incoming_messages.task_done()
                # now we add the next message
                self.incoming_messages.put(response)
        except Exception as e:
            print(f"Encountered exception while reading the gRPC stream {e}")

    def retrieve_connection_data(self) -> list:
        messages = []
        while not self.incoming_messages.empty():
            message = self.incoming_messages.get()
            self.incoming_messages.task_done()
            messages.append(message)

        return messages
