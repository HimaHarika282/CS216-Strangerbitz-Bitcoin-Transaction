from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from decimal import Decimal

RPC_USER = "strangerbitzuser"
RPC_PASSWORD = "strangerbitzpass123"
RPC_PORT = 18443

print("Connecting to Bitcoin Core...")

NODE = AuthServiceProxy(f"http://{RPC_USER}:{RPC_PASSWORD}@127.0.0.1:{RPC_PORT}")

print("NODE CONNECTION SUCCESSFUL")

WALLET_NAME = "labwallet"

try:
    NODE.createwallet(WALLET_NAME)
    print("Wallet created")
except JSONRPCException:
    try:
        NODE.loadwallet(WALLET_NAME)
        print("Wallet loaded")
    except:
        print("Wallet already loaded")

WALLET = AuthServiceProxy(
    f"http://{RPC_USER}:{RPC_PASSWORD}@127.0.0.1:{RPC_PORT}/wallet/{WALLET_NAME}"
)

print("Connected to wallet")

ADDRESS_A = WALLET.getnewaddress("NODE_A", "legacy")
ADDRESS_B = WALLET.getnewaddress("NODE_B", "legacy")

print("SOURCE ADDRESS (A):", ADDRESS_A)
print("DESTINATION ADDRESS (B):", ADDRESS_B)

print("Mining 101 blocks...")
WALLET.generatetoaddress(101, ADDRESS_A)
print("Block mining completed")

FUND_TXID = WALLET.sendtoaddress(ADDRESS_A, Decimal("5.0"))
print("Funding TXID:", FUND_TXID)

WALLET.generatetoaddress(1, ADDRESS_A)
print("Funding confirmed")

UTXO_LIST = WALLET.listunspent(1, 9999999, [ADDRESS_A])

if not UTXO_LIST:
    print("No UTXO found for address A")
    exit()

SELECTED_UTXO = UTXO_LIST[0]

print("Selected UTXO:", SELECTED_UTXO)

INPUTS = [{
    "txid": SELECTED_UTXO["txid"],
    "vout": SELECTED_UTXO["vout"]
}]

FEE = Decimal("0.0001")

TOTAL_AMOUNT = SELECTED_UTXO["amount"]

SEND_AMOUNT = (TOTAL_AMOUNT / 2).quantize(Decimal("0.00000001"))
CHANGE_AMOUNT = (TOTAL_AMOUNT - SEND_AMOUNT - FEE).quantize(Decimal("0.00000001"))

if CHANGE_AMOUNT <= 0:
    print("Insufficient balance for transaction")
    exit()

print("Send amount:", SEND_AMOUNT)
print("Change amount:", CHANGE_AMOUNT)

OUTPUTS = {
    ADDRESS_B: float(SEND_AMOUNT),
    ADDRESS_A: float(CHANGE_AMOUNT)
}

RAW_TX = WALLET.createrawtransaction(INPUTS, OUTPUTS)

print("\nRAW TRANSACTION:")
print(RAW_TX)

SIGNED_TX = WALLET.signrawtransactionwithwallet(RAW_TX)

if not SIGNED_TX["complete"]:
    print("Transaction signing failed")
    exit()

print("\nSIGNED TRANSACTION:")
print(SIGNED_TX["hex"])

TX_ID = WALLET.sendrawtransaction(SIGNED_TX["hex"])

print("\nTRANSACTION ID (A -> B):", TX_ID)

WALLET.generatetoaddress(1, ADDRESS_A)
print("Transaction confirmed")

FINAL_TX = WALLET.gettransaction(TX_ID)

print("\nDECODED TRANSACTION:")
print(FINAL_TX)

print("\nSCRIPT PUB KEY:")
print(SELECTED_UTXO["scriptPubKey"])