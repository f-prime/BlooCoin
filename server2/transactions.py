import mongo
import json

def transactions(obj, data):
    try:
        addr = str(data[u'addr'])
        pwd = str(data[u'pwd'])
    except KeyError:
        obj.send("Error")
        obj.close()
        return
    if mongo.db.addresses.find_one({"addr":addr, "pwd":pwd}):
        for x in mongo.db.transactions.find({"to":addr}):
            obj.send(json.dumps({"from":x['from'], "to":addr})+"\n")
        for x in mongo.db.transactions.find({"from":addr}):
            obj.send(json.dumps({"from":addr, "to":x['to']})+"\n")
        obj.close()
        return
