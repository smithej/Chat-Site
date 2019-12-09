from channels.generic.websocket import AsyncWebsocketConsumer
import json


class ChatConsumer(AsyncWebsocketConsumer):
    """
    This is an asynchronous WebSocket consumer that accepts all connections, receives messages from its client,
    and broadcasts messages to other clients in the same room.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        """       
        Obtains the 'room_name' parameter from the URL route in chat/routing.py that opened the WebSocket connection
        to the consumer. Every consumer has a scope that contains information about its connection, including in 
        particular any positional or keyword arguments from the URL route and the currently authenticated user if any.
        """
        self.room_name = self.scope['url_route']['kwargs']['room_name']

        """
        Constructs a Channels group name directly from the user-specified room name, without any quoting or escaping.
        Group names may only contain letters, digits, hyphens, and periods. Therefore this example code will fail on
        room names that have other characters.
        """
        self.room_group_name = 'chat_%s' % self.room_name

    async def connect(self):
        """
        Joins a group.
        Group names are restricted to ASCII alphanumerics, hyphens, and periods only. Since this code constructs a
        group name directly from the room name, it will fail if the room name contains any characters that are not
        valid in a group name.
        """
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        """
        Accepts the web socket connection. If not called then the connection will be rejected and closed. You may
        want to reject the connection e.g. if the requesting user is not authorized to perform the requested action.
        
        Note: This should be the last call in the connect() method.
        """
        await self.accept()

    async def disconnect(self, code):
        """
        Leaves a group.
        """
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    async def receive(self, text_data=None, bytes_data=None):
        """
        Sends an event to a group.
        An event has a special 'type' key corresponding to the name of the method that should be invoked on consumers
        that receive the event.
        """
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        """
        Method to be invoked on consumers of event type 'chat_message'.
        Relay the message contained in the event back to the client via WebSocket.
        """
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))
