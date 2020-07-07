from django.db import models

# Create your models here.
class Session(models.Model):
    student_id = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    booklet = models.PositiveIntegerField()
    status = models.PositiveIntegerField()

class Booklet(models.Model):
    BKLT_TYPE=((0, "10"),(1,"5"),(2,"4,3,3"))
    booklet_type = models.CharField(max_length=1,choices=BKLT_TYPE, default = 0)
    # questions and overall mark



