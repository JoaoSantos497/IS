Sistema de Gestão de Tarefas - Web Services Multitecnologia

Este projeto implementa um sistema cliente-servidor utilizando múltiplas tecnologias de serviços web, incluindo REST, SOAP, GraphQL e gRPC. Ele permite a gestão de tarefas e a exportação/importação de dados nos formatos JSON e XML.
Tecnologias Usadas:

    Backend: Python (Flask)

    Containers: Docker

    Testes: Postman

    Validação de Dados:

        JSON Schema (para validação de dados JSON)

        XSD (para validação de dados XML)

Estrutura do Projeto

/servidor
    /rest
    /soap
    /graphql
    /grpc
    /schema
    /proto
    /data
    /logs
    tarefas.py
/cliente
    main.py
    cliente.py
/documentacao
    tarefas.schema.json
    tarefas.xsd
docker-compose.yml
README.md

Detalhes da Estrutura:

/servidor: Contém o código do servidor, que implementa os endpoints REST, SOAP, GraphQL e gRPC.

/cliente: Contém o código para o cliente Python que interage com os endpoints do servidor.

/documentacao: Contém os arquivos de validação (JSON Schema e XSD).

Endpoints do Servidor:
Métodos:

GET /tarefas: Lista todas as tarefas.

POST /tarefas: Cria uma nova tarefa (requisição JSON).
    
1. REST API
   
    Para interagir com o servidor SOAP, utilize o endpoint http://localhost:8001/rest.

1. SOAP API

    Para interagir com o servidor SOAP, utilize o endpoint http://localhost:8002/soap.

2. GraphQL API

    Acesse o servidor GraphQL em http://localhost:8003/graphql para executar consultas e mutações no formato GraphQL.

3. gRPC API

    O servidor gRPC estará disponível na porta 5001, conforme configurado no server.py. Utilize o cliente gRPC para interagir com os serviços unários e de streaming.

4. Exportação e Importação de Dados

    Exportar JSON: GET /export/json 

    Importar JSON: POST /import/json (requisição JSON)

    Exportar XML: GET /export/xml

    Importar XML: POST /import/xml (requisição XML)

Validação de Dados
1. JSON

Os dados enviados via JSON são validados usando um JSON Schema (localizado em /documentacao/tarefas.schema.json). Todos os dados que não atenderem ao formato definido pelo schema receberão uma resposta de erro.
2. XML

Os dados enviados via XML são validados usando um XSD (localizado em /documentacao/tarefas.xsd). A validação ocorre para garantir que a estrutura do XML esteja correta.


Cliente Python

O cliente Python interage com o servidor, realizando operações de CRUD nas tarefas e testando os serviços (REST, SOAP, GraphQL, e gRPC).
Como executar o cliente Python:

    Instale as dependências necessárias:

pip install -r client/requirements.txt

    Execute o script do cliente:

python cliente/cliente.py

O cliente irá interagir com os diferentes serviços do servidor e demonstrar a importação e exportação de dados JSON e XML.


Considerações Finais

Este projeto tem como objetivo demonstrar o uso de múltiplas tecnologias de serviços web e a integração de diferentes padrões de comunicação (REST, SOAP, GraphQL, e gRPC) para a implementação de um sistema de gestão de tarefas.
