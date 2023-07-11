#!/bin/bash

apt-get update
apt-get install -y python3

pip3 install python-telegram-bot==12.8.0

pip3 install persiantools

wget https://github.com/MrAminiNezhad/3x-ui-Sanaei-TelegramBot -P /root
