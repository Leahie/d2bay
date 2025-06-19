from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader 
from .models import User

# Create your views here.
def tab(request):
    template = loader.get_template('myfirst.html')
    return HttpResponse(template.render())

def users(request):
    myusers = User.objects.all().values()
    template = loader.get_template('allusers.html')
    context = {
        'myusers': myusers,
    }
    return HttpResponse(template.render(context, request))

def details(request, id):
    myuser = User.objects.get(id=id)
    template = loader.get_template('details.html')
    context = {'user':myuser}
    return HttpResponse(template.render(context, request))