from web3 import Web3
import json
import Accounts

#Version controller address #调整成命令行输入
factory_contract_address = Accounts.VC

# 连接节点（如Infura或本地节点）
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

# 读取 JSON 文件
with open('../ABIs/versionController2.json', 'r') as file:
    factory_contract_abi = json.load(file)
# 打印 ABI
#print(factory_contract_abi)

# 创建合约实例
factory_contract = w3.eth.contract(address=factory_contract_address, abi=factory_contract_abi)

# 构建交易
print(f"Data storage is at {factory_contract.functions.checkDS().call()}")
print(f"World central bank is at {factory_contract.functions.checkWCB().call()}")
print(f"Central bank factory is at {factory_contract.functions.checkCB().call()}")
print(f"Vote factory is at {factory_contract.functions.checkVote().call()}")

print(f"Remittance factory is at {factory_contract.functions.checkRemittance().call()}")
print(f"Letter of credit factory is at {factory_contract.functions.checkLOC().call()}")
print(f"Collection factory is at {factory_contract.functions.checkCollection().call()}")
