import os

from flask import Flask, render_template

from controllers.clientes import clientes_bp
from controllers.mecanicos import mecanicos_bp
from controllers.ordens import ordens_bp
from controllers.relatorios import relatorios_bp
from controllers.servicos import servicos_bp
from controllers.veiculos import veiculos_bp
from db import consultar

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev")
app.url_map.strict_slashes = False  # /clientes e /clientes/ levam à mesma página

for blueprint in (clientes_bp, veiculos_bp, mecanicos_bp, servicos_bp, ordens_bp, relatorios_bp):
    app.register_blueprint(blueprint)


@app.route("/")
def home():
    total = consultar("SELECT COUNT(*) AS total FROM ordens_de_servico", um=True)["total"]
    return render_template("index.html", msg=f"conectado · {total} ordens de serviço")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=os.getenv("FLASK_DEBUG") == "1")
