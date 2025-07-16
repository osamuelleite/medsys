# medsys/start_medsys.py

# --- Documentação ---
# Propósito: Este é o arquivo principal que inicia o servidor da aplicação MedSYS.
# Ele configura um servidor web Gevent que é capaz de lidar tanto com as requisições
# web normais (HTTP) do Bottle quanto com as conexões em tempo real (WebSockets).
#
# Como usar: Execute este arquivo a partir do terminal com o comando: python start_medsys.py
# --------------------

# Importa a nossa aplicação WSGI, que é a combinação do Bottle com o SocketIO.
# Ela está definida no nosso controller.
from app.controllers.application_controller import app_wsgi

# Importa o servidor Gevent, que é um servidor de alta performance,
# e o WebSocketHandler para habilitar a comunicação via WebSocket.
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

# Importa o nosso arquivo de rotas para garantir que as URLs (@app.route)
# sejam registradas na aplicação antes de o servidor iniciar.
from app.controllers import routes

# Importa o nosso ficheiro de eventos WebSocket para que sejam registados.
# Embora não usemos nenhuma variável diretamente deste ficheiro, a importação
# garante que o código dentro dele é executado, registando os eventos @sio.on.
from app.controllers import websocket_controller

# O bloco `if __name__ == '__main__':` garante que o código do servidor
# só será executado quando este arquivo for chamado diretamente.
if __name__ == '__main__':
    # Cria a instância do servidor.
    # ('0.0.0.0', 8080) significa que o servidor irá escutar na porta 8080
    # e estará acessível a partir de qualquer endereço de IP da sua rede local.
    server = pywsgi.WSGIServer(
        ('0.0.0.0', 8080),
        app_wsgi,
        handler_class=WebSocketHandler
    )
    
    # Imprime uma mensagem no console para sabermos que o servidor iniciou com sucesso.
    print("Servidor MedSYS iniciado. Acesse em http://localhost:8080")
    
    # Inicia o servidor e o mantém rodando para receber requisições.
    server.serve_forever()