#!/bin/bash

apt-get update
apt-get install -y python3

pip3 install python-telegram-bot==12.8.0

pip3 install persiantools

wget https://raw.githubusercontent.com/MrAminiNezhad/3x-ui-Sanaei-TelegramBot/main/main.py
