from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from decimal import Decimal

RPC_USERNAME = "strangerbitzuser"
RPC_PASSWORD = "strangerbitzpass123"
RPC_PORT = 18443

print("CONNECTING TO BITCOIN CORE...")

NODE_CONNECTION = AuthServiceProxy(
    f"http://{RPC_USERNAME}:{RPC_PASSWORD}@127.0.0.1:{RPC_PORT}"
)

print("NODE CONNECTED")

WALLET_NAME = "segwit_lab"

try:
    NODE_CONNECTION.createwallet(WALLET_NAME)
    print("WALLET CREATED")
except JSONRPCException:
    try:
        NODE_CONNECTION.loadwallet(WALLET_NAME)
        print("WALLET LOADED")
    except:
        print("WALLET ALREADY ACTIVE")

WALLET_CONNECTION = AuthServiceProxy(
    f"http://{RPC_USERNAME}:{RPC_PASSWORD}@127.0.0.1:{RPC_PORT}/wallet/{WALLET_NAME}"
)

print("CONNECTED TO WALLET")

ADDRESS_A = WALLET_CONNECTION.getnewaddress("NODE_A_PRIME", "p2sh-segwit")
ADDRESS_B = WALLET_CONNECTION.getnewaddress("NODE_B_PRIME", "p2sh-segwit")
ADDRESS_C = WALLET_CONNECTION.getnewaddress("NODE_C_PRIME", "p2sh-segwit")

print("ADDRESS A':", ADDRESS_A)
print("ADDRESS B':", ADDRESS_B)
print("ADDRESS C':", ADDRESS_C)

print("MINING 101 BLOCKS...")
WALLET_CONNECTION.generatetoaddress(101, ADDRESS_A)
print("BLOCKS MINED")

FUND_TXID = WALLET_CONNECTION.sendtoaddress(ADDRESS_A, Decimal("5.0"))
print("FUNDING TXID:", FUND_TXID)

WALLET_CONNECTION.generatetoaddress(1, ADDRESS_A)
print("FUNDING CONFIRMED")

UTXO_LIST = WALLET_CONNECTION.listunspent(1, 9999999, [ADDRESS_A])

if len(UTXO_LIST) == 0:
    print("NO UTXO FOUND")
    exit()

SELECTED_UTXO = UTXO_LIST[0]

print("SELECTED UTXO:", SELECTED_UTXO)

INPUT_LIST = [{
    "txid": SELECTED_UTXO["txid"],
    "vout": SELECTED_UTXO["vout"]
}]

SEND_AMOUNT = Decimal("3.0")
TRANSACTION_FEE = Decimal("0.0001")

CHANGE_AMOUNT = SELECTED_UTXO["amount"] - SEND_AMOUNT - TRANSACTION_FEE

print("SEND AMOUNT:", SEND_AMOUNT)
print("CHANGE AMOUNT:", CHANGE_AMOUNT)

OUTPUT_MAP = {
    ADDRESS_B: float(SEND_AMOUNT),
    ADDRESS_A: float(CHANGE_AMOUNT)
}

RAW_TRANSACTION = WALLET_CONNECTION.createrawtransaction(INPUT_LIST, OUTPUT_MAP)

print("\nRAW TRANSACTION HEX:")
print(RAW_TRANSACTION)

DECODED_RAW = WALLET_CONNECTION.decoderawtransaction(RAW_TRANSACTION)

print("\nDECODED RAW TRANSACTION:")
print(DECODED_RAW)

SIGNED_TRANSACTION = WALLET_CONNECTION.signrawtransactionwithwallet(RAW_TRANSACTION)

if not SIGNED_TRANSACTION["complete"]:
    print("SIGNING FAILED")
    exit()

print("\nSIGNED TRANSACTION HEX:")
print(SIGNED_TRANSACTION["hex"])

TRANSACTION_ID = WALLET_CONNECTION.sendrawtransaction(SIGNED_TRANSACTION["hex"])

print("\nTRANSACTION ID (A' -> B'):", TRANSACTION_ID)

WALLET_CONNECTION.generatetoaddress(1, ADDRESS_A)

print("TRANSACTION CONFIRMED")

WALLET_TX = WALLET_CONNECTION.gettransaction(TRANSACTION_ID)

RAW_HEX = WALLET_TX["hex"]

FINAL_TRANSACTION = WALLET_CONNECTION.decoderawtransaction(RAW_HEX)

print("\nFINAL DECODED TRANSACTION:")
print(FINAL_TRANSACTION)

print("\nLOCKING SCRIPT (scriptPubKey) FOR B':")
print(FINAL_TRANSACTION["vout"][0]["scriptPubKey"])