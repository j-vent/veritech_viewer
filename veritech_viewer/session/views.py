from django.shortcuts import render
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from. models import Booklet, Session, Page, Question
from datetime import datetime



def home(request):
    studentID_Query = request.GET.get('student_id', '')
    date_Query = request.GET.get('date', '')

    # clean up later:
    if studentID_Query == '' and date_Query == '':
        filtered_sessions=Session.sessions.all()
    elif studentID_Query =='' and date_Query != '':
        filtered_sessions = Session.sessions.all().filter(timestamp__date=date_Query)
    elif studentID_Query != '' and date_Query == '':
        filtered_sessions = Session.sessions.all().filter(student_id=studentID_Query)
    else:
        filtered_sessions = Session.sessions.all().filter(student_id=studentID_Query, timestamp__date=date_Query)
        
    filtered_booklets = Booklet.booklets.all().filter(session__in=filtered_sessions)
    return render(request, 'index.html', {"sessions": filtered_sessions, "dates": date_Query, "booklets": filtered_booklets});

def pages(request):
    return render(request, 'pages.html')

def test(request):
    sessions = Session.objects
    studentID_Query = request.GET.get('student_id','')
    date_Query = request.GET.get('date','')

    if studentID_Query == '' or date_Query == '':
        filtered_sessions = sessions
    else:
        filtered_sessions = sessions.filter(student_id=studentID_Query, timestamp__date = date_Query)

    return render(request,'test.html',{"sessions":filtered_sessions, "dates":date_Query});

def questions(request):
    return render(request, 'question.html')


def booklet(request, booklet_id):
    # spec_booklet = get_object_or_404(Booklet, pk=booklet_id)
    # filtered_pages = Page.pages.all().filter(booklet__in=spec_booklet)
    # change to booklet.html later
    spec_booklet = Booklet.booklets.all().filter(id=booklet_id)
    filtered_pages = Page.pages.all().filter(booklet__in= spec_booklet)
    # return render(request, 'pages.html', {"booklet":spec_booklet}, {"pages":filtered_pages})
    #return render(request, 'pages.html', {"booklet": spec_booklet}, {'id':booklet_id})
    return render(request,'test.html',{"my_id":booklet_id, "booklet":spec_booklet, "pages":filtered_pages})

