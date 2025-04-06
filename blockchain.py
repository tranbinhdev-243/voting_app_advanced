import hashlib
import json
import os

class Block:
    def __init__(self, index, timestamp, voter_id, vote, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.voter_id = self.hash_voter(voter_id)
        self.vote = vote
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        content = str(self.index) + self.timestamp + self.voter_id + self.vote + self.previous_hash
        return hashlib.sha256(content.encode()).hexdigest()

    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "voter_id": self.voter_id,
            "vote": self.vote,
            "previous_hash": self.previous_hash,
            "hash": self.hash
        }

    @staticmethod
    def hash_voter(voter_id):
        return hashlib.sha256(voter_id.encode()).hexdigest()

class Blockchain:
    def __init__(self, storage_path="blockchain_data.json"):
        self.storage_path = storage_path
        if os.path.exists(self.storage_path):
            with open(self.storage_path, "r") as f:
                data = json.load(f)
                self.chain = [Block(**b) for b in data["chain"]]
                self.voted = set(data["voted"])
        else:
            self.chain = [self.create_genesis_block()]
            self.voted = set()
            self.save_chain()

    def create_genesis_block(self):
        return Block(0, "2025-01-01 00:00", "admin", "None", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block, voter_id):
        hashed_id = Block.hash_voter(voter_id)
        if hashed_id in self.voted:
            return False
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)
        self.voted.add(hashed_id)
        self.save_chain()
        return True

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            curr = self.chain[i]
            prev = self.chain[i - 1]
            if curr.hash != curr.calculate_hash() or curr.previous_hash != prev.hash:
                return False
        return True

    def save_chain(self):
        with open(self.storage_path, "w") as f:
            data = {
                "chain": [b.to_dict() for b in self.chain],
                "voted": list(self.voted)
            }
            json.dump(data, f, indent=4)