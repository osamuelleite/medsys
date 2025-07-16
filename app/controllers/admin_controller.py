# medsys/app/controllers/admin_controller.py

# --- Documentação ---
# Propósito: Este controller é dedicado a todas as funcionalidades
# do painel de administração (CRUD de usuários).
# Manter essa lógica separada deixa o projeto mais organizado.
# --------------------

from bottle import template, request, redirect
from .gerenciador_dados import GerenciadorDados

def exibir_dashboard_admin():
    """
    Busca todos os médicos и pacientes do banco de dados e
    renderiza o template do dashboard do admin, passando essas listas.
    """
    # Verifica se o cookie de sessão existe e se o usuário é um admin.
    # Esta é uma medida de segurança básica.
    user_session = request.get_cookie('user_session', secret='nossa-chave-secreta')
    if not user_session or user_session.split('|')[1] != 'admin':
        # Se não for admin, idealmente redirecionaríamos para a página de login.
        # Por enquanto, apenas retornamos uma mensagem de erro.
        return "<h1>Acesso Negado</h1><p>Você precisa ser um administrador para ver esta página.</p>"

    # Se a verificação de segurança passar, prossiga.
    db = GerenciadorDados()
    
    # Usa os novos métodos que criamos para buscar as listas completas.
    lista_medicos = db.listar_todos_os_medicos()
    lista_pacientes = db.listar_todos_os_pacientes()
    
    # Renderiza o template do dashboard, passando as listas para ele.
    # O template terá acesso às variáveis 'medicos' e 'pacientes'.
    return template(
        'app/views/html/dashboard_admin.html', 
        medicos=lista_medicos, 
        pacientes=lista_pacientes
    )

# -------------------- NOVAS FUNÇÕES DE DELEÇÃO --------------------

def apagar_medico(crm):
    """
    Recebe um CRM a partir do URL e apaga o médico correspondente.
    """
    # Verificação de segurança: Apenas administradores podem apagar.
    user_session = request.get_cookie('user_session', secret='nossa-chave-secreta')
    if not user_session or user_session.split('|')[1] != 'admin':
        return "<h1>Acesso Negado</h1>"

    db = GerenciadorDados()
    db.apagar_medico_por_crm(crm)
    
    # Após apagar, redireciona o admin de volta para o dashboard
    # para que ele veja a lista atualizada.
    return redirect('/dashboard_admin')

def apagar_paciente(cpf):
    """
    Recebe um CPF a partir do URL e apaga o paciente correspondente.
    """
    # Verificação de segurança
    user_session = request.get_cookie('user_session', secret='nossa-chave-secreta')
    if not user_session or user_session.split('|')[1] != 'admin':
        return "<h1>Acesso Negado</h1>"
    
    db = GerenciadorDados()
    db.apagar_paciente_por_cpf(cpf)
    
    # Redireciona de volta para o dashboard
    return redirect('/dashboard_admin')

# -------------------- NOVA FUNÇÃO PARA CRIAR UTILIZADORES --------------------

def criar_usuario_admin():
    """
    Recebe os dados do formulário do dashboard do admin para criar um novo
    médico ou paciente.
    """
    # Verificação de segurança: Apenas administradores podem criar utilizadores por aqui.
    user_session = request.get_cookie('user_session', secret='nossa-chave-secreta')
    if not user_session or user_session.split('|')[1] != 'admin':
        return "<h1>Acesso Negado</h1>"

    db = GerenciadorDados()
    tipo_usuario = request.forms.get('tipo_usuario')
    
    # Reutilizamos a nossa função de correção de encoding
    def corrigir(texto):
        return texto.encode('latin-1').decode('utf-8')

    # Coleta os dados do formulário
    dados_comuns = {
        "nome": corrigir(request.forms.get('nome')),
        "sobrenome": corrigir(request.forms.get('sobrenome')),
        "email": request.forms.get('email'),
        "senha": request.forms.get('senha')
    }

    if tipo_usuario == 'medico':
        dados_comuns['crm'] = request.forms.get('crm')
        dados_comuns['especialidade'] = corrigir(request.forms.get('especialidade'))
        # Usamos o método que já existe no GerenciadorDados
        db.adicionar_medico(dados_comuns)

    elif tipo_usuario == 'paciente':
        cpf_original = request.forms.get('cpf')
        cpf_limpo = cpf_original.replace('.', '').replace('-', '')
        dados_comuns['cpf'] = cpf_limpo
        # Usamos o método que já existe no GerenciadorDados
        db.adicionar_paciente(dados_comuns)

    # Após criar, redireciona de volta para o dashboard para ver a lista atualizada
    return redirect('/dashboard_admin')

# -------------------- NOVA FUNÇÃO PARA MOSTRAR A PÁGINA DE EDIÇÃO --------------------

def exibir_pagina_edicao_medico(crm):
    """
    Busca um médico específico pelo seu CRM e exibe a página de edição
    com os seus dados preenchidos no formulário.
    """
    # Verificação de segurança
    user_session = request.get_cookie('user_session', secret='nossa-chave-secreta')
    if not user_session or user_session.split('|')[1] != 'admin':
        return "<h1>Acesso Negado</h1>"

    db = GerenciadorDados()
    # Busca os dados do médico específico
    medico_para_editar = db.buscar_medico_por_crm(crm)

    if medico_para_editar:
        # Se o médico for encontrado, renderiza a página de edição
        # e passa o dicionário com os dados do médico para o template.
        return template(
            'app/views/html/editar_medico.html',
            medico=medico_para_editar
        )
    else:
        # Se nenhum médico for encontrado com aquele CRM, retorna um erro.
        return "<h1>Erro: Médico não encontrado!</h1>"

# -------------------- NOVA FUNÇÃO PARA PROCESSAR A ATUALIZAÇÃO --------------------

def processar_atualizacao_medico():
    """
    Recebe os dados do formulário de edição e chama o GerenciadorDados
    para atualizar o registo do médico no ficheiro JSON.
    """
    # Verificação de segurança
    user_session = request.get_cookie('user_session', secret='nossa-chave-secreta')
    if not user_session or user_session.split('|')[1] != 'admin':
        return "<h1>Acesso Negado</h1>"

    # Recolhe os dados do formulário
    crm_original = request.forms.get('crm_original')
    
    # Reutilizamos a nossa função de correção de encoding
    def corrigir(texto):
        return texto.encode('latin-1').decode('utf-8')

    novos_dados = {
        "nome": corrigir(request.forms.get('nome')),
        "sobrenome": corrigir(request.forms.get('sobrenome')),
        "email": request.forms.get('email'),
        "especialidade": corrigir(request.forms.get('especialidade')),
        # Não incluímos o CRM nem a senha, pois não os estamos a alterar neste formulário.
    }

    db = GerenciadorDados()
    db.atualizar_medico(crm_original, novos_dados)

    # Após atualizar, redireciona para o dashboard para ver a alteração.
    return redirect('/dashboard_admin')


# -------------------- NOVAS FUNÇÕES PARA EDIÇÃO DE PACIENTE --------------------

def exibir_pagina_edicao_paciente(cpf):
    """
    Busca um paciente específico pelo seu CPF e exibe a página de edição.
    """
    user_session = request.get_cookie('user_session', secret='nossa-chave-secreta')
    if not user_session or user_session.split('|')[1] != 'admin':
        return "<h1>Acesso Negado</h1>"

    db = GerenciadorDados()
    paciente_para_editar = db.buscar_paciente_por_cpf(cpf)

    if paciente_para_editar:
        return template(
            'app/views/html/editar_paciente.html',
            paciente=paciente_para_editar
        )
    else:
        return "<h1>Erro: Paciente não encontrado!</h1>"

def processar_atualizacao_paciente():
    """
    Recebe os dados do formulário de edição de paciente e atualiza o registo.
    """
    user_session = request.get_cookie('user_session', secret='nossa-chave-secreta')
    if not user_session or user_session.split('|')[1] != 'admin':
        return "<h1>Acesso Negado</h1>"

    cpf_original = request.forms.get('cpf_original')
    
    def corrigir(texto):
        return texto.encode('latin-1').decode('utf-8')

    novos_dados = {
        "nome": corrigir(request.forms.get('nome')),
        "sobrenome": corrigir(request.forms.get('sobrenome')),
        "email": request.forms.get('email'),
    }

    db = GerenciadorDados()
    db.atualizar_paciente(cpf_original, novos_dados)

    return redirect('/dashboard_admin')