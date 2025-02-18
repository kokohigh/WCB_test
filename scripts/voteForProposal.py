from web3 import Web3
import json
import Accounts


# 接收3个参数，央行地址，投票对象，私钥

#CB address
factory_contract_address =  Accounts.CB_1

#投票对象
vote= "0xB6596ef605B45F0601eF341A3c177535e47dDD78"

# 获取账户和私钥
account = Accounts.account_1
private_key = Accounts.private_key_1



# 连接节点（如Infura或本地节点）
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

# 检查连接
if w3.is_connected():
    print("Connected")
else:
    print("Failed to connect")

#account = w3.eth.account.from_key(private_key)  # 替换为你的私钥

# 读取 JSON 文件
with open('../ABIs/CB.json', 'r') as file:
    factory_contract_abi = json.load(file)
# 打印 ABI
#print(factory_contract_abi)

# 创建合约实例
factory_contract = w3.eth.contract(address=factory_contract_address, abi=factory_contract_abi)


# 构建交易
nonce = w3.eth.get_transaction_count(account)


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
print(txn_receipt)

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