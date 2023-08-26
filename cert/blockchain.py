# BLOCK CHAIN CORE
# DEVELOP BY Pham Van Minh - Steam - K22 - BDU

from hashlib import sha256
from datetime import datetime
from Crypto.PublicKey import RSA
from hashlib import sha512

import json

def write_data(data):
    with open("cert/ledger.json", "w", encoding='utf-8') as f:
        json.dump(data,f, indent=4)

def updatehash(*args):
    hashing_text = ""
    h = sha256()
    for arg in args:
        hashing_text+=str(arg)
    h.update(hashing_text.encode('utf-8'))
    return h.hexdigest()

class Block():
    id = None
    data = None
    hash = None
    nonce = 0
    previous_hash = "0"*64
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    def __init__(self, data):
        self.data = data
    
    def hash(self):
        return updatehash(self.previous_hash,
                            self.id,
                            self.data,
                            self.timestamp,
                            self.nonce,
        )

def add_block(data, block):
    block_dict = {
        "id": block.id,
        "timestamp": block.timestamp,
        "data": block.data,
        "hash": block.hash(),
        "previous_hash":block.previous_hash,
        "nonce":block.nonce
    }
    chain = data["chain"]

    chain.append(block_dict)
    write_data(data)

def mine(data, block):
    chain = data["chain"]
    num = len(chain)+1
    block.id = num
    try:
        block.previous_hash = chain[-1]["hash"]
    except IndexError:
        pass
    
    while True:
        if block.hash()[:4]=="0"*4:
            add_block(data, block)
            break
        else:
            block.nonce +=1

def check_block_isValid(filepath, id, e_key, n_key):
    file = open(filepath, "r", encoding='utf-8')
    data = json.load(file)
    chain = data["chain"]
    index = 0
    for i in chain:
        if i["id"]==id:
            index = chain.index(i)
    check_block = chain[index]
    _hash = updatehash(check_block['previous_hash'],
                            check_block['id'],
                            check_block['data'],
                            check_block['timestamp'],
                            check_block['nonce'])
    print(check_block["data"])
    
    if _hash != check_block["hash"]:
        return False
    if check_block['previous_hash'] != chain[index-1]["hash"]:
        return False
    
    data_for_sign = bytes(check_block["data"]["student_name"]+check_block["data"]["student_code"]
                            +check_block["data"]["teacher_name"]+check_block["data"]["teacher_id"]
                            +check_block["data"]["course_name"]+check_block["data"]["mark"]
                            +check_block["data"]["date"], 'utf-8')
    sign_hash = int.from_bytes(sha512(data_for_sign).digest(), byteorder='big')
    hashFromSignature = pow(check_block["data"]["signature"], int(e_key, 16), int(n_key, 16))
    
    if sign_hash != hashFromSignature:
        print("sign invalid")
        return False
    
    return True

def check_chain_isValid(filepath, data):
    file = open(filepath, "r", encoding='utf-8')
    data = json.load(file)
    chain = data["chain"]
    for i in range(1, len(chain)):
        _previous = chain[i]["previous_hash"]
        _current = updatehash(chain[i-1]['previous_hash'],
                            chain[i-1]['id'],
                            chain[i-1]['data'],
                            chain[i-1]['timestamp'],
                            chain[i-1]['nonce'])
        if _previous != _current or _current[:4] != "0"*4:
            return False
        if i==len(chain)-1:
            _current = updatehash(chain[i]['previous_hash'],
                            chain[i]['id'],
                            chain[i]['data'],
                            chain[i]['timestamp'],
                            chain[i]['nonce'])
            if _current != chain[i]["hash"] or _current[:4]!="0"*4:
                return False
    return True

def get_data(filepath):
    file = open(filepath, "r", encoding='utf-8')
    data = json.load(file)
    if len(data["chain"])==0:
        mine(data,Block("The First Block Of System"))
    return data

def get_cert_list_by_student_code(filepath, student_code):
    file = open(filepath, "r", encoding='utf-8')
    data = json.load(file)

    list_available_block_id = []

    chain = data["chain"]

    for block in chain:
        if "student_code" in block["data"]:
            if block["data"]["student_code"] == student_code:
                list_available_block_id.append(block["id"])
        else:
            continue

    for block2 in chain:
        if "target_block_id" in block2["data"] and block2["data"]["target_block_id"] in list_available_block_id:
            if block2["data"]["method"] == "delete":
                list_available_block_id.remove(block2["data"]["target_block_id"])
            if block2["data"]["method"] == "update":
                list_available_block_id.remove(block2["data"]["target_block_id"])
                list_available_block_id.append(block2["data"]["new_block_id"])

    list_cert_data = []

    for id in list_available_block_id:
        for block3 in chain:
            if block3["id"]==id:
                list_cert_data.append(block3)
    print('-'*5)
    print(list_cert_data)
    return list_cert_data

def get_cert_list_by_teacher_id(filepath, teacher_id):
    file = open(filepath, "r", encoding='utf-8')
    data = json.load(file)

    list_available_block_id = []

    chain = data["chain"]

    for block in chain:
        if "student_code" in block["data"]:
            if block["data"]["teacher_id"] == teacher_id:
                list_available_block_id.append(block["id"])
        else:
            continue

    for block2 in chain:
        if "target_block_id" in block2["data"] and block2["data"]["target_block_id"] in list_available_block_id:
            if block2["data"]["method"] == "delete":
                list_available_block_id.remove(block2["data"]["target_block_id"])
            if block2["data"]["method"] == "update":
                list_available_block_id.remove(block2["data"]["target_block_id"])
                list_available_block_id.append(block2["data"]["new_block_id"])

    list_cert_data = []

    for id in list_available_block_id:
        for block3 in chain:
            if block3["id"]==id:
                list_cert_data.append(block3)
    print('-'*5)
    print(list_cert_data)
    return list_cert_data

def get_cert_by_id(filepath, id):
    file = open(filepath, "r", encoding='utf-8')
    data = json.load(file)
    chain = data["chain"]
    result = {}
    for block in chain:
        if block["id"]==id:
            result = block["data"]
            return result
            


if __name__ == "__main__":
    print(get_cert_list_by_student_code("ledger.json", "19050012"))