#!flask/bin/python

from flask import Flask
import json
import sqlite3 as sql

app = Flask(__name__)


def dict_factory(cursor, row):
  d = {}
  for idx, col in enumerate(cursor.description):
    d[col[0]] = row[idx]
  return d

@app.route('/api', methods=['GET'])

def index():
  results = get_increasing_concurrencies()
  return json.dumps(results)

def get_increasing_concurrencies():
  con = sql.connect("database.sqlite")
  con.row_factory = dict_factory
  cur = con.cursor()
  cur.execute("select * from concurrencies where visitor_diff > 0")
  return cur.fetchall()

if __name__ == '__main__':
    app.run(debug=True)