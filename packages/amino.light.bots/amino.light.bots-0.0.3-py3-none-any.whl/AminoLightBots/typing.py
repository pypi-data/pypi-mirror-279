from AminoLightPy import SubClient
from AminoLightPy.lib.util.objects import Message

class CustomMessage(Message):
    def __init__(self, data: dict, sub_client: SubClient):
        super().__init__(data)

        self.sub_client = sub_client

    def reply(self, message: str) -> int:
        return self.sub_client.send_message(
            chatId=self.chatId,
            replyTo=self.messageId,
            message=message,
        )

    def get_sub_client(self):
        return self.sub_client

    def delete(self):
        return self.sub_client.delete_message(
            chatId=self.chatId,
            messageId=self.messageId
        )

    def read(self):
        return self.sub_client.mark_as_read(
            chatId=self.chatId,
            replyTo=self.messageId,
        )

