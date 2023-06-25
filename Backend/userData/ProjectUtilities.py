import string
import secrets
from .deaultValues import default_user_password_length


from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage
import os

from .models import *

import pandas as pd

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
    
    
def XlsxExporter(*fields, **model):
    """
    Create an Excel file (.xlsx) from a model.

    Args:
        *fields: Positional arguments (sequence of strings)
            - field1: Name of the first field in the model to include in the Excel file.
            - field2: Name of the second field in the model to include in the Excel file.
            - ...

        **model: Keyword arguments (dictionary)
            - model: The model class to export.

    Returns:
        True: If the Excel sheet is successfully created.
        Exception: If an error occurs during the file creation process
    """
    
    export_Model = model["model"]
    name = export_Model._meta.model_name +".xlsx"
    users = export_Model.objects.all()
    dicts = list(users.values(*fields))
    data_Frame = pd.DataFrame(dicts)
    try :
        data_Frame.to_excel(excel_writer=name,index=False)
        return (True) 
    except Exception as e:
        return (e)
    
    
def XlsxImporter(file , model):
      undone_list = []
      done = 0
      undone = 0
      df = pd.read_excel(file)
      for _,row in df.iterrows():
          print(row)
          new_model = model(**row)
          try:
            new_model.save()
            done+=1
          except Exception as e :
              value = row.values()[0]
              undone_list.append(value)
              undone+=1
      return (done , undone , undone_list)
  
def CreateNotification(user , message , messageCode):
     notification = Notification(message = message , 
                                 messageCode = messageCode                       
     )
     try:
        notification.save()
     except Exception as e :
         return e 
     user.notifications.add(notification)
     return  True
    
        
      
      