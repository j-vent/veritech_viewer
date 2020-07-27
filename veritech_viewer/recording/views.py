from django.shortcuts import render
from django.http import Http404
from django.db import models
from session.models import Session, Booklet, Page
from .forms import SessionForm, BookletForm, PageForm
# Create your views here.
from datetime import datetime
from time import strftime
# TODO: move to a single source to avoid redundant code
class UnixTimestampField(models.DateTimeField):
    """UnixTimestampField: creates a DateTimeField that is represented on the
    database as a TIMESTAMP field rather than the usual DATETIME field.
    """
    def __init__(self, null=False, blank=False, **kwargs):
        super(UnixTimestampField, self).__init__(**kwargs)
        # default for TIMESTAMP is NOT NULL unlike most fields, so we have to
        # cheat a little:
        self.blank, self.isnull = blank, null
        self.null = True # To prevent the framework from shoving in "not null".

    def db_type(self, connection):
        typ=['TIMESTAMP']
        # See above!
        if self.isnull:
            typ += ['NULL']
        if self.auto_created:
            typ += ['default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP']
        return ' '.join(typ)

    def to_python(self, value):
        if isinstance(value, int):
            return datetime.fromtimestamp(value)
        else:
            return models.DateTimeField.to_python(self, value)

    def get_db_prep_value(self, value, connection, prepared=False):
        if value==None:
            return None
        # Use '%Y%m%d%H%M%S' for MySQL < 4.1
        return strftime('%Y-%m-%d %H:%M:%S',value.timetuple())


def recording_home(request):
    page_forms = []
    # else case is for first time access
    if request.method == "POST":
        session_form = SessionForm(request.POST)
        booklet_form = BookletForm(request.POST)

        for i in range (10):
            page_forms.append(PageForm(request.POST, prefix=str(i)))

        #question_form = QuestionForm(request.POST)
    else:
        session_form = SessionForm()
        booklet_form = BookletForm()
        for i in range(10):
            page_forms.append(PageForm())
        #question_form = QuestionForm()

    session = session_form.save(commit=False)
    booklet = booklet_form.save(commit = False)
    for page_form in page_forms:
        page_form.save(commit = False)
    #page = page_form.save(commit = False)
    #question = question_form.save(commit= False)

    if session_form.is_valid():
        # commit false so we can add more fields
        # session = session_form.save(commit = False)
        # get time now
        dt = datetime.now()
        # format it to a string
        #session.timestamp = dt.strftime('%Y-%m-%d %H:%M:%S')
        session.timestamp=dt
        session.status = 1
        session.save()
        print("session is valid")
    else:
        print("session no valuid")
    if booklet_form.is_valid():
        booklet.session = session
        booklet.save()
    for page_form in page_forms:
        if page_form.is_valid():
            page_form.booklet = booklet
            page_form.save()
    #if p in page_form page_form.is_valid():
    #  page.booklet = booklet
    # page.save()


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


    return render(request, 'recording.html',
                  {"student_id": studentID_Query, "sessions": filtered_sessions, "booklet_info": list(zip(filtered_booklets, booklet_mark_list)),
                   "booklet_form": booklet_form, "session_form": session_form,
                   "forms": page_forms});

# "booklet_form": booklet_form, "session_form": session_form