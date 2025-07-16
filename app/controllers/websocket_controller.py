# medsys/app/controllers/websocket_controller.py

# --- Documentação ---
# Propósito: Este controller centraliza toda a lógica de eventos
# de WebSocket (Socket.IO) para o sistema de chat.
# --------------------

# Importamos a instância 'sio' do application_controller,
# que é onde ela foi criada. É sobre esta instância que vamos
# registar os nossos eventos.
from .application_controller import sio
from .gerenciador_dados import GerenciadorDados

print("Módulo de WebSocket carregado e eventos a serem registados.")

# --- EVENTOS DE WEBSOCKET PARA O CHAT ---

@sio.on('connect')
def ao_conectar(sid, environ):
    """Função chamada quando um cliente se conecta via WebSocket."""
    print(f'Cliente conectado ao WebSocket: {sid}')

@sio.on('entrar_na_sala')
def entrar_na_sala(sid, dados_sala):
    """
    Coloca o utilizador numa sala de chat específica e marca as mensagens
    dessa sala como lidas para ele.
    """
    # Dados esperados: {'sala': 'nome_da_sala', 'leitor': 'id_do_leitor'}
    nome_da_sala = dados_sala['sala']
    id_leitor = dados_sala['leitor']

    sio.enter_room(sid, nome_da_sala)
    print(f"Utilizador {sid} entrou na sala {nome_da_sala}")

    # Chama o novo método para marcar as mensagens como lidas
    db = GerenciadorDados()
    db.marcar_mensagens_como_lidas(nome_da_sala, id_leitor)

@sio.on('enviar_mensagem')
def enviar_mensagem(sid, dados):
    """
    Recebe uma mensagem de um cliente, guarda-a e retransmite-a
    para todos os outros na mesma sala.
    """
    # Dados esperados: {'sala': 'nome_da_sala', 'remetente': 'id_remetente', 'texto': '...'}
    print(f"Mensagem recebida na sala {dados['sala']}: {dados['texto']}")
    
    db = GerenciadorDados()
    db.adicionar_mensagem(dados)
    
    sio.emit('nova_mensagem', dados, room=dados['sala'])

@sio.on('disconnect')
def ao_desconectar(sid):
    """Função chamada quando um cliente se desconecta."""
    print(f'Cliente desconectado: {sid}')