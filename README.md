# Bitcoin Transaction Lab
## Legacy (P2PKH) and SegWit (P2SH-P2WPKH) Transaction Analysis

This project demonstrates how Bitcoin transactions work using both **Legacy (P2PKH)** and **SegWit (P2SH-P2WPKH)** transaction formats.

The experiment was conducted on the **Bitcoin Regtest Network**, which allows local testing of Bitcoin transactions without interacting with the real Bitcoin network.

---

# Team Name
**Strangerbitz**

# Team Members

| Name | Roll Number |
|------|-------------|
| Chandana Lakshmi Subhadra | 240041009 |
| Gopisetti Pradhyumna | 240041018 |
| Gujjula Siri Sahasra | 240001032 |
| Menni Hima Harika | 240001046 |

---

# Project Overview

The objective of this lab is to understand how Bitcoin transactions are created, signed, and validated using different script types.

The project demonstrates:

- Creation of Bitcoin wallets using Bitcoin Core
- Mining blocks on the Regtest network
- Generation of legacy and SegWit addresses
- Creation of raw Bitcoin transactions
- Signing and broadcasting transactions
- Decoding transactions and analyzing Bitcoin scripts
- Comparison of Legacy and SegWit transaction structures

---

# Technologies Used

- Bitcoin Core
- Bitcoin Regtest Network
- Python
- python-bitcoinrpc library

---

# Repository Structure


blockchain_ass2
│
├── part1
│ ├── legacy_A_B.py
│ └── legacy_B_C.py
│
├── part2
│ ├── segwit_A_B.py
│ └── segwit_B_C.py
│
└── Bitcoin_Transaction_Lab_Report.pdf


---

# Part 1 – Legacy Transactions (P2PKH)

Legacy transactions use the **Pay-to-Public-Key-Hash (P2PKH)** script format.

### Workflow

1. Generate legacy addresses **A, B, and C**
2. Mine **101 blocks** to generate spendable bitcoins
3. Create transaction **A → B**
4. Use a UTXO to create transaction **B → C**
5. Decode transactions and analyze scripts

### P2PKH Script Structure

**Locking Script (scriptPubKey)**


OP_DUP OP_HASH160 <pubKeyHash> OP_EQUALVERIFY OP_CHECKSIG


**Unlocking Script (scriptSig)**


<signature> <public_key>


The unlocking script provides the data required to satisfy the locking script conditions.

---

# Part 2 – SegWit Transactions (P2SH-P2WPKH)

SegWit transactions separate the signature data from the main transaction structure and store it in the **witness field**.

### Workflow

1. Generate SegWit addresses **A', B', and C'**
2. Mine blocks to generate spendable coins
3. Create transaction **A' → B'**
4. Use a UTXO to create transaction **B' → C'**
5. Decode transactions and analyze witness data

### SegWit Script Structure

**scriptPubKey**


OP_HASH160 <script_hash> OP_EQUAL


**redeemScript**


0 <public_key_hash>


**Witness Data**

<signature> <public_key> ```

In SegWit transactions, the signature and public key are stored in the witness field rather than the scriptSig.

Legacy vs SegWit Comparison
Feature	Legacy (P2PKH)	SegWit (P2SH-P2WPKH)
Signature Location	scriptSig	witness field
Transaction Size	Larger	Smaller
Transaction Malleability	Not fixed	Fixed
Fee Efficiency	Lower	Higher

SegWit improves Bitcoin scalability by reducing transaction weight and enabling technologies such as the Lightning Network.

How to Run the Project:
Start Bitcoin Core in regtest mode
bitcoind -regtest
Run Legacy Transaction Scripts
python part1/legacy_A_B.py
python part1/legacy_B_C.py
Run SegWit Transaction Scripts
python part2/segwit_A_B.py
python part2/segwit_B_C.py

Key Concepts Demonstrated:

Bitcoin UTXO model

Transaction creation and broadcasting

Bitcoin Script validation

Legacy vs SegWit transaction formats

Witness data and transaction weight

Conclusion

This lab demonstrates how Bitcoin transactions operate using both Legacy P2PKH and SegWit P2SH-P2WPKH formats.

The experiment highlights the UTXO-based transaction model, the script validation mechanism, and the advantages of SegWit transactions in reducing transaction size and improving network scalability.

