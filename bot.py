import socket
import re
from threading import Timer
import sys
import cfg
import requests
import cd

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
                   '!wr-k3': command_wr_k3,
                   '!wr-boshy': command_wr_b,
                   '!wr-nangtrue': command_wr_nangt,
                   '!wr-nangbad': command_wr_nangbad}
        if msg[0] in options:
            options[msg[0]]()


worldrekky = {'k3': 'Kamillia 3 Any% WR: 6h:20m:04s by Stinkycheeseone890',
              'boshy': 'I Wanna Be The Boshy Any% WR: 32m 24s by witwix',
              'nangtrue': 'NANG true end WR: 1h:38m:17s by Stinkycheeseone890',
              'nangbad': 'NANG bad end WR: 34m:27s by Maxinator235'}


# --------------------------------------------- End Helper Functions -----------------------------------------------


# --------------------------------------------- Start Command Functions --------------------------------------------
def command_wr_nangbad():
    if cd.cdwr == 0:
        send_message(cfg.CHAN, worldrekky.get('nangbad'))
        cd.cdwr = 1

        def testchange():
            cd.cdwr = 0

        t = Timer(10.0, testchange)
        t.start()


def command_wr_nangt():
    if cd.cdwr == 0:
        send_message(cfg.CHAN, worldrekky.get('nangtrue'))
        cd.cdwr = 1

        def testchange():
            cd.cdwr = 0

        t = Timer(10.0, testchange)
        t.start()


def command_wr_k3():
    if cd.cdwr == 0:
        send_message(cfg.CHAN, worldrekky.get('k3'))
        cd.cdwr = 1

        def testchange():
            cd.cdwr = 0

        t = Timer(10.0, testchange)
        t.start()


def command_wr_b():
    if cd.cdwr == 0:
        send_message(cfg.CHAN, worldrekky.get('boshy'))
        cd.cdwr = 1

        def testchange():
            cd.cdwr = 0

        t = Timer(10.0, testchange)
        t.start()


def command_uptime():
    if cd.cduptime == 0:
        send_message(cfg.CHAN, '420am69pm')
        cd.cduptime = 1

        def testchange():
            cd.cduptime = 0

        t = Timer(30.0, testchange)
        t.start()


def command_commands():
    if cd.cdcommands == 0:
        send_message(cfg.CHAN, 'I am a meme bot! Here is a list of available commands : http://pastebin.com/KChvqDGW ')
        cd.cdcommands = 1

        def testchange():
            cd.cdcommands = 0

        t = Timer(30.0, testchange)
        t.start()


def command_garbo():
    if cd.cdgarbo == 0:
        send_message(cfg.CHAN, 'Garbo Garbo Garbo Garbo Garbo Garbo Garbo Garbo Garbo Garbo Garbo Garbo ')
        cd.cdgarbo = 1

        def testchange():
            cd.cdgarbo = 0

        t = Timer(30.0, testchange)
        t.start()


def command_tag():
    if cd.cdtagface == 0:
        send_message(cfg.CHAN, 'HungryTag')
        cd.cdtagface = 1

        def testchange():
            cd.cdtagface = 0

        t = Timer(30.0, testchange)
        t.start()


def command_faq():
    if cd.cdfaq == 0:
        send_message(cfg.CHAN, 'Kappa')
        cd.cdfaq = 1

        def testchange():
            cd.cdfaq = 0

        t = Timer(30.0, testchange)
        t.start()


def command_memes():
    if cd.cdmemes == 0:
        send_message(cfg.CHAN, ' ˙͜ >˙ ‿☞')
        cd.cdmemes = 1

        def testchange():
            cd.cdmemes = 0

        t = Timer(30.0, testchange)
        t.start()


def command_kirbyskip():
    if cd.cdkirby == 0:
        send_message(cfg.CHAN, 'Go fuck yourself!!! 4Head')
        cd.cdkirby = 1

        def testchange():
            cd.cdkirby = 0

        t = Timer(30.0, testchange)
        t.start()


def command_uuptime():
    if cd.cduuptime == 0:
        r = requests.get('https://decapi.me/twitch/uptime.php?channel=stinkycheeseone890')
        send_message(cfg.CHAN, 'This channel has been live for: %s' % r.text)
        cd.cduuptime = 1

        def testchange():
            cd.cduuptime = 0

        t = Timer(30.0, testchange)
        t.start()


def command_important():
    if cd.cdimportant == 0:
        send_message(cfg.CHAN, 'b r e a k f a s t https://i.imgur.com/IjnhSOH.png')
        cd.cdimportant = 1

        def testchange():
            cd.cdimportant = 0

        t = Timer(30.0, testchange)
        t.start()


# --------------------------------------------- End Command Functions ----------------------------------------------

con = socket.socket()
con.connect((cfg.HOST, cfg.PORT))

send_pass(cfg.PASS)
send_nick(cfg.NICK)
join_channel(cfg.CHAN)

data = ""

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
                            send_message(cfg.CHAN, '/ban %s' % sender)
                            send_message(cfg.CHAN, 'Contact a mod if this ban was in error')

                    print(sender + ": " + message)
    except socket.error:
        print("Socket died")

    except socket.timeout:
        print("Socket timeout")
