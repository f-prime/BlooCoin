import socket
import hashlib
import json
import os
import random
import time

class BlooClient:
    def __init__(self):
        self.ip = ""
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
            except:
                continue
    def addr(self):
        with open("bloostamp", 'rb') as file:
            print "Your BlooCoin address is:", file.read().split(":")[0]
    def addr_get(self):
        with open("bloostamp", 'rb') as file:
            return file.read().split(":")[0]
    def coins(self):
        s = socket.socket()
        while True:
            try:
                s.connect((self.ip, self.port))
                break
            except:
                print "Server seems to be down... trying again in 10 seconds."
                time.sleep(10)
        s.send(json.dumps({"cmd":"my_coins", "addr":self.addr_get()}))
        print "You currently have", s.recv(1024), "coins."
        s.close()
     
    def sendcoin(self):
        s = socket.socket()
        while True:
            try:
                s.connect((self.ip, self.port))
                break
            except:
                print "Server seems to be down... trying again in 10 seconds."
                time.sleep(10)
        cmd = self.cmd.split()
        amount = cmd[1]
        to = cmd[2]
        addr = self.addr_get()
        s.send(json.dumps({"cmd":"send_coin", "amount":int(amount), "to":to, "addr":addr}))
        data = s.recv(1024)
        if data:
            print data
        s.close()
    
    def register(self, addr, pwd):
        s = socket.socket()
        while True:
            try:
                s.connect((self.ip, self.port))
                break
            except:
                print "Server seems to be down... trying again in 10 seconds."
                time.sleep(10)
        s.send(json.dumps({"cmd":"register", "addr":addr, "pwd":pwd}))
        check = s.recv(1024)
        if check == "Fasle":
            print "There was an error witht the registeration of your client, please delete your bloostamp file and relaunch"
            exit()
        s.close()

    def help(self):
        print """

        addr - Show your BlooCoin address.
        coins - Shows amount of coins owned.
        send <amount> <to> - Send coins to another bloocoin address.
    
        To generate a new BlooCoin address simply delete your bloostamp file and relaunch bloocoin.

        """


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
            file.write(addr+":"+key)
            print "Generated bloostamp! Your BlooCoin address is", addr
            BlooClient().register(addr, key)
    BlooClient().main()
