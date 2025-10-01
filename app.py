from flask import Flask, jsonify, request
import pandas as pd
import numpy as np

# --- 1. CONFIGURAÇÃO INICIAL E CARREGAMENTO ---

app = Flask(__name__)

# Configurações
ARQUIVO_DATASET = 'clash_wiki_dataset.csv'
# Campo string para o filtro de valor exato (Requisito B.2)
CAMPO_STRING_FILTRO = 'Card' 

# Variáveis globais para os dados (DataFrame do Pandas e Lista de Dicionários)
df = pd.DataFrame()
dados = []

# Carregamento e Preparação dos Dados
try:
    # Carrega o CSV
    df = pd.read_csv(ARQUIVO_DATASET)
    
    # Cria a coluna 'id' a partir do índice (chave primária)
    df = df.reset_index(names=['id']) 
    
    # Transforma o DataFrame em lista de dicionários (mais fácil para JSON)
    dados = df.to_dict('records')
    print(f"Dataset '{ARQUIVO_DATASET}' carregado com sucesso. Total de {len(dados)} registros.")

except FileNotFoundError:
    print(f"ERRO: Arquivo '{ARQUIVO_DATASET}' não encontrado.")
    dados = [] # Inicia vazio se falhar

# --- 2. ROTAS DE TESTE E CONSULTA (READ) ---

# Rota de teste
@app.route('/', methods=['GET'])
def inicio():
    return "API REST em execução! Acesse /api/unidades para ver os dados."

# Rota base para Consulta Geral (GET)
@app.route('/api/unidades', methods=['GET'])
def obter_todas_unidades():
    # Retorna todos os dados
    return jsonify(dados)

# --- 3. ROTAS DE CONSULTAS ESPECÍFICAS (REQUISITOS B.1, B.2, B.3) ---

# Rota B.1: Consulta por 'n' primeiros elementos (ex: /api/unidades/top/10)
@app.route('/api/unidades/top/<int:n>', methods=['GET'])
def obter_top_n_unidades(n):
    # Pega o número n, limita se for maior que o total
    if n > len(dados):
        n = len(dados) 
    
    # Retorna os n primeiros
    resultado = dados[:n] 
    
    return jsonify(resultado)

# Rota B.2: Consulta por campo string (Valor Exato)
# Recebe um valor e filtra no campo predefinido (CAMPO_STRING_FILTRO)
@app.route(f'/api/unidades/busca/<string:valor>', methods=['GET'])
def buscar_por_campo_string(valor):
    # Filtra onde a coluna STRING_FILTRO é igual ao valor
    resultado = [registro for registro in dados if str(registro.get(CAMPO_STRING_FILTRO)).lower() == valor.lower()]
    
    if not resultado:
        return jsonify({"message": f"Nenhuma unidade encontrada para '{valor}' no campo '{CAMPO_STRING_FILTRO}'."}), 404

    return jsonify(resultado)

# Rota B.3: Consulta por múltiplos campos (JSON Filter)
# Deve ser POST porque o filtro é enviado no corpo (JSON)
@app.route('/api/unidades/filtro', methods=['POST'])
def filtrar_por_json():
    # Pega o JSON de filtro que o usuário enviou
    filtros = request.get_json()
    
    if not filtros:
        return jsonify({"message": "Nenhum filtro JSON fornecido no corpo da requisição."}), 400
    
    # Começa com todos os dados
    resultado_filtrado = dados
    
    # Itera sobre cada filtro (campo e valor)
    for campo, valor in filtros.items():
        # Filtra os dados, mantendo apenas os que batem com o valor do campo
        # Converte para string e lower() para ser case-insensitive
        resultado_filtrado = [
            registro for registro in resultado_filtrado 
            if str(registro.get(campo)).lower() == str(valor).lower()
        ]

    if not resultado_filtrado:
        return jsonify({"message": "Nenhuma unidade encontrada com os filtros especificados."}), 404
        
    return jsonify(resultado_filtrado)

# --- 4. ROTAS DE MANIPULAÇÃO DE DADOS (CRUD: CREATE, UPDATE, DELETE) ---

# Rota C - CREATE (Inserção)
@app.route('/api/unidades', methods=['POST'])
def adicionar_unidade():
    global df # pra mudar o DataFrame
    global dados # pra mudar a lista de dados

    # Pega o JSON do novo registro
    novo_registro = request.get_json()
    
    if not novo_registro:
        return jsonify({"message": "Dados inválidos ou faltando"}), 400

    # Novo ID é o máximo atual + 1
    novo_id = df['id'].max() + 1
    novo_registro['id'] = int(novo_id) # Garante que o ID é inteiro

    # Adiciona na lista 'dados'
    dados.append(novo_registro)

    # Adiciona no DataFrame (pro df ficar igual à lista)
    nova_linha_df = pd.Series(novo_registro).to_frame().T
    df = pd.concat([df, nova_linha_df], ignore_index=True)
    
    # Retorna o registro criado (código 201 Created)
    return jsonify(novo_registro), 201

# Rota U - UPDATE (Atualização)
@app.route('/api/unidades/<int:id>', methods=['PUT'])
def atualizar_unidade(id):
    global df # pra mudar o DataFrame
    global dados # pra mudar a lista de dados

    # Pega os dados novos
    dados_atualizacao = request.get_json()
    
    # Acha o índice do registro na lista 'dados'
    index = next((i for i, registro in enumerate(dados) if registro['id'] == id), None)

    if index is None:
        return jsonify({"message": f"Unidade com id {id} não encontrada."}), 404

    # Atualiza cada campo no registro
    for chave, valor in dados_atualizacao.items():
        if chave != 'id': # Não deixa mudar o id
            dados[index][chave] = valor

    # Atualiza o DataFrame
    df_index = df[df['id'] == id].index
    if not df_index.empty:
        for chave, valor in dados_atualizacao.items():
            if chave != 'id':
                df.loc[df_index, chave] = valor
    
    # Retorna o registro atualizado (código 200 OK)
    return jsonify(dados[index]), 200

# Rota D - DELETE (Deleção)
@app.route('/api/unidades/<int:id>', methods=['DELETE'])
def deletar_unidade(id):
    global df # pra mudar o DataFrame
    global dados # pra mudar a lista de dados

    # Acha o índice do registro
    index = next((i for i, registro in enumerate(dados) if registro['id'] == id), None)

    if index is None:
        return jsonify({"message": f"Unidade com id {id} não encontrada."}), 404

    # Remove da lista 'dados'
    registro_deletado = dados.pop(index)

    # Remove do DataFrame
    df_index = df[df['id'] == id].index
    if not df_index.empty:
        df = df.drop(df_index)

    # Retorna mensagem de sucesso (código 200 OK)
    return jsonify({"message": f"Unidade com id {id} removida com sucesso.", "deletado": registro_deletado.get('Card', 'Registro sem nome')}), 200


if __name__ == '__main__':
    # Roda o servidor na porta 5000 (padrão do exercício)
    app.run(debug=True)