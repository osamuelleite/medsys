# medsys/app/controllers/application_controller.py (com a correção final)

import socketio
import os  # <-- A LINHA CRUCIAL QUE FALTAVA
from bottle import Bottle, static_file, template, request, redirect, response
from .gerenciador_dados import GerenciadorDados

# Define o caminho absoluto para a pasta 'app'
APP_DIR = os.path.join(os.path.dirname(__file__), '..')

# Criação das instâncias
app = Bottle()
sio = socketio.Server(async_mode='gevent')
app_wsgi = socketio.WSGIApp(sio, app)

# Rota para arquivos estáticos usando o caminho absoluto
@app.route('/static/<filepath:path>')
def server_static(filepath):
    """Serve os arquivos estáticos da pasta app/static usando um caminho absoluto."""
    static_path = os.path.join(APP_DIR, 'static')
    # --- LINHA DE DEPURAÇÃO ---
    # Imprime no terminal o caminho completo que está a ser tentado.
    #print(f"--- DEBUG: Tentando aceder ao ficheiro estático em: {os.path.join(static_path, filepath)}")
    # --- LINHA DE DEPURAÇÃO ---
    return static_file(filepath, root=static_path)

#
# --- O RESTO DO ARQUIVO CONTINUA EXATAMENTE O MESMO ---
#

def pagina_inicial():
    return template('app/views/html/index.html')

def processar_registro():
    db = GerenciadorDados()
    tipo_usuario = request.forms.get('tipo_usuario')
    def corrigir(texto):
        return texto.encode('latin-1').decode('utf-8')
    dados_comuns = {
        "nome": corrigir(request.forms.get('nome')),
        "sobrenome": corrigir(request.forms.get('sobrenome')),
        "email": request.forms.get('email'),
        "senha": request.forms.get('senha')
    }
    if tipo_usuario == 'medico':
        dados_comuns['crm'] = request.forms.get('crm')
        dados_comuns['especialidade'] = corrigir(request.forms.get('especialidade'))
        db.adicionar_medico(dados_comuns)
    elif tipo_usuario == 'paciente':
        cpf_original = request.forms.get('cpf')
        cpf_limpo = cpf_original.replace('.', '').replace('-', '')
        dados_comuns['cpf'] = cpf_limpo
        db.adicionar_paciente(dados_comuns)
        
    return redirect('/')

def processar_login():
    db = GerenciadorDados()
    login_id = request.forms.get('login_id')
    senha = request.forms.get('senha')

    usuario = None
    tipo_usuario = None

    if login_id == 'admin':
        usuario = db.buscar_super_usuario(login_id)
        tipo_usuario = 'admin'
    else:
        usuario = db.buscar_medico_por_crm(login_id)
        if usuario:
            tipo_usuario = 'medico'
        else:
            cpf_limpo = login_id.replace('.', '').replace('-', '')
            usuario = db.buscar_paciente_por_cpf(cpf_limpo)
            if usuario:
                tipo_usuario = 'paciente'

    if usuario and usuario.get('senha') == senha:
        id_sessao = usuario.get('crm') or usuario.get('cpf') or usuario.get('login')
        response.set_cookie('user_session', f'{id_sessao}|{tipo_usuario}', secret='nossa-chave-secreta', path='/')
        print(f"Login bem-sucedido para {login_id} como {tipo_usuario}.")
        return redirect(f'/dashboard_{tipo_usuario}')
    else:
        print(f"Falha no login para o usuário: {login_id}.")
        return redirect('/')

# --- NOVA FUNÇÃO DE LOGOUT ---

def fazer_logout():
    """
    Apaga o cookie de sessão do utilizador e redireciona para a página inicial.
    """
    response.delete_cookie('user_session', path='/')
    print("Utilizador fez logout.")
    return redirect('/')