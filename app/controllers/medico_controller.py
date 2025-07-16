# medsys/app/controllers/medico_controller.py (com pesquisa e filtros)

from bottle import template, request, redirect
from .gerenciador_dados import GerenciadorDados

def exibir_dashboard_medico():
    """
    Busca todos os pacientes e renderiza o template do dashboard do médico,
    aplicando filtros de pesquisa e ordenação, se existirem.
    """
    # Verificação de segurança
    user_session = request.get_cookie('user_session', secret='nossa-chave-secreta')
    try:
        # Renomeado id_usuario para crm_medico_logado para maior clareza
        crm_medico_logado, tipo_usuario = user_session.split('|')
    except (TypeError, ValueError):
        tipo_usuario = None

    if tipo_usuario != 'medico':
        return "<h1>Acesso Negado</h1><p>Você precisa ser um médico para ver esta página.</p>"

    db = GerenciadorDados()
    
    # --------------------------- LÓGICA DE PESQUISA E FILTRO ---------------------------

    # 1. Obter os parâmetros do URL (ex: ...?pesquisa=ana&ordem=nome_asc)
    termo_pesquisa = request.query.get('pesquisa', '').lower().strip()
    ordem = request.query.get('ordem', '')

    # 2. Obter a lista completa de todos os pacientes.
    lista_pacientes = db.listar_todos_os_pacientes()
    
    # 3. Aplicar o filtro de pesquisa, se um termo foi fornecido.
    if termo_pesquisa:
        pacientes_filtrados = []
        for paciente in lista_pacientes:
            # Verifica se o termo de pesquisa está no nome, sobrenome ou CPF.
            if (termo_pesquisa in paciente['nome'].lower() or
                termo_pesquisa in paciente['sobrenome'].lower() or
                termo_pesquisa in paciente['cpf']):
                pacientes_filtrados.append(paciente)
    else:
        # Se não houver pesquisa, a lista filtrada é a lista completa.
        pacientes_filtrados = lista_pacientes

    # 4. Aplicar a ordenação à lista já filtrada.
    if ordem == 'nome_asc':
        # Ordena pelo nome, ignorando maiúsculas/minúsculas.
        pacientes_filtrados.sort(key=lambda p: p['nome'].lower())
    elif ordem == 'cpf_asc':
        # Ordena pelo CPF.
        pacientes_filtrados.sort(key=lambda p: p['cpf'])

    # --- Enriquecer os dados com a contagem de mensagens não lidas ---
    for paciente in pacientes_filtrados:
        # Cria o nome da sala da mesma forma que no chat_controller
        ids_ordenados = sorted([crm_medico_logado, paciente['cpf']])
        nome_da_sala = '-'.join(ids_ordenados)
        # Conta as mensagens não lidas para o médico nesta sala
        paciente['nao_lidas'] = db.contar_mensagens_nao_lidas(nome_da_sala, crm_medico_logado)


    # 5. Renderiza o template, passando a lista final e os termos de pesquisa/ordem
    #    para que os campos do formulário possam manter os seus valores.
    return template(
        'app/views/html/dashboard_medico.html', 
        pacientes=pacientes_filtrados,
        termo_pesquisa_atual=termo_pesquisa,
        ordem_atual=ordem,
        id_medico_logado=crm_medico_logado
    )

# --------------------------- NOVA FUNÇÃO PARA ACOMPANHAR PACIENTE ---------------------------

def acompanhar_paciente(cpf_paciente):
    """
    Atribui o médico logado como responsável pelo paciente especificado.
    """
    user_session = request.get_cookie('user_session', secret='nossa-chave-secreta')
    try:
        crm_medico, tipo_usuario = user_session.split('|')
    except (TypeError, ValueError):
        return "<h1>Sessão inválida. Por favor, faça login novamente.</h1>"

    # Verificação de segurança extra
    if tipo_usuario != 'medico':
        return "<h1>Acesso Negado</h1>"

    db = GerenciadorDados()
    db.definir_medico_responsavel(cpf_paciente, crm_medico)

    # Após a ação, redireciona o médico de volta para o dashboard
    # para que ele veja a tabela atualizada.
    return redirect('/dashboard_medico')

# --------------------------- NOVA FUNÇÃO PARA EXIBIR O PRONTUÁRIO ---------------------------

def exibir_prontuario_paciente(cpf_paciente):
    """
    Busca os dados de um paciente e as suas prescrições e
    exibe a página do prontuário.
    """
    user_session = request.get_cookie('user_session', secret='nossa-chave-secreta')
    try:
        crm_medico_logado, tipo_usuario = user_session.split('|')
    except (TypeError, ValueError):
        tipo_usuario = None

    if tipo_usuario != 'medico':
        return "<h1>Acesso Negado</h1>"

    db = GerenciadorDados()
    # Busca os dados do paciente
    paciente = db.buscar_paciente_por_cpf(cpf_paciente)
    # Busca a lista de prescrições daquele paciente
    prescricoes = db.buscar_prescricoes_por_paciente(cpf_paciente)
    # Busca a lista de consultas daquele paciente
    consultas = db.buscar_consultas_por_paciente(cpf_paciente)

    if paciente:
        return template(
            'app/views/html/prontuario_paciente.html',
            paciente=paciente,
            prescricoes=prescricoes,
            consultas=consultas,
            crm_medico_logado=crm_medico_logado
        )
    else:
        return "<h1>Erro: Paciente não encontrado!</h1>"

def exibir_prontuario_paciente(cpf_paciente):
    """
    Busca os dados de um paciente e as suas prescrições e
    exibe a página do prontuário.
    """
    user_session = request.get_cookie('user_session', secret='nossa-chave-secreta')
    try:
        # Renomeado id_usuario para crm_medico para maior clareza
        crm_medico, tipo_usuario = user_session.split('|')
    except (TypeError, ValueError):
        tipo_usuario = None

    if tipo_usuario != 'medico':
        return "<h1>Acesso Negado</h1>"

    db = GerenciadorDados()
    paciente = db.buscar_paciente_por_cpf(cpf_paciente)
    prescricoes = db.buscar_prescricoes_por_paciente(cpf_paciente)
    # --- NOVO: Busca também a lista de consultas ---
    consultas = db.buscar_consultas_por_paciente(cpf_paciente)

    if paciente:
        return template(
            'app/views/html/prontuario_paciente.html',
            paciente=paciente,
            prescricoes=prescricoes,
            consultas=consultas,
            crm_medico_logado=crm_medico # Envia o CRM do médico para o template
        )
    else:
        return "<h1>Erro: Paciente não encontrado!</h1>"


# --------------------------- NOVA FUNÇÃO PARA PROCESSAR A PRESCRIÇÃO ---------------------------

def processar_adicao_prescricao():
    """
    Recebe os dados do formulário de nova prescrição, CORRIGE A CODIFICAÇÃO
    e guarda-os.
    """
    user_session = request.get_cookie('user_session', secret='nossa-chave-secreta')
    if not user_session or user_session.split('|')[1] != 'medico':
        return "<h1>Acesso Negado</h1>"

    # Reutilizamos a nossa função de correção de encoding
    def corrigir(texto):
        return texto.encode('latin-1').decode('utf-8')

    # Recolhe os dados do formulário e aplica a correção onde for necessário
    dados_prescricao = {
        "cpf_paciente": request.forms.get('cpf_paciente'),
        "crm_medico": request.forms.get('crm_medico'),
        "medicamento": corrigir(request.forms.get('medicamento')), # <-- CORRIGIDO
        "instrucoes": corrigir(request.forms.get('instrucoes'))      # <-- CORRIGIDO
    }

# --- NOVA FUNÇÃO PARA PROCESSAR O AGENDAMENTO ---

def processar_agendamento_consulta():
    """
    Recebe os dados do formulário de agendamento, corrige a codificação
    e guarda a nova consulta.
    """
    user_session = request.get_cookie('user_session', secret='nossa-chave-secreta')
    if not user_session or user_session.split('|')[1] != 'medico':
        return "<h1>Acesso Negado</h1>"

    # Define a função de correção de encoding
    def corrigir(texto):
        return texto.encode('latin-1').decode('utf-8')

    # Recolhe os dados do formulário e aplica a correção onde for necessário
    dados_consulta = {
        "cpf_paciente": request.forms.get('cpf_paciente'),
        "crm_medico": request.forms.get('crm_medico'),
        "data_consulta": request.forms.get('data_consulta'),
        "hora_consulta": request.forms.get('hora_consulta'),
        "notas": corrigir(request.forms.get('notas')) # Aplica a correção
    }

    db = GerenciadorDados()
    db.agendar_consulta(dados_consulta)

    return redirect(f"/medico/prontuario/{dados_consulta['cpf_paciente']}")