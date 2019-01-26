from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from .models import ContactMeData, task_type, plan_type, ContactMe, SubscriberEmail


def reply_contact(request):
    if request.method == "POST":
        name = request.POST['fullName']
        organization = request.POST['organization']
        task = request.POST['task_type']
        due_date = request.POST['due_date']
        plan = request.POST['plan_type']
        email = request.POST['email']
        language_code = request.POST['language_code']

        print(language_code)

        if language_code == 'en':
            new_ContactMeData = ContactMeData.objects.create(
                name=name,
                organization=organization,
                task = task_type.objects.get(name_en=task),
                due_date = due_date,
                plan = plan_type.objects.get(name_en=plan),
                email = email,
                receive_time = timezone.now(),
            )
        else:
            new_ContactMeData = ContactMeData.objects.create(
                name=name,
                organization=organization,
                task = task_type.objects.get(name=task),
                due_date = due_date,
                plan = plan_type.objects.get(name=plan),
                email = email,
                receive_time = timezone.now(),
            )
        
        new_ContactMeData.save()
        print('saving date')
        print('maybe direct send me an email??')
        
        page = [p for p in ContactMe.objects.all() if p.language.code == language_code][0]

        return HttpResponse(render(request, 'home/reply_contact.html', locals()))
    else:
        return HttpResponse(render(request, 'home/reply_contact.html', locals()))
        # return HttpResponse('<html><h1>Hey! You should visit this page by post!</h1></html>')


def add_subscribe(request):
    if request.method == "POST":
        email = request.POST['subscriber_mail']
        language_code = request.POST['language_code']
        new_subscriber = SubscriberEmail.objects.create(
            subsciber_email = email,
            receive_time = timezone.now(),
        )

        new_subscriber.save()

        return HttpResponse(render(request, 'home/thank_subscribe.html', locals()))

    else:
        return HttpResponse('<html><h1>Hey! You should visit this page by post!</h1></html>')
