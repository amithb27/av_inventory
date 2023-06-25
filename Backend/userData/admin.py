from django.contrib import admin
from  django.apps import apps
# Register your models here.

def allModels():
    models=apps.get_models()
    filtered_models = [model for model in models if model._meta.app_config.name == 'userData']
    for model in filtered_models :
       print(model)
       admin.site.register(model)
allModels()
