# medsys/app/controllers/paciente_controller.py

# --- Documentação ---
# Propósito: Este controller é dedicado a todas as funcionalidades
# do painel do paciente (visualizar médico, prescrições, chat, etc.).
# --------------------

from bottle import template, request, redirect
from .gerenciador_dados import GerenciadorDados

def exibir_dashboard_paciente():
    """
    Busca as informações do paciente logado, do seu médico responsável
    e das suas prescrições, e renderiza o seu dashboard.
    """
    # Verificação de segurança: Apenas pacientes podem aceder.
    user_session = request.get_cookie('user_session', secret='nossa-chave-secreta')
    
    try:
        cpf_paciente, tipo_usuario = user_session.split('|')
    except (TypeError, ValueError):
        tipo_usuario = None

    if tipo_usuario != 'paciente':
        return "<h1>Acesso Negado</h1><p>Você precisa ser um paciente para ver esta página.</p>"

    db = GerenciadorDados()
    
    # 1. Busca os dados do próprio paciente.
    paciente_logado = db.buscar_paciente_por_cpf(cpf_paciente)
    if not paciente_logado:
        return "<h1>Erro: Não foi possível encontrar os seus dados.</h1>"

    # 2. Busca os dados do médico responsável, se houver.
    medico_responsavel = None
    crm_responsavel = paciente_logado.get('medico_responsavel')
    if crm_responsavel:
        medico_responsavel = db.buscar_medico_por_crm(crm_responsavel)

    # 3. Busca a lista de prescrições do paciente.
    prescricoes = db.buscar_prescricoes_por_paciente(cpf_paciente)

    # 4. Busca a lista de consultas do paciente.
    consultas = db.buscar_consultas_por_paciente(cpf_paciente)

    #Contar mensagens não lidas para o paciente ---
    mensagens_nao_lidas = 0
    if crm_responsavel:
        # Cria o nome da sala da mesma forma que no chat_controller
        ids_ordenados = sorted([crm_responsavel, cpf_paciente])
        nome_da_sala = '-'.join(ids_ordenados)
        # Conta as mensagens não lidas para o paciente nesta sala
        mensagens_nao_lidas = db.contar_mensagens_nao_lidas(nome_da_sala, cpf_paciente)
    
    
    # Renderiza o template do dashboard do paciente, passando todos os dados recolhidos.
    return template(
        'app/views/html/dashboard_paciente.html', 
        paciente=paciente_logado,
        medico=medico_responsavel,
        prescricoes=prescricoes,
        consultas=consultas,
        nao_lidas=mensagens_nao_lidas
    )