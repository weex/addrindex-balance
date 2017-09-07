
import json
from decimal import Decimal
import daemon

def get_output(txout):
    output = {}
    if 'addresses' not in txout['scriptPubKey']:
        return None
    for a in txout['scriptPubKey']['addresses']:
        output['n'] = txout['n']
        output['value'] = txout['value']
        output['address'] = a
    return output

def get_outputs(transaction):
    outputs = []
    for txout in transaction['vout']:
        out = get_output(txout)
        if out:
            outputs.append(out)
    return outputs

def get_info(txid):
    d = daemon.Daemon()
    raw = d.getrawtransaction(txid)
    transaction = d.decoderawtransaction(raw)

    total_value = Decimal(0,8)

    outputs = get_outputs(transaction)

    inputs = []
    for txin in transaction['vin']:
        inp = {}
        inp['txid'] = txin['txid'] 
        inp['vout'] = txin['vout']
        transaction = d.decoderawtransaction(d.getrawtransaction(inp['txid']))
        source_outputs = get_outputs(transaction)
        if source_outputs:
            for s in source_outputs:
                print "comparing n {} to vout {}".format(s['n'], txin['vout'])
                if s['n'] == txin['vout']:
                    inp['amount'] = s['value']
        inputs.append(inp)
 
    stats = {    
      "url": 'https://blockchain.info/tx/' + txid,
      "inputs": inputs,
      "outputs": outputs,
      "size": transaction['size']
    }

    return stats
