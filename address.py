#!/usr/bin/env python
    
import json
from decimal import Decimal
import daemon
    
def get_stats(target, console=False, debug=False):
    d = daemon.Daemon()
    inp = d.searchrawtransactions(target)

    if not inp:
        return {
            "url": 'https://blockchain.info/address/' + target,
            "num_tx": 0,
            "num_deposits": 0,
            "balance": 0,
            "transactions": []
        }

    unspent_outputs = {}
    
    balance = Decimal(0,8)
    tx_count = 0
    deposit_count = 0
    transactions = []

    for tx in inp:
        if debug:
            print tx['txid'] + ",",

        tx_count += 1
        out_tx = {'txid': tx['txid']}
      
        # transaction
        for txout in tx['vout']:
            index = 0
            if 'addresses' not in txout['scriptPubKey']:
                # non-standard output
                continue
            for a in txout['scriptPubKey']['addresses']:
                if a == target:
                    deposit_count += 1
                    balance += Decimal(str(txout['value']))
                    if debug:
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

                if debug:
                    print "-" + str(unspent_outputs[key]) + ", " + str(balance)

                del unspent_outputs[key]

        transactions.append(out_tx)

    if console:
        print target + ' - https://blockchain.info/address/' + target
        print "Total transactions: " + str(tx_count)
        print "Total deposits: " + str(deposit_count)
        print "Ending balance: " + str(balance)

    return {
      "url": 'https://blockchain.info/address/' + target,
      "num_tx": tx_count,
      "num_deposits": deposit_count,
      "balance": balance,
      "transactions": transactions 
    }


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print "Usage: python address.py <address>"
        sys.exit()

    get_stats(sys.argv[1], console=True)
