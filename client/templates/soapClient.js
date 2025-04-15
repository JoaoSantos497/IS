const SOAP_URL = 'http://127.0.0.1:8000/?wsdl';

// Função para listar tarefas
function listarTarefas() {
    const requestXml = `
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:web="http://localhost:8000/">
            <soapenv:Header/>
            <soapenv:Body>
                <web:listar_tarefas/>
            </soapenv:Body>
        </soapenv:Envelope>
    `;
    
    fetch(SOAP_URL, {
        method: "POST",
        headers: {
            "Content-Type": "text/xml;charset=UTF-8"
        },
        body: requestXml
    })
    .then(response => response.text())
    .then(xml => {
        const parser = new DOMParser();
        const xmlDoc = parser.parseFromString(xml, "text/xml");
        const tarefas = xmlDoc.getElementsByTagName("tarefa");
        
        const taskList = document.getElementById('taskList');
        taskList.innerHTML = "";
        
        Array.from(tarefas).forEach(tarefa => {
            taskList.innerHTML += `
                <p>
                    ID: ${tarefa.getElementsByTagName("id")[0].textContent},
                    Título: ${tarefa.getElementsByTagName("titulo")[0].textContent},
                    Estado: ${tarefa.getElementsByTagName("estado")[0].textContent},
                    Data Limite: ${tarefa.getElementsByTagName("data_limite")[0].textContent}
                </p>
            `;
        });
    })
    .catch(error => console.error("Erro ao listar tarefas:", error));
}

// Função para criar uma nova tarefa
function criarTarefa() {
    const titulo = document.getElementById('titulo').value;
    const descricao = document.getElementById('descricao').value;
    const estado = document.getElementById('estado').value;
    const dataCriacao = document.getElementById('data_criacao').value;
    const dataLimite = document.getElementById('data_limite').value;

    const requestXml = `
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:web="http://localhost:8000/">
            <soapenv:Header/>
            <soapenv:Body>
                <web:criar_tarefa>
                    <titulo>${titulo}</titulo>
                    <descricao>${descricao}</descricao>
                    <estado>${estado}</estado>
                    <data_criacao>${dataCriacao}</data_criacao>
                    <data_limite>${dataLimite}</data_limite>
                </web:criar_tarefa>
            </soapenv:Body>
        </soapenv:Envelope>
    `;

    fetch(SOAP_URL, {
        method: "POST",
        headers: {
            "Content-Type": "text/xml;charset=UTF-8"
        },
        body: requestXml
    })
    .then(response => response.text())
    .then(xml => {
        const parser = new DOMParser();
        const xmlDoc = parser.parseFromString(xml, "text/xml");
        const resposta = xmlDoc.getElementsByTagName("resposta")[0].textContent;
        alert(resposta);
    })
    .catch(error => console.error("Erro ao criar tarefa:", error));
}
