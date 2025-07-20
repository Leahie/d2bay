from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader 
from .models import CustomUser

# Create your views here.
def tab(request):
    template = loader.get_template('myfirst.html')
    return HttpResponse(template.render())

def users(request):
    myusers = CustomUser.objects.all().values()
    template = loader.get_template('allusers.html')
    context = {
        'myusers': myusers,
    }
    return HttpResponse(template.render(context, request))

def details(request, id):
    myuser = CustomUser.objects.get(id=id)
    template = loader.get_template('details.html')
    context = {'user':myuser}
    return HttpResponse(template.render(context, request))