from django.shortcuts import render
from django.http import HttpResponse

def abcd(request):
    return HttpResponse(u'testdjtest')