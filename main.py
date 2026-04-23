import subprocess
import sys
import os
import re
from dotenv import load_dotenv

# patch lib for distutils
import site
from pathlib import Path
def patch_distutils():
    for sp in site.getsitepackages():
        f = Path(sp) / "undetected_chromedriver" / "patcher.py"
        if f.exists():
            text = f.read_text(encoding="utf-8")
            fixed = text.replace(
                "from distutils.version import LooseVersion",
                "from setuptools._distutils.version import LooseVersion"
            )
            if text != fixed:
                f.write_text(fixed, encoding="utf-8")
patch_distutils()

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
                0: ("- Login do Infocar: ", "Podaj login:", "LOGIN", "Brak loginu do infocar"),
                1: ("- Hasło do Infocar: ", "Podaj hasło:", "LOGIN_PASSWORD", "Brak hasła do infocar"),
                2: ("- Województwo: ", "Podaj województwo:", "PROVINCE", "Brak województwa"),
                3: ("- Ośrodek WORD: ", "Podaj ośrodek WORD:", "CENTER", "Brak ośroda WORD"),
                4: ("- Kategoria: ", "Podaj kategorię:", "CATEGORY", "Brak kategorii"),
                5: ("- Typ egzaminu: ", "Wybierz typ egzaminu (praktyka / teoria):", "EXAM_TYPE", "Brak typu egzaminu"),
                6: ("- Częstotliwość pobierania terminów: ", "Podaj częstotliwość w minutach:", "MIN_FREQUENCY", "Brak częstotliwości pobierania terminów"),
                7: ("- Ilość dni wyprzedzenia terminów: ", "Podaj liczbę dni wyprzedzenia terminów:", "DAYS_AHEAD", "Brak ilości dni wyprzedzania terminów"),
                8: ("- Gmail (SMTP): ", "Podaj adres Gmail do SMTP:", "EMAIL", "Brak gmaila dla SMTP"),
                9: ("- Hasło SMTP: ", "Podaj hasło do SMTP:", "EMAIL_PASSWORD", "Brak hasła dla SMTP"),
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
                current, prompt, key, missing = envPrint(index)

                print("")
                if "PASSWORD" in key:
                    display = "*" * 8 if key in env_data else missing
                else:
                    display = env_data.get(key) or missing
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