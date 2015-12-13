import socket
import re
from threading import Timer
import sys
import os
import time
import datetime
from bs4 import UnicodeDammit
import requests
sys.dont_write_bytecode = True

HOST = "irc.twitch.tv"                                  # the Twitch IRC server
PORT = 6667                                             # always use port 6667!
NICK = "GarboBot"                                       # your Twitch username, lowercase
PASS = "oauth:avg7hkxg7cosq6io1s197z22drxzv7"           # your Twitch OAuth token
CHAN = "#stinkycheeseone890"                            # the channel you want to join
RATE = (100/30)                                         # messages per second

# --------------------------------------------- Start Twitch API ---------------------------------------------

root = 'https://api.twitch.tv/kraken/'


def _apiget(path, root=root):
    r = requests.get(root+path, timeout=4)
    r.raise_for_status()

    try:
        return r.json()
    except Exception as e:
        print(r.status_code, r.reason)
        print(e)


def get(path='', key=None):
    return _apiget(path) if not key else _apiget(path)[key]


def is_streaming(channel):
    return get('streams/%s' % channel, 'stream') is not None


def get_chatters(channel):
    r = requests.get('https://tmi.twitch.tv/group/user/%s/chatters' % channel, timeout=4)
    r.raise_for_status()
    return r.json()


def get_chatters_list(channel):
    ctrs = get_chatters(channel)
    return ctrs['chatters']['admins'] + ctrs['chatters']['global_mods'] + ctrs['chatters']['moderators'] + ctrs['chatters']['staff'] + ctrs['chatters']['viewers']


# --------------------------------------------- End Twitch API ---------------------------------------------

# --------------------------------------------- Start Global Variables  ---------------------------------------------
cdtest = 0
cduptime = 0
cdcommands = 0
cdgarbo = 0
cdtagface = 0
cdfaq = 0
cdmemes = 0
# --------------------------------------------- End Global Variables  ---------------------------------------------

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
                   '!memes': command_memes}
        if msg[0] in options:
            options[msg[0]]()

# --------------------------------------------- End Helper Functions -----------------------------------------------


# --------------------------------------------- Start Command Functions --------------------------------------------

def command_uptime():
    global cduptime
    if cduptime==0:
        send_message(CHAN, '420am69pm')
        cduptime=1
        def testchange():
            global cduptime
            cduptime=0
        t = Timer(30.0, testchange)
        t.start()

def command_commands():
    global cdcommands
    if cdcommands==0:
        send_message(CHAN, 'I am a meme bot! Here is a list of available commands : http://pastebin.com/KChvqDGW ')
        cdcommands=1
        def testchange():
            global cdcommands
            cdcommands=0
        t = Timer(30.0, testchange)
        t.start()

def command_garbo():
    global cdgarbo
    if cdgarbo==0:
        send_message(CHAN, 'Garbo Garbo Garbo Garbo Garbo Garbo Garbo Garbo Garbo Garbo Garbo Garbo ')
        cdgarbo=1
        def testchange():
            global cdgarbo
            cdgarbo=0
        t = Timer(30.0, testchange)
        t.start()

def command_tag():
    global cdtagface
    if cdtagface==0:
        send_message(CHAN, 'HungryTag')
        cdtagface=1
        def testchange():
            global cdtagface
            cdtagface=0
        t = Timer(30.0, testchange)
        t.start()

def command_faq():
    global cdfaq
    if cdfaq==0:
        send_message(CHAN, 'Kappa')
        cdfaq=1
        def testchange():
            global cdfaq
            cdfaq=0
        t = Timer(30.0, testchange)
        t.start()


def command_memes():
    global cdmemes
    if cdmemes==0:
        send_message(CHAN, 'Memes! https://rngmeme.com/')
        cdmemes=1
        def testchange():
            global cdmemes
            cdmemes=0
        t = Timer(30.0, testchange)
        t.start()


# --------------------------------------------- End Command Functions ----------------------------------------------

con = socket.socket()
con.connect((HOST, PORT))

send_pass(PASS)
send_nick(NICK)
join_channel(CHAN)

data = ""

while True:
    try:
        data = data+con.recv(1024).decode('UTF-8')
        data_split = re.split(r"[~\r\n]+", data)
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

                    print(sender + ": " + message)


    except socket.error:
        print("Socket died")

    except socket.timeout:
        print("Socket timeout")
