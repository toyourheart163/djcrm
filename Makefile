run:
	python3 manage.py makemigrations
	python3 manage.py migrate

two:
	python3 manage.py makemigrations crm
	python3 manage.py makemigrations gbacc
	python3 manage.py makemigrations king_admin
	python3 manage.py migrate
	python3 manage.py createsuperuser
su:
	python3 manage.py makemigrations crm
	python3 manage.py makemigrations gbacc
	python3 manage.py makemigrations king_admin
	python3 manage.py migrate
