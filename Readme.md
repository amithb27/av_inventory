# av_inventory

## MAC OS X (Zshell) installation (Backend) . 

#### step1 install pip using get-pip.py.

cmd : curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py. 

cmd : sudo python get-pip.py. 

#### Step2 create an environment for the project 
-->navigate to the project directory 
cmd python3 -m venv myenv
cmd source myenv/bin/activate

#### step2  install django using pip.

cmd : pip install django

#### step3  Create Django project and app .

project_name= projectBackend

app_name=userData

cmd : django-admin startproject < project_name >

cmd : cd <project_name>

cmd : python manage.py startapp <app_name >

#### step4 install the packages 
  
cmd : pip install djangorestframework

#### step5  replace the app directory with the app directory in Backend folder 

directory_name=userData
 
#### step6 make migrations to database

cmd : python manage.py makemigrations

cmd : python manage.py migrate