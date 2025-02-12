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


private_key = "d6b11725f930f3905d9fabed40ecf26a34f8c4b85275d68e1cd874cf87f2f4c1"
account = w3.eth.account.from_key(private_key)  # 替换为你的私钥
w3.eth.default_account = account.address

# 读取ABI和字节码
with open('../ABIs/versionController2.json', 'r') as f:
    abi = json.load(f)
with open('../ABIs/versionController2.bin', 'r') as f:
    bytecode = f.read()

# 创建合约实例
MyContract = w3.eth.contract(abi=abi, bytecode=bytecode)

# 部署合约
owners = ["0xEa027DFaC014E764644c6c2D509783d66736F557","0x5C8E53DfbF8CcB5017582391EA73873afe44108E","0x99257983D6Faa395C88fa1ae5b94A6DF1b00FBf4"]
tx_hash = MyContract.constructor(owners).transact()
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# 打印合约地址
print(tx_receipt)
print('Version controllor deployed at:', tx_receipt.contractAddress)