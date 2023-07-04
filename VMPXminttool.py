import time
from web3 import Web3

# Set up Web3 instance and connect to the Ethereum Mainnet
infura_url = '(INSERT HTTP API ENDPOINT)'  # Replace with your Infura Project ID
web3 = Web3(Web3.HTTPProvider(infura_url))

# Set the contract address and ABI
contract_address = '0xb48Eb8368c9C6e9b0734de1Ef4ceB9f484B80b9C'  # Replace with the XEN contract address
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

# Hardcoded private key and public address
private_key = '(INSERT PRIVATE KEY HERE)'
account_address = '(INSERT PUBLIC ADDRESS HERE)'

# Get user inputs
user_gwei = float(input("Enter the Gwei value: "))
power = int(input("Enter the power value: "))
gas_limit = int(input("Enter the gas limit (1000000 to 30000000): "))

# Set the explicit starting block number
starting_block_number = 17622080  # Replace with your starting block number

# Display block numbers
current_block_number = web3.eth.block_number
print(f"Current Block Number: {current_block_number}")
print(f"Block Number the VMPX Mint Starts At: {starting_block_number}")

# Wait for the desired starting block number
while current_block_number < starting_block_number:
    remaining_blocks = starting_block_number - current_block_number
    current_gas_price = web3.eth.gas_price
    current_gwei = web3.from_wei(current_gas_price, 'gwei')
    print(f"Waiting for block number {starting_block_number}... Current block: {current_block_number}. Remaining blocks: {remaining_blocks}. Current Gwei: {current_gwei}")
    time.sleep(6.035)  # Delay for approximately half of the average Ethereum block time
    current_block_number = web3.eth.block_number

# Check wallet balance
balance = web3.eth.get_balance(account_address)
print(f"Wallet Balance: {web3.from_wei(balance, 'ether')} ETH")

# Check if balance is sufficient
if balance < web3.to_wei(user_gwei, 'gwei') * 1000000:
    print("Insufficient balance in the wallet. Please fill the wallet and retry.")
    exit()

# Get the nonce
nonce = web3.eth.get_transaction_count(account_address)

# Ethereum Mainnet chain ID
chain_id = 1
# Monitor GWEI and mint only if GWEI is under or equal to the user-defined value
while True:
    # Get the current gas price
    current_gas_price = web3.eth.gas_price
    current_gwei = web3.from_wei(current_gas_price, 'gwei')

    # Calculate transaction cost in Ether
    txn_cost = web3.from_wei((current_gwei + 10) * 1000000, 'ether')
    print(f"Transaction cost at current Gwei: {txn_cost} ETH")

    # Check if balance is sufficient
    if balance < web3.to_wei(user_gwei, 'gwei') * 1000000:
        print("Insufficient balance in the wallet. Please fill the wallet and retry.")
        exit()

    # Check if the current GWEI is less than or equal to the user-defined GWEI
    if current_gwei <= user_gwei:
        # Mint VMPX tokens
        transaction = contract.functions.mint(power).build_transaction({
            'from': account_address,
            'gas': gas_limit,  # Use the user-defined gas limit
            'gasPrice': web3.to_wei(current_gwei + 10, 'gwei'),  # Execute the trade at +10 GWEI of the current GWEI
            'nonce': nonce,
            'chainId': chain_id
        })

        # Sign and send the transaction
        signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)
        txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

        # Display information
        print("Minting VMPX tokens...")
        print(f"Account Address: {account_address}] ")
        print(f"Gwei: {current_gwei + 10}")
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
        
        # Exit the loop after minting
        break

    else:
        print(f"Current GWEI ({current_gwei}) is higher than user-defined GWEI ({user_gwei}). Waiting for the next block...")
        time.sleep(6.035)  # Wait for 5 seconds before checking the next block
