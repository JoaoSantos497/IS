const BASE_URL = "http://localhost:5000";

// Função para listar tarefas
function listarTarefas() {
    fetch(`${BASE_URL}/tarefas`)
        .then(response => response.json())
        .then(tarefas => {
            const taskList = document.getElementById('taskList');
            taskList.innerHTML = "";
            tarefas.forEach(tarefa => {
                taskList.innerHTML += `<p>ID: ${tarefa.id}, Título: ${tarefa.titulo}, Estado: ${tarefa.estado}, Data Limite: ${tarefa.data_limite}</p>`;
            });
        })
        .catch(error => console.error("Erro ao listar tarefas:", error));
}

// Função para criar uma nova tarefa
function criarTarefa() {
    const titulo = document.getElementById('titulo').value;
    const descricao = document.getElementById('descricao').value;
    const estado = document.getElementById('estado').value;
    const data_limite = document.getElementById('data_limite').value;

    const novaTarefa = {
        titulo: titulo,
        descricao: descricao,
        estado: estado,
        data_limite: data_limite
    };

    fetch(`${BASE_URL}/tarefas`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(novaTarefa)
    })
    .then(response => response.json())
    .then(data => {
        alert(`Tarefa criada com sucesso! ID: ${data.id}`);
    })
    .catch(error => console.error("Erro ao criar tarefa:", error));
}

// Função para atualizar uma tarefa existente
function atualizarTarefa() {
    const id = document.getElementById('id_atualizar').value;
    const titulo = document.getElementById('titulo').value;
    const descricao = document.getElementById('descricao').value;
    const estado = document.getElementById('estado').value;
    const data_limite = document.getElementById('data_limite').value;

    const dadosAtualizados = {};
    if (titulo) dadosAtualizados.titulo = titulo;
    if (descricao) dadosAtualizados.descricao = descricao;
    if (estado) dadosAtualizados.estado = estado;
    if (data_limite) dadosAtualizados.data_limite = data_limite;

    fetch(`${BASE_URL}/tarefas/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(dadosAtualizados)
    })
    .then(response => response.json())
    .then(() => {
        alert(`Tarefa ${id} atualizada com sucesso!`);
    })
    .catch(error => console.error("Erro ao atualizar tarefa:", error));
}

// Função para apagar uma tarefa
function apagarTarefa() {
    const id = document.getElementById('id_apagar').value;

    fetch(`${BASE_URL}/tarefas/${id}`, {
        method: "DELETE"
    })
    .then(() => {
        alert(`Tarefa ${id} apagada com sucesso!`);
    })
    .catch(error => console.error("Erro ao apagar tarefa:", error));
}

// Função para exportar tarefas
function exportarTarefas() {
    fetch(`${BASE_URL}/export/json`)
        .then(response => response.json())
        .then(tarefas => {
            alert(JSON.stringify(tarefas, null, 2));
        })
        .catch(error => console.error("Erro ao exportar tarefas:", error));
}
