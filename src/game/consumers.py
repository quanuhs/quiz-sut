import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer



class GameConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send_json({"hello": "world"})
    
    
    async def receive_json(self, content, **kwargs):
        pass
    
    
    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        pass
    
    
    async def disconnect(self, code):
        pass
    