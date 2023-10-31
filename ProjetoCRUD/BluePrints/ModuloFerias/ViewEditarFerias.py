from flask import render_template, request, redirect, flash
from datetime import date


from ProjetoCRUD import app
from ProjetoCRUD.BluePrints.ModuloFerias.ViewCadastrarFerias import buscar_informacoes_ferias, e_fim_de_semana, atualizar_ferias


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
                return redirect('/ferias')
            else:
                # Se a atualização falhar (por exemplo, se ferias_id não existir), renderize a página de edição com uma mensagem de erro
                return render_template('templates_ferias/pagina_editar.html', ferias_id=ferias_id, ferias_info=ferias_info, error_message='Falha na atualização das férias')

    return render_template('templates_ferias/pagina_editar.html', ferias_id=ferias_id, ferias_info=ferias_info)
