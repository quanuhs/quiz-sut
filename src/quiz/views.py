from django.shortcuts import render, redirect
from .models import Module, Topic, CustomUser
from django.contrib.auth import authenticate


def main_page(request):
    return render(request, "main.html")


def topic_page(request, id):
    topic = Topic.objects.all()
    return render(request, "topic.html", {"topic": topic})


def module_create(request):
    if not request.user.is_authenticated:
        return redirect('login')

    module = Module(author=request.user, title=f"Quiz {request.user.username}")
    module.save()

    return redirect("module_edit", module.id)


def module_edit(request, id):

    if not request.user.is_authenticated:
        return redirect('login')

    module = Module.objects.filter(id=id, author=request.user).first()
    if module is None:
        return redirect('')
    
    return render(request, "module_edit.html", {"module": module})



def module_page(request, id):
    module = Module.objects.filter(id=id).first()
    return render(request, "module.html", {"module": module})

def modules_page(request):
    modules = Module.objects.all()
    return render(request, "topic.html", {"modules": modules})

def author_page(request, id):
    author = CustomUser.objects.filter(id=id).first()
    if author is None:
        return redirect("")
    
    modules = author.modules.all()
    return render(request, "author.html", {"modules": modules, "author": author})



from django.contrib.auth import authenticate
def login_page(request):
    if request.method == "POST":
        pass
    
    return render(request, "login.html")


def register_page(request):
    return render(request, "register.html")