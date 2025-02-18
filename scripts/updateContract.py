from web3 import Web3
import json
import Accounts


# 连接节点（如Infura或本地节点）
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

# 检查连接
if w3.is_connected():
    print("Connected")
else:
    print("Failed to connect")

#VS2 address
factory_contract_address = Accounts.VC 

# 读取 JSON 文件
with open('../ABIs/versionController2.json', 'r') as file:
    factory_contract_abi = json.load(file)
# 打印 ABI
#print(factory_contract_abi)

# 创建合约实例
factory_contract = w3.eth.contract(address=factory_contract_address, abi=factory_contract_abi)


# 获取账户和私钥
account = Accounts.account_1
private_key = Accounts.private_key_1
# acct1 = w3.eth.accounts[0]
# print(acct1)

# 构建交易
nonce = w3.eth.get_transaction_count(account)

voteAddr= "0xB6596ef605B45F0601eF341A3c177535e47dDD78"
Name = "remittanceVersion"
newVersion="0x7E93b63B305F03B182662C0eb1CAaf760ED4aFEF" #remittance factory 2
start= 1739866892
over= 1739867012
transaction = factory_contract.functions.updateSFSVersion(voteAddr,Name,newVersion,start,over).build_transaction({
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

# for log in event_logs:
#     if log['topics'][0].hex() == event_signature:
#         addr= log['topics'][1].hex()
#         #print(addr)
#         new_contract_address = w3.to_checksum_address(addr[-40:])
#         print(f"New contract deployed at: {new_contract_address}")
#         break