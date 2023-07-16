#!/bin/bash

apt-get update

rm main.py

wget https://raw.githubusercontent.com/MrAminiNezhad/3x-ui-Sanaei-TelegramBot/main/main.py

pkill -f "main.py"

nohup python3 main.py &
