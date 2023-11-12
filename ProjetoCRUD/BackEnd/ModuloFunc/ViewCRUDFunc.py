from flask import render_template, redirect, request, flash, url_for
from flask_login import login_required
from ProjetoCRUD import app, db, Funcionario, Departamento


@app.route("/funcionario")
@login_required
def listar_funcionarios():
    # Carrega os dados da tabela Funcionario
    lista_func = Funcionario.query.all()

    # Crie um dicionário para mapear o ID do departamento ao nome do departamento
    departamento_dict = {dpto.id: dpto.nome for dpto in Departamento.query.all()}

    return render_template('templates_func/tela_inicial_func.html', lista_func=lista_func, departamento_dict=departamento_dict)


@app.route('/editar_funcionario/<mat>/', methods=['GET', 'POST'])
@login_required
def editar_funcionario(mat):
    # Lógica para buscar as informações do departamento com base em dpto_id
    func = Funcionario.query.get(mat)

    if func is None:
        flash("Funcionário não encontrado.", "error")
        return redirect(url_for("listar_funcionarios"))

    if request.method == 'POST':
        # Processar as informações atualizadas do formulário
        novo_nome = request.form["nome"]
        nova_matricula = request.form["mat"]

        if novo_nome:
            func.nome = novo_nome
            func.mat = nova_matricula
            db.session.commit()
            flash("Funcionario atualizado com sucesso!", "success")
            return redirect(url_for("listar_funcionarios"))
        else:
            flash("O nome do funcionário não pode estar em branco.", "error")

    return render_template('templates_func/pagina_editar.html', funcionario=func)


@app.route("/deletar_funcionario/<mat>/", methods=['GET', 'POST'])
@login_required
def deletar_funcionario(mat):
    if request.method == 'POST':
        # Processar a exclusão do departamento com base no dpto_id
        func = Funcionario.query.get(mat)  # Obtém o objeto Departamento com base no "ID"
        if func:
            db.session.delete(func)
            db.session.commit()

        return redirect(url_for("listar_funcionarios"))

    # Lógica para deletar o departamento com o nome fornecido
    else:

        # Renderiza um formulário de confirmação de exclusão ou uma página de confirmação
        # para que o usuário confirme a exclusão antes de realizar a ação.
        return render_template('templates_func/pagina_delete.html', mat=mat)


@app.route("/cadastrar_funcionarios", methods=["GET", "POST"])
@login_required
def cadastrar_funcionarios():
    if request.method == "POST":
        # Obter os dados do formulário

        func_nome = request.form["nome"]
        func_mat = request.form["matricula"]
        dpto_id = request.form["dpto_id_hidden"]

        # Criar um novo objeto Funcionario
        novo_func = Funcionario(mat=func_mat, nome=func_nome, dpto_id=dpto_id)

        # Adicionar o novo funcionário ao banco de dados
        db.session.add(novo_func)
        db.session.commit()

        # Redirecionar para a página de listar funcionários
        return redirect(url_for("listar_funcionarios"))

    return render_template('templates_func/tela_cadastro_func.html')
