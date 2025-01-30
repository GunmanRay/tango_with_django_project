from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from rango.models import Category


def index(request):
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage matches to {{ boldmessage }} in the template!
    category_list = Category.objects.order_by('-likes')[:5]

    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list

    return render(request, 'rango/index.html', context=context_dict)
    # return HttpResponse("Rango says hey there partner! <a href='/rango/about/'>About</a>")

def about(request):
    context_dict = {'greeting': 'This tutorial has been put together by President William Howard Taft'}
    return render(request, 'rango/about.html', context=context_dict)
    # return HttpResponse("Rango says here is the about page. <a href='/rango/'>Index</a>")