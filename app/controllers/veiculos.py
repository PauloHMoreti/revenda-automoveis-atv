import re

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from mysql.connector import Error as MySQLError

from controllers import mensagem_erro
from models import veiculo

veiculos_bp = Blueprint("veiculos", __name__, url_prefix="/veiculos")


def dados_formulario():
    return (
        request.form["modelo"].strip(),
        request.form["marca"].strip(),
        int(request.form["ano"]),
        re.sub(r"[^A-Z0-9]", "", request.form["placa"].upper()),
    )


@veiculos_bp.route("/")
def lista():
    return render_template("veiculos/lista.html", veiculos=veiculo.listar())


@veiculos_bp.route("/novo", methods=["GET", "POST"])
def novo():
    if request.method == "POST":
        try:
            veiculo.inserir(*dados_formulario())
        except MySQLError as erro:
            flash(mensagem_erro(erro), "erro")
            return redirect(request.url)
        flash("Veículo cadastrado com sucesso.", "sucesso")
        return redirect(url_for("veiculos.lista"))
    return render_template("veiculos/form.html", veiculo=None)


@veiculos_bp.route("/<int:veiculo_id>/editar", methods=["GET", "POST"])
def editar(veiculo_id):
    registro = veiculo.buscar(veiculo_id) or abort(404)
    if request.method == "POST":
        try:
            veiculo.atualizar(veiculo_id, *dados_formulario())
        except MySQLError as erro:
            flash(mensagem_erro(erro), "erro")
            return redirect(request.url)
        flash("Veículo atualizado com sucesso.", "sucesso")
        return redirect(url_for("veiculos.lista"))
    return render_template("veiculos/form.html", veiculo=registro)


@veiculos_bp.route("/<int:veiculo_id>/excluir", methods=["POST"])
def excluir(veiculo_id):
    try:
        veiculo.excluir(veiculo_id)
        flash("Veículo excluído.", "sucesso")
    except MySQLError as erro:
        flash(mensagem_erro(erro), "erro")
    return redirect(url_for("veiculos.lista"))
