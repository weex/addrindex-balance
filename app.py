from flask import Flask, render_template

from address import get_stats
from transaction import get_info

app = Flask(__name__)

@app.route('/<address>')
def rt_address(address):
    stats = get_stats(address)
    return render_template('index.html', address=address, stats=stats)

@app.route('/tx/<txid>')
def rt_transaction(txid):
    stats = get_info(txid)
    return render_template('tx.html', stats=stats)

app.run(host='0.0.0.0', debug=True)
