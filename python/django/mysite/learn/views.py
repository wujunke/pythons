#coding:utf-8
from django.template import Template, Context
from django.http import HttpResponse
import datetime

def index(request):
    now = datetime.datetime.now()
    # Simple, "dumb" way of saving templates on the filesystem.
    # This doesn't account for missing files!
    fp = open('/Users/investarget/Desktop/python/django/mysite/learn/learn.html')
    t = Template(fp.read())
    fp.close()
    html = t.render(Context({'current_date': now}))
    return HttpResponse(html)
