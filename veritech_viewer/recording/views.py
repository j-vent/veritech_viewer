from django.shortcuts import render
from django.http import Http404
from session.models import Session
# Create your views here.

def recording_home(request):
    return render(request, "recording.html")