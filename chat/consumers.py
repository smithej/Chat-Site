from channels.generic.websocket import WebsocketConsumer
import json


class ChatConsumer(WebsocketConsumer):
    """
    This is a synchronous WebSocket consumer that accepts all connections, receives messages from its client,
    and echos those messages back to the same client. For now it does not broadcast messages to other clients
    in the same room.
    """
    def connect(self):
        self.accept()

    def disconnect(self, code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'message': message
        }))
