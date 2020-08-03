from django.contrib import admin

from .models import Session, Booklet, Page, Question

# Register your models here.

class SessionAdmin(admin.ModelAdmin):
    readonly_fields = ['id', ]
    fields = ['student_id', 'timestamp', 'status']
    list_display = ['id', 'student_id', 'timestamp', 'status_text']

class BookletAdmin(admin.ModelAdmin):
    readonly_fields = ['id', ]
    fields = ['session', 'booklet_type', 'class_or_homework', 'student_time_range', 'comments']
    list_display = ['id', 'session', 'booklet_type']

class PageAdmin(admin.ModelAdmin):
    readonly_fields = ['id', ]
    fields = ['booklet', 'page_number', 'overall_mark']
    list_display = ['id', 'booklet', 'page_number', 'overall_mark', 'counts']

class QuestionAdmin(admin.ModelAdmin):
    readonly_fields = ['id', ]
    fields = ['page', 'marking_outcome', 'correct_ans', 'pred_regex', 'images']
    list_display = ['id', 'page', 'marking_outcome']


admin.site.register(Session, SessionAdmin)
admin.site.register(Booklet, BookletAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Question, QuestionAdmin)

