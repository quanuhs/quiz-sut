from django.shortcuts import render
from .models import Module, Topic


def main_page(request):
    return render(request, "main.html")

def topic_page(request, id):
    topic = Topic.objects.all()
    return render(request, "topic.html", {"topic": topic})

def module_page(request, id):
    modules = Module.objects.all()
    module = Module.objects.filter(id=id).first()
    return render(request, "module.html", {"module": module})

def modules_page(request):
    modules = Module.objects.all()
    return render(request, "topic.html", {"modules": modules})

def author_page(request, id):
    modules = Module.objects.all()
    return render(request, "topic.html", {"modules": modules})

def login_page(request):
    return render(request, "login.html")