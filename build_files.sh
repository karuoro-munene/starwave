# build_files.sh
pip install -r requirements.txt

# make migrations
python3.9 manage.py migrate
python3.9 manage.py collectstatic

#create admin
python3.9 manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@clinton', 'droid')"

