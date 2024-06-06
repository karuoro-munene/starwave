# build_files.sh
pip install -r requirements.txt

# make migrations
python3.9 manage.py migrate
python3.9 manage.py collectstatic

#create admin
#DJANGO_SUPERUSER_USERNAME=admin DJANGO_SUPERUSER_EMAIL=admin@clinton.dev DJANGO_SUPERUSER_PASSWORD=droidstarwave python3.9 manage.py createsuperuser --noinput

