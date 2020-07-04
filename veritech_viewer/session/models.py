from django.db import models

# Create your models here.
class Session(models.Model):
    student_id = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    booklet = models.PositiveIntegerField()
    status = models.PositiveIntegerField()
