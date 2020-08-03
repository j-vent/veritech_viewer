from django import forms

from session.models import Session, Booklet, Page, Question

class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ('student_id',)
        
        
class BookletForm(forms.ModelForm):
    class Meta:
        model = Booklet
        fields = ('student_time_range','class_or_homework', 'comments',)
        
class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ('page_number', 'overall_mark')

class ModBookletForm(forms.ModelForm):
    class Meta:
        model = Booklet
        fields = ('class_or_homework', 'comments',)
