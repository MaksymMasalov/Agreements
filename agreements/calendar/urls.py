from django.urls import path
from . import views

urlpatterns = [
   path('agreement/', views.calendar)
]
