from django.shortcuts import render
from django.http import Http404
from session.models import Session, Booklet, Page
# Create your views here.

# TO DO: Default to all
def recording_home(request):
    studentID_Query = request.GET.get('student_id', '')
    month_Query = request.GET.get('month', '')
    year_Query = month_Query[0:4]
    month_Query = month_Query[6:]


    if studentID_Query == '' and month_Query == '':
        filtered_sessions=Session.sessions.all().filter(status=1)
    elif studentID_Query =='' and month_Query != '':
        filtered_sessions = Session.sessions.all().filter(timestamp__month=month_Query, timestamp__year=year_Query).filter(status=1)
    elif studentID_Query != '' and month_Query == '':
        filtered_sessions = Session.sessions.all().filter(student_id=studentID_Query).filter(status=1)
    else:
        filtered_sessions = Session.sessions.all().filter(student_id=studentID_Query, timestamp__month=month_Query,
                                                          timestamp__year=year_Query).filter(status=1)
    filtered_booklets = Booklet.booklets.all().filter(session__in=filtered_sessions)

    booklet_mark_list = []

    for booklet in filtered_booklets:
        page_mark_list = []
        spec_booklet = Booklet.booklets.all().filter(id=booklet.id)
        filtered_pages = Page.pages.all().filter(booklet__in=spec_booklet)

        for page in filtered_pages[::2]:  # since marks attached to 'a' side
          page_mark_list.append(int(str(page.overall_mark)[:-1]))  # remove the last digit-- want 10,9,8,7,6 only

        booklet_mark_list.append(str(page_mark_list)[1:-1].split(", "))
    print(booklet_mark_list)
    print("****")
    
    return render(request, 'recording.html',
                  {"sessions": filtered_sessions, "booklet_info": list(zip(filtered_booklets, booklet_mark_list))});

