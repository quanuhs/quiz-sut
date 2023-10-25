from django.shortcuts import render, redirect
from .models import Lobby


def join_game(request):
    return render(request, "game/join.html")


def lobby_page(request, lobby_id):
    lobby = Lobby.objects.filter(uuid=lobby_id).first()

    return render(request, "game/lobby.html", {"lobby": lobby})


def host_lobby_page(request):
    if not request.user.is_authenticated:
         return redirect("")
        
    lobby = Lobby.objects.filter(author=request.user).first()

    if lobby is None:
        return redirect("")
    

    return render(request, "game/host_lobby.html", {"lobby": lobby})



def create_game(request, module_id):
    if request.user.is_authenticated:
        lobby, created = Lobby.objects.get_or_create(author=request.user)
        lobby.module_id = module_id
        lobby.save()
        return redirect("host")

    else:
        return redirect("")