### addrindex balances

A couple scripts to report on transaction history and ending balance for a Bitcoin address.

Requires addrindex patched version of Bitcoin Core available from: https://github.com/btcdrak/bitcoin/tree/addrindex

## Setup

Copy default_settings.py to settings.py and update paths to .bitcoin directory and an existing folder where a log can be saved.

Then run:

    python ai-balance.py 1someaddress.........xxx

To report on multiple addresses:

    python multiple-balances.py filename.txt

where filename.txt contains Bitcoin addresses one-per-line.
