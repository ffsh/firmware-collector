#! python3

from tinydb import TinyDB, Query

db = TinyDB('db.json')
db.insert({'int': 1, 'char': 'a'})
db.insert({'int': 1, 'char': 'b'})