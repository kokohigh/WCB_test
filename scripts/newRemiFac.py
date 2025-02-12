from web3 import Web3
import json
from Accounts import accounts,private_keys


# 连接节点（如Infura或本地节点）
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

# 检查连接
# if w3.is_connected():
#     print("Connected to Ethereum node")
# else:
#     print("Failed to connect")


private_key = "d6b11725f930f3905d9fabed40ecf26a34f8c4b85275d68e1cd874cf87f2f4c1"
account = w3.eth.account.from_key(private_key)  # 替换为你的私钥
w3.eth.default_account = account.address

# 读取ABI和字节码
with open('../ABIs/Remi2.json', 'r') as f:
    abi = json.load(f)
with open('../ABIs/Remi2.bin', 'r') as f:
    bytecode = f.read()

# 创建合约实例
MyContract = w3.eth.contract(abi=abi, bytecode=bytecode)
DataStorage ="0x76Ce76D296C40E9E13EE156988e25F5767545849"
# 部署合约
tx_hash = MyContract.constructor(DataStorage).transact()
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# 打印合约地址
print(tx_receipt)
print('New remittance factory deployed at:', tx_receipt.contractAddress)