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

def pobierz(mydb):
    cursor = mydb.cursor()

    sql_minimum = """SELECT data, temperatura FROM pomiar
                     WHERE temperatura = (SELECT MIN(temperatura) FROM pomiar)
                     ORDER BY data ASC, pomiar_id ASC
                     LIMIT 1"""
    cursor.execute(sql_minimum)
    minimum = cursor.fetchone()

    sql_maksimum = """SELECT data, temperatura FROM pomiar
                      WHERE temperatura = (SELECT MAX(temperatura) FROM pomiar)
                      ORDER BY data ASC, pomiar_id ASC
                      LIMIT 1"""
    cursor.execute(sql_maksimum)
    maksimum = cursor.fetchone()

    sql_aktualna = """SELECT data, temperatura FROM pomiar
                      ORDER BY data DESC, pomiar_id DESC
                      LIMIT 1"""
    cursor.execute(sql_aktualna)
    aktualna = cursor.fetchone()

    return minimum, maksimum, aktualna

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
    print("utworzono tabele Pomiar")
