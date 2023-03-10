from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer, WebsocketConsumer

from chat.models import Room

class Hello(WebsocketConsumer):
    def connect(self):
        super().connect()

        user=self.scope["user"]
        message = f"Hello, {user.username}, "
        self.send(message)
class ChatConsumer(JsonWebsocketConsumer):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group_name =""

    def connect(self):
        user = self.scope["user"]

        if not user.is_authenticated:
            self.close()
        else:
            room_pk = self.scope["url_route"]["kwargs"]["room_pk"]
            self.group_name = Room.make_chat_group_name(room_pk=room_pk)

            async_to_sync(self.channel_layer.group_add)(
                self.group_name,
                self.channel_name
            )
            self.accept()

    def disconnect(self, code):
        if self.group_name:
            async_to_sync(self.channel_layer.group_discard)(
                self.group_name,
                self.channel_name
            )

    def receive_json(self, content, **kwargs):
        user=self.scope["user"]

        _type = content["type"]

        if _type == "chat.message":
            message = content["message"]
            sender=user.username
            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    "type": "chat.message",
                    "message": message,
                    "sender": sender,
                },
            )
        else:
            print(f"Invalid message type : {_type}")
    def chat_message(self, message_dict):
        self.send_json({
            "type":"chat.message",
            "message":message_dict["message"],
            "sender": message_dict["sender"],
        })

