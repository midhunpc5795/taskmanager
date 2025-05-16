import json
from channels.generic.websocket import AsyncWebsocketConsumer


class TaskConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer to handle real-time task updates.
    Clients connect to a specific task's group to receive and send updates.
    """

    async def connect(self):
        """
        Called when the WebSocket connection is established.
        Joins a group based on the task ID.
        """
        self.task_id = self.scope['url_route']['kwargs']['task_id']
        self.group_name = f"task_{self.task_id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        """
        Called when the WebSocket connection is closed.
        Leaves the task group.
        """
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        """
        Called when a message is received from the WebSocket.
        Broadcasts the message to the task group.
        """
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({"error": "Invalid JSON format"}))
            return

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'task_update',
                'message': data
            }
        )

    async def task_update(self, event):
        """
        Called when a message is received from the group.
        Forwards the message to the WebSocket client.
        """
        await self.send(text_data=json.dumps(event['message']))
