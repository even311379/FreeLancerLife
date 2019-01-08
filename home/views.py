from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from .models import ContactMeData, task_type, plan_type, ContactMe

def reply_contact(request):
    if request.method == "POST":
        name = request.POST['fullName']
        organization = request.POST['organization']
        task = request.POST['task_type']
        due_date = request.POST['due_date']
        plan = request.POST['plan_type']
        email = request.POST['email']

        new_ContactMeData = ContactMeData.objects.create(
            name=name,
            organization=organization,
            task = task_type.objects.get(name=task),
            due_date = due_date,
            plan = plan_type.objects.get(name=plan),
            email = email,
            receive_time = timezone.now(),
        )
        print('saving date')
        print('maybe direct send me an email??')
        page = ContactMe.objects.all()[0]

        return HttpResponse(render(request, 'home/reply_contact.html', locals()))
    else:
        return HttpResponse(render(request, 'home/reply_contact.html', locals()))
