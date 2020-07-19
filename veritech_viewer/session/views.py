from django.shortcuts import render
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from. models import Booklet, Session, Page, Question
from datetime import datetime
import re


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
    return render(request, 'index.html', {"sessions": filtered_sessions, "dates": date_Query, "student_id": studentID_Query, "booklets": filtered_booklets});

def pages(request, page_id):
    spec_page = Page.pages.all().filter(id=page_id)
    filtered_questions = Question.questions.all().filter(page__in=spec_page)
    predicted = []

    for q in filtered_questions:
        # predicted.append(q.pred_regex[2:-2])
        trim = q.pred_regex[2:-2]
        singledigit = re.search("^([0-9])$", trim)
        doubledigit = re.search("^([0-9])\)\(([0-9])$", trim)
        single_bracket_or = re.search("^(([0-9])\|)+",trim)
        bracket_then_or = re.search("^([0-9])\)\((([0-9])\|*)+$", trim)
        or_then_bracket = re.search("^(([0-9])\|*)+\)\(([0-9])$", trim)
        if(singledigit):
            predicted.append(trim)
        elif(doubledigit):
            predicted.append(trim[0]+trim[3])
        elif(bracket_then_or):
            tens_digit = trim[0]
            ones_digit = trim[3:].split("|")
            result = ""
            for i in range(0,len(ones_digit)):
                if(i != 0):
                    result = result + " or "
                result = result+ tens_digit + ones_digit[i]
            predicted.append(result)
        elif (or_then_bracket):
            tens_digit = trim[:-3].split("|")
            ones_digit = trim[-1]
            result = ""
            for i in range(0, len(tens_digit)):
                if (i != 0):
                    result = result + " or "
                result = result + tens_digit[i] + ones_digit
            print(result)
        elif (single_bracket_or):
            print(trim.replace("|", " or "))
    zip(filtered_questions, predicted)
    # if(trim[1]==')' and trim[2]=='(' and trim[])
    return render(request, 'question.html', {"questions":filtered_questions, "predicted":predicted, "pid":page_id, "full": zip(filtered_questions, predicted)})

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
    return render(request,'pages.html',{"my_id":booklet_id, "booklet":spec_booklet, "pages":filtered_pages})



