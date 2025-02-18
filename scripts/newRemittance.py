from web3 import Web3
import json
import Accounts


#接收4个参数：CB地址，Remi工厂地址，收款人地址，私钥
#CB address
factory_contract_address = Accounts.CB_1 
remittanceFac= Accounts.Remi
toAddr =  Accounts.account_2

account = Accounts.account_1
private_key = Accounts.private_key_1

# 连接节点（如Infura或本地节点）
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

# 检查连接
if w3.is_connected():
    print("Connected")
else:
    print("Failed to connect")


# 读取 JSON 文件
with open('../ABIs/CB.json', 'r') as file:
    factory_contract_abi = json.load(file)
# 打印 ABI
#print(factory_contract_abi)

# 创建合约实例
factory_contract = w3.eth.contract(address=factory_contract_address, abi=factory_contract_abi)


# 构建交易
nonce = w3.eth.get_transaction_count(account)
value_in_wei = w3.to_wei(0.1, 'ether')

#投票对象

transaction = factory_contract.functions.createRemittance(remittanceFac, toAddr).build_transaction({
    'chainId': 5777,  # ganache
    'gas': 16721975,
    'gasPrice': w3.to_wei('50', 'gwei'),
    'value': value_in_wei,
    'nonce': nonce,
})

# 签名交易
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# 发送交易
txn_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)

txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
#print(f"Transaction receipt: {txn_receipt}")

# # 假设工厂合约触发了一个 NewInstanceCreated 事件

event_signature = w3.keccak(text="logRemittance(address,address)").hex()
#print(event_signature)

event_logs = txn_receipt['logs']

for log in event_logs:
    if log['topics'][0].hex() == event_signature:
        remi = log['topics'][1].hex()
        receiver = log['topics'][2].hex()
        new_contract_address = w3.to_checksum_address(remi[-40:])
        print(f"New Remittance deployed at: {new_contract_address}")
        receiver_address = w3.to_checksum_address(receiver[-40:])
        print(f"Receiver is: {receiver_address}")
    break