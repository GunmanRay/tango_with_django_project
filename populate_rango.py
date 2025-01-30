import os 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 
                     'tango_with_django_project.settings')

import django
django.setup()

from rango.models import Category, Page

def populate():
    # This creates a list of pages that are meant to be found within each
    # Category, where each page has a respective Name/Title and URL
    python_pages = [
        {'title': 'Official Python Tutorial',
         'url':'http://docs.python.org/3/tutorial/',
         'views': 5},

        {'title':'How to Think like a Computer Scientist',
         'url':'http://www.greenteapress.com/thinkpython/',
         'views': 27},

        {'title':'Learn Python in 10 Minutes',
         'url':'http://www.korokithakis.net/tutorials/python/',
         'views': 139}
    ]
    
    django_pages = [
        {'title':'Official Django Tutorial',
        'url':'https://docs.djangoproject.com/en/2.1/intro/tutorial01/',
        'views': 1},

        {'title':'Django Rocks',
         'url':'http://www.djangorocks.com/',
         'views': 8812},

        {'title':'How to Tango with Django',
         'url':'http://www.tangowithdjango.com/',
         'views': 9000}
    ]

    other_pages = [
        {'title':'Bottle',
         'url':'http://bottlepy.org/docs/dev/',
         'views': 50},

        {'title':'Flask',
         'url':'http://flask.pocoo.org',
         'views': 111}
    ]

    # Short for Category
    cats = {'Python' : {'pages': python_pages,
                        'views': 128,
                        'likes': 64},
            'Django' : {'pages': django_pages,
                        'views': 64,
                        'likes': 32},
            'Other Frameworks' : {'pages': other_pages, 
                                  'views': 32,
                                  'likes': 16}}
    
    # Goes through the 'cats' dictionary, adding/creating each (proper) category
    # and thus populating the categories with their associated pages
    for cat, cat_data in cats.items():
        c = add_cat(cat, cat_data['views'], cat_data['likes'])
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'], p['views']) 

    # Printing out every page that we added, organized by their respective categories
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'{c}: {p}')


# Helper functions that do the heavy lifting w/ adding categories
# Add a Page
def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title, views=views)[0]
    p.url = url
    p.views = views
    p.save()
    return p
    
# Add a Category
def add_cat(name, views, likes):
    c = Category.objects.get_or_create(name=name, views=views, likes=likes)[0]
    c.save()
    return c

# This is here to make it such that this program is only executed
# as a standalone script and NOT AN IMPORT.
if __name__ == '__main__':
    print("Starting the Rango Population Script.............")
    populate()