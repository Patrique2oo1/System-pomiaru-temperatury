import json
import math
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import database

class Server(BaseHTTPRequestHandler):
    def response(self, kod, dane):
        wynik = json.dumps(dane).encode("utf-8")

        self.send_response(kod)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header( "Content-Length", str( len( wynik ) ) )
        self.end_headers()
        self.wfile.write(wynik)

    def do_POST(self):
        if self.path != "/pomiar":
            self.response(404, {"blad": "nieznany adres"})
            return

        try:
            dlugosc = int(self.headers.get("Content-Length", 0))
            if dlugosc <= 0 or dlugosc > 4096:
                self.response(400, {"blad": "nieprawidlowa dlugosc naglowka"})
                return

            dane = json.loads(self.rfile.read(dlugosc))
            czujnik_id = dane["czujnik_id"]
            temperatura = dane["temperatura"]
            data = dane["data"]

            if type(czujnik_id) is not int or czujnik_id <= 0:
                raise ValueError("nieprawidlowy identyfikator!")
            if type(temperatura) is not int:
                raise ValueError("nieprawidlowa temperatura!")
            if temperatura < 15 or temperatura > 30:
                raise ValueError("temperatura poza zakresem!")

            data = datetime.strptime(data, "%Y-%m-%d %H:%M:%S")

        except (ValueError, KeyError, TypeError):
            self.response(400, {"blad": "nieprawidlowe dane"})
            return

        try:
            baza = database.polacz()
            zapis_danych = database.zapisz(baza, (czujnik_id, data, temperatura))
            if zapis_danych:
                print(f"ZAPIS: {data} | {temperatura} *C")
                self.response(201, {"status": "zapisano pomiar"})
            else:
                self.response(500, {"blad": "nie zapisano pomiaru"})
        except Exception as e:
            print(f"blad serwera: {e}")
            self.response(500, {"blad": "blad serwera"})

    def do_GET(self):
        if self.path != "/pomiary":
            self.response(404, {"blad": "nieznany adres"})
            return

        try:
            baza = database.polacz()
            minimum, maksimum, aktualna = database.pobierz(baza)

            wynik = {
                "minimalna temperatura": {
                    "data": str(minimum[0]),
                    "temperatura": minimum[1]
                }
                if minimum else None,
                "maksymalna temperatura": {
                    "data": str(maksimum[0]),
                    "temperatura": maksimum[1]
                }
                if maksimum else None,
                "aktualna temperatura": {
                    "data": str(aktualna[0]),
                    "temperatura": aktualna[1]
                }
                if aktualna else None,
            }

            self.response(200, wynik)
        except Exception as e:
            print(f"blad serwera: {e}")
            self.response(500, {"blad": "blad serwera"})

def uruchom_serwer():
    server = ThreadingHTTPServer( ("127.0.0.1", 2137), Server )
    print("serwer uruchomiony!")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("zatrzymano serwer!")
    finally:
        server.server_close()
            
