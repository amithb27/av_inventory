from django.contrib.auth.backends import BaseBackend 

from .models import Admin
from .models import user as use
from django.contrib.auth.hashers import check_password
class AdminBackend(BaseBackend):
    # manuall Authentication 

    def authenticate(self ,request, username = None , password= None ,**kwargs):
        try :
            user =  use.objects.get(username = username)
            print("got in " , username , password)
            HashPassword = user.password
            value    =  check_password( password,HashPassword )
            print(value,user)
            if value :
                return user.objects.get(username = "av")
            return None
        except Exception :
            return None
          
          
          