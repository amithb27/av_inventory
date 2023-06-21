import string
import random
from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage
import os
print( os.path.abspath(""))
def makePassword():
    letters = string.ascii_letters
    digits = string.digits
    special_chars = string.punctuation
    chars = letters +digits+special_chars
    password = ""
    pass_len = 10
    alphas = 5
    nums = 2
    while True :
        c = random.choice(chars)
        print(c)
        if pass_len == 0:
            print(nums , alphas)
            if (nums==0 and alphas==0):
                return password
                
            else:
                pass_len = 10
                password=""
                alphas =5 
                nums = 2 
        if c!=" ":
            if c.isalpha():
                alphas -=1
            elif c.isdigit():
                nums-=1
            password+=c
            pass_len -=1

def CustomsendMail(subject , message , to_Person , template 
             , vedioFiles =None , imageFiles =None):
   
    email = EmailMultiAlternatives(subject=subject , body=message ,
                           to=[to_Person] 
    )
    email.mixed_subtype = 'related'
    if vedioFiles is not None:
        for vedio in vedioFiles:
            (file_name , content) = vedio
            email.attach(filename=file_name , content=content)
    if imageFiles is not None:
        for image in vedioFiles:
            (file_name , content) = image
            email.attach(filename=file_name , content=content)
    email.attach_file("/Users/manikanta/Desktop/Logo.png" ,"image/png")
    email.attach_alternative(template , "text/html")
    logo_path = os.path.abspath( os.path.join("userData","static","userData","images","Logo.png"))
    with open(logo_path  ,'rb') as f:
        img = MIMEImage(f.read())
        print(f)
        img.add_header('Content-ID','<Logo.png>')
        img.add_header('Content-Disposition','inline')  
    email.attach(img)
    try :
        email.send(fail_silently=False )
        return True
    except Exception as e:
        return e