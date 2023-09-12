# ربات تلگرامی مخصوص پنل سنایی
در حال حاضر ربات فقط میزان حجم باقی مانده کاربر را با استفاده از Email نمایش میدهد در پنل مقدار email به صورت 8to5wxh0 نمایش داده میشود و با ID متفاوت میباشد.<br>
به مرور زمان با توجه به حمایت شما قابلیت های ساخت اکانت ، حذف اکانت و... به آن افزوده میشود

# لیست امکانات ربات ورژن 1.3.0 
1- نمایش میزان ترافیک مصرفی <br> 
2- نمایش تاریخ انقضا اکانت <br>
3- نمایش میزان دانلود و اپلود به صورت جدا گانه<br>
4- نمایش میزان ترافیک باقی مانده <br>
5- قابلیت ارسال پیام همگانی ( فقط مدیر ربات میتوانید اقدام به ارسال پیام بکند ) <br>
6- قابلیت اتصال به چنیدن پنل به صورت همزمان <br>
7- قابلیت اد کردن چندین ادمین <br>

# پیش نمایش 
![Borzoo Demo](https://raw.githubusercontent.com/MrAminiNezhad/BorzooBot/main/demo.JPG)
# آموزش نصب
1- جهت نصب سریع دستور زیر را بزنید تا پیشنیاز های اسکریپت نصب شود.<br>
```
 bash <(curl -Ls https://raw.githubusercontent.com/MrAminiNezhad/BorzooBot/main/install.sh)
```
2- سپس با دستور زیر محتوای درون فایل را ویرایش نمایید <br>
```
nano info.json
```
3- جهت اجرای اسکریپت دستور زیر را بزنید <br>
```
nohup python3 main.py &
```
4- جهت خاموش کردن ربات میتوانید از دستور زیر استفاده بکنید <br>
```
pkill -f "main.py"
```
# آموزش تنظیمات مولتی پنل

1-برای تنظیمات مولتی پنل کافیت اول دستور خاموش کردن ربات را بزنید <br>
```
pkill -f "main.py"
```

2- سپس با دستور زیر فایل Info را ویرایش کنید <br>
```
nano info.json
```

3- محتوای فایل را به صورت زیر تغییر دهید ( میتوانید بی نهایت پنل اضافه بکنید فقط کافیست بخش مربوط به اطلاعات را کپی بکنید و در ادامه کد قرار بدید <br>
لطفا توجه داشته باشید که مقدار cookies_file و connection_name باید نسبت به شماره پنل ویرایش شود <br>
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
  "Support_text": "متن پشتیبانی شما",
  "welcome_text": "به ربات نمایش حجم خوش آمدید",
  "admin_id": 123456789
}

```

4- جهت اجرای اسکریپت دستور زیر را بزنید <br>
```
nohup python3 main.py &
```
# بروز رسانی ( بعد از بروز رسانی به ورزن 1.3.0 نیازمند وارد کردن مجدد اطلاعات پنل و ربات هستید )
1- جهت بروز رسانی از دستور زیر استفاده بکنید <br>
```
 bash <(curl -Ls https://raw.githubusercontent.com/MrAminiNezhad/BorzooBot/main/update.sh)
```
2- اطلاعات پنل را مجدد در فایل زیر وارد بکنید <br>
```
nano info.json
```
3- سپس با دستور زیر ربات را روشن بکنید <br>
```
nohup python3 main.py &
```
# حمایت از پروژه
جهت حمایت از پروژه و ارائه بروز رسانی های بیشتر از پروژه حمایت بکنید <br>
Trx Wallet: TQhwK6q94GgpUZSsHBjiUWc6xAHz5Df9mW
<br>
شماره کارت : <br>
50222910479892094<br>
به نام : پوریا امینی<br>

تلگرام جهت ارسال فیش و یا گذارش باگ ها <br>
t.me/MrAminiNezhad

