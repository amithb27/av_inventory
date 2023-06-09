from __future__ import absolute_import,unicode_literals
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from userData.models import Employee
from celery import shared_task


def MailSender(template, to_Person):
    
    send_mail(
    html_message=template,
    subject ="Email_testing",
    message= "...Analytics Valley...",
    from_email=settings.EMAIL_HOST_USER,
    recipient_list=to_Person,
    fail_silently=False,
        ) 

def show():
    today_Date = timezone.now()
    return(today_Date)

@shared_task
def add():
    k= show()
    return k
    
    
@shared_task
def BirthdayMail():
    today_Date = timezone.now()
    current_Year = int(today_Date.strftime("%Y"))
    month =int(today_Date.strftime("%m"))
    day =int(today_Date.strftime("%d"))
    filtered_Employees = Employee.objects.filter(birthdate__month = month , birthdate__day = day )
    if filtered_Employees.exists():
        for emp in filtered_Employees:
                birthDayContext={
                    "name" :emp.name,
                    "year" : current_Year
                }
                template = render_to_string(template_name="birthday.html",context=birthDayContext)
                MailSender(template,emp.email)

@shared_task
def AniversayMail():
    today_Date = timezone.now()
    current_Year = int(today_Date.strftime("%Y"))
    month =int(today_Date.strftime("%m"))
    day =int(today_Date.strftime("%d"))
    filtered_Employees = Employee.objects.filter(joining_Date__month = month ,joining_Date__day = day )
    if filtered_Employees.exists():
        for emp in filtered_Employees:
                working_Years = current_Year - int(emp.joining_Date.year)
                aniversaryContext={
                    "name" :emp.name,
                    "year" : current_Year,
                    "workingYears" : working_Years 
                }
                template = render_to_string(template_name="aniversary.html",context=aniversaryContext)
                MailSender(template,emp.email)

    
