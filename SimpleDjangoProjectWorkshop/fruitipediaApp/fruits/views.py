from idlelib.rpc import request_queue

from django.shortcuts import render

from fruitipediaApp.fruits.models import Fruit


# Create your views here.
def index(request):
    return render(request, 'common/index.html')

def create_category(request):
    return render(request, 'categories/create-category.html')


def dashboard(request):

    fruits = Fruit.objects.all()

    context = {
        'fruits': fruits
    }
    return render(request, 'common/dashboard.html', context)

def create_fruit(request):
    return render(request, 'fruits/create-fruit.html' )

def details_fruit(request, pk):
    return render(request, 'fruits/details-fruit.html')

def edit_fruit(request, pk):
    return render(request, 'fruits/edit-fruit.html')

def delete_fruit(request, pk):
    return render(request, 'fruits/details-fruit.html')