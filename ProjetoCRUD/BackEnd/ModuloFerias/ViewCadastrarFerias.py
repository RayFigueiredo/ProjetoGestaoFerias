from flask import render_template, redirect, request, jsonify, flash
from ProjetoCRUD import app, db, Departamento, Ferias, Funcionario
from flask_login import login_required, current_user
from sqlalchemy.sql import text
from datetime import date, timedelta, datetime


def e_fim_de_semana(data):
    return data.weekday() >= 5  # 5 representa sábado e 6 representa domingo


def ajustar_data_se_fim_de_semana(data):
    while e_fim_de_semana(data):
        data += timedelta(days=1)
    return data


@app.route("/ferias")
@login_required
def listar_ferias():

    # Consulte todos os funcionários e suas férias
    lista_ferias = Ferias.query.all()
    # Formate a data no formato desejado
    for ferias in lista_ferias:
        ferias.data_ini_formatada = ferias.data_ini.strftime('%d/%m/%Y')

    return render_template('templates_ferias/tela_inicial_ferias.html', lista_ferias=lista_ferias)


@app.route('/carregar_departamentos', methods=['GET'])
@login_required
def carrega_departamentos():
    # Execute consultas no banco de dados para obter a lista de departamentos
    departamentos = Departamento.query.all()

    # Converta os resultados em uma lista de dicionários no formato {'value': 'Departamento1', 'text': 'Departamento1'}
    departamentos_para_formulario = [{'value': dpto.id, 'text': dpto.nome} for dpto in departamentos]
    # Retorne os dados como uma resposta JSON
    return jsonify(departamentos_para_formulario)


@app.route('/carregar_funcionarios', methods=['GET'])
@login_required
def carrega_funcionarios():
    dpto_id = request.args.get('dpto_id')  # Obtém o nome do departamento da solicitação GET
    try:
        # Consulte o banco de dados para obter os nomes dos funcionários com base no id do departamento
        funcionarios = Funcionario.query.filter_by(dpto_id=dpto_id).all()
        # Extraia os nomes dos funcionários da consulta
        funcionarios_data = [{'nome': funcionario.nome, 'matricula': funcionario.mat} for funcionario in funcionarios]
        # Retorne os nomes dos funcionários como uma resposta JSON
        return jsonify(funcionarios_data)
    except Exception as e:
        # Trate os erros de banco de dados, se necessário
        return jsonify({'error': str(e)})


@app.route("/tela_cadastro", methods=["GET", "POST"])
@login_required
def cadastro_ferias():
    if request.method == "POST":
        # Verifique se a data de início das férias é um fim de semana
        data_ini = datetime.strptime(request.form["data_ini"], "%Y-%m-%d")
        if data_ini.weekday() >= 5:  # 5 é sábado e 6 é domingo
            flash("A data de início das férias não pode ser um fim de semana.", "error")
            return render_template('templates_ferias/tela_cadastro_ferias.html')

        dpto_id_html = request.form["dpto_nome"]
        # Crie uma consulta SQL parametrizada para obter o nome do departamento com base no ID
        consulta = text("SELECT nome FROM tb_dpto WHERE id = :dpto_id")
        resultado = db.session.execute(consulta, {"dpto_id": dpto_id_html})
        resultadodaconsulta = resultado.scalar()

        dpto_nome = resultadodaconsulta
        func_nome = request.form["func_nome"]
        func_mat = request.form["func_mat_hidden"]
        data_ini = request.form["data_ini"]
        qtd_dias = int(request.form["qtd_dias"])  # Converta para inteiro

        # Validação: Verifique se qtd_dias está dentro do intervalo desejado
        if qtd_dias < 5 or qtd_dias > 30:
            flash('A quantidade de dias de férias deve estar entre 5 e 30 dias', 'error')
            return redirect('/tela_cadastro')

        # Garanta que a data de início seja superior a 5 dias a partir da data atual e não comece em um fim de semana
        data_atual = date.today()
        data_ini = date.fromisoformat(data_ini)
        if (data_ini - data_atual).days < 5:
            flash('A data de início deve ser superior a 5 dias a partir da data atual.', 'error')
        elif e_fim_de_semana(data_ini):
            flash('A data de início não pode ser um fim de semana.', 'error')
        else:
            # Crie um novo objeto de férias
            nova_ferias = Ferias(dpto_nome=dpto_nome, func_nome=func_nome, func_mat=func_mat, data_ini=data_ini, qtd_dias=qtd_dias)

            # Adicione as novas férias ao banco de dados
            db.session.add(nova_ferias)
            db.session.commit()

            # Redirecionar para a página de índice (substitua 'index' pelo nome da sua rota)
            return redirect('/ferias')

    return render_template('templates_ferias/tela_cadastro_ferias.html')


# Função para buscar informações das férias com base no ferias_id
def buscar_informacoes_ferias(ferias_id):
    ferias = Ferias.query.get(ferias_id)
    return ferias  # Retorne o objeto Ferias encontrado ou None se não encontrado


# Função para atualizar informações das férias com base no ferias_id
def atualizar_ferias(ferias_id, data_ini, qtd_dias):
    ferias = Ferias.query.get(ferias_id)  # Supondo que você tenha um modelo chamado Ferias
    if ferias:
        # Atualize os campos com as novas informações
        ferias.data_ini = data_ini
        ferias.qtd_dias = qtd_dias

        # Commit a transação para salvar as atualizações no banco de dados
        db.session.commit()
        return True  # Indicação de sucesso na atualização
    return False  # Indicação de que as férias não foram encontradas para atualização
