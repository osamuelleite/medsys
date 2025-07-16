# medsys/app/controllers/gerenciador_dados.py

# --- Documentação ---
# Propósito: Esta classe é responsável por toda a interação com os arquivos de
# banco de dados JSON. Ela abstrai a lógica de ler e escrever nos arquivos,
# fornecendo métodos simples para o resto da aplicação usar (ex: adicionar_medico).
# --------------------

import json
from datetime import datetime 

class GerenciadorDados:
    
    CAMINHO_MEDICOS = 'app/db/medicos.json'
    CAMINHO_PACIENTES = 'app/db/pacientes.json'
    # Adicionando o caminho para o arquivo do super usuário
    CAMINHO_SUPER_USUARIO = 'app/db/super_usuario.json'
    # --- Atributo de classe para prescrições ---
    CAMINHO_PRESCRICOES = 'app/db/prescricoes.json'
    # --- Atributo de classe para consultas ---
    CAMINHO_CONSULTAS = 'app/db/consultas.json'
    # --- Atributo de classe para mensagens ---
    CAMINHO_MENSAGENS = 'app/db/mensagens.json'

    def __init__(self):
        pass

    # --------------------------- Métodos para ler e escrever JSON ---------------------------
    def _ler_json(self, caminho_arquivo):
        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                conteudo = json.load(f)
                return conteudo
        except (FileNotFoundError, json.JSONDecodeError):
            # Se o arquivo não for uma lista (ex: super_usuario.json), retorna um dict vazio
            if 'super_usuario' in caminho_arquivo:
                return {}
            return []

    def _escrever_json(self, caminho_arquivo, dados):
        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)

    # --------------------------- MÉTODOS PÚBLICOS PARA GERENCIAR DADOS ---------------------------

    def adicionar_medico(self, dados_medico):
        # ... (sem alterações)
        lista_medicos = self._ler_json(self.CAMINHO_MEDICOS)
        lista_medicos.append(dados_medico)
        self._escrever_json(self.CAMINHO_MEDICOS, lista_medicos)
        print(f"Médico adicionado: {dados_medico['nome']}")
        
    def adicionar_paciente(self, dados_paciente):
        # ... (sem alterações)
        lista_pacientes = self._ler_json(self.CAMINHO_PACIENTES)
        lista_pacientes.append(dados_paciente)
        self._escrever_json(self.CAMINHO_PACIENTES, lista_pacientes)
        print(f"Paciente adicionado: {dados_paciente['nome']}")

    def buscar_medico_por_crm(self, crm):
        # ... (sem alterações)
        lista_medicos = self._ler_json(self.CAMINHO_MEDICOS)
        for medico in lista_medicos:
            if medico['crm'] == crm:
                return medico
        return None

    def buscar_paciente_por_cpf(self, cpf):
        # ... (sem alterações)
        lista_pacientes = self._ler_json(self.CAMINHO_PACIENTES)
        for paciente in lista_pacientes:
            if paciente['cpf'] == cpf:
                return paciente
        return None

    # --------------------------- NOVO MÉTODO DE BUSCA ---------------------------
    def buscar_super_usuario(self, login):
        """
        Busca os dados do super usuário. Retorna os dados ou None.
        """
        dados_admin = self._ler_json(self.CAMINHO_SUPER_USUARIO)
        if dados_admin.get('login') == login:
            return dados_admin
        return None

    # --------------------------- NOVOS MÉTODOS PARA O DASHBOARD ---------------------------

    def listar_todos_os_medicos(self):
        """
        Retorna a lista completa de todos os médicos cadastrados.
        """
        return self._ler_json(self.CAMINHO_MEDICOS)

    def listar_todos_os_pacientes(self):
        """
        Retorna a lista completa de todos os pacientes cadastrados.
        """
        return self._ler_json(self.CAMINHO_PACIENTES)

    def apagar_medico_por_crm(self, crm_para_apagar):
        """
        Apaga um médico do banco de dados com base no seu CRM.
        """
        # 1. Lê a lista completa de médicos.
        lista_medicos = self.listar_todos_os_medicos()
        
        # 2. Cria uma nova lista contendo apenas os médicos que NÃO têm o CRM a ser apagado.
        # Esta é uma forma segura e eficiente de remover um item de uma lista.
        medicos_mantidos = [medico for medico in lista_medicos if medico['crm'] != crm_para_apagar]
        
        # 3. Salva a nova lista (sem o médico apagado) de volta no ficheiro JSON.
        self._escrever_json(self.CAMINHO_MEDICOS, medicos_mantidos)
        
        print(f"Médico com CRM {crm_para_apagar} foi apagado.")

    def apagar_paciente_por_cpf(self, cpf_para_apagar):
        """
        Apaga um paciente do banco de dados com base no seu CPF.
        """
        lista_pacientes = self.listar_todos_os_pacientes()
        
        # A lógica é a mesma: manter todos, exceto aquele que queremos apagar.
        pacientes_mantidos = [paciente for paciente in lista_pacientes if paciente['cpf'] != cpf_para_apagar]
        
        self._escrever_json(self.CAMINHO_PACIENTES, pacientes_mantidos)

        print(f"Paciente com CPF {cpf_para_apagar} foi apagado.")

# --------------------------- NOVO MÉTODO PARA ATUALIZAR DADOS DE CADASTRO DOS MÉDICOS ---------------------------

    def atualizar_medico(self, crm_original, novos_dados_medico):
        """
        Encontra um médico pelo seu CRM original e atualiza os seus dados.
        """
        # 1. Lê a lista completa de médicos.
        lista_medicos = self.listar_todos_os_medicos()
        
        # 2. Percorre a lista para encontrar o médico a ser atualizado.
        for i, medico in enumerate(lista_medicos):
            # Compara o CRM de cada médico na lista com o CRM original que queremos editar.
            if medico['crm'] == crm_original:
                # Quando encontra, atualiza o dicionário daquele médico com os novos dados.
                lista_medicos[i].update(novos_dados_medico)
                print(f"Dados do médico com CRM {crm_original} foram atualizados.")
                break # Interrompe o loop, pois já encontrámos e atualizámos o médico.

        # 3. Salva a lista inteira, agora com o registo atualizado, de volta no ficheiro.
        self._escrever_json(self.CAMINHO_MEDICOS, lista_medicos)


# --------------------------- NOVO MÉTODO PARA ATUALIZAR DADOS DE CADASTRO DO PACIENTE ---------------------------

    def atualizar_paciente(self, cpf_original, novos_dados_paciente):
        """
        Encontra um paciente pelo seu CPF original и atualiza os seus dados.
        """
        lista_pacientes = self.listar_todos_os_pacientes()
        
        for i, paciente in enumerate(lista_pacientes):
            if paciente['cpf'] == cpf_original:
                lista_pacientes[i].update(novos_dados_paciente)
                print(f"Dados do paciente com CPF {cpf_original} foram atualizados.")
                break

        self._escrever_json(self.CAMINHO_PACIENTES, lista_pacientes)

# --------------------------- NOVO MÉTODO PARA ACOMPANHAR PACIENTE ---------------------------

    def definir_medico_responsavel(self, cpf_paciente, crm_medico):
        """
        Encontra um paciente pelo seu CPF e define ou atualiza
        o campo 'medico_responsavel'.
        """
        lista_pacientes = self.listar_todos_os_pacientes()
        
        for i, paciente in enumerate(lista_pacientes):
            if paciente['cpf'] == cpf_paciente:
                # Adiciona ou atualiza o campo com o CRM do médico.
                lista_pacientes[i]['medico_responsavel'] = crm_medico
                print(f"O médico com CRM {crm_medico} está agora a acompanhar o paciente com CPF {cpf_paciente}.")
                break

        self._escrever_json(self.CAMINHO_PACIENTES, lista_pacientes)

# --------------------------- NOVO MÉTODO PARA BUSCAR PRESCRIÇÕES ---------------------------

    def buscar_prescricoes_por_paciente(self, cpf_paciente):
        """
        Lê o ficheiro de prescrições e retorna uma lista de todas as
        prescrições para um CPF de paciente específico.
        """
        todas_as_prescricoes = self._ler_json(self.CAMINHO_PRESCRICOES)
        prescricoes_do_paciente = [
            p for p in todas_as_prescricoes if p.get('cpf_paciente') == cpf_paciente
        ]
        return prescricoes_do_paciente

# --------------------------- NOVO MÉTODO PARA ADICIONAR PRESCRIÇÃO ---------------------------

    def adicionar_prescricao(self, dados_prescricao):
        """
        Adiciona uma nova prescrição ao banco de dados.
        """
        # 1. Lê a lista atual de prescrições.
        lista_prescricoes = self._ler_json(self.CAMINHO_PRESCRICOES)
        
        # 2. Adiciona a data atual aos dados da prescrição.
        #    Formata a data como Dia/Mês/Ano.
        dados_prescricao['data'] = datetime.now().strftime('%d/%m/%Y')
        
        # 3. Adiciona a nova prescrição à lista.
        lista_prescricoes.append(dados_prescricao)
        
        # 4. Salva a lista atualizada de volta no ficheiro JSON.
        self._escrever_json(self.CAMINHO_PRESCRICOES, lista_prescricoes)
        print(f"Nova prescrição adicionada para o paciente {dados_prescricao['cpf_paciente']}.")

# --------------------------- NOVO MÉTODO PARA AGENDAR CONSULTA ---------------------------

    def agendar_consulta(self, dados_consulta):
        """
        Adiciona uma nova consulta ao banco de dados.
        """
        # 1. Lê a lista atual de consultas.
        lista_consultas = self._ler_json(self.CAMINHO_CONSULTAS)
        
        # 2. Adiciona a nova consulta à lista.
        lista_consultas.append(dados_consulta)
        
        # 3. Salva a lista atualizada de volta no ficheiro JSON.
        self._escrever_json(self.CAMINHO_CONSULTAS, lista_consultas)
        print(f"Nova consulta agendada para o paciente {dados_consulta['cpf_paciente']} no dia {dados_consulta['data_consulta']}.")

# --------------------------- NOVO MÉTODO PARA BUSCAR CONSULTAS ---------------------------
    def buscar_consultas_por_paciente(self, cpf_paciente):
        """
        Lê o ficheiro de consultas e retorna uma lista de todas as
        consultas para um CPF de paciente específico.
        """
        todas_as_consultas = self._ler_json(self.CAMINHO_CONSULTAS)
        # --- LINHA DE DEPURAÇÃO ---
        print(f"--- DEBUG: Conteúdo lido de consultas.json: {todas_as_consultas}")
        
        consultas_do_paciente = [
            c for c in todas_as_consultas if c.get('cpf_paciente') == cpf_paciente
        ]
        # Ordena as consultas por data (opcional, mas bom para usabilidade)
        consultas_do_paciente.sort(key=lambda c: c['data_consulta'])
        return consultas_do_paciente

# --------------------------- NOVOS MÉTODOS PARA O CHAT ---------------------------

    def adicionar_mensagem(self, dados_mensagem):
        """Adiciona uma nova mensagem de chat ao histórico."""
        # Adiciona o estado 'lido: false' a cada nova mensagem ---
        dados_mensagem['lido'] = False
        lista_mensagens = self._ler_json(self.CAMINHO_MENSAGENS)
        lista_mensagens.append(dados_mensagem)
        self._escrever_json(self.CAMINHO_MENSAGENS, lista_mensagens)

    def buscar_mensagens_por_sala(self, nome_da_sala):
        """Busca todas as mensagens de uma sala de chat específica."""
        todas_as_mensagens = self._ler_json(self.CAMINHO_MENSAGENS)
        mensagens_da_sala = [
            msg for msg in todas_as_mensagens if msg.get('sala') == nome_da_sala
        ]
        return mensagens_da_sala
# --------------------------- NOVO MÉTODO PARA MARCAR MENSAGENS COMO LIDAS ---------------------------
    def marcar_mensagens_como_lidas(self, nome_da_sala, id_leitor):
        """
        Encontra todas as mensagens numa sala que não foram enviadas pelo leitor
        e marca-as como lidas.
        """
        lista_mensagens = self._ler_json(self.CAMINHO_MENSAGENS)
        
        for msg in lista_mensagens:
            # Verifica se a mensagem está na sala correta,
            # se ainda não foi lida, e se o remetente não é o próprio leitor.
            if (msg.get('sala') == nome_da_sala and 
                msg.get('remetente') != id_leitor and 
                not msg.get('lido')):
                
                msg['lido'] = True
        
        # Salva a lista inteira com os estados atualizados.
        self._escrever_json(self.CAMINHO_MENSAGENS, lista_mensagens)
        print(f"Mensagens na sala {nome_da_sala} marcadas como lidas para o utilizador {id_leitor}.")

# --------------------------- NOVO MÉTODO PARA CONTAR MENSAGENS NÃO LIDAS -------
    def contar_mensagens_nao_lidas(self, nome_da_sala, id_destinatario):
        """
        Conta quantas mensagens numa sala foram enviadas para um destinatário
        e que ele ainda não leu.
        """
        todas_as_mensagens = self._ler_json(self.CAMINHO_MENSAGENS)
        contador = 0
        for msg in todas_as_mensagens:
            # Conta se a mensagem é da sala correta, se o destinatário não é o remetente,
            # e se a mensagem ainda não foi lida.
            if (msg.get('sala') == nome_da_sala and 
                msg.get('remetente') != id_destinatario and 
                not msg.get('lido')):
                contador += 1
        return contador