# 🚀 Projeto API REST - Coleta e Análise de Dados (PUCRS)
---
Integrantes:
- **Antonio Vilela**
- **Gabriel Kirchmann Kondach**
- **Heitor Burnett Garcia Hack**
- **Lucas Leuck de Oliveira** 

Este repositório contém uma API REST desenvolvida em Flask utilizando a biblioteca **Pandas** para disponibilizar e manipular o dataset `clash_wiki_dataset.csv`. O projeto atende aos requisitos das Tarefas 1 e 2 da disciplina de Coleta, Preparação e Análise de Dados.

---

## ⚙️ Tecnologias Utilizadas

- **API Framework:** Flask  
- **Manipulação de Dados:** Pandas  
- **Linguagem:** Python  
- **Consumo e Teste:** Postman e biblioteca `requests`  

---

## 📂 Estrutura do Projeto
API/
- ├── app.py                                                    # Código da API Flask (Tarefa 1)
- ├── consumo_api.py                                            # Script Python de Consumo (Tarefa 2b)
- ├── Aula 10 - Exercício Criação API.pdf                       # PDF da tarefa
- ├── API PUCRS - Coleta e Análise.postman_collection.json      # Coleção do Postman com as chamadas para a API
- ├── clash_wiki_dataset.csv                                    # Dataset utilizado
- └── README.md                                                 # Este arquivo


---

## 💻 Como Executar a API

Para testar a API localmente, você deve ter o Python instalado e as bibliotecas necessárias.

### Instale as dependências:

```bash
pip install flask pandas requests
```
### Execute a API Flask (app.py):

```bash
python app.py
```
O servidor será iniciado em: http://127.0.0.1:5000/
Mantenha este terminal aberto enquanto testa ou executa o script de consumo.

## ✅ Tarefa 1: Funcionalidades da API (CRUD e Consultas)

A API baseia-se no endpoint principal `/api/unidades` e implementa todas as operações de manipulação (CRUD) e as consultas específicas exigidas.

### 1. Manipulação de Dados (CRUD)

| Método | Endpoint                  | Descrição                                           | Status de Sucesso |
|--------|---------------------------|----------------------------------------------------|-----------------|
| GET    | /api/unidades             | Consulta Geral. Retorna todos os registros do dataset. | 200 OK          |
| POST   | /api/unidades             | Inserção (Create). Adiciona um novo registro a partir do JSON enviado no corpo. | 201 Created     |
| PUT    | /api/unidades/<id>        | Atualização (Update). Altera os campos do registro com o ID especificado. | 200 OK          |
| DELETE | /api/unidades/<id>        | Deleção (Delete). Remove o registro com o ID especificado. | 200 OK          |

---

### 2. Consultas Específicas

| Método | Endpoint                   | Requisito                         | Exemplo de Uso |
|--------|----------------------------|----------------------------------|----------------|
| GET    | /api/unidades/top/<n>      | B.1: Top N Elementos. Retorna os n primeiros registros. | /api/unidades/top/5 |
| GET    | /api/unidades/busca/<valor>| B.2: Busca por Valor Exato. Filtra pelo valor no campo Card. | /api/unidades/busca/Archers |
| POST   | /api/unidades/filtro       | B.3: Filtro Múltiplo (JSON Filter). Recebe um JSON no corpo para filtrar por múltiplos campos (lógica "E"). | JSON: `{"Type": "Troops and Defenses", "Cost": 5.0}` |

---

## 📦 Tarefa 2: Entregáveis e Consumo

### (a) Coleção Postman

A coleção completa de requisições está salva no arquivo `[Seu Nome Aqui].postman_collection.json` (ou o nome que você usou na exportação).  
Ela contém exemplos válidos para todas as 7 funcionalidades da API.

### (b) Script Python de Consumo (`consumo_api.py`)

O arquivo `consumo_api.py` demonstra o consumo de todas as rotas da API usando a biblioteca `requests`.

Para executá-lo, mantenha o servidor Flask rodando e execute:

```bash
python consumo_api.py
```

O script executa uma sequência de testes: Insere, Consulta, Atualiza e, por fim, Deleta o registro de teste, além de testar os filtros.