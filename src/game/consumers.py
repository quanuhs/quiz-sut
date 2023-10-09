import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer



class GameConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.check_code(self.scope["url_route"]["kwargs"].get("code"))
    
    
    async def receive_json(self, content, **kwargs):
        pass
    
    
    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        pass
    
    
    async def disconnect(self, code):
        pass


    async def check_code(self, join_code):
        
        if join_code in [None, 'hello']:
            self.close()
            return
    
        
        await self.accept()
        self.room_group_name = f"game_{join_code}"
        await self.send_json({"hello": "world"})
    