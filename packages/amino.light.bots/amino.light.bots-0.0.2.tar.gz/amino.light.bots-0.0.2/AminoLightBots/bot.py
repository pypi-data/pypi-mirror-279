
import re
import sys
import logging

from time import sleep
from threading import Thread
from AminoLightBots import util
from AminoLightPy.lib.util import objects
from AminoLightPy import Client, SubClient
from typing import Callable, Optional, List
from AminoLightBots.typing import CustomMessage
from AminoLightPy.lib.util.objects import Event
from AminoLightPy.managers import Typing, Recording

from AminoLightBots.handler_backends import MemoryHandlerBackend, ContinueHandling
from AminoLightBots.custom_filters import SimpleCustomFilter, AdvancedCustomFilter


logger = logging.getLogger('AminoBot')
formatter = logging.Formatter(
    '%(asctime)s (%(filename)s:%(lineno)d %(threadName)s) %(levelname)s - %(name)s: "%(message)s"'
)

console_output_handler = logging.StreamHandler(sys.stderr)
console_output_handler.setFormatter(formatter)
logger.addHandler(console_output_handler)

logger.setLevel(logging.ERROR)

class Handler:
    """
    Class for (next step|reply) handlers.
    """

    def __init__(self, callback, *args, **kwargs):
        self.callback = callback
        self.args = args
        self.kwargs = kwargs

    def __getitem__(self, item):
        return getattr(self, item)

class Bot(Client):
    def __init__(
        self, *, email = None, password = None, threaded = True, num_threads = 2,
        ignore_myself = True
    ) -> None:
        super().__init__()
        if email is None or password is None:
            raise ValueError("Either email and password must be specified")
        Thread(target=self._login, args=(email, password)).start()

        self.next_step_backend = MemoryHandlerBackend()
        self.reply_backend = MemoryHandlerBackend()
        self.user_backend = MemoryHandlerBackend()
        self.sub_client_dict: dict[str, SubClient] = {}
        self.custom_filters = {}
        self.prefix = "!"

        self.message_handlers = []
        self.ignore_myself = ignore_myself
        self.threaded = threaded
        if self.threaded:
            self.worker_pool = util.ThreadPool(num_threads=num_threads)

        self.start_text_message()

    def _login(self, email: str, password: str):
        while True:
            super().login(email, password)
            sleep(82800)

    def clear_step_handler_by_chat_id(self, chat_id: str) -> None:
        """
        Clears all callback functions registered by register_next_step_handler().

        :param chat_id: The chat for which we want to clear next step handlers
        :type chat_id: :obj:`str`

        :return: None
        """
        self.next_step_backend.clear_handlers(chat_id)

    def clear_reply_handlers(self, message: objects.Message) -> None:
        """
        Clears all callback functions registered by register_for_reply() and register_for_reply_by_message_id().

        :param message: The message for which we want to clear reply handlers
        :type message: :class:`AminoLightPy.lib.util.objects.Message`

        :return: None
        """
        message_id = message.messageId
        self.clear_reply_handlers_by_message_id(message_id)

    def clear_reply_handlers_by_message_id(self, message_id: str) -> None:
        """
        Clears all callback functions registered by register_for_reply() and register_for_reply_by_message_id().

        :param message_id: The message id for which we want to clear reply handlers
        :type message_id: :obj:`str`

        :return: None
        """
        self.reply_backend.clear_handlers(message_id)

    def register_for_reply(self, message: objects.Message, callback: Callable, *args, **kwargs) -> None:
        """
        Registers a callback function to be notified when a reply to `message` arrives.

        Warning: In case `callback` as lambda function, saving reply handlers will not work.

        :param message: The message for which we are awaiting a reply.
        :type message: :class:`AminoLightPy.lib.util.objects.Message`

        :param callback: The callback function to be called when a reply arrives. Must accept one `message`
            parameter, which will contain the replied message.
        :type callback: :obj:`Callable[[AminoLightPy.lib.util.objects.Message], None]`

        :param args: Optional arguments for the callback function.
        :param kwargs: Optional keyword arguments for the callback function.
        
        :return: None
        """
        message_id = message.messageId
        self.register_for_reply_by_message_id(message_id, callback, *args, **kwargs)

    def register_next_step_handler(self, message: objects.Message, callback: Callable, *args, **kwargs) -> None:
        """
        Registers a callback function to be notified when new message arrives after `message`.

        Warning: In case `callback` as lambda function, saving next step handlers will not work.

        :param message: The message for which we want to handle new message in the same chat.
        :type message: :class:`AminoLightPy.lib.util.objects.Message`

        :param callback: The callback function which next new message arrives.
        :type callback: :obj:`Callable[[AminoLightPy.lib.util.objects.Message], None]`

        :param args: Args to pass in callback func

        :param kwargs: Args to pass in callback func

        :return: None
        """
        chat_id = message.chatId
        self.register_next_step_handler_by_chat_id(chat_id, callback, *args, **kwargs)

    def register_for_user(self, message: objects.Message, callback: Callable, *args, **kwargs) -> None:
        """
        Registers a callback function that will be notified when a new message arrives from the user..

        Warning: In case `callback` as lambda function, saving next step handlers will not work.

        :param message: The message for which we want to handle new message in the same chat.
        :type message: :class:`AminoLightPy.lib.util.objects.Message`

        :param callback: The callback function which next new message arrives.
        :type callback: :obj:`Callable[[AminoLightPy.lib.util.objects.Message], None]`

        :param args: Args to pass in callback func

        :param kwargs: Args to pass in callback func

        :return: None
        """
        chat_id = message.author.userId
        self.register_for_user_id(chat_id, callback, *args, **kwargs)

    def register_for_reply_by_message_id(
            self, message_id: str, callback: Callable, *args, **kwargs) -> None:
        """
        Registers a callback function to be notified when a reply to `message` arrives.

        Warning: In case `callback` as lambda function, saving reply handlers will not work.

        :param message_id: The id of the message for which we are awaiting a reply.
        :type message_id: :obj:`str`

        :param callback: The callback function to be called when a reply arrives. Must accept one `message`
            parameter, which will contain the replied message.

        :type callback: :obj:`Callable[[AminoLightPy.lib.util.objects.Message], None]`

        :param args: Optional arguments for the callback function.
        :param kwargs: Optional keyword arguments for the callback function.

        :return: None
        """
        self.reply_backend.register_handler(message_id, Handler(callback, *args, **kwargs))

    def register_next_step_handler_by_chat_id(
            self, chat_id: str, callback: Callable, *args, **kwargs) -> None:
        """
        Registers a callback function to be notified when new message arrives in the given chat.

        Warning: In case `callback` as lambda function, saving next step handlers will not work.

        :param chat_id: The chat (chat ID) for which we want to handle new message.
        :type chat_id: :obj:`str`

        :param callback: The callback function which next new message arrives.
        :type callback: :obj:`Callable[[AminoLightPy.lib.util.objects.Message], None]`

        :param args: Args to pass in callback func
        
        :param kwargs: Args to pass in callback func

        :return: None
        """
        self.next_step_backend.register_handler(chat_id, Handler(callback, *args, **kwargs))

    def register_for_user_id(
            self, user_id: str, callback: Callable, *args, **kwargs) -> None:
        """
        Warning: In case `callback` as lambda function, saving reply handlers will not work.

        :param callback: The callback function which next new message arrives.
        :type callback: :obj:`Callable[[AminoLightPy.lib.util.objects.Message], None]`

        :param args: Args to pass in callback func
        
        :param kwargs: Args to pass in callback func

        :return: None
        """
        self.user_backend.register_handler(user_id, Handler(callback, *args, **kwargs))

    @staticmethod
    def check_commands_input(commands, method_name):
        """
        :meta private:
        """
        if not isinstance(commands, list) or not all(isinstance(item, str) for item in commands):
            logger.error(f"{method_name}: Commands filter should be list of strings (commands), unknown type supplied to the 'commands' filter list. Not able to use the supplied type.")

    @staticmethod
    def check_regexp_input(regexp, method_name):
        """
        :meta private:
        """
        if not isinstance(regexp, str):
            logger.error(f"{method_name}: Regexp filter should be string. Not able to use the supplied type.")

    @staticmethod
    def _build_handler_dict(handler, **filters):
        """
        Builds a dictionary for a handler

        :param handler:
        :param filters:
        :return:
        """
        return {
            'function': handler,
            'filters': {ftype: fvalue for ftype, fvalue in filters.items() if fvalue is not None}
            # Remove None values, they are skipped in _test_filter anyway
            #'filters': filters
        }

    def message_handler(
            self,
            commands: Optional[List[str]]=None,
            regexp: Optional[str]=None,
            func: Optional[Callable]=None,
            **kwargs):
        """
        Handles New incoming message of any kind - text, photo, sticker, etc.
        As a parameter to the decorator function, it passes :class:`AminoLightPy.lib.util.objects.Message` object.
        All message handlers are tested in the order they were added.

        Example:

        .. code-block:: python3
            :caption: Usage of message_handler

            bot = Bot('email', 'password')

            # Handles all messages which text matches regexp.
            @bot.message_handler(regexp='someregexp')
            def command_help(message):
                bot.send_message(message.chatId, 'Did someone call for help?')

            # Handle all sent documents of type 'text/plain'.
            @bot.message_handler(func=lambda message: True)
            def command_handle_audio(message):
                bot.send_message(message.chatId, 'Audio received, sir!')

        :param commands: Optional list of strings (commands to handle).
        :type commands: :obj:`list` of :obj:`str`

        :param regexp: Optional regular expression.
        :type regexp: :obj:`str`

        :param func: Optional lambda function. The lambda receives the message to test as the first parameter.
            It must return True if the command should handle the message.
        :type func: :obj:`lambda`

        :param kwargs: Optional keyword arguments(custom filters)

        :return: decorated function
        """

        method_name = "message_handler"

        if commands is not None:
            self.check_commands_input(commands, method_name)
            if isinstance(commands, str):
                commands = [commands]

        if regexp is not None:
            self.check_regexp_input(regexp, method_name)


        def decorator(handler):
            handler_dict = self._build_handler_dict(handler,
                                                    commands=commands,
                                                    regexp=regexp,
                                                    func=func,
                                                    **kwargs)
            self.add_message_handler(handler_dict)
            return handler

        return decorator

    def add_message_handler(self, handler_dict):
        """
        Adds a message handler
        Note that you should use register_message_handler to add message_handler to the bot.

        :meta private:

        :param handler_dict:
        :return:
        """
        self.message_handlers.append(handler_dict)

    def _notify_next_handlers(self, message: objects.Message):
        """
        Description: TBD

        :param new_messages:
        :return:
        """
        handlers = self.next_step_backend.get_handlers(message.chatId)
        if handlers:
            for handler in handlers:
                self._exec_task(handler["callback"], message, *handler["args"], **handler["kwargs"])

    def _notify_reply_handlers(self, message: objects.Message) -> None:
        """
        Notify handlers of the answers

        :param new_messages:
        :return:
        """
        if hasattr(message, "reply_to_message") and message.reply_to_message is not None:
            handlers = self.reply_backend.get_handlers(message.reply_to_message.message_id)
            if handlers:
                for handler in handlers:
                    self._exec_task(handler["callback"], message, *handler["args"], **handler["kwargs"])
    
    def _test_filter(self, message_filter, filter_value, message):
        """
        Test filters

        :param message_filter: Filter type passed in handler
        :param filter_value: Filter value passed in handler
        :param message: Message to test
        :return: True if filter conforms
        """

        if message_filter == 'content_types':
            return True
        elif message_filter == 'regexp':
            return  re.search(filter_value, message.content, re.IGNORECASE)
        elif message_filter == 'commands':
            return  util.extract_command(self.prefix, message.content.lower()) in filter_value
        elif message_filter == 'func':
            return filter_value(message)
        elif self.custom_filters and message_filter in self.custom_filters:
            return self._check_filter(message_filter,filter_value,message)
        else:
            return False

    def _check_filter(self, message_filter, filter_value, message):
        filter_check = self.custom_filters.get(message_filter)
        if not filter_check:
            return False
        elif isinstance(filter_check, SimpleCustomFilter):
            return filter_value == filter_check.check(message)
        elif isinstance(filter_check, AdvancedCustomFilter):
            return filter_check.check(message, filter_value)
        else:
            logger.error("Custom filter: wrong type. Should be SimpleCustomFilter or AdvancedCustomFilter.")
            return False

    def _test_message_handler(self, message_handler, message):
        """
        Test message handler

        :param message_handler:
        :param message:
        :return:
        """
        for message_filter, filter_value in message_handler['filters'].items():
            if filter_value is None:
                continue

            if not self._test_filter(message_filter, filter_value, message):
                return False

        return True

    def _run_middlewares_and_handler(self, message, handlers):
        """
        This method is made to run handlers and middlewares in queue.

        :param message: received message (update part) to process with handlers and/or middlewares
        :param handlers: all created handlers (not filtered)
        :param middlewares: middlewares that should be executed (already filtered)
        :param update_type: handler/update type (Update field name)
        :return:
        """
        if handlers:
            for handler in handlers:
                if self._test_message_handler(handler, message):
                    result = handler['function'](message)
                    if not isinstance(result, ContinueHandling):
                        break

        
    def _notify_command_handlers(self, handlers, message):
        """
        Notifies command handlers.

        :param handlers: all created handlers
        :param new_messages: received messages to proceed
        :param update_type: handler/update type (Update fields)
        :return:
        """

        if not(handlers):
            return
        
        self._exec_task(
            self._run_middlewares_and_handler,
            message,
            handlers=handlers)

    def process_new_message(self, new_message):
        """
        :meta private:
        """
        self._notify_next_handlers(new_message)
        self._notify_reply_handlers(new_message)
        self._notify_command_handlers(self.message_handlers, new_message)

    def _exec_task(self, task, *args, **kwargs):
        if self.threaded:
            self.worker_pool.put(task, *args, **kwargs)
        else:
            try:
                task(*args, **kwargs)
            except Exception as e:
                raise e

    def process_new_updates(self, event: Event):
        if self.ignore_myself:
            if self.profile.userId == event.message.author.userId:
                return
        
        if event.comId not in self.sub_client_dict:
            if event.comId:
                sub_client = SubClient(comId=event.comId, profile=self.profile)
            else:
                sub_client = self

            self.sub_client_dict[event.comId] = sub_client
        
        else:
            sub_client = self.sub_client_dict[event.comId]
        
        custom_message = CustomMessage(event.message.json, sub_client)
        self.process_new_message(custom_message)

    def start_text_message(self):
        self.event("on_text_message")(self.process_new_updates)

    def typing(self, message: CustomMessage) -> Typing:
        return super().typing(message.chatId, message.sub_client.comId)

    def recording(self, message: CustomMessage) -> Recording:
        return super().recording(message.chatId, message.sub_client.comId)