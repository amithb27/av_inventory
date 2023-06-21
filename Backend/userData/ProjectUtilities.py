import string
import random
from django.core.mail import EmailMultiAlternatives
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
    if vedioFiles is not None:
        for vedio in vedioFiles:
            (file_name , content) = vedio
            email.attach(filename=file_name , content=content)
    if imageFiles is not None:
        for image in vedioFiles:
            (file_name , content) = image
            email.attach(filename=file_name , content=content)
    # email.attach_file("/Users/manikanta/Desktop/pic.png" ,"image/png")
    email.attach_alternative(template , "text/html")
    email.send(fail_silently=False )
    return True