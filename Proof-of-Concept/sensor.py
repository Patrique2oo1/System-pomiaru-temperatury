from datetime import datetime
import random
import time

import database

while True:
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    temperature = random.randint(15, 30)
    # print(f"{current_time} | {temperature} *C")

    if (temperature < 20):
        print("ALERT: niska temperatura!")
    elif (temperature > 25):
        print("ALERT: wysoka temperatura!")

    dane = (1, current_time, temperature)
    baza = database.polacz()
    if baza.is_connected():
        if database.zapisz(baza, dane):
            print(f"ZAPIS: {current_time} | {temperature} *C")
        else:
            print("BLAD: nie zapisano danych!")


    time.sleep(5)