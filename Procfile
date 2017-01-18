web: gunicorn app:app --log-file=-
init: python db-create.py
upgrade: python db-upgrade.py

heroku ps:scale web=1
