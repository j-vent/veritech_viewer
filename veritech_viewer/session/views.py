from django.shortcuts import render
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from .forms import MyForm
from. models import Booklet
from .models import Session
from datetime import datetime



def home(request):
    form = MyForm()
    return render(request, 'index.html',  {'form':form})
    # return render(request, 'index.html');

def pages(request):

    return render(request, 'pages.html')

#07%2F15%2F2020+10%3A15+PM
def test(request):
    form = MyForm()
    sessions = Session.objects
    studentID_Query = request.GET.get('student_id','')
    date_Query = request.GET.get('date','')

    if studentID_Query == '' or date_Query == '':
        filtered_sessions = sessions
    else:
        filtered_sessions = sessions.filter(student_id=studentID_Query, timestamp__date = date_Query)
    return render(request,'test.html',{"sessions":filtered_sessions, 'form':form,"dates":date_Query});

def questions(request):
    return render(request, 'question.html')

'''
def booklet(request, booklet_id):
    spec_booklet = get_object_or_404(Booklet, pk=booklet_id)
    # change to booklet.html later
    return render(request, 'pages.html', {"booklet":spec_booklet})
'''