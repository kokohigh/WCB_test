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

#WCB address
factory_contract_address = '0xf13e7a8ADde96f8FFEF2b6258833D48eD9D78B8b' 

# 读取 JSON 文件
with open('../ABIs/WCB.json', 'r') as file:
    factory_contract_abi = json.load(file)
# 打印 ABI
#print(factory_contract_abi)

# 创建合约实例
factory_contract = w3.eth.contract(address=factory_contract_address, abi=factory_contract_abi)


# 获取账户和私钥
account = "0xa8e4C3b0264D54d6270ADCC58b759068B626A150"
private_key = "d6b11725f930f3905d9fabed40ecf26a34f8c4b85275d68e1cd874cf87f2f4c1"
# acct1 = w3.eth.accounts[0]
# print(acct1)

# 构建交易
nonce = w3.eth.get_transaction_count(account)

uaddr = "0xEa027DFaC014E764644c6c2D509783d66736F557"
vote = "0x09970531a67876553ce644E91B3C73B814FBF9c0"
start = 1739254643
over = 1739254743
transaction = factory_contract.functions.addOwner(uaddr,vote,start,over).build_transaction({
    'chainId': 5777,  # ganache
    'gas': 16721975,
    'gasPrice': w3.to_wei('50', 'gwei'),
    'nonce': nonce,
})

# 签名交易
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# 发送交易
txn_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)

# 获取交易收据
txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
print(f"Transaction receipt: {txn_receipt}")


# # 假设工厂合约触发了一个 NewInstanceCreated 事件
# event_signature = w3.keccak(text="logCentralBank(CentralBank,address)").hex()
# event_signature = w3.keccak(text="logCentralBank(address,address,uint256)").hex()
# #print(event_signature)
# event_logs = txn_receipt['logs']

# #解析数据，返回新合约地址
# for log in event_logs:
#     if log['topics'][0].hex() == event_signature:
#         addr= log['topics'][1].hex()
#         #print(addr)
#         new_contract_address = w3.to_checksum_address(addr[-40:])
#         print(f"New contract deployed at: {new_contract_address}")
#         break