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
        self.cmds = {

            "addr":self.addr,
            "coins":self.coins,
            "send":self.sendcoin,
            "help":self.help,
            }
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
    
    def addr(self):
        with open("bloostamp", 'rb') as file:
            print "Your BlooCoin address is:", file.read().split(":")[0]
        return
            
    def addr_get(self):
        with open("bloostamp", 'rb') as file: # Check for file error.
            return file.read().split(":")[0]

    def pwd_get(self):
        with open("bloostamp", "rb") as file:
            return file.read().split(":")[1]
        
    def coins(self):
        s = socket.socket()
        s.settimeout(3)
        while True:
            try:
                s.connect((self.ip, self.port))
                break
            except:
                print "Server seems to be down... trying again in 10 seconds."
                time.sleep(10)
                continue
        s.send(json.dumps({ "cmd":"my_coins", "addr":self.addr_get() }))
        print "You currently have", s.recv(1024), "coins."
        s.close()
        return
     
    def sendcoin(self):
        s = socket.socket()
        s.settimeout(3)

        # Connect
        while True:
            try:
                s.connect((self.ip, self.port))
                break
            except:
                print "Server seems to be down... trying again in 10 seconds."
                time.sleep(10)

        # Send request.               
        cmd = self.cmd.split()
        amount = cmd[1]
        to = cmd[2]
        addr = self.addr_get()
        pwd = self.pwd_get()
        s.send(json.dumps({ "cmd":"send_coin", "amount":amount, "to":to, "addr":addr, "pwd":pwd }))

        # Get response
        try:
            data = s.recv(1024)
        except socket.timeout:
            print "Server is not responding."
            s.close()
            return
        if data:
            print data
        s.close()
        return
    
    def register(self, addr, pwd):
        s = socket.socket()
        while True:
            try:
                s.connect((self.ip, self.port))
                break
            except:
                print "Server seems to be down... trying again in 10 seconds."
                time.sleep(10)
        s.send(json.dumps({ "cmd":"register", "addr":addr, "pwd":pwd }))
        s.settimeout(3)
        try:
            check = s.recv(1024)
        except socket.timeout:
            print "Server is not responding."
            s.close()
            return
        if not check == "True":
            print check
            s.close()
            return
        s.close()
        return

    def help(self):
        print """
addr - Show your BlooCoin address.
coins - Shows amount of coins owned.
send <amount> <to> - Send coins to another bloocoin address.
To generate a new BlooCoin address simply delete your bloostamp file and relaunch bloocoin."""

if __name__ == "__main__":
    if not os.path.exists("bloostamp"):
        print "A bloostamp does not exist in this directory, generating one..."
        with open("bloostamp", 'w') as file:
            addr = ""
            for x in range(100):
                addr = addr + random.choice("abcdefghijklmnopqrstuvwxzyABCDEFGHIJKLMNOPQRSTUVWZYZ1234567890")
            for x in range(50):
                addr = hashlib.sha1(addr).hexdigest()
            key = ""
            for x in range(5000):
                key = key + random.choice("abcdefghijklmnopqrstuvwxzyABCDEFGHIJKLMNOPQRSTUVWZYZ1234567890")
            for x in range(1000):
                key = hashlib.sha1(key).hexdigest()
            file.write(addr + ":" + key + ":1")
            print "Generated bloostamp! Your BlooCoin address is", addr
            BlooClient().register(addr, key)
    with open("bloostamp", "r+") as file: # Register old accounts properly.
        data = file.read().split(":")
        file.seek(0)
        if len(data) == 2:
            addr = data[0]
            key = data[1]
            BlooClient().register(addr, key)
            print "Your account has been registered with the new system."
            file.write(addr + ":" + key + ":" + ":1")
    BlooClient().main()
