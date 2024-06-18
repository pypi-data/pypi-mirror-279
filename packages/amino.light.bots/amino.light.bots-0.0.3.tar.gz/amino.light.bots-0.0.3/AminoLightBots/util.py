
import logging
import traceback
import threading
import queue as Queue
from typing import Union

logger = logging.getLogger('AminoBot')

class WorkerThread(threading.Thread):
    """
    :meta private:
    """
    count = 0

    def __init__(self, exception_callback=None, queue=None, name=None):
        if not name:
            name = "WorkerThread{0}".format(self.__class__.count + 1)
            self.__class__.count += 1
        if not queue:
            queue = Queue.Queue()

        threading.Thread.__init__(self, name=name)
        self.queue = queue
        self.daemon = True

        self.received_task_event = threading.Event()
        self.done_event = threading.Event()
        self.exception_event = threading.Event()
        self.continue_event = threading.Event()

        self.exception_callback = exception_callback
        self.exception_info = None
        self._running = True
        self.start()

    def run(self):
        while self._running:
            try:
                task, args, kwargs = self.queue.get(block=True, timeout=.5)
                self.continue_event.clear()
                self.received_task_event.clear()
                self.done_event.clear()
                self.exception_event.clear()
                logger.debug("Received task")
                self.received_task_event.set()

                task(*args, **kwargs)
                logger.debug("Task complete")
                self.done_event.set()
            except Queue.Empty:
                pass
            except Exception as e:
                logger.debug(type(e).__name__ + " occurred, args=" + str(e.args) + "\n" + traceback.format_exc())
                self.exception_info = e
                self.exception_event.set()
                if self.exception_callback:
                    self.exception_callback(self, self.exception_info)
                self.continue_event.wait()

    def put(self, task, *args, **kwargs):
        self.queue.put((task, args, kwargs))

    def raise_exceptions(self):
        if self.exception_event.is_set():
            raise self.exception_info

    def clear_exceptions(self):
        self.exception_event.clear()
        self.continue_event.set()

    def stop(self):
        self._running = False


class ThreadPool:
    """
    :meta private:
    """

    def __init__(self,num_threads=2):
        self.tasks = Queue.Queue()
        self.workers = [WorkerThread(self.on_exception, self.tasks) for _ in range(num_threads)]
        self.num_threads = num_threads

        self.exception_event = threading.Event()
        self.exception_info = None

    def put(self, func, *args, **kwargs):
        self.tasks.put((func, args, kwargs))

    def on_exception(self, worker_thread, exc_info):
        print(exc_info)
        self.exception_info = exc_info
        self.exception_event.set()
        worker_thread.continue_event.set()

    def raise_exceptions(self):
        if self.exception_event.is_set():
            raise self.exception_info

    def clear_exceptions(self):
        self.exception_event.clear()

    def close(self):
        for worker in self.workers:
            worker.stop()
        for worker in self.workers:
            if worker != threading.current_thread():
                worker.join()

def is_command(prefix: str, text: str) -> bool:
    r"""
    Checks if `text` is a command. Amino chat commands start with the '!' character.
    
    :param text: Text to check.
    :type text: :obj:`str`

    :return: True if `text` is a command, else False.
    :rtype: :obj:`bool`
    """
    if text is None: return False
    return text.startswith(prefix)

def extract_command(prefix: str, text: str) -> Union[str, None]:
    """
    Extracts the command from `text` (minus the '/') if `text` is a command (see is_command).
    If `text` is not a command, this function returns None.

    .. code-block:: python3
        :caption: Examples:
        
        extract_command('/help'): 'help'
        extract_command('/help@BotName'): 'help'
        extract_command('/search black eyed peas'): 'search'
        extract_command('Good day to you'): None

    :param text: String to extract the command from
    :type text: :obj:`str`

    :return: the command if `text` is a command (according to is_command), else None.
    :rtype: :obj:`str` or :obj:`None`
    """

    if text is None: return None
    return text.split()[0].split('@')[0][1:] if is_command(prefix, text) else None