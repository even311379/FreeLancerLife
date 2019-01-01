from django.shortcuts import render, redirect
from django.http import HttpResponse
import os

# Create your views here.
def test(request):
    return HttpResponse(render(request, 'index.html', locals()))

def root(request):
    return redirect('/home')