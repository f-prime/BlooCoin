import mongo

def my_coins(obj, data):
    try:
        addr = str(data[u'addr'])
        pwd = str(data[u'pwd'])
    except KeyError:
        obj.send("Error")
        obj.close()
        return
    if mongo.db.addresses.find_one({"addr":addr, "pwd":pwd}):
        coins = 0                                # I am sure there is a better way of doing this
        for x in mongo.db.coins.find({"addr":addr}):   # Finds all coins belonging to an address and increases coins by 1.
            coins += 1
        obj.send(str(coins))
        obj.close()
    else:
        obj.send("Key Error")
    return
