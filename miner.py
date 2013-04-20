import socket
import hashlib
import json
import time
import multiprocess
import sys

class BlooMiner:
    def __init__(self):
        self.ip = "bloocoin.zapto.org"
        self.port = 3122
        self.addr = sys.argv[2]
    def main(self):
        while True:
            self.continue_mining = True
            problem = self.get_coin()
            threading.Thread(target=self.check_coin).start()
            print problem
            difficulty = problem['difficulty']
            start_string = str(problem['start_string'])
            num = 0
            #hashes = 0
            #khps = time.time()
            while self.continue_mining:
                test = hashlib.sha512(start_string+str(num)).hexdigest()
                #hashes += 1
                #if time.time() - 1 >= khps:
                    #print str(hashes)+" KHps"
                   # hashes = 0
                  #  khps = time.time()
                if test.startswith("0"*difficulty):
                    print test, "possible solution"
                    self.send_work(start_string+str(num), test)
                    break
                else:
                    num += 1
    def check_coin(self):
        while True:
            current = self.get_coin()
            while True:
                if self.get_coin()['id'] == current['id']:
                    time.sleep(60)
                    continue
                else:
                    self.continue_mining = False
                    break

    def get_coin(self):
        s = socket.socket()
        try:
            s.connect((self.ip, self.port))
        except:
            s.close()
            time.sleep(10)
            self.get_coin()
        s.send(json.dumps({"cmd":"get_coin"}))
        data = json.loads(s.recv(1024))
        s.close()
        return data
    
    def send_work(self, string, hash):
        s = socket.socket()
        try:
            s.connect((self.ip, self.port))
        except:
            s.close()
            time.sleep(10)
            self.send_work(string, hash)
        s.send(json.dumps({"cmd":"check", "winning_string":string, "winning_hash":hash, "addr":self.addr}))
        result = s.recv(1024)
        if result == "True":
            print "Winning solution found!"
        else:
            print "Not a winning solution"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: python miner.py <threads> <bloocoin address>"
        exit()
    b = BlooMiner()
    for x in range(int(sys.argv[1])):
        multiprocessing.Process(target=b.main).start()
        time.sleep(1)
