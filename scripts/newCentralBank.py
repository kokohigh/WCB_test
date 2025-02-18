from web3 import Web3
import json
import Accounts

#这个需要三个参数，WCB地址，CBfac地址，私钥
factory_contract_address = Accounts.WCB #WCB address
cbFactory= Accounts.CBFac #str(sys.argv[2])
# 获取账户和私钥
account = Accounts.account_1 #w3.eth.account.from_key(private_key)  # 替换为你的私钥
private_key = Accounts.private_key_1 #str(sys.argv[3])


# 连接节点（如Infura或本地节点）
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
# 检查连接
if w3.is_connected():
    print("Connected")
else:
    print("Failed to connect")

# 读取 JSON 文件
with open('../ABIs/WCB.json', 'r') as file:
    factory_contract_abi = json.load(file)
# 打印 ABI
#print(factory_contract_abi)

# 创建合约实例
factory_contract = w3.eth.contract(address=factory_contract_address, abi=factory_contract_abi)


# 构建交易
nonce = w3.eth.get_transaction_count(account)

transaction = factory_contract.functions.createCentralBank(cbFactory).build_transaction({
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
#print(f"Transaction receipt: {txn_receipt}")


# # 假设工厂合约触发了一个 NewInstanceCreated 事件
event_signature = w3.keccak(text="logCentralBank(address,address,uint256)").hex()

#print(event_signature)
event_logs = txn_receipt['logs']

for log in event_logs:
    if log['topics'][0].hex() == event_signature:
        addr= log['topics'][1].hex()
        #print(addr)
        new_contract_address = w3.to_checksum_address(addr[-40:])
        print(f"New Central bank deployed at: {new_contract_address}")
        break