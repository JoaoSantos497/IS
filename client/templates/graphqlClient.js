const URL = 'http://127.0.0.1:4000/graphql'; // URL do servidor GraphQL

// Função para listar tarefas
function listarTarefas() {
    const query = `
        query {
            tarefas {
                id
                titulo
                descricao
                estado
                data_criacao
                data_limite
            }
        }
    `;

    fetch(URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: query }),
    })
    .then(response => response.json())
    .then(data => {
        const tarefas = data.data.tarefas;
        const taskList = document.getElementById('taskList');
        taskList.innerHTML = ''; // Limpa a lista de tarefas
        tarefas.forEach(tarefa => {
            taskList.innerHTML += `
                <p>
                    ID: ${tarefa.id}, Título: ${tarefa.titulo}, Estado: ${tarefa.estado}, Data Limite: ${tarefa.data_limite}
                </p>
            `;
        });
    })
    .catch(error => console.error('Erro ao listar tarefas:', error));
}

// Função para criar uma nova tarefa
function criarTarefa() {
    const titulo = document.getElementById('titulo').value;
    const descricao = document.getElementById('descricao').value;
    const estado = document.getElementById('estado').value;
    const dataLimite = document.getElementById('data_limite').value;

    const mutation = `
        mutation($titulo: String!, $descricao: String!, $estado: String!, $data_limite: String!) {
            criarTarefa(titulo: $titulo, descricao: $descricao, estado: $estado, data_limite: $data_limite) {
                tarefa {
                    id
                    titulo
                    descricao
                    estado
                    data_criacao
                    data_limite
                }
            }
        }
    `;

    const variables = {
        titulo: titulo,
        descricao: descricao,
        estado: estado,
        data_limite: dataLimite,
    };

    fetch(URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: mutation, variables: variables }),
    })
    .then(response => response.json())
    .then(data => {
        const tarefa = data.data.criarTarefa.tarefa;
        alert(`Tarefa criada com sucesso! ID: ${tarefa.id}`);
        listarTarefas(); // Atualiza a lista de tarefas
    })
    .catch(error => console.error('Erro ao criar tarefa:', error));
}
