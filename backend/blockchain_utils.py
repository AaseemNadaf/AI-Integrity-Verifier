from web3 import Web3

GANACHE_URL = "http://127.0.0.1:8545"
CONTRACT_ADDRESS = "0x36DbA7F784d7782C08a09BcBa2E1371872aA6a10"

CONTRACT_ABI = [
    {
        "inputs": [
            {"internalType": "string", "name": "modelName", "type": "string"},
            {"internalType": "string", "name": "modelHash", "type": "string"}
        ],
        "name": "registerModel",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "string", "name": "modelName", "type": "string"},
            {"internalType": "string", "name": "modelHash", "type": "string"}
        ],
        "name": "verifyModel",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "string", "name": "modelName", "type": "string"}
        ],
        "name": "getLatestModelInfo",
        "outputs": [
            {"internalType": "string", "name": "name", "type": "string"},
            {"internalType": "string", "name": "hash", "type": "string"},
            {"internalType": "address", "name": "registeredBy", "type": "address"},
            {"internalType": "uint256", "name": "timestamp", "type": "uint256"},
            {"internalType": "uint256", "name": "version", "type": "uint256"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "string", "name": "modelName", "type": "string"},
            {"internalType": "uint256", "name": "versionIndex", "type": "uint256"}
        ],
        "name": "getModelVersion",
        "outputs": [
            {"internalType": "string", "name": "name", "type": "string"},
            {"internalType": "string", "name": "hash", "type": "string"},
            {"internalType": "address", "name": "registeredBy", "type": "address"},
            {"internalType": "uint256", "name": "timestamp", "type": "uint256"},
            {"internalType": "uint256", "name": "version", "type": "uint256"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "string", "name": "modelName", "type": "string"}
        ],
        "name": "getVersionCount",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "string", "name": "modelName", "type": "string"}
        ],
        "name": "isModelRegistered",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function"
    }
]

w3 = Web3(Web3.HTTPProvider(GANACHE_URL))
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)
default_account = w3.eth.accounts[0]

def is_connected():
    return w3.is_connected()

def register_model(model_name, model_hash):
    tx_hash = contract.functions.registerModel(model_name, model_hash).transact({
        "from": default_account,
        "gas": 300000
    })
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return receipt.transactionHash.hex()

def verify_model(model_name, model_hash):
    is_valid = contract.functions.verifyModel(model_name, model_hash).call({
        "from": default_account
    })
    contract.functions.verifyModel(model_name, model_hash).transact({
        "from": default_account,
        "gas": 300000
    })
    return is_valid

def get_model_info(model_name):
    name, hash_val, registered_by, timestamp, version = contract.functions.getLatestModelInfo(model_name).call()
    return {
        "name": name,
        "hash": hash_val,
        "registered_by": registered_by,
        "timestamp": timestamp,
        "version": version
    }

def get_version_count(model_name):
    return contract.functions.getVersionCount(model_name).call()

def get_model_version(model_name, version_index):
    name, hash_val, registered_by, timestamp, version = contract.functions.getModelVersion(model_name, version_index).call()
    return {
        "name": name,
        "hash": hash_val,
        "registered_by": registered_by,
        "timestamp": timestamp,
        "version": version
    }

def get_all_versions(model_name):
    count = get_version_count(model_name)
    versions = []
    for i in range(count):
        v = get_model_version(model_name, i)
        versions.append(v)
    return versions

def is_model_registered(model_name):
    return contract.functions.isModelRegistered(model_name).call()