# Z1 api demo
Example Project using Django and Graphql

## The Environment

We are going to use pipenv to manage environment.

I like to use other tools to improve code quality and make easy to have clean projects
- Precommit
- isort
- black
- flake8


###Preparing developing environment
- Install pipenv with `pip install pipenv`
- Create environment `pipenv install --dev`
- Synchronize environment `pipenv lock & pipenv sync`


manage.py dumpdata --exclude auth.permission --exclude contenttypes > db.json


Launch Fake Mail server to log mails:
```
python -m smtpd -n -c DebuggingServer localhost:1025
```

End point de cambiar password -> manual
Probar que se puede usar model user a pelo
activar url en activar cuenta y activar password
Quitar harcodeos y poner entornos en settings
model exception en seguimiento al mismo usuario
refactorizar change status de peticion
Listado de usuarios tienen que paginar-> Relay?
Django Cache
Test
Posgre test


django-admin startproject z1socialideas
django-admin startapp smartnote
django-admin startapp smartrelations
django-admin startapp socialuser
copiar las apps del setting
python manage.py makemigrations
python manage.py migrate
python manage.py flush
python manage.py createsuperuser
meter datos
