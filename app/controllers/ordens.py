from datetime import date

from flask import Blueprint, flash, redirect, render_template, request, url_for
from mysql.connector import Error as MySQLError

from controllers import mensagem_erro
from models import cliente, mecanico, ordem_servico, servico, veiculo

ordens_bp = Blueprint("ordens", __name__, url_prefix="/ordens")


@ordens_bp.route("/")
def lista():
    return render_template("ordens/lista.html", ordens=ordem_servico.listar())


@ordens_bp.route("/nova", methods=["GET", "POST"])
def nova():
    if request.method == "POST":
        try:
            ordem_id = ordem_servico.inserir(
                cliente_id=int(request.form["cliente_id"]),
                veiculo_id=int(request.form["veiculo_id"]),
                mecanico_id=int(request.form["mecanico_id"]),
                servico_id=int(request.form["servico_id"]),
                data_abertura=request.form["data_abertura"],
                observacoes=request.form["observacoes"].strip() or None,
            )
        except MySQLError as erro:
            flash(mensagem_erro(erro), "erro")
            return redirect(request.url)
        flash(f"Ordem de serviço #{ordem_id} cadastrada com sucesso.", "sucesso")
        return redirect(url_for("ordens.lista"))

    return render_template(
        "ordens/form.html",
        clientes=cliente.listar(),
        veiculos=veiculo.listar(),
        mecanicos=mecanico.listar(),
        servicos=servico.listar(),
        hoje=date.today().isoformat(),
    )
