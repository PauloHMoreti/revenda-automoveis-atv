from flask import Blueprint, render_template

from models import relatorio

relatorios_bp = Blueprint("relatorios", __name__, url_prefix="/relatorios")


@relatorios_bp.route("/mecanicos")
def mecanicos():
    return render_template("relatorios/mecanicos.html", ranking=relatorio.mecanicos_mais_servicos())
