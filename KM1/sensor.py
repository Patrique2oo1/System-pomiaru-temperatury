from datetime import datetime
import random
import time
import json
import urllib.request
import urllib.error

while True:
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    temperature = random.randint(15, 30)
    # print(f"{current_time} | {temperature} *C")

    if (temperature < 20):
        print("ALERT: niska temperatura!")
    elif (temperature > 25):
        print("ALERT: wysoka temperatura!")

    dane = {
        "czujnik_id": 1,
        "data": current_time,
        "temperatura": temperature
    }

    request = urllib.request.Request(
        "http://127.0.0.1:2137/pomiar",
        data = json.dumps(dane).encode("utf-8"),
        headers = {"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            if response.status == 201:
                print(f"WYSLANO: {current_time} | {temperature} *C")
    except urllib.error.HTTPError as e:
        print(f"BLAD HTTP: {e.code}")
    except (urllib.error.URLError, TimeoutError) as e:
        print(f"BLAD POLACZENIA: {e}")

    time.sleep(5)
