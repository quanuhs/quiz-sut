import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer, AsyncWebsocketConsumer

from game.models import Lobby



# Игрок
class GamePlayerConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        await self.check_code(self.scope["url_route"]["kwargs"].get("lobby_id"))
    
    
    async def receive_json(self, content, **kwargs):
        pass
    
    
    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        pass
    
    
    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)


    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send_json({"message": message})


    async def check_code(self, join_code):
        # Получаем информацию о лобби
        lobby = await Lobby.objects.filter(uuid=join_code).afirst()

        if lobby is None:
            self.close()
            return
    



        await self.accept()
        self.room_group_name = f"p_game_{lobby.id}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        # await self.channel_layer.group_send(self.room_group_name, {"type": "chat_message", "message": {"LobbyID": self.lobby.id, "UUID": self.lobby.uuid.hex}})




# Администратор / создатель игры
class GameAdminConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.check_id(self.scope["url_route"]["kwargs"].get("secret_id"))

        # await self.accept()
    

    async def receive_json(self, content, **kwargs):
        if content.get("command") == "start":
            await self.send_json({"hello": "world"})
        
    
    
    async def disconnect(self, code):
        pass


    async def check_id(self, secret_id):

        lobby = await Lobby.objects.filter(secret=secret_id).afirst()
        # Проверяем, если пользователь - создатель
        if lobby is None:
            self.close()
            return
    
        await self.accept()
        self.room_group_name = f"a_game_{lobby.id}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        # await self.send_json({"hello": "world"})