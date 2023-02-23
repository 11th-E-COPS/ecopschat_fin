import json

from channels.generic.websocket import WebsocketConsumer

class LiveblogConsumer(WebsocketConsumer):
    #메세지 받을 그룹명 명시
    groups = ["liveblog"]

    #수신 메세지에 대응되는 인자는 1개
    def liveblog_post_created(self, event_dict):
        self.send(json.dumps(event_dict))

    def liveblog_post_updated(self, event_dict):
        self.send(json.dumps(event_dict))

    def liveblog_post_deleted(self, event_dict):
        self.send(json.dumps(event_dict))

class EchoConsumer(WebsocketConsumer):
    def receive(self,text_data=None,bytes_data=None):
        obj=json.loads(text_data)
        print("received: ",obj)

        json_string = json.dumps({
            "content": obj["content"],
            "user": obj["user"],
        })
        self.send(json_string)