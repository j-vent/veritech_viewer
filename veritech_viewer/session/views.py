from django.shortcuts import render
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from .forms import MyForm
from. models import Booklet
from .models import Session

sessions = Session.objects

def home(request):
    form = MyForm()
    return render(request, 'index.html',  {'form':form})
    # return render(request, 'index.html');

def pages(request):
    studentIDQuery = request.Get.get('student_id')
    sessionQuery = request.Get.get('session_id')
    filtered_sessions = sessions.filter(student_id=studentIDQuery)
    return render(request, 'pages.html')

def test(request):
    studentID_Query = request.GET.get('student_id','')
    if studentID_Query == '':
        filtered_sessions = sessions
    else:
        filtered_sessions = sessions.filter(student_id=studentID_Query)
    return render(request,'test.html',{"sessions":filtered_sessions});

def questions(request):
    return render(request, 'question.html')

'''
def booklet(request, booklet_id):
    spec_booklet = get_object_or_404(Booklet, pk=booklet_id)
    # change to booklet.html later
    return render(request, 'pages.html', {"booklet":spec_booklet})
'''