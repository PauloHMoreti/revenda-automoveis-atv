from decimal import Decimal

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from mysql.connector import Error as MySQLError

from controllers import mensagem_erro
from models import servico

servicos_bp = Blueprint("servicos", __name__, url_prefix="/servicos")


def dados_formulario():
    return (
        request.form["descricao"].strip(),
        Decimal(request.form["valor"]),
    )


@servicos_bp.route("/")
def lista():
    return render_template("servicos/lista.html", servicos=servico.listar())


@servicos_bp.route("/novo", methods=["GET", "POST"])
def novo():
    if request.method == "POST":
        try:
            servico.inserir(*dados_formulario())
        except MySQLError as erro:
            flash(mensagem_erro(erro), "erro")
            return redirect(request.url)
        flash("Serviço cadastrado com sucesso.", "sucesso")
        return redirect(url_for("servicos.lista"))
    return render_template("servicos/form.html", servico=None)


@servicos_bp.route("/<int:servico_id>/editar", methods=["GET", "POST"])
def editar(servico_id):
    registro = servico.buscar(servico_id) or abort(404)
    if request.method == "POST":
        try:
            servico.atualizar(servico_id, *dados_formulario())
        except MySQLError as erro:
            flash(mensagem_erro(erro), "erro")
            return redirect(request.url)
        flash("Serviço atualizado com sucesso.", "sucesso")
        return redirect(url_for("servicos.lista"))
    return render_template("servicos/form.html", servico=registro)


@servicos_bp.route("/<int:servico_id>/excluir", methods=["POST"])
def excluir(servico_id):
    try:
        servico.excluir(servico_id)
        flash("Serviço excluído.", "sucesso")
    except MySQLError as erro:
        flash(mensagem_erro(erro), "erro")
    return redirect(url_for("servicos.lista"))
