import threading
from queue import Queue, Empty
from typing import Callable, Iterator, Any


class IteratorStopped(Exception):
    pass


def requires_active_iterator(func):
    def wrapper(*args, **kwargs):
        iterator = args[0]
        assert isinstance(iterator, MessageIterator), "Decorator 'requires_active_iterator' used outside of MessageIterator!"
        if iterator.stop_iteration:
            raise IteratorStopped("Unable to fulfill request, as the iterator has been stopped.")
        return func(*args, **kwargs)
    return wrapper


class MessageIterator:

    def __init__(self, message: Any = None):
        self.next_messages = Queue()
        self.next_iteration_condition = threading.Condition()   # Acts as a lock
        if message is not None:
            self.send_message(message)
        self.stop_iteration = False

    def __iter__(self):
        return self

    def __next__(self):
        with self.next_iteration_condition:
            if self.stop_iteration:
                raise StopIteration
            if self.next_messages.qsize() == 0:
                self.next_iteration_condition.wait()
                if self.stop_iteration:
                    raise StopIteration
            value = self.next_messages.get()
        return value

    @requires_active_iterator
    def send_message(self, message: Any):
        with self.next_iteration_condition:
            self.next_messages.put(message)
            self.next_iteration_condition.notify_all()

    @requires_active_iterator
    def stop(self):
        with self.next_iteration_condition:
            self.stop_iteration = True
            self.next_iteration_condition.notify_all()


class StreamStopped(Exception):
    pass


class TimeoutException(Exception):
    pass


def requires_active_stream(func):
    def wrapper(*args, **kwargs):
        stream_manager = args[0]
        assert isinstance(stream_manager, StreamManager), "Decorator 'requires_active_stream' used outside of StreamManager!"
        if stream_manager.stream_finished:
            raise StreamStopped("Unable to fulfill request, as the stream has finished.")
        return func(*args, **kwargs)
    return wrapper


class StreamManager:

    def __init__(self, stream_function: Callable[[Iterator], Iterator]):
        """
        Allows easier handling of a gRPC stream by providing methods to send and receive messages.

        :param stream_function: a reference to the function which should be used to send and receive messages.
        """
        self.incoming_messages = Queue()
        self.iterator = MessageIterator()
        self.stream_thread = threading.Thread(target=self._stream, args=[stream_function], daemon=True)
        self.stream_thread.start()
        self.stream_finished = False

    @requires_active_stream
    def receive(self, block: bool = True, timeout: float | None = None) -> Any:
        """
        Retrieves the oldest pending message. If there are no pending messages, wait until a new message arrives.

        :param block: whether to wait for a new message if there are no pending messages.
        :param timeout: time in seconds to wait for a new message before raising a TimeoutException. None will wait forever.
        :return: a message received by the gRPC stream.
        """
        try:
            return self.incoming_messages.get(block=block, timeout=timeout)
        except Empty:
            raise TimeoutException

    @requires_active_stream
    def send(self, message: Any, clear_received_messages=False):
        """
        Sends a new message to this object's stream.

        :param message: the message to send to the stream.
        :param clear_received_messages: clears received messages that haven't been read yet. Can be helpful to find the response to this message.
        """
        if clear_received_messages:
            with self.incoming_messages.mutex:
                self.incoming_messages.queue.clear()
        self.iterator.send_message(message)

    @requires_active_stream
    def stop_stream(self):
        """
        Closes the stream. A new StreamManager object will have to be created to start another stream.
        """
        self.iterator.stop()

    def _stream(self, stream_function: Callable[[Iterator], Iterator]):
        """
        Starts a bidirectional stream. Places incoming messages in self.incoming_messages as they arrive.

        :param stream_function: a reference to the function which will be used to send and receive messages.
        """
        try:
            response_iterator = stream_function(self.iterator)
            for response in response_iterator:
                self.incoming_messages.put(response)
        except Exception as e:
            print(f"Encountered exception while reading the gRPC stream: {e}")
            self.stop_stream()
        finally:
            self.stream_finished = True
