web: gunicorn app:app --log-file=-
init: python db_create.py
upgrade: python db_upgrade.py

heroku ps:scale web=1
