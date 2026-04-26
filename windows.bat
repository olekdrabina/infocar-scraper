@echo off

if not exist venv (
    echo Tworzenie venv...
    python -m venv venv
)

call venv\Scripts\activate

echo Instalacja pakietów...
pip install -r requirements.txt

echo Start aplikacji...
python main.py

pause