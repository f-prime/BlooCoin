import mongo

def send_coin(obj, data):
    #{"cmd":'send_coin', 'amount':_, 'to':addr, 'addr':addr}
    try:
        amount = int(data[u'amount'])
        to = str(data[u'to'])
        addr = str(data[u'addr'])
        pwd = str(data[u'pwd'])
    except:
        obj.send("Error")
        obj.close()
        return
                    
    if mongo.db.addresses.find_one({"addr":addr, "pwd":pwd}) and  mongo.db.addresses.find_one({"addr":addr}): #All conditions
        if amount <= 0: #checking amounts
            obj.send("Amount can not be zero")
            obj.close()
            return

        coins = 0
        for x in mongo.db.coins.find({"addr":addr}):
            coins += 1
        if coins >= amount:
            for x in xrange(0, amount):
                before = mongo.db.coins.find_one({"addr":addr})
                before['addr'] = to
                mongo.db.coins.update({'addr':addr}, before)
            mongo.db.transactions.insert({"to":to, "from":addr, "amount":amount})     
            obj.send("Transaction Successful!")
            obj.close()
            return
        else:
            obj.send("You don't have enough coins")
            obj.close()
            return
    else:
        obj.send("Error")
        obj.close()
    return
