"""veritech_viewer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
import session.views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', session.views.home, name='home'),
    path('test/',session.views.test,name='test'),
    # path('page/<int:page_a_id>/<int:page_b_id>', session.views.pages, name='pages'),
    path('page/<int:page_id>/', session.views.pages, name='pages'),
    path('questions/', session.views.questions, name='questions'),
    path('booklet/<int:booklet_id>/', session.views.booklet, name='booklet')
]
