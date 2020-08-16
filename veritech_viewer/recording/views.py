from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.db import models
from session.models import Session, Booklet, Page
from .forms import SessionForm, BookletForm, ModBookletForm
from django.forms import modelformset_factory
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

@login_required
def recording_home(request):
    page_forms = []
    PageFormSet = modelformset_factory(Page, fields=('page_number', 'overall_mark'), extra=10)

    # else case is for first time access
    if request.method == "POST":
        session_form = SessionForm(request.POST)
        booklet_form = BookletForm(request.POST)
        pages_form = PageFormSet(request.POST)
        mod_booklet_form = ModBookletForm(request.POST)

        session = session_form.save(commit=False)
        booklet = booklet_form.save(commit=False)
        instances = pages_form.save(commit=False)
        mod_booklet = mod_booklet_form.save(commit=False)
        if session_form.is_valid():
            # commit false so we can add more fields
            # session = session_form.save(commit = False)
            # get time now
            dt = datetime.now()
            # format it to a string
            # session.timestamp = dt.strftime('%Y-%m-%d %H:%M:%S')
            session.timestamp = dt
            session.status = 1
            session.save()
            #print("session is valid")
        #else:
            #print("session no valuid")
        if booklet_form.is_valid():
            #print("booklet valid")
            booklet.session = session
            booklet.save()

        for instance in instances:
            # print(pages_form.is_valid())
            instance.booklet = booklet
            # print(instance.overall_mark)
            instance.save();
            # print("saved")
        if mod_booklet_form.isValid():
            # booklet = request.GET.get('booklet')
            # mod_booklet.booklet = request.GET.get('booklet')
            mod_booklet.save()
        #question_form = QuestionForm(request.POST)
    else:
        session_form = SessionForm()
        booklet_form = BookletForm()
        pages_form = PageFormSet(queryset=Page.pages.none())
        mod_booklet_form = ModBookletForm()



        #question_form = QuestionForm()



    #for page_form in page_forms:
     #   page_form.save(commit = False)
    #page = page_form.save(commit = False)
    #question = question_form.save(commit= False)


    '''
    for page_form in page_forms:
        print("form!")
        page = page_form.save(commit = False)
        if page_form.is_valid():
          page.booklet = booklet
          print("PAGE VALID")
          page.save()
    '''

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
        #print(booklet.id);
        spec_booklet = Booklet.booklets.all().filter(id=booklet.id)
        filtered_pages = Page.pages.all().filter(booklet__in=spec_booklet)
        if(len(filtered_pages) != 0):

            for page in filtered_pages[::2]:  # since marks attached to 'a' side
                #print("pgnum" + page.page_number);
                if str(page.overall_mark)[:-1].isdigit():
                     page_mark_list.append(int(str(page.overall_mark)[:-1]))  # remove the last digit-- want 10,9,8,7,6 only
                else:
                    page_mark_list.append(0)
            booklet_mark_list.append(str(page_mark_list)[1:-1].split(", "))
        else:
            booklet_mark_list.append([0,0,0,0,0,0,0,0,0,0])
        #print(booklet.comments);
    #print("len")
    #print(len(filtered_booklets))
    #print(len(booklet_mark_list))
    return render(request, 'recording.html',
                  {"student_id": studentID_Query, "sessions": filtered_sessions, "booklet_info": list(zip(filtered_booklets, booklet_mark_list)),
                   "booklet_form": booklet_form, "session_form": session_form, "formset": pages_form, "mod" : mod_booklet_form})

# "booklet_form": booklet_form, "session_form": session_form


def edit_booklet(request):
    #print("here")
    #print(request.GET.get('booklet'))
    # return render(request, "edit.html")
    # booklet_obj = Booklet.objects.get(booklet_id)
    booklet_id = request.GET.get('booklet', '')

    if booklet_id != "":
      instance = get_object_or_404(Booklet, pk = booklet_id)
    else:
        instance = get_object_or_404(Booklet, pk=request.POST.get('booklet', ''))
    print(instance)
    if request.method == "POST":
        print("POST")
        mod_booklet_form = ModBookletForm(request.POST, instance = instance)
        booklet = mod_booklet_form.save(commit=False)
        #if mod_booklet_form.is_valid():
        booklet.save()
        return redirect('recording')
    else:
        mod_booklet_form = ModBookletForm(instance=instance)

    return render(request, "edit.html", {"form":mod_booklet_form, "id": booklet_id})
 

