import requests
import json

# URL base da API Flask
URL_BASE = "http://127.0.0.1:5000/api/unidades"

def imprimir_resposta(response, titulo="Resposta"):
    """Função auxiliar para imprimir o resultado de forma legível."""
    print(f"\n{'='*50}")
    print(f"[{titulo} - Status: {response.status_code}]")
    try:
        # Tenta imprimir o JSON de resposta
        print(json.dumps(response.json(), indent=4, ensure_ascii=False))
    except requests.exceptions.JSONDecodeError:
        # Se não for JSON, imprime o texto (erros 404/400, etc.)
        print(response.text)
    print("="*50)


# 1. TESTE DE INSERÇÃO (POST - CREATE)
def testar_insercao():
    print("--- 1. TESTE DE INSERÇÃO (POST) ---")
    
    # JSON do novo registro para inserir
    novo_registro = {
        "Card": "Poste Teste",
        "Card Level (Spawn Level)": None, 
        "Cost": 5.0,
        "Count": "1",
        "Crown Tower Damage": None, 
        "Damage": "211",
        "Damage per second": "140",
        "Death Damage": 0.0,
        "Health (+Shield)": "3,344",
        "Hit Speed": "1.5",
        "Level": 7.0,
        "Maximum Spawned": None, 
        "Radius": None, 
        "Range": "0",
        "Spawn DPS": None, 
        "Spawn Damage": None, 
        "Spawn Health": None, 
        "Spawn Speed": None,
        "Spawner Health": None, 
        "Troop Spawned": None, 
        "Type": "Troops and Defenses",
    }

    response = requests.post(URL_BASE, json=novo_registro)
    
    imprimir_resposta(response, "POST - NOVO REGISTRO")
    
    if response.status_code == 201:
        return response.json().get('id')
    return None

# 2. TESTE DE CONSULTA GERAL (GET - READ)
def testar_consulta_geral():
    print("--- 2. TESTE DE CONSULTA GERAL (GET) ---")
    response = requests.get(URL_BASE)
    imprimir_resposta(response, "GET - GERAL")

# 3. TESTE DE CONSULTA TOP N (GET - REQUISITO B.1)
def testar_consulta_top_n(n=3):
    print(f"--- 3. TESTE DE CONSULTA TOP {n} (GET) ---")
    url_top_n = f"{URL_BASE}/top/{n}"
    response = requests.get(url_top_n)
    imprimir_resposta(response, f"GET - TOP {n}")

# 4. TESTE DE ATUALIZAÇÃO (PUT - UPDATE)
def testar_atualizacao(id_para_atualizar):
    if not id_para_atualizar:
        return
    
    print(f"--- 4. TESTE DE ATUALIZAÇÃO (PUT) - ID: {id_para_atualizar} ---")
    
    dados_atualizacao = {
        "Damage": "9999", 
        "Card": "Poste Teste - ATUALIZADO"
    }

    url_put = f"{URL_BASE}/{id_para_atualizar}"
    response = requests.put(url_put, json=dados_atualizacao)
    imprimir_resposta(response, f"PUT - ID {id_para_atualizar}")

# 5. TESTE DE FILTRO MÚLTIPLO (POST - REQUISITO B.3)
def testar_filtro_multiplo():
    print("--- 5. TESTE DE FILTRO MÚLTIPLO (POST) ---")
    
    filtro_json = {
        "Type": "Troops and Defenses",
        "Cost": 5.0
    }

    url_filtro = f"http://127.0.0.1:5000/api/unidades/filtro" 
    response = requests.post(url_filtro, json=filtro_json)
    imprimir_resposta(response, "POST - FILTRO MÚLTIPLO")

# 6. TESTE DE (DELETE - DELETE)
def testar_delecao(id_para_deletar):
    if not id_para_deletar:
        return
    
    print(f"--- 6. TESTE DE DELETE - ID: {id_para_deletar} ---")
    url_delete = f"{URL_BASE}/{id_para_deletar}"
    response = requests.delete(url_delete)
    imprimir_resposta(response, f"DELETE - ID {id_para_deletar}")



if __name__ == '__main__':
    
    # 1. TENTA INSERIR (C) e pega o ID
    novo_id = testar_insercao()
    
    # 2. SE CONSEGUIR O ID, EXECUTA TODOS OS TESTES EM SEQUÊNCIA
    if novo_id is not None:
        print(f"\n[SUCESSO] ID do novo registro para testes: {novo_id}")
        
        # CONSULTAS (R)
        testar_consulta_geral()
        testar_consulta_top_n(n=3)
        
        # ATUALIZAÇÃO (U)
        testar_atualizacao(novo_id)
        
        # FILTRO COMPLEXO (R)
        testar_filtro_multiplo()
        
        # DELETE (D)
        testar_delecao(novo_id)
    
        # ESTA MENSAGEM SÓ RODA DEPOIS DE TODAS AS FUNÇÕES ACIMA
        print("\n[FIM] Todos os testes de consumo concluídos.")
    else:
        print("\n[ERRO FATAL] Não foi possível obter um ID para testes. API falhou ou não está rodando.")