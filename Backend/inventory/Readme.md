# av_inventory

## Backend Installation (for Mac Users) . 

#### step1 Check For python 

    Ensure that you have <Python> installed on your system. You can check if it is already installed by running the 

    cmd (zsh): python3 --version

    python = v3.11.1

    if you are not installed then download and install 

  go to here 👉👉    https://www.python.org/downloads/macos/
    

#### step2 install pip using get-pip.py.
    Ensure that you have <pip> installed on your system. You can check if it is already installed by running the 

    cmd (zsh): pip --version 

    if you are not installed then run these commands on terminal 

    cmd (zsh): curl https://bootstrap.pypa.io/get-pip.py -o get-pippy. 

    cmd (zsh): sudo python get-pip.py. 

#### Step3 Navigate to the project 
    cmd (zsh): git init
    cmd (zsh): git clone <repository_url>
    cmd (zsh): cd Backend/inventory

#### Step4 create an environment 
-->navigate to the project directory 
cmd (zsh): python3 -m venv myenv
cmd (zsh): source myenv/bin/activate

#### step5 install the necessary requirements

cmd (zsh): pip install -r requirements.txt

### step6 Setup Mysql Database

 if you are not installed <mysql> then download and install

 go to here 👉👉  https://dev.mysql.com/downloads/mysql/ 
  
    cmd (zsh) : mysql -u root -p

 create username and password for your psql server

  cmd (mysql) : CREATE USER 'username'@'localhost' IDENTIFIED BY 'password';

  cmd(mysql) : GRANT ALL PRIVILEGES ON *.* TO'username'@'localhost';
  
  cmd (mysql) : exit;

#### step6 Update the database settings
 navigate to  Backend/inventory/inventory/settings.py

in settings.py you will see similar to this 

 DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

replace that with the above one with the below one 

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your_database_name',
        'USER': 'your_mysql_username',
        'PASSWORD': 'your_mysql_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

#### step6 make migrations to database

cmd(zsh) : python3 manage.py makemigrations

cmd (zsh) : python3 manage.py migrate

#### step7 start the django server

cmd (zsh) : python3 manage.py runserver
