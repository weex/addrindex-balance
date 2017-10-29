#!/usr/bin/env python

import sys
from decimal import Decimal
from address import get_stats


def process_wallet(f, console=False, detail=False):
    wallet = {
              'num_addresses': len(target_addresses),
              'balance': Decimal(0,8)
             }

    for line in target_addresses:
        row = line.split(',')
        if len(row) > 1:
            target, comment = row
        else:
            target = row[0]
            comment = "No comment"

        address = get_stats(target)
        wallet['balance'] += address['balance']

        if console and detail:
            print str(address['balance']), comment.strip()

    if console:
        print "Total balance: {}".format(wallet['balance'])

    return wallet

if __name__ == "__main__":
   recursive = sys.argv[1] == '-r'

   if recursive:
       pass
   else:
       f = open(sys.argv[1])

   target_addresses = f.readlines()
   process_wallet(target_addresses, True, True)
