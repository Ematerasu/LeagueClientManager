# League Client Manager (obsolete, will create new one from scratch)

# IMPORTANT December 2022
League client has been updated, another option to log in was introduced and LCM right now doesn't work properly, I know how to fix that but I'm too busy with work and another project so right now this manager isn't fully operable. Language change still work
---------
<p align="center">
  <img src="https://i.imgur.com/iaJR4mC.png">
</p>

## What is it?
App that automates logging in League of Legends client. Especially useful when changing accounts.
Log in only with one click instead of typing your username and password

## Why?
I use a lot of different accounts, since I'm in Europe I play on two servers and often changing accounts takes some time. Also I have to remember all of the login/password
combinations so this app is quite useful for me. Hopefully it will be useful for someone else.

## What I used to create this app
* Python:
    * pyautogui
    * PySide6

## How to run this app?
Download from my google disc: https://drive.google.com/file/d/1tIxCJ_UnT1H_QKI_Ieqlic7tp5DA2L_I/view?usp=sharing, unzip and run LCM.exe (make shortcut on Desktop or anywhere you want).

When running first time it will automatically locate League of Legends on your computer.

## How to run locally with python
I intend to make an exe file from this. But if you clone this repo you need to install the requirements with
```
pip install -r requirements.txt
```

And then you can run from src directory
```
python main.py
```

That's all :)

## How does it work?
The moment you click on your account in LCM, LeagueClient is running and then app takes your mouse and keyboard to log into client for you with credentials you just selected.
When you want to change account LCM closes every process related to League of Legends and then runs new one and logs automatically with new credentials.

## Version 1.2 Update:
* Option to add and delete accounts
* GUI overhaul, it's still in progress
* Change language of the client (Any language supported by League of Legends)
* Set path to 'Riot Games' directory

## Important things!
After you click on account you want to play, **dont move your mouse**, because this app can type credentials in different place.
Let LCM do the work and when you are already logged in then you can take over again. Also don't close the app while playing, this will close all League related processes. This app doesn't use much resources while running, basically zero so you don't have to worry about your fps
