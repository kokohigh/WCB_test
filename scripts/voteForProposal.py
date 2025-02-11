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
vote="0x765Edf7b2D5c13896260EB4FeDa3e81518232f79"

transaction = factory_contract.functions.affirmativeVote(vote).build_transaction({
    'chainId': 5777,  # ganache
    'gas': 16721975,
    'gasPrice': w3.to_wei('50', 'gwei'),
    'nonce': nonce,
})

# 签名交易
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# 发送交易
txn_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)

# 获取交易收据 # 解包有问题
txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)

event_signature = w3.keccak(text="logVoteSuccess(address, bool)").hex()

#print(event_signature)
event_logs = txn_receipt['logs']

for log in event_logs:
    result = log["data"].hex()

    if result[-1]=="0":
        print("Failed to vote")
    elif result[-1]=="1":
        print("Successed to vote")
    else:
        print("Error.")
    break