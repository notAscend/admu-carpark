import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ParkingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'parking_updates'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        # This consumer can also receive messages from clients if needed,
        # but for real-time updates, it primarily sends data.
        pass

    # Receive message from room group (sent from Django views/signals)
    async def parking_zone_update(self, event):
        parking_zone_data = {
            'id': event['id'],
            'name': event['name'],
            'current_available_slots': event['current_available_slots'],
            'total_slots': event['total_slots'],
            'occupancy_percentage': event['occupancy_percentage']
        }
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'parking_zone_update',
            'data': parking_zone_data
        }))