#!/bin/bash

if [ ! -d "venv" ]; then
    echo "Tworzenie venv..."
    python3 -m venv venv
fi

source venv/bin/activate

echo "Instalacja pakietów..."
pip install -r requirements.txt

echo "Start aplikacji..."
python main.py