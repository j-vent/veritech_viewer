from django.db import models
from datetime import datetime
from time import strftime

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

class Booklet(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="booklet", null=True, default=None)
    BKLT_TYPE=((0, "10"),(1,"5"),(2,"4,3,3"))
    booklet_type = models.CharField(max_length=1, choices=BKLT_TYPE, default=0)
    booklets = models.Manager()

class Page(models.Model):
    booklet = models.ForeignKey(Booklet, on_delete=models.CASCADE, null=True, default=None)
    page_number = models.CharField(max_length=45)
    overall_mark = models.PositiveIntegerField()

class Question(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, null=True, default=None)
    marking_outcome = models.CharField(max_length=45)
    correct_ans = models.CharField(max_length=45)
    pred_regex = models.CharField(max_length=45)


