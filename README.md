# VMPX Mint Tool
VMPX Mint Tool on Ethereum 
# VMPX Mint Tool

Xenians! I am not a coder but this was successful on the X1 Devnet. I am posting it for community review and feedback. 
The script asks for your private key, public key, gwei, and power value. 
It then builds a transaction and broadcasts when the block number listed in the script hits. 
It does not use a smart contract. 

The VMPX Mint Tool is a Python script that automates the process of minting VMPX tokens as soon as the contract reaches a specified block number. 
It interacts with the VMPX smart contract and allows users to set their private key, account address, gas parameters, and power value for minting.

## Prerequisites

Before running the script, make sure you have the following:

- Python 3.x installed
- `web3` library installed (`pip install web3`)

## Usage

1. Clone this repository or download the `vmpxminttool.py` file.
2. Open a terminal or command prompt and navigate to the directory containing the `vmpxminttool.py` file.
3. Run the script with the command `python vmpxminttool.py`.

## Configuration

When running the script, you will be prompted to enter the following information:

- Private Key: The private key of your Ethereum account used for signing transactions.
- Account Address: The Ethereum address associated with your private key.
- Gwei Value: The desired gas price in Gwei for the transaction.
- Gas Limit: The maximum amount of gas to be used for the transaction.
- Power Value: The power value for minting VMPX tokens.

## Functionality

1. Connects to the Ethereum network using the specified QuickNode endpoint.
2. Sets up the Web3 instance and loads the VMPX smart contract using the contract address and ABI.
3. Waits until the current block number reaches or exceeds the specified starting block number.
4. Builds a transaction to mint VMPX tokens with the specified power value.
5. Signs and sends the transaction using the provided private key and gas parameters.
6. Waits for the transaction to be mined and retrieves the transaction receipt.
7. Displays the status of the minting process.

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please create a new issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

Special thanks to the developers of VMPX for providing the smart contract used by this script.

## Disclaimer

Please note that this script interacts with the Ethereum network and involves real transactions. Use it at your own risk. Always double-check the code and verify the transaction details before running the script with your private key.

