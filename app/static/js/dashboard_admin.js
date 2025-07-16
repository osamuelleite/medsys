// medsys/app/static/js/dashboard_admin.js

function confirmarDelete(tipo, id) {
    // Exibe uma caixa de diálogo de confirmação no navegador
    const confirmacao = confirm(`Tem a certeza de que deseja apagar este ${tipo}? Esta ação não pode ser desfeita.`);

    // Se o administrador clicar em "OK", redireciona para a URL de deleção
    if (confirmacao) {
        window.location.href = `/admin/deletar_${tipo}/${id}`;
    }
}
// --- NOVA FUNÇÃO PARA MOSTRAR/ESCONDER FORMULÁRIOS ---
function toggleForm(formId) {
    const form = document.getElementById(formId);
    // Alterna a visibilidade do formulário
    if (form.style.display === 'block') {
        form.style.display = 'none';
    } else {
        form.style.display = 'block';
    }
}
