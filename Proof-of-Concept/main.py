import setup_db
import database

setup_db.create_db()
mydb = database.polacz()

if mydb.is_connected():
    database.utworz_tabele(mydb)

import sensor