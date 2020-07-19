from django.shortcuts import render
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from. models import Booklet, Session, Page, Question
from datetime import datetime
import os
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
    booklet_mark_list = []
    for booklet in filtered_booklets:
        page_mark_list = []
        spec_booklet = Booklet.booklets.all().filter(id=booklet.id)
        filtered_pages = Page.pages.all().filter(booklet__in=spec_booklet)
        for page in filtered_pages:
            page_mark_list.append(page.overall_mark)
        booklet_mark_list.append(page_mark_list)
    # TODO: remove [] from list, convert to string
    return render(request, 'index.html', {"sessions": filtered_sessions, "dates": date_Query, "student_id": studentID_Query, "booklet_info": zip(filtered_booklets, booklet_mark_list), "booklets": filtered_booklets, "list":booklet_mark_list});

def pages(request, page_id_a, page_id_b):
    spec_page_a = Page.pages.all().filter(id=page_id_a)
    spec_page_b = Page.pages.all().filter(id=page_id_b)
    filtered_questions_a = Question.questions.all().filter(page__in=spec_page_a)
    filtered_questions_b = Question.questions.all().filter(page__in=spec_page_b)
    predicted_a = []
    predicted_b = []
    img_orig_a = []
    img_proc_a = []
    img_recog_a = []
    # img_a = filtered_questions_a.values_list('images', flat=True)
    # img_orig_a, img_proc_a, img_recog = img_a.split(",")
    # print("ORIG A", img_orig_a)
    for q in filtered_questions_a:
        # predicted.append(q.pred_regex[2:-2])
        orig,proc,recog = q.images.split(",")
        img_root = "\root\images"
        img_orig_a.append(os.path.join(img_root, orig+".png"))
        img_proc_a.append(os.path.join(img_root, proc+".png"))
        img_recog_a.append(os.path.join(img_root, recog+".png"))

        trim = q.pred_regex[2:-2]
        singledigit = re.search("^([0-9])$", trim)
        doubledigit = re.search("^([0-9])\)\(([0-9])$", trim)
        single_bracket_or = re.search("^(([0-9])\|)+",trim)
        bracket_then_or = re.search("^([0-9])\)\((([0-9])\|*)+$", trim)
        or_then_bracket = re.search("^(([0-9])\|*)+\)\(([0-9])$", trim)

        if(singledigit):
            predicted_a.append(trim)
        elif(doubledigit):
            predicted_a.append(trim[0]+trim[3])
        elif(bracket_then_or):
            tens_digit = trim[0]
            ones_digit = trim[3:].split("|")
            result = ""
            for i in range(0,len(ones_digit)):
                if(i != 0):
                    result = result + " or "
                result = result+ tens_digit + ones_digit[i]
            predicted_a.append(result)
        elif (or_then_bracket):
            tens_digit = trim[:-3].split("|")
            ones_digit = trim[-1]
            result = ""
            for i in range(0, len(tens_digit)):
                if (i != 0):
                    result = result + " or "
                result = result + tens_digit[i] + ones_digit
            predicted_a.append(result)
        elif (single_bracket_or):
            predicted_a.append(trim.replace("|", " or "))

    for q in filtered_questions_b:
        # predicted.append(q.pred_regex[2:-2])
        trim = q.pred_regex[2:-2]
        singledigit = re.search("^([0-9])$", trim)
        doubledigit = re.search("^([0-9])\)\(([0-9])$", trim)
        single_bracket_or = re.search("^(([0-9])\|)+", trim)
        bracket_then_or = re.search("^([0-9])\)\((([0-9])\|*)+$", trim)
        or_then_bracket = re.search("^(([0-9])\|*)+\)\(([0-9])$", trim)

        if (singledigit):
            predicted_b.append(trim)
        elif (doubledigit):
            predicted_b.append(trim[0] + trim[3])
        elif (bracket_then_or):
            tens_digit = trim[0]
            ones_digit = trim[3:].split("|")
            result = ""
            for i in range(0, len(ones_digit)):
                if (i != 0):
                    result = result + " or "
                result = result + tens_digit + ones_digit[i]
            predicted_b.append(result)
        elif (or_then_bracket):
            tens_digit = trim[:-3].split("|")
            ones_digit = trim[-1]
            result = ""
            for i in range(0, len(tens_digit)):
                if (i != 0):
                    result = result + " or "
                result = result + tens_digit[i] + ones_digit
            predicted_b.append(result)
        elif (single_bracket_or):
            predicted_b.append(trim.replace("|", " or "))

    # if(trim[1]==')' and trim[2]=='(' and trim[])
    return render(request, 'question.html', {"questions":filtered_questions_a, "predicted":predicted_a, "pid":page_id_a,
                         "page_a_info": zip(filtered_questions_a, predicted_a, img_orig_a, img_proc_a, img_recog_a),
                                             "page_b_info": zip(filtered_questions_b, predicted_b)})

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
    filtered_pages = Page.pages.all().filter(booklet__in= spec_booklet).order_by('page_number')
    num_of_questions = []
    for p in filtered_pages:
        spec_page = Page.pages.all().filter(id=p.id)
        filtered_questions = Question.questions.all().filter(page__in=spec_page)
        num_of_questions.append(len(filtered_questions))
    print("numqs" , num_of_questions)

    a_id = []
    b_id = []
    page_numbers = []
    correct = []
    marks = []
    x = mark =  0
    y = 1

    for i in range(0,len(filtered_pages)):
        if (i % 2 == 0):
            page_numbers.append(filtered_pages[i].page_number[:-1])
            a_id.append(filtered_pages[i].id)
            x = x + filtered_pages[i].overall_mark
            y = num_of_questions[i]
        else:
            b_id.append(filtered_pages[i].id)
            # y + num of questions in page
            mark = (str)(x + filtered_pages[i].overall_mark) + "/" +  (str)(y+ num_of_questions[i])
            correct.append(mark)
            mark = (x + filtered_pages[i].overall_mark)/(y + num_of_questions[i])
            mark = 69 if mark <= 0.6 else round(mark*100)
            marks.append(mark)
            x = y = mark = 0

            # y = y + # number of questions in page

    # return render(request,'pages.html',{"my_id":booklet_id, "booklet":spec_booklet, "pages":filtered_pages, "test_id":2})
    return render(request,'pages.html',{"page_info": zip(page_numbers, a_id, b_id, correct, marks)})


