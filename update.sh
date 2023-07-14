#!/bin/bash

apt-get update

wget https://raw.githubusercontent.com/MrAminiNezhad/3x-ui-Sanaei-TelegramBot/main/main.py

wget https://raw.githubusercontent.com/MrAminiNezhad/3x-ui-Sanaei-TelegramBot/main/info.json

pkill -f "main.py"

nohup python3 main.py &
