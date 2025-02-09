from django.shortcuts import render
from django.urls import reverse

# Create your views here.
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page

from rango.forms import CategoryForm
from rango.forms import PageForm
from django.shortcuts import redirect

def index(request):
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage matches to {{ boldmessage }} in the template!
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list

    return render(request, 'rango/index.html', context=context_dict)
    # return HttpResponse("Rango says hey there partner! <a href='/rango/about/'>About</a>")

def about(request):
    context_dict = {'greeting': 'This tutorial has been put together by President William Howard Taft'}
    return render(request, 'rango/about.html', context=context_dict)
    # return HttpResponse("Rango says here is the about page. <a href='/rango/'>Index</a>")

def show_category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)

        pages = Page.objects.filter(category=category)

        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None
    return render(request, 'rango/category.html', context=context_dict)

def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid(): 
            form.save(commit=True)

            return redirect('/rango/')
        
        else:
            print(form.errors)

    return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    if category is None:
        return redirect('/rango/')
    
    form = PageForm()
    
    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

                return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
            
        else:
            print(form.errors)
        
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)