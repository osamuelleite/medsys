/* medsys/app/static/js/main.js */

function mostrarCamposEspecificos() {
    // Pega os elementos do formulário pelo ID
    const camposMedico = document.getElementById('campos-medico');
    const camposPaciente = document.getElementById('campos-paciente');

    // Verifica qual botão de rádio está selecionado
    // Adicionamos uma verificação para o caso de nenhum estar selecionado ainda
    const tipoUsuarioSelecionado = document.querySelector('input[name="tipo_usuario"]:checked');
    if (!tipoUsuarioSelecionado) {
        return;
    }

    const tipoUsuario = tipoUsuarioSelecionado.value;

    if (tipoUsuario === 'medico') {
        camposMedico.style.display = 'block'; // Mostra campos de médico
        camposPaciente.style.display = 'none'; // Esconde campos de paciente
    } else if (tipoUsuario === 'paciente') {
        camposMedico.style.display = 'none'; // Esconde campos de médico
        camposPaciente.style.display = 'block'; // Mostra campos de paciente
    }
}