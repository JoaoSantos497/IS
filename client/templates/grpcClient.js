// Define the gRPC client and the URL of the gRPC server exposed through grpc-web
const grpc = require('grpc-web-client');
const TarefaService = require('./tarefa_pb_service'); // Import gRPC service

// URL do servidor gRPC via grpc-web
const GRPC_SERVER_URL = 'http://localhost:8080'; // O servidor gRPC via Envoy ou outro proxy

// Função para listar tarefas
function listarTarefas() {
    const request = new TarefaService.ListarTarefasRequest();

    grpc.unary(TarefaService.ListarTarefas, {
        request: request,
        url: GRPC_SERVER_URL,
        onEnd: function(response) {
            if (response.status === grpc.Code.OK) {
                const tarefas = response.message.tarefasList;
                const taskList = document.getElementById('taskList');
                taskList.innerHTML = "";
                tarefas.forEach(tarefa => {
                    taskList.innerHTML += `
                        <p>
                            ID: ${tarefa.id}, Título: ${tarefa.titulo}, Estado: ${tarefa.estado}, Data Limite: ${tarefa.dataLimite}
                        </p>
                    `;
                });
            } else {
                console.error("Erro ao listar tarefas", response.statusText);
            }
        }
    });
}

// Função para criar uma nova tarefa
function criarTarefa() {
    const titulo = document.getElementById('titulo').value;
    const descricao = document.getElementById('descricao').value;
    const estado = document.getElementById('estado').value;
    const dataLimite = document.getElementById('data_limite').value;

    const request = new TarefaService.CriarTarefaRequest();
    request.setTitulo(titulo);
    request.setDescricao(descricao);
    request.setEstado(estado);
    request.setDataLimite(dataLimite);

    grpc.unary(TarefaService.CriarTarefa, {
        request: request,
        url: GRPC_SERVER_URL,
        onEnd: function(response) {
            if (response.status === grpc.Code.OK) {
                alert(`Tarefa criada com sucesso! ID: ${response.message.id}`);
            } else {
                console.error("Erro ao criar tarefa", response.statusText);
            }
        }
    });
}
