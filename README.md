# info-car.pl scraper
Automatyczny scraper do wyszukiwania dostępnych terminów egzaminów na prawo jazdy na stronie **info-car.pl**

Terminy egzaminów często pojawiają się nagle, na przykład gdy ktoś anuluje rezerwację albo WORD udostępni nowe miejscam, często znikają w ciągu kilku minutaa a ten bot pomoże ci ich nie przegapić, automatycznie wysyłając powiadomienie e-mail jeśli pojawi się nowy termin

> [!TIP]
> Zalecam korzystać z konta innego niż główne, aby zminimalizować ryzyko ewentualnej blokady konta oficjalnego

## Działanie
- Automatycznie loguje do Info-Car.pl
- Wybiera województwo, WORD, kategorie i typ egzaminu
- Filtruje terminy według liczby dni w przód
- Wykrywa nowe terminy
- Wysyła powiadomieie na e-mail poprzez SMTP Gmail

> [!NOTE]
> Działa w godzinach 7:00–16:00, z pominięciem niedziel

## Instalacja
### Wymagania
- [Python 3.10+](https://www.python.org/downloads/)
- Chrome / Chromium
- Konto w info-car.pl
- Konto Gmail SMTP (poradnik poniżej)
### Konto Gmail SMTP
1. Wejdź na https://myaccount.google.com/apppasswords
2. Wpisz nazwe aplikacji (np. infocar-scraper)
3. Kliknij „Utwórz”
4. Skopiuj wygenerowane hasło (16 znaków)
5. Wklej w terminalu po włączeniu aplikacji
### Aplikacja
1. Pobierz pliki z tego repozytorium
2. Otwórz folder z plikami w terminalu
3. Utwórz środowisko komendą:
    - Windows - `python -m venv venv`
    - Linux / MacOS - `python3 -m venv venv`
4. Aktywuj środowisko komendą:
    - Windows - `venv\Scripts\activate`
    - Linux / MacOS - `source venv/bin/activate`
5. Zainstaluj wymagane pakiety komendą `pip install -r requirements.txt`
6. Uruchom aplikacje komendą `python main.py`

> [!TIP]
> Aby zatrzymać bota naciśnij `CTRL + C`

> [!IMPORTANT]
> Aby uruchomić ponownie bota należy:
> - Jeśli terminal nadal jest otwarty wystarczy ponownie uruchom aplikację (krok 6)
> - Jeśli terminal został zamknięty najpierw aktywuj środowisko (krok 4), a następnie uruchom aplikację (krok 6)

## Ostrzeżenie
> [!CAUTION]
> - Program powstał w celach edukacyjnych, użytkownik korzysta z niego na własną odpowiedzialność
> - Nie biore odpowiedzialności za ewentualne blokady konta ani inne konsekwencje wynikające z korzystania z bota

## Zgłaszanie błędów i sugestii
Jeśli napotkasz błędy, masz pomysły na ulepszenia lub chcesz zaproponować nowe funkcje:
- **Zgłaszanie błędów:** użyj zakładki [Issues](https://github.com/olekdrabina/infocar-scraper/issues), aby zgłaszać błędy lub nieoczekiwane działanie
- **Propozycje funkcji:** nowe pomysły i sugestie również możesz przesyłać przez zakładkę [Issues](https://github.com/olekdrabina/infocar-scraper/issues)
- **Współtworzenie:** zrób fork repozytorium, wprowadź zmiany i wyślij pull request