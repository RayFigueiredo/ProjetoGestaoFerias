from flask import render_template, redirect, request, flash, url_for
from ProjetoCRUD import app, db, Departamento


@app.route("/departamento")
def listar_departamentos():
    # Consulte a coluna "nome" da tabela "tb_dpto" e retorne os resultados
    lista_dpto = Departamento.query.all()

    return render_template('templates_dpto/tela_inicial_dpto.html', lista_dpto=lista_dpto)

# @app.route("/visualizar_departamento/<nome>")
# def visualizar_departamento(nome):
#     # Lógica para visualizar o departamento com o nome fornecido
#     return f"Visualizando departamento: {nome}"
#
@app.route('/editar_departamento/<int:dpto_id>/', methods=['GET', 'POST'])
def editar_departamento(dpto_id):
    # Lógica para buscar as informações do departamento com base em dpto_id
    dpto = Departamento.query.get(dpto_id)

    if dpto is None:
        flash("Departamento não encontrado.", "error")
        return redirect(url_for("listar_departamentos"))

    if request.method == 'POST':
        # Processar as informações atualizadas do formulário
        novo_nome = request.form["nome"]

        if novo_nome:
            dpto.nome = novo_nome
            db.session.commit()
            flash("Departamento atualizado com sucesso!", "success")
            return redirect(url_for("listar_departamentos"))
        else:
            flash("O nome do departamento não pode estar em branco.", "error")

    return render_template('templates_dpto/pagina_editar.html', departamento=dpto)


@app.route("/delete_departamento/<int:dpto_id>/", methods=['GET', 'POST'])
def delete_departamento(dpto_id):
    if request.method == 'POST':
        # Processar a exclusão do departamento com base no dpto_id
        dpto = Departamento.query.get(dpto_id)  # Obtém o objeto Departamento com base no "ID"
        if dpto:
            db.session.delete(dpto)
            db.session.commit()

        return redirect(url_for("listar_departamentos"))

    # Lógica para deletar o departamento com o nome fornecido
    else:

        # Renderiza um formulário de confirmação de exclusão ou uma página de confirmação
        # para que o usuário confirme a exclusão antes de realizar a ação.
        return render_template('templates_dpto/pagina_delete.html', dpto_id=dpto_id)


@app.route("/cadastrar_departamento", methods=["GET", "POST"])
def cadastrar_departamento():
    if request.method == "POST":
        nome_departamento = request.form.get("dpto_nome")

        if nome_departamento:
            # Crie um novo objeto de Departamento
            novo_departamento = Departamento(nome=nome_departamento)

            # Adicione o novo departamento ao banco de dados
            db.session.add(novo_departamento)
            db.session.commit()

            flash("Departamento cadastrado com sucesso!", "success")
            return redirect(url_for("listar_departamentos"))

    return render_template("templates_dpto/tela_cadastro_dpto.html")
