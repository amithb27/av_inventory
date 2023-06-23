import string
import secrets
from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage
from .deaultValues import default_user_password_length
import os
def makePassword():
    letters = string.ascii_letters
    digits = string.digits
    special_chars = string.punctuation
    chars = letters +digits+special_chars
    pass_len = default_user_password_length
    password = ""
    nums = 1
    lower = 1
    special = 1
    upper = 1
    while 1 :
        ele = secrets.choice(chars)
        if (ele.isupper()) and (upper>0):
            password+=ele
            upper-=1
        elif (ele.isdigit()) and (nums>0):
            password+=ele
            nums-=1
        elif (ele.islower()) and (lower>0):
            password+=ele
            lower-=1
        elif (ele !=" ") and (special>0):
            password+=ele
            special -=1
        if (nums+lower+special+upper==0) and ele!=" " :
            if len(password)==pass_len:
                break
            password+=ele
  
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
    # email.attach_file("/Users/manikanta/Desktop/Logo.png" ,"image/png")
    email.attach_alternative(template , "text/html")
    logo_path = os.path.abspath( os.path.join("userData","static","userData","images","Logo.png"))
    with open(logo_path  ,'rb') as f:
        img = MIMEImage(f.read())
        img.add_header('Content-ID','<Logo.png>')
        img.add_header('Content-Disposition','inline')  
    email.attach(img)
    try :
        email.send(fail_silently=False )
        return True
    except Exception as e:
        return e