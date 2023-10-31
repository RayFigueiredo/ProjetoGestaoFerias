//Função para carregar departamentos do servidor
// Função para carregar departamentos do servidor
function carregarDepartamentos() {
    $.ajax({
        url: '/carregar_departamentos',
        type: 'GET',
        success: function (data) {
            // Preencha o elemento select com os departamentos retornados do servidor
            var selectDepartamento = $('#dpto_nome');
            selectDepartamento.empty();
            selectDepartamento.append('<option disabled selected>Selecione um departamento</option>');

            // Variável para armazenar o departamento selecionado
            var departamentoSelecionado;

            // Itere sobre os dados e adicione as opções ao elemento select
            $.each(data, function (key, value) {
                selectDepartamento.append($('<option>', {
                    value: value.value,  // Use o valor (ID) em vez do nome
                    text: value.text
                }));
            });

            // Configure o evento de mudança de departamento aqui, após preencher as opções
            $('#dpto_nome').change(function () {
                departamentoSelecionado = $('#dpto_nome').val();
                carregarFuncionarios(departamentoSelecionado); // Chame a função carregarFuncionarios com o ID do departamento
                $('#dpto_id_hidden').val(departamentoSelecionado); // Defina o valor do campo oculto

            });
        }
    });
}


// Função para carregar funcionários com base no código do departamento
function carregarFuncionarios(departamentoSelecionado) {

    $.ajax({
        url: '/carregar_funcionarios',
        type: 'GET',
        data: { dpto_id: departamentoSelecionado }, // Agora envie o ID do departamento
        success: function (data) {
            var selectFuncionario = $('#func_nome');
            var hiddenFuncMat = $('#func_mat_hidden'); // Selecione o campo oculto

            selectFuncionario.empty();
            selectFuncionario.append($('<option disabled selected>Selecione um funcionário</option>'));

            $.each(data, function (key, value) {
                selectFuncionario.append($('<option></option>').attr('value', value.nome).text(value.nome));

                // Quando um funcionário é selecionado, defina o valor do campo oculto
                selectFuncionario.on('change', function () {
                    if (selectFuncionario.val() === '') {
                        hiddenFuncMat.val(''); // Defina o valor do campo oculto como vazio se "Selecione um funcionário" for escolhido
                    } else {
                        hiddenFuncMat.val(value.matricula);
                    }
                });
            });
        }
    });
}