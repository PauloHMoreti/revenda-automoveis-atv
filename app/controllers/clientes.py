from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from mysql.connector import Error as MySQLError

from controllers import mensagem_erro, somente_digitos
from models import cliente

clientes_bp = Blueprint("clientes", __name__, url_prefix="/clientes")


def dados_formulario():
    return (
        request.form["nome"].strip(),
        somente_digitos(request.form["telefone"]),
        request.form["email"].strip().lower(),
    )


@clientes_bp.route("/")
def lista():
    return render_template("clientes/lista.html", clientes=cliente.listar())


@clientes_bp.route("/novo", methods=["GET", "POST"])
def novo():
    if request.method == "POST":
        try:
            cliente.inserir(*dados_formulario())
        except MySQLError as erro:
            flash(mensagem_erro(erro), "erro")
            return redirect(request.url)
        flash("Cliente cadastrado com sucesso.", "sucesso")
        return redirect(url_for("clientes.lista"))
    return render_template("clientes/form.html", cliente=None)


@clientes_bp.route("/<int:cliente_id>/editar", methods=["GET", "POST"])
def editar(cliente_id):
    registro = cliente.buscar(cliente_id) or abort(404)
    if request.method == "POST":
        try:
            cliente.atualizar(cliente_id, *dados_formulario())
        except MySQLError as erro:
            flash(mensagem_erro(erro), "erro")
            return redirect(request.url)
        flash("Cliente atualizado com sucesso.", "sucesso")
        return redirect(url_for("clientes.lista"))
    return render_template("clientes/form.html", cliente=registro)


@clientes_bp.route("/<int:cliente_id>/excluir", methods=["POST"])
def excluir(cliente_id):
    try:
        cliente.excluir(cliente_id)
        flash("Cliente excluído.", "sucesso")
    except MySQLError as erro:
        flash(mensagem_erro(erro), "erro")
    return redirect(url_for("clientes.lista"))
