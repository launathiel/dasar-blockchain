from flask.json import jsonify
from blockchain import Blockchain
from uuid import uuid4
from flask.globals import request

node_identifier = str(uuid4()).replace('-', "")

blockchain = Blockchain()

def full_chain():
    response = {
        'chain' : blockchain.chain,
        'length' : len(blockchain.chain)
    }
    return jsonify(response), 200

def mine_block():
    blockchain.add_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1
    )

    last_block_hash = blockchain.hash_block(blockchain.last_block)

    index = len(blockchain.chain)
    nonce = blockchain.proof_of_work(index, last_block_hash, blockchain.current_transaction)

    block = blockchain.append_block(nonce, last_block_hash)

    response = {
        'message' : "block baru telah ditambahkan (mined)",
        'index' : block['index'],
        'hash_of_previous_block': block['hash_of_previous_block'],
        'nonce': block['nonce'],
        'transaction': block['transaction']
    }

    return jsonify(response), 200

def new_transaction():
    values = request.get_json()

    required_fields = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required_fields):
        return ('Missing fields!', 400)
    
    index = blockchain.add_transaction(
        values['sender'],
        values['recipient'],
        values['amount']
    )

    response = {'message' : f'Transaksi akan ditambahkan ke blok {index}'}
    return(jsonify(response), 201)

def add_nodes():
    values = request.get_json()
    nodes = values.get('nodes')

    if nodes is None:
        return "Error, missing node(s) info", 400

    for node in nodes:
        blockchain.add_node(node)
    
    response = {
        'message' : "Node baru telah ditambahkan",
        'nodes' : list(blockchain.nodes)
    }

    return jsonify(response), 200

def sync():
    updated = blockchain.update_blockchain()
    if updated:
        response = {
            'message' : "Blockchain telah diupdate dengan data terbaru",
            'blockchain' : blockchain.chain
        }
    else:
        response = {
            'message' : "Blockchain telah menggunakan data paling baru",
            'blockchain' : blockchain.chain
        }
    
    return jsonify(response), 200