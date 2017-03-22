#!/usr/bin/env python

import json
import sys
from decimal import Decimal
import daemon

f = open(sys.argv[1])

target_addresses = f.readlines()

d = daemon.Daemon()

for t in target_addresses:
    #print "Getting json..."
    inp = d.searchrawtransactions(t)

    #print "Processing transaction history..."
    unspent_outputs = {}

    balance = Decimal(0,8)
    tx_count = 0
    deposit_count = 0
    for tx in inp:
        tx_count += 1
        for txout in tx['vout']:
            index = 0
            for a in txout['scriptPubKey']['addresses']:
                if a == t.strip():
                    deposit_count += 1
                    balance += Decimal(str(txout['value']))
                    #print "+" + str(txout['value']) + " = " + str(balance)
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
                #print "-" + str(unspent_outputs[key]) + " = " + str(balance)
                del unspent_outputs[key]

    print t.strip(), str(balance)
