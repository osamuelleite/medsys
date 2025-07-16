// medsys/app/static/js/chat.js

document.addEventListener('DOMContentLoaded', () => {
    // Liga-se ao servidor de WebSocket.
    const socket = io();

    // Elementos da página
    const formChat = document.getElementById('form-chat');
    const inputMensagem = document.getElementById('input-mensagem');
    const historicoMensagens = document.getElementById('historico-mensagens');

    // --- LÓGICA DE NOTIFICAÇÃO ---

    // 1. Pede permissão para notificações assim que a página carrega.
    if (Notification.permission !== 'granted') {
        Notification.requestPermission();
    }

    function mostrarNotificacao(remetente, texto) {
        // Verifica se o utilizador deu permissão e se a janela não está em foco.
        if (Notification.permission === 'granted' && !document.hasFocus()) {
            // Cria a notificação.
            const notificacao = new Notification('Nova Mensagem em MedSYS', {
                body: texto,
                icon: '/static/img/notification_icon.png' // Opcional: adicione um ícone para a notificação
            });
        }
    }

    // --- FIM DA LÓGICA DE NOTIFICAÇÃO ---


    // Função para adicionar uma mensagem à janela de chat
    function adicionarMensagem(remetente, texto) {
        const divMensagem = document.createElement('div');
        const pMensagem = document.createElement('p');
        pMensagem.textContent = texto;
        divMensagem.appendChild(pMensagem);

        if (remetente === ID_REMETENTE) {
            divMensagem.classList.add('mensagem-enviada');
        } else {
            divMensagem.classList.add('mensagem-recebida');
        }

        historicoMensagens.appendChild(divMensagem);
        historicoMensagens.scrollTop = historicoMensagens.scrollHeight;
    }

     // Assim que a ligação é estabelecida, entra na sala de chat
     socket.on('connect', () => {
        console.log('Conectado ao servidor de WebSocket!');
        // Envia o nome da sala E o ID do leitor atual
        const dados_sala = {
            sala: NOME_DA_SALA,
            leitor: ID_REMETENTE
        };
        socket.emit('entrar_na_sala', dados_sala);
    });

    // Quando o formulário de chat é submetido...
    formChat.addEventListener('submit', (e) => {
        // ... (código existente, sem alterações) ...
        e.preventDefault();
        const texto = inputMensagem.value.trim();
        if (texto) {
            const dados = { sala: NOME_DA_SALA, remetente: ID_REMETENTE, texto: texto };
            socket.emit('enviar_mensagem', dados);
            inputMensagem.value = '';
        }
    });

    // "Ouve" por novas mensagens que chegam do servidor
    socket.on('nova_mensagem', (dados) => {
        adicionarMensagem(dados.remetente, dados.texto);
        // Chama a função de notificação sempre que uma mensagem chega
        mostrarNotificacao(dados.remetente, dados.texto);
    });

    // Rola para o fundo ao carregar a página
    historicoMensagens.scrollTop = historicoMensagens.scrollHeight;
});