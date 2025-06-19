from django.urls import path
from . import views

urlpatterns = [
    path('tab/', views.tab, name='tab'),
]