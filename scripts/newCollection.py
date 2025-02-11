from web3 import Web3
import json
from Accounts import accounts,private_keys


# 连接节点（如Infura或本地节点）
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

# 检查连接
if w3.is_connected():
    print("Connected to Ethereum node")
else:
    print("Failed to connect")

# 获取账户和私钥
account = "0xa8e4C3b0264D54d6270ADCC58b759068B626A150"
private_key = "d6b11725f930f3905d9fabed40ecf26a34f8c4b85275d68e1cd874cf87f2f4c1"

#CB address
factory_contract_address = '0x061C644683961256BB06637Cd1e6FD867F0B3b11' 

# 读取 JSON 文件
with open('../ABIs/CB.json', 'r') as file:
    factory_contract_abi = json.load(file)
# 打印 ABI
#print(factory_contract_abi)

# 创建合约实例
factory_contract = w3.eth.contract(address=factory_contract_address, abi=factory_contract_abi)


# 构建交易
nonce = w3.eth.get_transaction_count(account)

#投票对象
collectionFac="0xB52e3942ce2a1B5ECe9F2Ae9A353FD7F6B3AB795"
importerAddr = "0xEa027DFaC014E764644c6c2D509783d66736F557"
amount = 10000000
transaction = factory_contract.functions.createCollection(collectionFac, importerAddr,amount).build_transaction({
    'chainId': 5777,  # ganache
    'gas': 16721975,
    'gasPrice': w3.to_wei('50', 'gwei'),
    'value': 0,
    'nonce': nonce,
})

# 签名交易
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# 发送交易
txn_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)

txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
print(f"Transaction receipt: {txn_receipt}")

# 假设工厂合约触发了一个 NewInstanceCreated 事件
event_signature = w3.keccak(text="logCollection(address,address,address,uint256)").hex()
# print(event_signature)

event_logs = txn_receipt['logs']

for log in event_logs:
    if log['topics'][0].hex() == event_signature:
        collection = log['topics'][1].hex()
        print(f"New Letter of Credit is deployed at: {w3.to_checksum_address(collection[-40:])}")
        break