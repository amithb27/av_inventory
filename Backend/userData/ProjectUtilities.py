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
    pass_len = 10
    password = ""
    nums = 3
    alphas = 4
    special = 3
    while 1 :
        ele = random.choice(chars)
        if (ele.isalpha()) and (alphas>0):
            password+=ele
            alphas-=1
        elif (ele.isdigit()) and (nums>0):
            password+=ele
            nums-=1
        elif (ele !=" ") and (special>0):
            password+=ele
            special -=1
        if len(password) == pass_len :
            break
        print(len(password))
    return password
        

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