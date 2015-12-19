#!/usr/bin/python3.5
import cd
import cfg
import re
import requests
import socket
import sys
from threading import Timer
import spl
import os
import time
import datetime
import json

sys.dont_write_bytecode = True


# ---------------------------------- Start Functions ----------------------------------------------------



def send_pong(msg):
    con.send(bytes('PONG %s\r\n' % msg, 'UTF-8'))


def send_message(chan, msg):
    con.send(bytes('PRIVMSG %s :%s\r\n' % (chan, msg), 'UTF-8'))



def send_nick(nick):
    con.send(bytes('NICK %s\r\n' % nick, 'UTF-8'))


def send_pass(password):
    con.send(bytes('PASS %s\r\n' % password, 'UTF-8'))


def join_channel(chan):
    con.send(bytes('JOIN %s\r\n' % chan, 'UTF-8'))


def part_channel(chan):
    con.send(bytes('PART %s\r\n' % chan, 'UTF-8'))


# --------------------------------------------- End Functions ------------------------------------------------------


# --------------------------------------------- Start Helper Functions ---------------------------------------------
def get_sender(msg):
    result = ""
    for char in msg:
        if char == "!":
            break
        if char != ":":
            result += char
    return result


def get_message(msg):
    result = ""
    i = 3
    length = len(msg)
    while i < length:
        result += msg[i] + " "
        i += 1
    result = result.lstrip(':')
    return result


def parse_message(msg):
    if len(msg) >= 1:
        msg = msg.split(' ')
        options = {'!uptime': command_uptime,
                   '!commands': command_commands,
                   '!garbo': command_garbo,
                   '!tag': command_tag,
                   '!faq': command_faq,
                   '!memes': command_memes,
                   '!kirbyskip': command_kirbyskip,
                   '!uuptime': command_uuptime,
                   '!important': command_important,
                   '!k3': command_wr_k3,
                   '!boshy': command_wr_b,
                   '!nangtrue': command_wr_nangt,
                   '!nangbad': command_wr_nangbad
                   '!wr': command_wr}
        if msg[0] in options:
            options[msg[0]]()


# --------------------------------------------- End Helper Functions -----------------------------------------------

worldrekky = {'k3': 'Kamillia 3 Any% WR: 6h:20m:04s by Stinkycheeseone890',
              'boshy': 'I Wanna Be The Boshy Any% WR: 32m 24s by witwix',
              'nangtrue': 'NANG true end WR: 1h:38m:17s by Stinkycheeseone890',
              'nangbad': 'NANG bad end WR: 34m:27s by Maxinator235'}


# --------------------------------------------- Start Command Functions --------------------------------------------


def command_wr_nangbad():
    if cd.cdwr == 0:
        send_message(cfg.CHAN, worldrekky.get('nangbad'))
        cd.cdwr = 1

        def testchange():
            cd.cdwr = 0

        t = Timer(10.0, testchange)
        t.start()

def command_wr(msg):
    if cd.cdwr==0:
        if len(msg)>=2:
            game=msg[1]
            r=requests.get('http://www.speedrun.com/api/v1/games?name=%s' % game)
            rjs=json.loads(r.text)
            try:
                rjs['data'][0]['names']['international']
            except:
                send_message(cfg.CHAN, 'No game found.')
                return None
            gamename=rjs['data'][0]['names']['international']
            category=rjs['data'][0]['links'][4]['uri']
            catlink=requests.get(category)
            cjs=json.loads(catlink.text)
            try:
                cjs['data'][0]['name']
            except:
                send_message(cfg.CHAN, 'No game found.')
                return(None)
            catname=cjs['data'][0]['name']
            records=cjs['data'][0]['links'][3]['uri']
            reclink=requests.get(records)
            recjs=json.loads(reclink.text)
            try:
                recjs['data'][0]['runs'][0]['run']
            except:
                send_message(cfg.CHAN, 'No runs found for %s.' gamename)
                return(None)
            wr=recjs['data'][0]['runs'][0]['run']
            time=wr['times']['primary_t']
            timename=str(datetime.timedelta(seconds=time))
            playerlink=wr['players'][0]['uri']
            player=requests.get(playerlink)
            pjs=json.loads(player.text)
            playername=pjs['data']['names']['international']
            send_message(cfg.CHAN, 'The record in %s %s is held by %s with %s' % (gamename, catname, playername, timename))
        else:
            send_message(cfg.CHAN, 'Specify a game.')
        cd.cdwr=1
        def testchange():
            cd.cdwr = 0

        t = Timer(10.0, testchange)
        t.start()



# --------------------------------------------- End Command Functions ----------------------------------------------

con = socket.socket()
con.connect((cfg.HOST, cfg.PORT))

send_pass(cfg.PASS)
send_nick(cfg.NICK)
join_channel(cfg.CHAN)

data = ""

logpath = 'C:/Users/NovaMoon/PycharmProjects/TwitchBot/'
if not os.path.isfile(logpath + "log.txt"):
    print("Creating log file for" + cfg.CHAN)
    if not os.path.isdir(logpath): os.makedirs(logpath)


def formatdate():
    now = datetime.date.today()
    return "[" + " ".join([now.strftime("%A")[0:3], now.strftime("%B")[0:3], now.strftime("%d"),
                           datetime.datetime.now().strftime("%H:%M:%S"), time.tzname[0], now.strftime("%Y")]) + "]"


now = formatdate()

while True:
    try:
        data = data + con.recv(1024).decode('UTF-8')
        data_split = re.split(r"[\r\n]+", data)
        data = data_split.pop()
        for line in data_split:
            line = str.rstrip(line)
            line = str.split(line)

            if len(line) >= 1:
                if line[0] == 'PING':
                    send_pong(line[1])

                if line[1] == 'PRIVMSG':
                    sender = get_sender(line[0])
                    message = get_message(line)
                    parse_message(message)
                    for word in cfg.PATT:
                        if word in message:
                            send_message(cfg.CHAN, '/ban  %s ' % sender)
                            send_message(cfg.CHAN, 'banned for being a shithead 4Head')
                    for spoiler in spl.SPLR:
                        if spoiler in message:
                            send_message(cfg.CHAN, '/timeout %s' % sender)
                            send_message(cfg.CHAN, 'No Star Wars spoilers allowed.')
                    print(sender + ": " + message)

                    with open(logpath + 'log.txt', 'a+') as f:
                        f.write('%s %s: %s\n"' % (now, sender, message))





    except socket.error:
        print("Socket died")

    except socket.timeout:
        print("Socket timeout")
