import os
import time
import mysql.connector
from jinja2 import Environment, FileSystemLoader


QUERY = "SELECT title, text FROM articles order by rand() limit 1;"
INDEX_FILEPATH = "/usr/share/nginx/html/index.html"
SLEEP = 30

config = {
  'user': os.environ['MYSQL_USERNAME'],
  'password': os.environ['MYSQL_PASSWORD'],
  'host': os.environ['MYSQL_HOSTNAME'],
  'database': 'mysql',
}

env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('index.j2')

while True:
    try:
        with mysql.connector.connect(**config) as connection:
            cursor = connection.cursor()
            cursor.execute(QUERY)
            title, text = next(cursor)
            data = {
                'title': title,
                'text': text
            }
    except Exception as ex:
        data = {
            'error': ex,
        }
    with open(INDEX_FILEPATH, "w") as f:
        f.write(template.render(data))
    time.sleep(SLEEP)
