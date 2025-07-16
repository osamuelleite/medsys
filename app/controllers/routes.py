# -------------------- medsys/app/controllers/routes.py (com a correção final da rota) --------------------

# -------------------- Importa as funções globais, já sem 'dashboard_medico' --------------------
from .application_controller import app, pagina_inicial, processar_registro, processar_login, fazer_logout

# -------------------- Importa as funções do admin --------------------
from .admin_controller import (exibir_dashboard_admin, apagar_medico, apagar_paciente, 
                               criar_usuario_admin, exibir_pagina_edicao_medico, processar_atualizacao_medico,
                               exibir_pagina_edicao_paciente, processar_atualizacao_paciente)

# -------------------- Importa a função do medico_controller --------------------
from .medico_controller import (exibir_dashboard_medico, acompanhar_paciente, exibir_prontuario_paciente,
                                processar_adicao_prescricao, processar_agendamento_consulta)

# -------------------- Importa a função do paciente_controller --------------------
from .paciente_controller import exibir_dashboard_paciente

# -------------------- Importa a função do chat_controller --------------------
from .chat_controller import exibir_pagina_chat

# -------------------- ROTAS GLOBAIS --------------------
app.route('/', 'GET', pagina_inicial)
app.route('/registrar', 'POST', processar_registro)
app.route('/login', 'POST', processar_login)
app.route('/logout', 'GET', fazer_logout)


# ---------------------- ROTAS DOS DASHBOARDS ----------------------
app.route('/dashboard_admin', 'GET', exibir_dashboard_admin)
app.route('/dashboard_medico', 'GET', exibir_dashboard_medico)
app.route('/dashboard_paciente', 'GET', exibir_dashboard_paciente)

# ---------------------- ROTAS DAS AÇÕES DO ADMIN (CRUD) ----------------------
# Rotas para deletar
app.route('/admin/deletar_medico/<crm>', 'GET', apagar_medico)
app.route('/admin/deletar_paciente/<cpf>', 'GET', apagar_paciente)

# Rota de criação do admin
app.route('/admin/criar_usuario', 'POST', criar_usuario_admin)

# Rotas de edição de médico
app.route('/admin/editar_medico/<crm>', 'GET', exibir_pagina_edicao_medico)
app.route('/admin/atualizar_medico', 'POST', processar_atualizacao_medico)

# Rotas de edição de paciente
app.route('/admin/editar_paciente/<cpf>', 'GET', exibir_pagina_edicao_paciente)
app.route('/admin/atualizar_paciente', 'POST', processar_atualizacao_paciente)

# ---------------------- ROTA PARA ACOMPANHAR PACIENTE ----------------------
app.route('/medico/acompanhar/<cpf_paciente>', 'GET', acompanhar_paciente)

# ---------------------- ROTA PARA O PRONTUÁRIO ----------------------
app.route('/medico/prontuario/<cpf_paciente>', 'GET', exibir_prontuario_paciente)

# ---------------------- ROTA PARA ADICIONAR PRESCRIÇÃO ----------------------
app.route('/medico/adicionar_prescricao', 'POST', processar_adicao_prescricao)

# ---------------------- NOVA ROTA PARA AGENDAR CONSULTA ----------------------
app.route('/medico/agendar_consulta', 'POST', processar_agendamento_consulta)

# ---------------------- ROTAS DO CHAT ----------------------
# Esta rota dinâmica aceita o ID do destinatário (seja CRM ou CPF)
app.route('/chat/<id_destinatario>', 'GET', exibir_pagina_chat)