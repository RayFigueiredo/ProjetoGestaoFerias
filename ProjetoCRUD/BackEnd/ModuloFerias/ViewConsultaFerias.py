from flask import render_template
from ProjetoCRUD import app
from flask_login import login_required, current_user
from ProjetoCRUD.BackEnd.ModuloFerias.ViewCadastrarFerias import buscar_informacoes_ferias


@login_required
@app.route('/visualizar/<int:ferias_id>/', methods=['GET'])
def visualizar_ferias(ferias_id):
    # Lógica para buscar as informações das férias com base em ferias_id
    ferias_info = buscar_informacoes_ferias(ferias_id)

    if ferias_info:
        return render_template('templates_ferias/pagina_visualizar.html', ferias_info=ferias_info)
    else:
        return render_template('pagina_erro.html', mensagem='Férias não encontradas')
