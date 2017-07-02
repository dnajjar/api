#!/usr/bin/python

import requests
import json
import sqlite3  
import config

# Get data from Chartbeat API
url ='http://api.chartbeat.com/live/toppages/?apikey=%s&host=someecards.com&limit=100' % config.api_key
r = requests.get(url)
page_data = r.json() 
# results from api - latest visitors num

# Store data
conn = sqlite3.connect('%s/database.sqlite' % config.file_path)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS concurrencies (title TEXT, `path` TEXT, last_visitors REAL, visitor_diff REAL)''')

for item in page_data:
  # does a db entry exist for this path?
  c.execute("SELECT last_visitors FROM concurrencies where `path` = ?", (item['path'],) )
  data = c.fetchall()
  # if no db entry exists for a given path, create it
  if len(data) == 0:
    c.execute("INSERT INTO concurrencies VALUES (?, ?, ?, ?);", (item['i'], item['path'], item['visitors'], 0))
  else:
    # If db entry already exists for a given path, find visitor diff and modify diff and visitor columns
    last_visitors = int(data[0][0])
    new_visitors = item['visitors']
    visitor_diff = new_visitors - last_visitors
    c.execute("UPDATE concurrencies SET last_visitors = (?), visitor_diff = (?) WHERE `path` = (?);", (new_visitors, visitor_diff, item['path']))

conn.commit()
conn.close()
