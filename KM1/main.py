import setup_db
import database
import server

setup_db.create_db()
mydb = database.polacz()

if mydb.is_connected():
    database.utworz_tabele(mydb)

server.uruchom_serwer()
