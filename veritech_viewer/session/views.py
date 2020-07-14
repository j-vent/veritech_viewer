from django.shortcuts import render
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from. models import Booklet
from .models import Session
from datetime import datetime



def home(request):

    #sessions = Session.objects
    #booklets = Booklet.objects
    studentID_Query = request.GET.get('student_id', '')
    date_Query = request.GET.get('date', '')

    # clean up later:
    if studentID_Query == '' and date_Query == '':
    # filtered_sessions = sessions
        filtered_sessions=Session.sessions.all()
    elif studentID_Query =='' and date_Query != '':
    # filtered_sessions = sessions.filter(timestamp__date=date_Query)
        filtered_sessions = Session.sessions.all().filter(timestamp__date=date_Query)
    elif studentID_Query != '' and date_Query == '':
    # filtered_sessions = sessions.filter(student_id=studentID_Query)
        filtered_sessions = Session.sessions.all().filter(student_id=studentID_Query)
    else:
    # filtered_sessions = sessions.filter(student_id=studentID_Query, timestamp__date=date_Query)
        filtered_sessions = Session.sessions.all().filter(student_id=studentID_Query, timestamp__date=date_Query)

    # filtered_booklets = Booklet.booklets.all().filter(session=filtered_sessions)
    #filtered_booklets = Booklet.booklets.all(sessiodsnfiltered_sessions__id)
    filtered_booklets = Booklet.booklets.all().filter(session__in=filtered_sessions)
    #filtered_booklets=[]
    #for session in filtered_sessions.all:
      #filtered_booklets.add(booklets.filter(session=session))
    return render(request, 'index.html', {"sessions": filtered_sessions, "dates": date_Query, "booklets": filtered_booklets});

def pages(request):

    return render(request, 'pages.html')

#07%2F15%2F2020+10%3A15+PM
def test(request):

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