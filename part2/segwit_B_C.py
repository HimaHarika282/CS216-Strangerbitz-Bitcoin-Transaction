from bitcoinrpc.authproxy import AuthServiceProxy
from decimal import Decimal
from bitcoinrpc.authproxy import JSONRPCException

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
    NODE_CONNECTION.loadwallet(WALLET_NAME)
    print("WALLET LOADED")
except JSONRPCException:
    print("WALLET ALREADY ACTIVE OR EXISTS")

WALLET_CONNECTION = AuthServiceProxy(
    f"http://{RPC_USERNAME}:{RPC_PASSWORD}@127.0.0.1:{RPC_PORT}/wallet/{WALLET_NAME}"
)

print("CONNECTED TO WALLET")

ADDRESS_C = WALLET_CONNECTION.getnewaddress("NODE_C_PRIME", "p2sh-segwit")

print("DESTINATION ADDRESS C':", ADDRESS_C)

UTXO_LIST = WALLET_CONNECTION.listunspent()

if len(UTXO_LIST) == 0:
    print("NO UTXO AVAILABLE")
    exit()

SELECTED_UTXO = max(UTXO_LIST, key=lambda x: x["amount"])

print("SELECTED UTXO:", SELECTED_UTXO)

INPUT_LIST = [{
    "txid": SELECTED_UTXO["txid"],
    "vout": SELECTED_UTXO["vout"]
}]

SEND_AMOUNT = (SELECTED_UTXO["amount"] / 2).quantize(Decimal("0.00000001"))
TRANSACTION_FEE = Decimal("0.0001")

CHANGE_AMOUNT = (SELECTED_UTXO["amount"] - SEND_AMOUNT - TRANSACTION_FEE).quantize(Decimal("0.00000001"))

if CHANGE_AMOUNT <= 0:
    print("INSUFFICIENT BALANCE")
    exit()

print("SEND AMOUNT:", SEND_AMOUNT)
print("CHANGE AMOUNT:", CHANGE_AMOUNT)

OUTPUT_MAP = {
    ADDRESS_C: float(SEND_AMOUNT),
    SELECTED_UTXO["address"]: float(CHANGE_AMOUNT)
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

print("\nTRANSACTION ID (B' -> C'):", TRANSACTION_ID)

WALLET_CONNECTION.generatetoaddress(1, ADDRESS_C)

print("TRANSACTION CONFIRMED")

WALLET_TX = WALLET_CONNECTION.gettransaction(TRANSACTION_ID)

RAW_HEX = WALLET_TX["hex"]

FINAL_TRANSACTION = WALLET_CONNECTION.decoderawtransaction(RAW_HEX)

print("\nFINAL DECODED TRANSACTION:")
print(FINAL_TRANSACTION)

print("\nUNLOCKING SCRIPT (scriptSig):")
print(FINAL_TRANSACTION["vin"][0]["scriptSig"])