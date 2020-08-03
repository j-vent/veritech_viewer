from django.db import models
from datetime import datetime
from time import strftime

import re
import os

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

# Create your models here.
class Session(models.Model):
    student_id = models.PositiveIntegerField()
    # timestamp = models.DateTimeField(auto_now_add=True)
    timestamp = UnixTimestampField()
    status = models.PositiveIntegerField()
    sessions = models.Manager()

    def status_text(self):
        return {0: "Pending", 1: "Completed", 2: "Hidden"}[self.status]

class Booklet(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="booklet", null=True, default=None)
    BKLT_TYPE=((0, "10"),(1,"5"),(2,"4,3,3"))
    booklet_type = models.CharField(max_length=1, choices=BKLT_TYPE, default=0)
    student_time_range = models.CharField(max_length=128, null=True)
    scans = models.TextField(null=True)
    class_or_homework = models.CharField(null=True, max_length=1, default="H")
    comments = models.CharField(null=True, max_length=240)
    booklets = models.Manager()
    # if mod_page_range then don't
    def page_range(self):
        def sort_key(page_number):

            if page_number[0].isdigit():
                page_number = page_number[2:-1]
            else:
                page_number = page_number[1:-1]
                level = page_number[0]

            return int(page_number)

        def get_level(page_number):
            if page_number[0].isdigit():
                level = page_number[0:2]
            else:
                level = page_number[0]

            return level

        pages = Page.pages.all().filter(booklet__exact=self.id)
        page_numbers = [ p.page_number for p in pages ]
        page_numbers.sort(key=sort_key)
        if len(page_numbers) == 0:
            return 0,0,"A"

        return min(page_numbers), max(page_numbers), get_level(page_numbers[0])


    # TODO: Use wentao's function
    def fix_missing_pages(booklet_id, min_page):
        if booklet_id == 0:
            min_page = int(np.floor((min_page - 1) / 10)) * 10 + 1
            max_page = int(np.ceil((min_page - 1) / 10)) * 10 + 10
        elif booklet_id == 1:
            min_page = int(np.floor((min_page - 1) / 5)) * 5 + 1
            max_page = int(np.ceil((min_page - 1)) / 5) * 5 + 5
        elif booklet_id == 2:
            if int(str(min_page)[-1]) in [1, 2, 3, 4]:
                min_page = int(str(min_page - 1)[:-1] + "1")
                max_page = int(str(min_page - 1)[:-1] + "4")
            elif int(str(min_page)[-1]) in [5, 6, 7]:
                min_page = int(str(min_page - 1)[:-1] + "5")
                max_page = int(str(min_page - 1)[:-1] + "7")
            elif int(str(min_page)[-1]) in [8, 9, 0]:
                min_page = int(str(min_page - 1)[:-1] + "8")
                max_page = int(str(min_page - 1)[:-1] + "0") + 10

        return min_page, max_page

    def image_paths(self):
        return [ os.path.join("images", x + ".png") for x in self.scans.split(",") ]

class Page(models.Model):
    booklet = models.ForeignKey(Booklet, on_delete=models.CASCADE, null=True, default=None)
    page_number = models.CharField(max_length=45)
    overall_mark = models.PositiveIntegerField()
    pages = models.Manager()

    # returns (accept, not_sure, reject, total)
    def counts(self):
        counts = [ len(Question.questions.all().filter(page__exact=self.id, marking_outcome=outcome)) for outcome in ['ACCEPT', 'NOT_SURE', 'REJECT'] ]
        counts.append(len(Question.questions.all().filter(page__exact=self.id)))
        return counts

    # return count of accepted (ACCEPT or NOT_SURE)
    def num_accepted(self):
        counts = self.counts()
        return counts[0] + counts[1]

class Question(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, null=True, default=None)
    marking_outcome = models.CharField(max_length=45)
    correct_ans = models.CharField(max_length=45)
    pred_regex = models.CharField(max_length=45)
    images = models.TextField()
    questions = models.Manager();

    def color_code_html(self):
        colors = {
            'REJECT': '#FF3A01',
            'NOT_SURE': '#DDAE58',
            'ACCEPT': '#5BBA64'
        }
        
        return colors[self.marking_outcome]

    def predicted_answer(self):
        def proposals(lst):
            if len(lst) == 0: return []
            if len(lst) == 1: return lst[0]
            p = proposals(lst[1:])

            ret = []
            for x in lst[0]:
                for y in p:
                    ret.append(str(x) + str(y))

            return ret

        if len(self.pred_regex) < 4:
            return "No text detected"
        tokens = [x.split("|") for x in self.pred_regex[2:-2].split(")(")]
        prop = list(set(proposals(tokens)))

        text = " or ".join(prop)
        return text

    def image_paths(self):
        return [ os.path.join("images", x + ".png") for x in self.images.split(",") ]


