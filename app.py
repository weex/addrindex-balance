from flask import Flask, render_template
from datetime import datetime

import util
from daemon import Daemon
from address import get_stats
from transaction import get_info

app = Flask(__name__)

@app.route('/')
def home():
    d = Daemon()

    # chain info
    info = d.getblockchaininfo()

    # blocks
    blocks = []
    block_hash = d.get_best_block_hash()
    for i in range(24):
        block = d.get_block(block_hash)
        block['ago'] = util.pretty_date(block['time'])
        block['datetime'] = datetime.fromtimestamp(block['time'])
        blocks.append(block)
        block_hash = block['previousblockhash']

    return render_template('index.html', info=info, blocks=blocks)

@app.route('/block/<block_hash>')
def rt_block(block_hash):
    d = Daemon()
    block = d.get_block(block_hash)
    block['datetime'] = datetime.fromtimestamp(block['time'])
    block['ago'] = util.pretty_date(block['time'])
    return render_template('block.html', block=block)

@app.route('/address/<address>')
def rt_address(address):
    stats = get_stats(address)
    return render_template('address.html', address=address, stats=stats)

@app.route('/tx/<txid>')
def rt_transaction(txid):
    stats = get_info(txid)
    return render_template('tx.html', stats=stats)

app.run(host='0.0.0.0', debug=True)
