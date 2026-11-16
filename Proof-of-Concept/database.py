import setup_db
import mysql.connector

def polacz():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database=setup_db.db
    )
    return mydb

def zapisz(mydb, dane):
    cursor = mydb.cursor()

    sql = """INSERT INTO Pomiar (czujnik_id, data, temperatura) VALUES (%s, %s, %s)"""
    try:
        cursor.execute(sql, dane)
        mydb.commit()
        return True
    except mysql.connector.errors.IntegrityError:
        return False

def utworz_tabele(mydb):
    cursor = mydb.cursor()

    sql = """CREATE TABLE IF NOT EXISTS Pomiar
            (
            pomiar_id INT PRIMARY KEY AUTO_INCREMENT,
            czujnik_id INT,
            data DATETIME,
            temperatura INT
            )"""
    cursor.execute(sql)
    mydb.commit()
    print("Utworzono tabele Pomiar")