
import json
from decimal import Decimal
import daemon

def get_info(txid):
    d = daemon.Daemon()
    raw = d.getrawtransaction(txid)
    transaction = d.decoderawtransaction(raw)

    outputs = []
    total_value = Decimal(0,8)

    for txout in transaction['vout']:
        out = {}
        if 'addresses' not in txout['scriptPubKey']:
            # non-standard output
            continue
        for a in txout['scriptPubKey']['addresses']:
            out['n'] = txout['n'] 
            out['value'] = txout['value']
            out['address'] = a
        outputs.append(out)    

    inputs = []
    for txin in transaction['vin']:
        inp = {}
        inp['txid'] = txin['txid'] 
        inp['vout'] = txin['vout']
        inputs.append(inp)
 
    stats = {    
      "url": 'https://blockchain.info/tx/' + txid,
      "inputs": inputs,
      "outputs": outputs,
      "size": transaction['size']
    }

    return stats
