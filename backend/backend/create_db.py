import sqlite3

con = sqlite3.connect("db")

cur = con.cursor()
cur.execute("CREATE TABLE session(id, name, start, end, duration)")
cur.execute("CREATE TABLE window(id, title, app, time, session_id)")
