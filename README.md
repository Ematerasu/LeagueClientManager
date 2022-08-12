# League Client Manager v1.1

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

## How does it work?
The moment you click on your account in LCM, LeagueClient is running and then app takes your mouse and keyboard to log into client for you with credentials you just selected.
When you want to change account LCM closes every process related to League of Legends and then runs new one and logs automatically with new credentials.

## Version 1.1 Update:
* Option to add and delete accounts
* GUI overhaul, it's still in progress

## Important things!
After you click on account you want to play, **dont move your mouse**, because this app can type credentials in different place.
Let LCM do the work and when you are already logged in then you can take over again. Also don't close the app while playing, this will close all League related processes. This app doesn't use much resources while running, basically zero so you don't have to worry about your fps
