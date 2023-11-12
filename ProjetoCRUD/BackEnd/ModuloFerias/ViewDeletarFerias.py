from flask import render_template, request, redirect
from flask_login import login_required, current_user
from ProjetoCRUD import app, db, Ferias



@app.route('/delete/<int:ferias_id>/', methods=['GET', 'POST'])
@login_required
def delete_ferias(ferias_id):
    if request.method == 'POST':
        # Processar a exclusão das férias com base no ferias_id
        ferias = Ferias.query.get(ferias_id)  # Obtém o objeto Ferias com base no "ID"

        if ferias:
            # Exclui as férias se elas existirem
            db.session.delete(ferias)
            db.session.commit()

        # Redirecione para a página principal após a exclusão ou qualquer outra página desejada
        return redirect('/ferias')
    else:
        # Renderiza um formulário de confirmação de exclusão ou uma página de confirmação
        # para que o usuário confirme a exclusão antes de realizar a ação.
        return render_template('templates_ferias/pagina_delete.html', ferias_id=ferias_id)
