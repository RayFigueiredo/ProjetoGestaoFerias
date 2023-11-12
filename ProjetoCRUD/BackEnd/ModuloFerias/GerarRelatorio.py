from flask import render_template, request
from flask_login import login_required, current_user
from ProjetoCRUD import db, Departamento, Ferias, app


@app.route("/pagina_relatorio", methods=["GET", "POST"])
@login_required
def pagina_gera_relatorio():
    if request.method == "POST":
        departamento_id = request.form.get("departamento")

        if departamento_id:
            ferias = (db.session.query(Ferias, Departamento).join(Departamento).
                      filter(Departamento.id == departamento_id).all())
        else:
            ferias = db.session.query(Ferias, Departamento).join(Departamento).all()

        departamentos = Departamento.query.all()

        return render_template('templates_ferias/pagina_relatorio.html', ferias=ferias, departamentos=departamentos)

    ferias = db.session.query(Ferias, Departamento).join(Departamento).all()
    departamentos = Departamento.query.all()

    return render_template('templates_ferias/pagina_relatorio.html', ferias=ferias, departamentos=departamentos)
