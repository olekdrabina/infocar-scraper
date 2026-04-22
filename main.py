import subprocess
import sys
import os
import re
from dotenv import load_dotenv

# global functions
def is_valid_email(email: str) -> bool:
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
    return re.match(pattern, email) is not None

try:
    print("""
==================================
        INFO CAR SCRAPER
==================================
    """)

    while True:
        print("\"0\" - Rozpoczęcie pobierania danych")
        print("\"1\" - Zmiana danych")
        choice = input()

        if choice == "0":
            subprocess.run([sys.executable, "scraper.py"])
            break

        elif choice == "1":
            load_dotenv()

            FIELDS = {
                0: ("- Login do Infocar: ", "Podaj nowy login:", "LOGIN"),
                1: ("- Hasło do Infocar: ", "Podaj nowe hasło:", "LOGIN_PASSWORD"),
                2: ("- Województwo: ", "Podaj nowe województwo:", "PROVINCE"),
                3: ("- Ośrodek WORD: ", "Podaj nowy ośrodek WORD:", "CENTER"),
                4: ("- Kategoria: ", "Podaj nową kategorię:", "CATEGORY"),
                5: ("- Typ egzaminu: ", "Wybierz typ egzaminu (praktyka / teoria):", "EXAM_TYPE"),
                6: ("- Częstotliwość pobierania terminów: ", "Podaj częstotliwość w minutach:", "MIN_FREQUENCY"),
                7: ("- Wyprzedzenie powiadomień: ", "Podaj liczbę dni wyprzedzenia:", "DAYS_AHEAD"),
                8: ("- Gmail (SMTP): ", "Podaj adres Gmail używany do SMTP:", "EMAIL"),
                9: ("- Hasło SMTP: ", "Podaj hasło SMTP:", "EMAIL_PASSWORD"),
            }
            def envPrint(index):
                return FIELDS.get(index, (None, None, None))

            env_data = {}
            if os.path.exists(".env"):
                with open(".env", "r") as f:
                    for line in f:
                        line = line.strip()
                        if "=" in line:
                            k, v = line.split("=", 1)
                            env_data[k] = v

            print("")
            print("--- Jeśli nie chcesz zmieniać konkretnej informacji naciśnij \"ENTER\" ---")
            for index in range(10):
                current, prompt, key = envPrint(index)

                print("")
                if "PASSWORD" in key:
                    display = "*" * 8
                else:
                    display = os.getenv(key)
                print(current + display)

                print(prompt)

                if key == "EXAM_TYPE":
                    while True:
                        raw = input().strip().lower()
                        if raw == "":
                            new_value = env_data.get(key, "")
                            break
                        if raw in ("praktyka", "teoria"):
                            new_value = raw
                            break
                        print("Wpisz: praktyka / teoria")
                elif key in ("DAYS_AHEAD", "MIN_FREQUENCY"):
                    while True:
                        raw = input().strip()
                        if raw == "":
                            new_value = env_data.get(key, "")
                            break
                        try:
                            value = int(raw)
                            if 0 < value < 1000:
                                new_value = str(value)
                                break
                            else:
                                print("Liczba musi być w zakresie 0-1000")
                        except ValueError:
                            print("To musi być liczba")
                elif key == "EMAIL":
                    while True:
                        raw = input().strip()
                        if raw == "":
                            new_value = env_data.get(key, "")
                            break
                        if is_valid_email(raw):
                            new_value = raw
                            break
                        else:
                            print("Nieprawidłowy email (np. user@gmail.com)")
                else:
                    raw = input().strip()
                    if raw == "":
                        new_value = env_data.get(key, "")
                    else:
                        new_value = raw
                if new_value != "":
                    env_data[key] = new_value
            with open(".env", "w") as f:
                for k, v in env_data.items():
                    f.write(f'{k}="{v}"\n')

            print("--- Zapisano nowe dane ---")
            subprocess.run([sys.executable, "scraper.py"])
            break
        else:
            print("")
            print("Nieprawidłowy wybór, spróbuj ponownie.")
except KeyboardInterrupt:
    print("")
    print("\nZamknięto program.")