import mongo
from get_coin import difficulty
from hashlib import sha512

#{"cmd":"check", "winning_string":string, "winning_hash":hash, 'addr':addr}
def check(obj, data):
    try:
        winstr = str(data['winning_string'])
        winhash = str(data['winning_hash'])
        addr = str(data['addr'])
    except KeyError:
        obj.send("False")
        obj.close()
        return
    
    if not mongo.db.addresses.find_one({"addr":addr}):
        obj.send("False")
        obj.close()
        return

    if winhash == sha512(winstr).hexdigest() and not mongo.db.coins.find_one({"hash":winhash}) and winhash.startswith(difficulty() * "0") and mongo.db.addresses.find_one({"addr":addr}):
        obj.send("True")
        mongo.db.coins.insert({"hash":winhash, "addr":addr})
    else:
        obj.send("False")
    obj.close()
    return
    
    
