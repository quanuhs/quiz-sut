from django.shortcuts import render

# Create your views here.
def test(request, code):
    return render(request, "lobby.html", {"game_code": code})