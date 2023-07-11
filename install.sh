#!/bin/bash

apt-get update
apt-get install -y python3

apt install python3-pip

pip install python-telegram-bot==12.8.0

pip install persiantools

wget https://raw.githubusercontent.com/MrAminiNezhad/3x-ui-Sanaei-TelegramBot/main/main.py
