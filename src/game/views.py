from django.shortcuts import render, redirect
from .models import Lobby, LobbyPlayer, Module


def join_game(request):

    error = request.session.get("error")
    code = request.session.get("lobby_code")
    name=request.POST.get("nickname")

    if code is not None:
        del request.session["lobby_code"]

    if error is not None:
        del request.session["error"]

    if request.method == "POST":

        lobby = Lobby.objects.filter(code=request.POST.get("code"), is_open=True).first()

        if lobby is None:
            error = "Игры с таким кодом не найдено!"
        
        if name is None or name.replace(" ", "") == "":
            error = "Укажите имя"        
        
        if error is not None:
            return render(request, "game/join.html", {"error": error, "code": code or ""})
        
        player_id = request.session.get("player_id")

        player = None

        if player_id is not None and player_id is not None:
            player = LobbyPlayer.objects.filter(player_id = player_id, lobby = lobby).first()
        

        if player is None:
            player = LobbyPlayer(lobby = lobby, name=name)
            player.save()
            request.session["player_id"] = player.player_id.hex
            request.session.save()
        
        else:
            if player.name != name:
                player.name = name
                player.save()
    

        return redirect("play", lobby_id = lobby.uuid)
    

    return render(request, "game/join.html", {"error": error or "", "code": code or ""})


def lobby_page(request, lobby_id):
    lobby = Lobby.objects.filter(uuid=lobby_id).first()
    player_id = request.session.get("player_id")

    if lobby is None:
        return redirect("join")

    if player_id is None:
        request.session["lobby_code"] = lobby.code
        request.session.save()
        return redirect("join")
    
    player = LobbyPlayer.objects.filter(player_id = player_id, lobby = lobby).first()
    
    if player is None:
        return redirect("join")


    # fix later
    if lobby.in_play:
        quiz_data, correct_data = generate_quiz_data(player.player_id, lobby.module)
        request.session["correct_answers"] = correct_data
        request.session.save()

        return render(request, "game/game.html", {"lobby": lobby, "player": player, "quiz_data": quiz_data, "correct_data": correct_data})

    return render(request, "game/lobby.html", {"lobby": lobby, "player": player})


import random
def generate_quiz_data(player_seed, module, num_questions=5, num_answers=4):
    random.seed(player_seed)

    quiz_data = []
    correct_data = []

    all_cards = list(module.cards.all())
    cards = list(module.cards.all())

    for _ in range(num_questions):
        
        # Get random cards from the selected module

        correct_answer_card = cards.pop(random.randint(0, len(cards)-1))
        correct_answer = correct_answer_card.back_text
        question_title = correct_answer_card.front_text

        # Get incorrect answers
        incorrect_answers = [card.back_text for card in random.sample(all_cards, num_answers - 1) if card != correct_answer_card]

        # Shuffle correct and incorrect answers
        answers = incorrect_answers
        _correct = random.randint(0, num_answers-1)
        answers.insert(_correct, correct_answer)

        correct_data.append(_correct)

        # Create dictionary for the question
        question_data = {"title": question_title, "answers": answers}
        quiz_data.append(question_data)

    return quiz_data, correct_data




def host_lobby_page(request):
    if not request.user.is_authenticated:
         return redirect("/")
        
    lobby = Lobby.objects.filter(admin=request.user).first()

    if lobby is None:
        return redirect("/")
    

    return render(request, "game/host_lobby.html", {"lobby": lobby})



def create_game(request, module_id):
    if request.user.is_authenticated:
        lobby, created = Lobby.objects.get_or_create(admin=request.user, module_id=module_id)
        lobby.module_id = module_id
        lobby.save()
        return redirect("host")

    else:
        return redirect("login")
    


def solo_quiz(request, module_id):
    module = Module.objects.filter(id=module_id).first()
    if module is None:
        return redirect("/")
    
    cards = module.cards.all()
    cards_data = []

    for card in cards:
        cards_data.append({"title": card.front_text, "answer": card.back_text})


    return render(request, "solo/testing_page.html", {"cards": cards_data, "module": module})


def solo_match(request, module_id):
    module = Module.objects.filter(id=module_id).first()
    if module is None:
        return redirect("/")
    
    cards = module.cards.all()
    cards_data = []

    for card in cards:
        cards_data.append({"title": card.front_text, "answer": card.back_text})


    return render(request, "solo/match_page.html", {"cards": cards_data, "module": module})