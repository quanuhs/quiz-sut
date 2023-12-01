import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer, AsyncWebsocketConsumer

from game.models import Lobby, LobbyPlayer
from asgiref.sync import sync_to_async
import asyncio


# Игрок
class GamePlayerConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        self.user = self.scope["user"]
        await self.check_code(self.scope["url_route"]["kwargs"].get("lobby_id"))
    
    
    async def receive_json(self, content, **kwargs):
        match content.get("command"):
            case "ready":
                await self.command_ready(content)
            
            case "results":
                await self.command_results()
    
    

    async def command_results(self):
        await self.send_json({"command": "results"})


    async def command_ready(self, content):
        question_index = content.get("message").get("question")
        answer_index = content.get("message").get("answer")
        is_last = content.get("message").get("last")

        if self.player.word_index > question_index:
            return

        if self.scope["session"].get("correct_answers")[question_index] == answer_index:
            self.player.points += 1
        
        self.player.word_index += 1
        await self.player.asave()

        await self.send_json({"command": "correct", "answer": self.scope["session"].get("correct_answers")[question_index]})
    
        # УБРАТЬ!
        await asyncio.sleep(1.5)
        await self.send_json({"command": "next"})



    
    async def disconnect(self, code):
        if code == 1:
            await self.close()
        
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        await self.channel_layer.group_send(self.room_group_name, {"type": "left", "message": {"id": self.player.player_id.hex}})
        await self.channel_layer.group_send("host"+self.room_group_name, {"type": "left", "message": {"id": self.player.player_id.hex}})
        await self.close()
        

    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send_json({"message": message})


    async def joined(self, event):
        if event["message"].get("to") is None:
            await self.send_json({"command": "join", "message": event["message"]})
            await self.channel_layer.group_send(self.room_group_name, {"type": "joined", "message": {"id": self.player.player_id.hex, "name": self.player.name, "to": event["message"]["id"]}})
        
        elif event["message"].get("to") == self.player.player_id.hex:
            await self.send_json({"command": "join", "message": event["message"]})

    async def left(self, event):
        if event["message"]["id"] == self.player.player_id:
            return
        
        await self.send_json({"command": "left", "message": event["message"]})


    async def start(self, event):
        await self.send_json({"command": "start", "message": event["message"]})
    

    async def remove(self, event):
        if event["id"] == self.player.player_id.hex:
            await self.player.adelete()
            await self.disconnect(1000)


    async def check_code(self, join_code):
        # Получаем информацию о лобби
        
        player = await LobbyPlayer.objects.filter(player_id = join_code).afirst()

        if player is None:
            await self.close()
            return
        
        lobby = await Lobby.objects.filter(players__id=player.id).afirst()

        if lobby is None:
            await self.close()
            return
        
        self.player = player
        self.lobby = lobby
        
        await self.accept()

        self.room_group_name = f"game_{lobby.id}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.channel_layer.group_send(self.room_group_name, {"type": "joined", "message": {"id": self.player.player_id.hex, "name": self.player.name}})
        await self.channel_layer.group_send("host"+self.room_group_name, {"type": "joined", "message": {"id": self.player.player_id.hex, "name": self.player.name}})








# Администратор / создатель игры
class GameAdminConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        await self.check_id(self.scope["url_route"]["kwargs"].get("secret_id"))

        # await self.accept()


    async def receive_json(self, content, **kwargs):
        match content.get("command"):
            case "start":
                self.lobby.in_play = True
                await self.lobby.asave()
                await self.channel_layer.group_send(self.room_group_name, {"type": "start", "message": {}})

            case "remove":
                await self.channel_layer.group_send(self.room_group_name, {"type": "remove", "id": content.get("id")})

            case "change_code":
                await sync_to_async(self.lobby.generate_code)()
                await self.lobby.asave()
                await self.send_json({"command": "new_code", "code": self.lobby.code})

            case "change_settings":
                print(content.get("settings"))
        
    
    
    async def disconnect(self, code):
        await self.channel_layer.group_send(self.room_group_name, {"type": "disconnect", "code": 1})
        # await self.lobby.adelete()
        await self.close()


    async def joined(self, event):
        await self.send_json({"command": "join", "message": event["message"]})
    
    
    async def left(self, event):
        await self.send_json({"command": "left", "message": event["message"]})



    async def check_id(self, secret_id):        
        lobby = await Lobby.objects.filter(admin=self.user).afirst()
        # Проверяем, если пользователь - создатель
        if lobby is None:
            self.close()
            return
    
        await self.accept()
        self.lobby = lobby
        self.room_group_name = f"game_{lobby.id}"
        await self.channel_layer.group_add("host"+self.room_group_name, self.channel_name)

        # await self.send_json({"hello": "world"})