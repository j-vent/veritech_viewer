from django.shortcuts import render
from .models import Session
from .forms import MyForm
# Create your views here.

def home(request):
    form = MyForm()
    return render(request, 'index.html',  {'form':form})

def booklets(request):
    return render(request, 'booklet.html')

def questions(request):

    return render(request, 'question.html')