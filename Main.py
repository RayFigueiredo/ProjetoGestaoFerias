from flask import Flask, render_template, redirect, request, jsonify, flash
from Classes import init_app, Departamento, Funcionario, Ferias, db
from sqlalchemy.sql import text
from datetime import date, timedelta
from datetime import datetime
app = Flask(__name__)
app.secret_key = '12345678'  # Defina uma chave secreta única aqui

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Mack#2351@localhost/bdferias'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:945bo1bQFfqgqWY3NtLH@containers-us-west-87.railway.app:6810/railway'

init_app(app)


@app.route("/")
def home():
    # Consulte todos os funcionários e suas férias

    return render_template('index.html')


def e_fim_de_semana(data):
    return data.weekday() >= 5  # 5 representa sábado e 6 representa domingo

def ajustar_data_se_fim_de_semana(data):
    while e_fim_de_semana(data):
        data += timedelta(days=1)
    return data

@app.route("/ferias")
def ferias():
    # Consulte todos os funcionários e suas férias
    ferias = Ferias.query.all()

    return render_template('tela_inicial_ferias.html', ferias=ferias)

@app.route('/carregar_departamentos', methods=['GET'])
def carrega_departamentos():
    # Execute consultas no banco de dados para obter a lista de departamentos
    departamentos = Departamento.query.all()

    # Converta os resultados em uma lista de dicionários no formato {'value': 'Departamento1', 'text': 'Departamento1'}
    departamentos_para_formulario = [{'value': dpto.id, 'text': dpto.nome} for dpto in departamentos]
    # Retorne os dados como uma resposta JSON
    return jsonify(departamentos_para_formulario)

@app.route('/carregar_funcionarios', methods=['GET'])
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
        return jsonify({'error': str(e)})  # Você pode lidar com o erro aqui ou passá-lo para um manipulador de erros global

@app.route("/tela_cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":



        # Verifique se a data de início das férias é um fim de semana
        data_ini = datetime.strptime(request.form["data_ini"], "%Y-%m-%d")
        if data_ini.weekday() >= 5:  # 5 é sábado e 6 é domingo
            flash("A data de início das férias não pode ser um fim de semana.", "error")
            return render_template('tela_cadastro_ferias.html')

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
            return redirect('/')

    return render_template('tela_cadastro_ferias.html')

@app.route('/delete/<int:ferias_id>/', methods=['GET', 'POST'])
def delete_ferias(ferias_id):
    if request.method == 'POST':
        # Processar a exclusão das férias com base no ferias_id
        ferias = Ferias.query.get(ferias_id)  # Obtém o objeto Ferias com base no ID

        if ferias:
            # Exclui as férias se elas existirem
            db.session.delete(ferias)
            db.session.commit()

        # Redirecione para a página principal após a exclusão ou qualquer outra página desejada
        return redirect('/')
    else:
        # Renderize um formulário de confirmação de exclusão ou uma página de confirmação
        # para que o usuário confirme a exclusão antes de realizar a ação.
        return render_template('pagina_delete.html', ferias_id=ferias_id)

# Função para buscar informações das férias com base no ferias_id
def buscar_informacoes_ferias(ferias_id):
    ferias = Ferias.query.get(ferias_id)  # Supondo que você tenha um modelo chamado Ferias
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

@app.route('/editar/<int:ferias_id>/', methods=['GET', 'POST'])
def editar_ferias(ferias_id):
    # Lógica para buscar as informações das férias com base em ferias_id
    ferias_info = buscar_informacoes_ferias(ferias_id)

    if request.method == 'POST':
        # Processar as informações atualizadas do formulário
        data_ini = request.form["data_ini"]
        qtd_dias = request.form["qtd_dias"]

        # Garanta que a data de início seja superior a 5 dias a partir da data atual e não comece em um fim de semana
        data_atual = date.today()
        data_ini = date.fromisoformat(data_ini)
        if (data_ini - data_atual).days < 5:
            flash('A data de início deve ser superior a 5 dias a partir da data atual.', 'error')
        elif e_fim_de_semana(data_ini):
            flash('A data de início não pode ser um fim de semana.', 'error')
        else:
            # Atualize as informações no banco de dados
            sucesso = atualizar_ferias(ferias_id, data_ini, qtd_dias)

            if sucesso:
                # Redirecione para a página principal após a edição ou qualquer outra página desejada
                return redirect('/')
            else:
                # Se a atualização falhar (por exemplo, se ferias_id não existir), renderize a página de edição com uma mensagem de erro
                return render_template('pagina_editar.html', ferias_id=ferias_id, ferias_info=ferias_info, error_message='Falha na atualização das férias')

    return render_template('pagina_editar.html', ferias_id=ferias_id, ferias_info=ferias_info)

@app.route('/visualizar/<int:ferias_id>/', methods=['GET'])
def visualizar_ferias(ferias_id):
    # Lógica para buscar as informações das férias com base em ferias_id
    ferias_info = buscar_informacoes_ferias(ferias_id)

    if ferias_info:
        return render_template('pagina_visualizar.html', ferias_info=ferias_info)
    else:
        # Se as férias não foram encontradas, você pode renderizar uma página de erro ou redirecionar para a página principal
        return render_template('pagina_erro.html', mensagem='Férias não encontradas')

if __name__ == "__main__":
    app.run(debug=True)
