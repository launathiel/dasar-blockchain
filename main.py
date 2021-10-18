import sys
import views

from flask import Flask

app = Flask(__name__)

app.add_url_rule('/blockchain', methods = ['GET'], view_func=views.full_chain)
app.add_url_rule('/transaction/new', methods = ['POST'], view_func=views.new_transaction)
app.add_url_rule('/mining', methods = ['GET'], view_func=views.mine_block)
app.add_url_rule('/nodes/add_nodes', methods = ['POST'], view_func=views.add_nodes)
app.add_url_rule('/nodes/sync', methods = ['GET'], view_func=views.sync)

if(__name__) == '__main__':
    app.run(host='127.0.0.1', port=int(sys.argv[1]))