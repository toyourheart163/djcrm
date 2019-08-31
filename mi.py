import os

os.system('python manage.py makemigrations crm')
os.system('python manage.py migrate')
os.system('python manage.py createsuperuser')
