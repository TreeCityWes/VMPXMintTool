import time
from web3 import Web3

# Set up Web3 instance and connect to the Ethereum mainnet
web3 = Web3(Web3.HTTPProvider('Insert QuickNode API address'))

# Set the contract address and ABI
contract_address = '0xb48Eb8368c9C6e9b0734de1Ef4ceB9f484B80b9C'
contract_abi = [
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "cycles_",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "startBlockNumber_",
                "type": "uint256"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "power",
                "type": "uint256"
            }
        ],
        "name": "mint",
        "outputs": [],
        "stateMutability": "external",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "totalSupply",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

# Load the contract
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Get user inputs
private_key = input("Enter your private key: ")
account_address = input("Enter your account address: ")
gwei = float(input("Enter the Gwei value: "))
gas_limit = int(input("Enter the gas limit: "))
power = int(input("Enter the power value: "))

# Convert Gwei to Wei
gas_price = web3.to_wei(gwei, 'gwei')

# Set the explicit starting block number
starting_block_number = 17622079

# Display block numbers
current_block_number = web3.eth.block_number
print(f"Current Block Number: {current_block_number}")
print(f"Block Number the VMPX Mint Starts At: {starting_block_number}")

# Wait for the desired starting block number
while current_block_number < starting_block_number:
    remaining_blocks = starting_block_number - current_block_number
    print(f"Waiting for block number {starting_block_number}... Current block: {current_block_number}. Remaining blocks: {remaining_blocks}")
    time.sleep(780)  # Delay for 13 minutes (780 seconds)
    current_block_number = web3.eth.block_number

# Get the nonce
nonce = web3.eth.get_transaction_count(account_address)

# Ethereum mainnet chain ID
chain_id = 1

# Mint VMPX tokens
transaction = contract.functions.mint(power).buildTransaction({
    'from': account_address,
    'gas': gas_limit,
    'gasPrice': gas_price,
    'nonce': nonce,
    'chainId': chain_id
})

# Sign and send the transaction
signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)
txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

# Display information
print("Minting VMPX tokens...")
print(f"Account Address: {account_address}")
print(f"Gwei: {gwei}")
print(f"Gas Limit: {gas_limit}")
print(f"Power: {power}")
print(f"Starting Block Number: {starting_block_number}")
print("Waiting for the transaction to be mined...")

# Wait for the transaction to be mined and get the receipt
txn_receipt = web3.eth.wait_for_transaction_receipt(txn_hash)

# Process the transaction receipt
if txn_receipt.status == 1:
    print("Batch claimed successfully!")
else:
    print("Batch claim failed.")
