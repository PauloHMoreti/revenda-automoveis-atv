from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from mysql.connector import Error as MySQLError

from controllers import mensagem_erro
from models import mecanico

mecanicos_bp = Blueprint("mecanicos", __name__, url_prefix="/mecanicos")


def dados_formulario():
    return (
        request.form["nome"].strip(),
        request.form["especialidade"].strip(),
    )


@mecanicos_bp.route("/")
def lista():
    return render_template("mecanicos/lista.html", mecanicos=mecanico.listar())


@mecanicos_bp.route("/novo", methods=["GET", "POST"])
def novo():
    if request.method == "POST":
        try:
            mecanico.inserir(*dados_formulario())
        except MySQLError as erro:
            flash(mensagem_erro(erro), "erro")
            return redirect(request.url)
        flash("Mecânico cadastrado com sucesso.", "sucesso")
        return redirect(url_for("mecanicos.lista"))
    return render_template("mecanicos/form.html", mecanico=None)


@mecanicos_bp.route("/<int:mecanico_id>/editar", methods=["GET", "POST"])
def editar(mecanico_id):
    registro = mecanico.buscar(mecanico_id) or abort(404)
    if request.method == "POST":
        try:
            mecanico.atualizar(mecanico_id, *dados_formulario())
        except MySQLError as erro:
            flash(mensagem_erro(erro), "erro")
            return redirect(request.url)
        flash("Mecânico atualizado com sucesso.", "sucesso")
        return redirect(url_for("mecanicos.lista"))
    return render_template("mecanicos/form.html", mecanico=registro)


@mecanicos_bp.route("/<int:mecanico_id>/excluir", methods=["POST"])
def excluir(mecanico_id):
    try:
        mecanico.excluir(mecanico_id)
        flash("Mecânico excluído.", "sucesso")
    except MySQLError as erro:
        flash(mensagem_erro(erro), "erro")
    return redirect(url_for("mecanicos.lista"))
