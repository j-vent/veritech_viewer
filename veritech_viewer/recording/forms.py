from django import forms

from session.models import Session, Booklet, Question

class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ('student_id')
        
class BookletForm(forms.ModelForm):
    class Meta:
        model = Booklet
        fields = ('student_id','student_time_range')