
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Order

def home(request):
    print(request.body)
    return HttpResponse("Hello Worlds")

def hello(request, name):
    return HttpResponse(f"Hello {name}")


def json(request):
    return JsonResponse({'halle': 'valhala'})


def orders(request):
    orders = Order.objects.all()
    return HttpResponse(
        "<br>".join([order.title for order in orders])
    )