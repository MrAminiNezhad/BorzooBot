#!/bin/bash

apt-get update

rm main.py

rm info.json

wget https://raw.githubusercontent.com/MrAminiNezhad/3x-ui-Sanaei-TelegramBot/main/main.py

wget https://raw.githubusercontent.com/MrAminiNezhad/3x-ui-Sanaei-TelegramBot/main/info.json

pkill -f "main.py"
