# medsys/app/controllers/chat_controller.py (Versão Final)

from bottle import template, request
from .gerenciador_dados import GerenciadorDados

def exibir_pagina_chat(id_destinatario):
    """
    Exibe a página de chat, criando um ID de sala único e consistente.
    """
    user_session = request.get_cookie('user_session', secret='nossa-chave-secreta')
    try:
        id_remetente, tipo_usuario = user_session.split('|')
    except (TypeError, ValueError):
        return "<h1>Sessão inválida.</h1>"

    db = GerenciadorDados()
    destinatario = db.buscar_medico_por_crm(id_destinatario) or db.buscar_paciente_por_cpf(id_destinatario)
    
    if not destinatario:
        return "<h1>Destinatário não encontrado.</h1>"

    nome_destinatario = f"{destinatario.get('nome')} {destinatario.get('sobrenome')}"

    # --- LÓGICA DO NOME DA SALA ---
    # Ordena os IDs para garantir que a sala seja sempre a mesma,
    # independentemente de quem inicia a conversa.
    # Ex: 'medicoA-pacienteB' será a mesma sala que 'pacienteB-medicoA'.
    ids_ordenados = sorted([id_remetente, id_destinatario])
    nome_da_sala = '-'.join(ids_ordenados)

    # Busca o histórico de mensagens para esta sala específica.
    historico_mensagens = db.buscar_mensagens_por_sala(nome_da_sala)

    return template(
        'app/views/html/chat.html',
        nome_destinatario=nome_destinatario,
        tipo_usuario=tipo_usuario,
        id_remetente=id_remetente,
        id_destinatario=id_destinatario,
        nome_da_sala=nome_da_sala,
        historico_mensagens=historico_mensagens # Envia o histórico para o HTML
    )