from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import Http404
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from. models import Booklet, Session, Page, Question
from datetime import datetime
import os
import re

@login_required
def home(request):
    studentID_Query = request.GET.get('student_id', '')
    date_Query = request.GET.get('date', '')

    # clean up later:
    if studentID_Query == '' and date_Query == '':
        filtered_sessions=Session.sessions.all().filter(status=1)
    elif studentID_Query =='' and date_Query != '':
        filtered_sessions = Session.sessions.all().filter(timestamp__date=date_Query).filter(status=1)
    elif studentID_Query != '' and date_Query == '':
        filtered_sessions = Session.sessions.all().filter(student_id=studentID_Query).filter(status=1)
    else:
        filtered_sessions = Session.sessions.all().filter(student_id=studentID_Query, timestamp__date=date_Query).filter(status=1)


    filtered_booklets = Booklet.booklets.all().filter(session__in=filtered_sessions)
    booklet_mark_list = []
    for booklet in filtered_booklets:
        page_mark_list = []
        spec_booklet = Booklet.booklets.all().filter(id=booklet.id)
        filtered_pages = Page.pages.all().filter(booklet__in=spec_booklet)
        
        for page in filtered_pages[::2]: # since marks attached to 'a' side
            page_mark_list.append(int(str(page.overall_mark)[:-1])) # remove the last digit-- want 10,9,8,7,6 only
        booklet_mark_list.append(str(page_mark_list)[1:-1])

    return render(request, 'index.html', {"sessions": filtered_sessions, "dates": date_Query, "student_id": studentID_Query, 
        "booklet_info": list(zip(filtered_booklets, booklet_mark_list)), "booklets": filtered_booklets, "list":booklet_mark_list});


@login_required
def pages(request, page_id_a, page_id_b):
    show_recog = 0
    if request.GET.get('show_recog') == '1':
        show_recog = 1

    spec_page_a = Page.pages.all().filter(id=page_id_a)
    spec_page_b = Page.pages.all().filter(id=page_id_b)


    booklet = spec_page_a[0].booklet
    counts_a = spec_page_a[0].counts()
    counts_b = spec_page_b[0].counts()
    counts = [ x[0]+x[1] for x in zip(counts_a, counts_b) ]

    filtered_questions_a = Question.questions.all().filter(page__in=spec_page_a)
    filtered_questions_b = Question.questions.all().filter(page__in=spec_page_b)


    predicted_a = []
    predicted_b = []

    img_orig_a = []
    img_proc_a = []
    img_recog_a = []

    img_orig_b = []
    img_proc_b = []
    img_recog_b = []

    for q in filtered_questions_a:
        orig,proc,recog = q.images.split(",")
        img_orig_a.append(os.path.join('images', orig+".png"))
        img_proc_a.append(os.path.join('images', proc+".png"))
        img_recog_a.append(os.path.join('images', recog+".png"))

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
        orig, proc, recog = q.images.split(",")
        img_orig_b.append(os.path.join('images', orig + ".png"))
        img_proc_b.append(os.path.join('images', proc + ".png"))
        img_recog_b.append(os.path.join('images', recog + ".png"))

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
    tmp = list(zip(filtered_questions_a, predicted_a, img_orig_a, img_proc_a, img_recog_a))
    return render(request, 'question.html', {"questions":filtered_questions_a, "predicted":predicted_a, "pid":page_id_a,
                         "page_a": filtered_questions_a, "page_b": filtered_questions_b, 
                         "parent": booklet, 'counts': counts, 'pages': (spec_page_a[0], spec_page_b[0]), 'show_recog': show_recog})

# Renders the page that displays all the REJECTs and allows for the amendment
# of marking outcomes
@login_required
def fails(request):
    if request.GET.get('question_id') is not None:
        # I regret doing this shit in production
        outcomes = {0: 'ACCEPT', 1: 'NOT_SURE'};
        question_id = int(request.GET.get('question_id'))
        new_outcome = outcomes[int(request.GET.get('marking_outcome'))]

        Question.questions.filter(id=question_id).update(marking_outcome=new_outcome)

    questions = Question.questions.all().filter(marking_outcome='REJECT')

    # apply filter
    if request.GET.get('sessid') is not None:
        questions = questions.filter(page__booklet__session__id=request.GET.get('sessid'))

    paginator = Paginator(questions, 25)

    page_number = request.GET.get('page')
    if page_number is None: page_number = 1

    questions_page = paginator.get_page(page_number)

    return render(request, 'fails.html', {'fails': questions_page})

@login_required
def booklet_pages(request, booklet_id):
    booklet = Booklet.booklets.all().filter(id=booklet_id)

    if len(booklet) == 0:
        raise Http404("Booklet not found")

    booklet = booklet[0]

    return render(request, "booklet_pages.html", {"booklet": booklet})

@login_required
def test(request):
    sessions = Session.objects
    studentID_Query = request.GET.get('student_id','')
    date_Query = request.GET.get('date','')

    if studentID_Query == '' or date_Query == '':
        filtered_sessions = sessions
    else:
        filtered_sessions = sessions.filter(student_id=studentID_Query, timestamp__date = date_Query)

    return render(request,'test.html',{"sessions":filtered_sessions, "dates":date_Query});


@login_required
def questions(request):
    return render(request, 'question.html')


@login_required
def booklet(request, booklet_id):
    # spec_booklet = get_object_or_404(Booklet, pk=booklet_id)
    # filtered_pages = Page.pages.all().filter(booklet__in=spec_booklet)
    # change to booklet.html later
    spec_booklet = Booklet.booklets.all().filter(id=booklet_id)

    cur_booklet = spec_booklet[0]

    filtered_pages = Page.pages.all().filter(booklet__in= spec_booklet).order_by('page_number')
    num_of_questions = []
    for p in filtered_pages:
        spec_page = Page.pages.all().filter(id=p.id)
        filtered_questions = Question.questions.all().filter(page__in=spec_page)
        num_of_questions.append(len(filtered_questions))

    a_id, b_id = [], []
    page_numbers = []
    correct = []
    marks = []
    questions_right = 0

    for i in range(0,len(filtered_pages)):
        if (i % 2 == 0):
            page_numbers.append(filtered_pages[i].page_number[:-1])
            a_id.append(filtered_pages[i].id)

            questions = Question.questions.all().filter(page__id= filtered_pages[i].id)
            for q in questions:
                if q.marking_outcome != "REJECT":
                    questions_right += 1
        else:
            b_id.append(filtered_pages[i].id)
            marks.append(filtered_pages[i].overall_mark)

            questions = Question.questions.all().filter(page__id= filtered_pages[i].id)
            for q in questions:
                if q.marking_outcome != "REJECT":
                    questions_right += 1

            correct.append(str(questions_right) + "/" +  str(num_of_questions[i-1] + num_of_questions[i]))
            questions_right = 0

    # return render(request,'pages.html',{"my_id":booklet_id, "booklet":spec_booklet, "pages":filtered_pages, "test_id":2})
    return render(request,'pages.html',{"page_info": zip(page_numbers, a_id, b_id, correct, marks), 'booklet': cur_booklet})


