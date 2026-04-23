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

def validate_env():
    REQUIRED_KEYS = {
        "LOGIN": "Login do Infocar",
        "LOGIN_PASSWORD": "Hasło do Infocar",
        "PROVINCE": "Województwo",
        "CENTER": "Ośrodek WORD",
        "CATEGORY": "Kategoria",
        "EXAM_TYPE": "Typ egzaminu",
        "MIN_FREQUENCY": "Częstotliwość pobierania terminów",
        "DAYS_AHEAD": "Ilość dni wyprzedzenia",
        "EMAIL": "Gmail (SMTP)",
        "EMAIL_PASSWORD": "Hasło SMTP",
    }

    if not os.path.exists(".env"):
        print("Musisz najpierw uzupełnić dane, wybierz opcję \"1\"")
        print("")
        return False

    env_data = {}
    with open(".env", "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if "=" in line:
                k, v = line.split("=", 1)
                env_data[k] = v.strip('"').strip()

    missing = [label for key, label in REQUIRED_KEYS.items() if not env_data.get(key)]

    if missing:
        print("\nBrakuje następujących danych:")
        for field in missing:
            print(f"   • {field}")
        print("\nUzupełnij je wybierając opcję \"1\"")
        print("")
        return False

    return True

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
            if validate_env():
                subprocess.run([sys.executable, "scraper.py"])
                break

        elif choice == "1":
            load_dotenv()

            FIELDS = {
                0: ("- Login do Infocar: ", "Podaj login:", "LOGIN", "BRAK LOGINU DO INFOCAR"),
                1: ("- Hasło do Infocar: ", "Podaj hasło:", "LOGIN_PASSWORD", "BRAK HASŁA DO INFOCAR"),
                2: ("- Województwo: ", "Podaj województwo:", "PROVINCE", "BRAK WOJEWÓDZTWA"),
                3: ("- Ośrodek WORD: ", "Podaj ośrodek WORD:", "CENTER", "BRAK OŚRODKA WORD"),
                4: ("- Kategoria: ", "Podaj kategorię:", "CATEGORY", "BRAK KATEGORII"),
                5: ("- Typ egzaminu: ", "Wybierz typ egzaminu (praktyka / teoria):", "EXAM_TYPE", "BRAK TYPU EGZAMINU"),
                6: ("- Częstotliwość pobierania terminów: ", "Podaj częstotliwość w minutach:", "MIN_FREQUENCY", "BRAK CZĘSTOTLIWOŚCI POBIERANIA TERMINÓW"),
                7: ("- Ilość dni wyprzedzenia terminów: ", "Podaj liczbę dni wyprzedzenia terminów:", "DAYS_AHEAD", "BRAK ILOŚCI DNI WYPRZEDZANIA TERMINÓW"),
                8: ("- Gmail (SMTP): ", "Podaj adres Gmail do SMTP:", "EMAIL", "BRAK GMAILA DO SMTP"),
                9: ("- Hasło SMTP: ", "Podaj hasło do SMTP:", "EMAIL_PASSWORD", "BRAK HASŁA DO SMTP"),
            }
            def envPrint(index):
                return FIELDS.get(index, (None, None, None))

            env_data = {}
            if os.path.exists(".env"):
                with open(".env", "r", encoding="utf-8", errors="ignore") as f:
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
            with open(".env", "w", encoding="utf-8") as f:
                for k, v in env_data.items():
                    f.write(f'{k}="{v}"\n')

            print("--- Zapisano nowe dane ---")
            subprocess.run([sys.executable, "scraper.py"])
            break
        else:
            print("")
            print("Nieprawidłowy wybór, spróbuj ponownie")
except KeyboardInterrupt:
    print("")
    print("\nZamknięto program")