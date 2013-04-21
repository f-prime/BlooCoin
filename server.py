import socket
import hashlib
import json
import threading
import pymongo
import random
import sys
import time

class BlooServer:
    def __init__(self):
        self.port = 3122
        self.db = pymongo.MongoClient('localhost', 27017).bloocoin
        self.cmds = {
            
            "register":self.register, # Clients
            "get_coin":self.get_coin, # Miners
            "send_coin":self.send_coin, # Clients
            "my_coins":self.my_coins, # Clients
            "check":self.check, #Checks works (Miners)
        }

    def main(self):
        sock = socket.socket()
        while True:
            try:
                sock.bind(('0.0.0.0', self.port))
                break
            except:
                print "Address already in use... trying again."
                time.sleep(2)
                continue
        sock.listen(5)
        self.generate_coin_work()
        while True:
            #{'cmd':'send_coin', 'addr':'users_addr', 'to':'to_addr', 'amount':5}
            obj, conn = sock.accept()
            try:
                cmd = json.loads(obj.recv(1024))
            except:
                continue
            print conn[0], str(cmd)
            if str(cmd['cmd']) not in self.cmds:
                continue
            threading.Thread(target=self.cmds[str(cmd['cmd'])], args=(cmd, obj)).start()
    
    def difficulty(self):
        
        return self.db.coins.count() / 1000 + 7
        

    def get_coin(self, cmd, obj): #Miners only
        current_coin = self.current_coin
        current_coin['start_string'] = self.start_string()
        obj.send(json.dumps(current_coin))
        obj.close()
    
    def register(self, cmd, obj):    
        addr = str(cmd['addr'])
        pwd = str(cmd['pwd'])
        if not self.db.addresses.find_one({"addr":addr}) and not self.addresses.find({"pwd":pwd}):
            self.db.addresses.insert({"addr":addr, "pwd":pwd})
        else:
            obj.send("False")
        obj.close()

    def send_coin(self, cmd, obj): #Client only
        #{"cmd":'send_coin', 'amount':_, 'to':addr, 'addr':addr}
        amount = int(cmd[u'amount'])
        to = str(cmd[u'to'])
        addr = str(cmd[u'addr'])
        check = 0
        for x in self.db.coins.find({"amount":addr}):
            check += 1
        if check <= amount:
            if not self.db.addresses.find_one({"addr":to}):
                obj.send("Address does not exist")
            elif amount == 0:
                obj.send("You can not send 0 bloocoins")
            else:
                for x in range(amount):
                    before = self.db.coins.find_one({"addr":addr})
                    before['addr'] = to
                    self.db.coins.update({"addr":addr}, before)
                obj.send("Transaction successful.")
            
        else:
            obj.send("You don't have enough coins.")
        obj.close()
    def my_coins(self, cmd, obj):
        addr = str(cmd['addr'])
        try:
            d = 0
            for x in self.db.coins.find({"addr":addr}):
                d += 1
            obj.send(str(d))
        except Exception, error:
            print error
        obj.close()
    
    def check(self, cmd, obj): #Miners only
        #{"cmd":"check", "winning_string":string, "winning_hash":hash, 'addr':addr}
        winstr = str(cmd['winning_string'])
        winhash = str(cmd['winning_hash'])
        addr = str(cmd['addr'])
        if hashlib.sha512(winstr).hexdigest() == winhash and not self.db.coins.find_one({"hash":winhash}):
            obj.send("True")
            self.generate_coin_work()
            self.db.coins.insert({"hash":winhash, "addr":addr})
        else:
            obj.send("False")
        obj.close()

    def generate_coin_work(self):
        id = ""
        for x in range(5):
            id = id + random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWZYZ1234567890")
        difficulty = self.difficulty()
        self.current_coin = {"id":id, "difficulty":difficulty}
    
    def start_string(self):
        start_string = ""
        for x in range(5):
            start_string = start_string + random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWZYZ1234567890")
        return start_string

if __name__ == "__main__":
    BlooServer().main()
