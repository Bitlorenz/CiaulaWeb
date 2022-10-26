from django.urls import path, include
from django.contrib import admin
from . import views
from .initcmds import *

urlpatterns = [
    path('', views.index, name='index')
]