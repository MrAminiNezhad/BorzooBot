<div align="center">
برای توضیحات <a href="https://github.com/MrAminiNezhad/tcp_optimizer_hybla/blob/main/README-fa.md"> فارسی اینجا بزنید </a>
</div>
<br><br>

# Telegram bot for the  <a href="https://github.com/MrAminiNezhad/tcp_optimizer_hybla/blob/main/README-fa.md"> MHSanaei </a> panel
Currently, the robot only displays the amount of the user's remaining volume using Email. In the panel, the email value is displayed as 8to5wxh0 and is different from the ID.<br>
Over time, according to your support, the capabilities of creating an account, deleting an account, etc. will be added to it

# List of robot features version 1.3.0
1- Display the amount of consumed traffic
2- Display account expiration date
3- Display the amount of download and upload separately<br>
4- Display the amount of remaining traffic
5- The ability to send public messages (only the bot manager can send messages) <br>
6- The ability to connect to pick the panel at the same time <br>
7- The ability to add several admins

# Preview
![Borzoo Demo](https://raw.githubusercontent.com/MrAminiNezhad/BorzooBot/main/demo.JPG)
# learn inistallation
1- For quick installation, type the following command to install the script prerequisites.<br>
```
  bash <(curl -Ls https://raw.githubusercontent.com/MrAminiNezhad/BorzooBot/main/install.sh)
```
2- Then edit the contents of the file with the command below
```
nano info.json
```
3- To run the script, press <br>
```
nohup python3 main.py &
```
4- You can use the following command to turn off the robot
```
pkill -f "main.py"
```
# Teaching multi-panel settings

1- For multi-panel settings, just press the command to turn off the robot
```
pkill -f "main.py"
```

2- Then edit the Info file with the command below
```
nano info.json
```

3- Change the content of the file as follows (you can add infinite panels, just copy the relevant section of the information and put the following code <br>
Please note that the value of cookies_file and connection_name should be edited according to the panel number <br>
```
{
   "TOKEN": "Your_token",
   "panels": [
     {
       "panel_url": "https://panel_address:port",
       "panel_user": "your_user",
       "panel_pass": "your_password",
       "cookies_file": "panel1.txt",
       "connection_name": "sv1"
     },
     {
       "panel_url": "https://panel_address:port",
       "panel_user": "your_user",
       "panel_pass": "your_password",
       "cookies_file": "panel2.txt",
       "connection_name": "sv2"
     }
   ],
   "Support_text": "Your support text",
   "welcome_text": "Welcome to the volume display bot",
   "admin_id": 123456789
}

```

4- To execute the script, press <br>
```
nohup python3 main.py &
```
# Update (after updating to version 1.3.0, you need to re-enter panel and robot information)
1- Use the following command to update
```
  bash <(curl -Ls https://raw.githubusercontent.com/MrAminiNezhad/BorzooBot/main/update.sh)
```
2- Re-enter the panel information in the following file <br>
```
nano info.json
```
3- Then turn on the robot with the command below
```
nohup python3 main.py &
```
# Support the project
Support the project to support the project and provide more updates
Trx Wallet: TQhwK6q94GgpUZSsHBjiUWc6xAHz5Df9mW
