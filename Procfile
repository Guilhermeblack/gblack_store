web: gunicorn django_project.wsgi:gbstr --log-file - --log-level debug
python manage.py collectstatic --noinput
manage.py migrate