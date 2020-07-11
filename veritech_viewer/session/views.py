from django.shortcuts import render
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from .forms import MyForm
from. models import Booklet
from .models import Session

def home(request):
    form = MyForm()
    return render(request, 'index.html',  {'form':form})

def pages(request):
    return render(request, 'pages.html')

def questions(request):
    return render(request, 'question.html')

def booklet(request, booklet_id):
    spec_booklet = get_object_or_404(Booklet, pk=booklet_id)
    # change to booklet.html later
    return render(request, 'pages.html')