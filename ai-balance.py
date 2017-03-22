#!/usr/bin/env python

import json
import sys
from decimal import Decimal
import daemon


if len(sys.argv) < 2:
    print "Usage: python ai-balance.py <address>"
    sys.exit()

target_address = sys.argv[1]

print "Getting json..."

d = daemon.Daemon()
inp = d.searchrawtransactions(sys.argv[1])

print "Processing transaction history..."

unspent_outputs = {}

balance = Decimal(0,8)
tx_count = 0
deposit_count = 0
for tx in inp:
    tx_count += 1
    print tx['txid'] + ",",
    for txout in tx['vout']:
        index = 0
        if 'addresses' not in txout['scriptPubKey']:
            # non-standard output
            continue
        for a in txout['scriptPubKey']['addresses']:
            if a == target_address:
                deposit_count += 1
                balance += Decimal(str(txout['value']))
                print str(txout['value']) + ", " + str(balance)
                unspent_outputs[tx['txid'] + '-' + str(txout['n'])] = txout['value']
            index += 1

    # here we're looking at all of the inputs consumed by this transaction
    for txin in tx['vin']:
        # skip coinbase transactions
        if 'txid' not in txin:
            continue

        key = txin['txid'] + '-' + str(txin['vout'])

        # then we look through all of our unspent outputs
        if key in unspent_outputs:
            balance -= Decimal(str(unspent_outputs[key]))
            print "-" + str(unspent_outputs[key]) + ", " + str(balance)
            del unspent_outputs[key]

print target_address + ' - https://blockchain.info/address/' + target_address
print "Total transactions: " + str(tx_count)
print "Total deposits: " + str(deposit_count)
print "Ending balance: " + str(balance)
