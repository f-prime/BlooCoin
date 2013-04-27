import socket
import hashlib
import json
import os
import random
import time

class BlooClient:
    def __init__(self):
        self.ip = "bloocoin.zapto.org"
        self.port = 3122
        self.type = "client"
        self.ver = "1.05"
        self.cmds = {
            "transactions": self.transactions,
            "addr": self.addr,
            "coins": self.coins,
            "send": self.sendcoin,
            "help": self.help,
        }
        self.update()
        return
    
    def main(self):
        while True:
            cmd = raw_input("BlooCoin> ")
            self.cmd = cmd
            try:
                self.cmds[cmd.split()[0]]()
                print ""
            except:
                continue
        return

    def _send_json(self, data, buff=1024):
        """ This function does most of the leg work for the script,
            since almost all functionality required by the client
            sends and receives some JSON data to/from the server.
        """
        s = socket.socket()
        s.settimeout(3)
        try:
            s.connect((self.ip, self.port))
        except IOError as e:
            print "[ ! ] Problem connecting to server: {0}".format(e)
            return
        if isinstance(data, dict):
            data = json.dumps(data)
        try:
            s.send(data)
        except IOError as e:
            print "[ ! ] Problem sending data to server: {0}".format(e)
            return
        reply = None
        try:
            reply = s.recv(buff)
        except IOError as e:
            print "[ ! ] Problem in recv(): {0}".format(e)
        return reply

    def transactions(self):
        data = self._send_json({
            "cmd": "transactions",
            "addr": self.addr_get(),
            "pwd":self.pwd_get()
        })
        if data:
            print data
        else:
            print "Something went wrong getting transactions! :("

    def addr(self):
        with open("bloostamp", 'rb') as f:
            print "Your BlooCoin address is:", f.read().split(":")[0]
        return
            
    def addr_get(self):
        with open("bloostamp", 'rb') as f:
            return f.read().split(":")[0]

    def pwd_get(self):
        with open("bloostamp", "rb") as f:
            return f.read().split(":")[1]
        
    def coins(self):
        data = self._send_json({
            "cmd": "my_coins",
            "addr": self.addr_get(),
            "pwd": self.pwd_get()
        })
        if data:
            print "You currently have", data, "coins."
        else:
            print "Something went wrong getting coin listings! :("
     
    def sendcoin(self):
        cmd = self.cmd.split()
        amount = cmd[1]
        to = cmd[2]
        addr = self.addr_get()
        pwd = self.pwd_get()
        data = self._send_json({
            "cmd": "send_coin",
            "amount": amount,
            "to": to,
            "addr": addr,
            "pwd": pwd
        })
        if data:
            print data
        else:
            print "Unable to send your coin! Uh oh! :("
    
    def register(self, addr, pwd):
        data = self._send_json({
            "cmd": "register",
            "addr": addr,
            "pwd": pwd
        })
        if data.strip() == "True":
            print "Registration successful! Your address is: {0}".format(addr)
        else:
            print "Registration failed! '{0}' :(".format(data)

    def help(self):
        print """
addr - Show your BlooCoin address.
coins - Shows amount of coins owned.
send <amount> <to> - Send coins to another bloocoin address.
transactions - Shows all transactions you have made.

To generate a new BlooCoin address simply delete your bloostamp file and relaunch bloocoin."""

    def update(self):
        data = self._send_json({
            "ver": self.ver,
            "cmd": "update",
            "type": self.type
        })
        if data[0] == "0":
            print "Your {0} is running the latest version.\n".format(self.type)
        elif data[0] == "1":
            print "A new version is available. It can be downloaded at:\nhttps://raw.github.com/Max00355/BlooCoin/master/bloocoin.py\n"
        elif data[0] == "2":
            print data[1:] + "\n"
        else:
            print "Unknown data returned from update: {0}".format(data)

if __name__ == "__main__":
    if not os.path.exists("bloostamp"):
        print "A bloostamp does not exist in this directory, generating one..."
        with open("bloostamp", 'w') as f:
            addr = ""
            for x in xrange(100):
                addr = addr + random.choice("abcdefghijklmnopqrstuvwxzyABCDEFGHIJKLMNOPQRSTUVWZYZ1234567890")
            for x in xrange(50):
                addr = hashlib.sha1(addr).hexdigest()
            key = ""
            for x in xrange(5000):
                key = key + random.choice("abcdefghijklmnopqrstuvwxzyABCDEFGHIJKLMNOPQRSTUVWZYZ1234567890")
            for x in xrange(1000):
                key = hashlib.sha1(key).hexdigest()
            f.write(addr + ":" + key + ":1")
            print "Generated bloostamp! Your BlooCoin address is", addr
            BlooClient().register(addr, key)
    with open("bloostamp", "r+") as f:   # Register old accounts properly. - Remove on next update.
        data = f.read().split(":")
        f.seek(0)
        if len(data) == 2:
            addr = data[0]
            key = data[1]
            BlooClient().register(addr, key)
            print "Your account has been registered with the new system."
            f.write(addr + ":" + key + ":1")
    BlooClient().main()
