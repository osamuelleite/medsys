MedSYS - Sistema de Gestão Médica
MedSYS é uma aplicação web completa, construída com Python e o micro-framework Bottle, que simula um sistema de gestão de interações entre médicos e pacientes. A plataforma inclui gestão de utilizadores, prontuários, agendamento de consultas e um sistema de chat em tempo real com notificações, tudo isto utilizando uma arquitetura modular e organizada.

✨ Funcionalidades Principais
O sistema está dividido em três perfis de utilizador, cada um com as suas próprias permissões e funcionalidades:

👤 Administrador
Login Seguro: Acesso a um painel de controlo exclusivo.

CRUD Completo de Utilizadores: Capacidade de Criar, Ler, Atualizar e Apagar registos de Médicos e Pacientes, tudo a partir de um dashboard central.

Gestão Centralizada: Visualização completa de todos os utilizadores registados no sistema.

👨‍⚕️ Médico
Dashboard Personalizado: Visualização de todos os pacientes do sistema.

Pesquisa e Filtros: Ferramentas para encontrar e ordenar pacientes por nome ou CPF.

Acompanhamento de Pacientes: Um médico pode "acompanhar" um paciente, criando uma ligação profissional que desbloqueia outras funcionalidades.

Prontuário Eletrónico: Acesso a uma página de prontuário para cada paciente, onde é possível:

Prescrever Medicamentos: Adicionar novas prescrições ao histórico do paciente.

Agendar Consultas: Marcar novas consultas com data, hora e notas.

Visualizar Histórico: Ver a lista de consultas e prescrições passadas.

Chat em Tempo Real: Comunicação direta e privada com os pacientes que acompanha, com notificações no navegador e indicador de mensagens não lidas.

🧍 Paciente
Dashboard Pessoal: Uma área segura onde o paciente pode ver as suas informações.

Visualização de Informações: Acesso fácil aos dados do seu médico responsável, à lista de medicamentos prescritos e às consultas agendadas.

Chat em Tempo Real: Comunicação direta com o seu médico responsável, com notificações.

🛠️ Tecnologias Utilizadas
Backend:

Linguagem: Python

Framework Web: Bottle

Servidor WSGI: Gevent

WebSockets: python-socketio

Frontend:

HTML5

CSS3 (com ficheiros dedicados por módulo)

JavaScript (Vanilla JS para interatividade e comunicação com WebSockets)

Base de Dados:

Ficheiros JSON para persistência de dados, simulando uma base de dados simples e eficaz para este projeto.

📂 Estrutura do Projeto
O projeto segue uma arquitetura modular, inspirada no padrão MVC, para garantir organização e manutenibilidade.

medsys/
│
├── start_medsys.py         # Ponto de entrada para iniciar o servidor.
│
└── app/
    ├── controllers/        # Contém a lógica de negócio e o controlo de rotas.
    │   ├── application_controller.py
    │   ├── admin_controller.py
    │   ├── medico_controller.py
    │   ├── paciente_controller.py
    │   ├── websocket_controller.py
    │   ├── gerenciador_dados.py    # Classe que interage com os ficheiros JSON.
    │   └── routes.py               # Mapeamento central de todas as rotas HTTP.
    │
    ├── db/                   # "Base de dados" da aplicação.
    │   ├── medicos.json
    │   ├── pacientes.json
    │   ├── prescricoes.json
    │   ├── consultas.json
    │   └── ...
    │
    ├── static/               # Ficheiros estáticos (CSS, JS, Imagens).
    │   ├── css/
    │   └── js/
    │
    └── views/
        └── html/             # Templates HTML para todas as páginas.
🚀 Como Executar o Projeto Localmente
Para executar o MedSYS no seu ambiente local, siga estes passos:

Clone o repositório:

Bash

git clone [URL_DO_SEU_REPOSITORIO]
cd medsys
Instale as dependências:
Certifique-se de que tem o Python 3 instalado. Depois, instale as bibliotecas necessárias:

Bash

pip install bottle python-socketio gevent gevent-websocket
Inicie o servidor:
Execute o script principal a partir da raiz do projeto:

Bash

python start_medsys.py
Aceda à aplicação:
Abra o seu navegador e vá para http://localhost:8080.

UML
Diagrama de Casos de Uso
Code snippet

graph TD
    subgraph MedSYS
        UC1(Realizar Login)
        UC2(Realizar Logout)
        UC3(Cadastrar-se)
        UC4(Gerir Utilizadores <br> (CRUD))
        UC5(Visualizar Lista de Pacientes <br> com filtros)
        UC6(Acompanhar Paciente)
        UC7(Ver Prontuário do Paciente)
        UC8(Prescrever Medicamento)
        UC9(Agendar Consulta)
        UC10(Trocar Mensagens no Chat)
        UC11(Ver Médico Responsável)
        UC12(Ver Prescrições)
        UC13(Ver Consultas Agendadas)
    end

    Admin(Administrador)
    Medico(Médico)
    Paciente(Paciente)

    Admin --|> UC1 & UC2 & UC4
    Medico --|> UC1 & UC2 & UC3 & UC5 & UC6 & UC7 & UC10
    UC7 --> UC8 & UC9
    Paciente --|> UC1 & UC2 & UC3 & UC10 & UC11 & UC12 & UC13

    classDef actor fill:#f9f,stroke:#333,stroke-width:2px;
    class Admin,Medico,Paciente actor;
Diagrama de Classes
Code snippet

classDiagram
    class GerenciadorDados {
        +adicionar_medico(dados)
        +buscar_medico_por_crm(crm)
        +adicionar_paciente(dados)
        +buscar_paciente_por_cpf(cpf)
        +adicionar_prescricao(dados)
        +buscar_prescricoes_por_paciente(cpf)
        +agendar_consulta(dados)
        +buscar_consultas_por_paciente(cpf)
        +adicionar_mensagem(dados)
        +buscar_mensagens_por_sala(sala)
    }
    class Usuario {<<Conceptual>>}
    class Medico {crm, especialidade}
    class Paciente {cpf}
    class Prescricao {cpf_paciente, crm_medico, data, medicamento}
    class Consulta {cpf_paciente, crm_medico, data, hora}
    class Mensagem {sala, remetente, texto, lido}
    Usuario <|-- Medico
    Usuario <|-- Paciente
    Medico "1" -- "0..*" Paciente : acompanha
    Medico "1" -- "0..*" Prescricao : prescreve
    Medico "1" -- "0..*" Consulta : agenda
    Medico "1" -- "0..*" Mensagem
    Paciente "1" -- "0..*" Mensagem
    class Controller {<<Conceptual>>}
    Controller ..> GerenciadorDados : utiliza






