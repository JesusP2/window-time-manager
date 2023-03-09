import sqlite3

con = sqlite3.connect("db")

cur = con.cursor()
res = cur.execute("SELECT name FROM sqlite_master")
