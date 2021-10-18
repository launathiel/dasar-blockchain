import hashlib
import json 

from time import time

import requests
from urllib.parse import urlparse

class Blockchain(object):
    difficulty_target = "1010"

    def hash_block(self, block):
        block_encoded = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_encoded).hexdigest()

    def __init__(self): #constructor
        self.nodes = set()
        self.chain = []
        self.current_transaction = []
        genesis_hash = self.hash_block("genesis_block")

        self.append_block(
            hash_of_previous_block = genesis_hash,
            nonce = self.proof_of_work(0, genesis_hash, [])
        )

    def add_node(self, address):
        parse_url = urlparse(address)
        self.nodes.add(parse_url.netloc)
        print(parse_url.netloc)

    def valid_chain(self, chain):
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]

            if block['hash_of_previous_block'] != self.hash_block(last_block):
                return False

            if not self.valid_proof(
                current_index,
                block['hash_of_previous_block'],
                block['transaction'],
                block['nonce']):
                return False

            last_block = block
            current_index += 1

        return True

    def update_blockchain(self):
        neighbours = self.nodes
        new_chain = None
        
        max_length = len(self.chain)

        for node in neighbours:
            response = requests.get(f'http://{node}/blockchain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

                if new_chain:
                    self.chain = new_chain
                    return True              
        return False      

    def proof_of_work(self, index, hash_of_previous_block, transaction):
        nonce = 0

        while self.valid_proof(index, hash_of_previous_block, transaction, nonce) is False:
            nonce += 1
        return nonce

    def valid_proof(self, index, hash_of_previous_block, transaction, nonce):
        content = f'{index}{hash_of_previous_block}{transaction}{nonce}'.encode()

        content_hash = hashlib.sha256(content).hexdigest()

        return content_hash[:len(self.difficulty_target)] == self.difficulty_target

    def append_block(self, nonce, hash_of_previous_block):
        block = {
            'index' : len(self.chain),
            'timestamp' : time(),
            'transaction' : self.current_transaction,
            'nonce' : nonce,
            'hash_of_previous_block' : hash_of_previous_block
        }

        self.current_transaction = []

        self.chain.append(block)
        return block

    def add_transaction(self, sender, recipient, amount):
        self.current_transaction.append({
            'sender' : sender,
            'amount' : amount,
            'recipient' : recipient
        })
        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]