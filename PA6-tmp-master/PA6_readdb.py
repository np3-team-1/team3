import sqlite3
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "citysearch_project.settings")
django.setup()
from cities.models import City



conn=sqlite3.connect('temperature.db')
c=conn.cursor()

for row in c.execute('SELECT * FROM TMP'):
	City(name=row[0], state=row[1]).save()
	print(row)

