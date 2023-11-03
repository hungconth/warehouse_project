# consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Component

class ComponentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        # Subscribe to a group for updates
        await self.channel_layer.group_add("component_updates", self.channel_name)

    async def disconnect(self, close_code):
        # Unsubscribe from the group when the WebSocket connection closes
        await self.channel_layer.group_discard("component_updates", self.channel_name)

    @staticmethod
    async def send_component_updates(event):
        await event["channel_layer"].send(event["channel_name"], {
            "type": "component.update",
            "message": event["message"]
        })

    async def component_update(self, event):
        # Send the message to the WebSocket
        await self.send(text_data=json.dumps(event["message"]))

    @staticmethod
    def notify_clients_about_update():
        message = {"update": "Database has been updated!"}
        async_to_sync(ComponentConsumer.send_component_updates)({
            "type": "component.update",
            "message": message
        })
