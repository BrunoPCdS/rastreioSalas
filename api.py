# Importa a classe Path para localizar o arquivo arestas.txt na mesma pasta
# deste arquivo, independentemente do local em que a API for executada.
from pathlib import Path

# Importa os recursos do FastAPI usados para criar a API, tratar erros HTTP
# e definir um parâmetro de consulta com valor padrão.
from fastapi import FastAPI, HTTPException, Query

# Importa as quatro funções de busca que serão disponibilizadas pela API.
from buscas import bfs, dfs, dijkstra, gulosa

# Importa a função responsável por ler o arquivo e montar o grafo do prédio.
from grafo import carregar_grafo


# Cria a aplicação FastAPI que disponibiliza as buscas por meio de endpoints.
# Carrega o arquivo de conexões localizado na mesma pasta deste arquivo.

app = FastAPI(title="API de Rotas")
grafo = carregar_grafo(str(Path(__file__).with_name("arestas.txt")))



# Serve para relacionar o nome recebido pela API à função de busca correspondente.

BUSCAS = {
    "bfs": bfs,
    "dfs": dfs,
    "gulosa": gulosa,
    "dijkstra": dijkstra,
}


# Esta parte é responsável por validar se as portas informadas existem no grafo antes de executar qualquer busca. Se alguma porta não existir, a função interrompe a requisição e retorna um erro HTTP 404 (Not Found) com uma mensagem indicando qual porta não foi encontrada.

"""
for porta in portas:
    # Percorre todas as portas recebidas pela rota.

if porta not in grafo:
    # Verifica se a porta existe no grafo carregado.

raise HTTPException(...)
# Interrompe a requisição e informa que a porta não foi encontrada.

Essa validação evita que a API tente executar uma busca usando locais
inexistentes e retorna ao cliente o código HTTP adequado.
"""
def validar_portas(*portas):
    for porta in portas:
        if porta not in grafo:
            raise HTTPException(
                status_code=404,
                detail=f"Porta não encontrada: {porta}",
            )


# Esta função é responsável por localizar a função de busca correspondente ao nome recebido na requisição, executar a busca no grafo e organizar os resultados em um formato padronizado para a resposta JSON.

"""
busca = BUSCAS.get(algoritmo.lower())
# Converte o nome para letras minúsculas e procura a função correspondente.

if busca is None:
    # Verifica se o algoritmo informado está disponível.

caminho, custo, visitados = busca(grafo, origem, destino)
# Executa o algoritmo escolhido usando a origem e o destino recebidos.

if not caminho:
    # Verifica se o algoritmo encontrou uma rota.

O dicionário retornado padroniza a resposta da API, informando o algoritmo
utilizado, o caminho encontrado, o custo em passos e os locais visitados.
"""
def executar_busca(origem, destino, algoritmo):
    busca = BUSCAS.get(algoritmo.lower())
    if busca is None:
        raise HTTPException(
            status_code=400,
            detail=(
                "Algoritmo inválido. Use: "
                "bfs, dfs, gulosa ou dijkstra"
            ),
        )

    caminho, custo, visitados = busca(grafo, origem, destino)
    if not caminho:
        raise HTTPException(
            status_code=404,
            detail=f"Não existe rota entre {origem} e {destino}",
        )

    return {
        "algoritmo": algoritmo.lower(),
        "caminho": caminho,
        "custo": custo,
        "unidade": "passos",
        "visitados": visitados,
    }


# esta parte define as rotas da API, que são os caminhos que o usuário pode acessar para interagir com o grafo e executar as buscas. Cada rota é associada a uma função que processa a requisição e retorna uma resposta.


"""
@app.get("/portas")
# Define que a função responderá às requisições GET feitas no endereço /portas.

sorted(grafo)
# Organiza os nomes das portas em ordem alfabética para facilitar a consulta.

"""

@app.get("/portas")
def listar_portas():
    return {"portas": sorted(grafo)}


# Esta rota permite consultar os vizinhos de uma porta específica, ou seja, os locais que estão diretamente conectados a ela. A função retorna um dicionário com o nome da porta consultada e uma lista de seus vizinhos, cada um representado por um dicionário contendo o nome do vizinho e o peso da ligação.

"""
@app.get("/vizinhos/{porta}")
# Cria uma rota GET com a porta recebida diretamente na URL.

validar_portas(porta)
# Confirma que a porta informada existe antes de consultar seus vizinhos.

Essa rota é útil para consultar a estrutura do grafo a partir de um local.
"""
@app.get("/vizinhos/{porta}")
def listar_vizinhos(porta: str):
    # Valida a porta recebida no caminho da requisição.
    validar_portas(porta)
    # Retorna a porta consultada e todos os seus vizinhos.
    return {
        "porta": porta,
        "vizinhos": [
            # Converte cada tupla (vizinho, peso) em um objeto JSON.
            {"porta": vizinho, "peso": peso}
            for vizinho, peso in grafo[porta]
        ],
    }

# Esta rota permite calcular uma rota entre dois locais usando um dos algoritmos de busca disponíveis. O usuário deve fornecer a origem e o destino como parâmetros obrigatórios da consulta, e pode opcionalmente especificar o algoritmo a ser usado. Se nenhum algoritmo for informado, o padrão será "bfs". A função valida se os locais existem no grafo antes de executar a busca e retorna o caminho encontrado, o custo em passos e a quantidade de locais visitados.

"""
@app.get("/rota")
# Define o endpoint que calcula uma rota entre dois locais.

"""

@app.get("/rota")
def buscar_rota(
    origem: str,
    destino: str,
    algoritmo: str = Query("bfs"),
):
    validar_portas(origem, destino)
    return executar_busca(origem, destino, algoritmo)

# Esta rota permite comparar os resultados de todos os algoritmos de busca disponíveis para encontrar uma rota entre dois locais. O usuário deve fornecer a origem e o destino como parâmetros obrigatórios da consulta. A função valida se os locais existem no grafo antes de executar as buscas e retorna um dicionário contendo os resultados de cada algoritmo, permitindo comparar caminhos, custos e quantidades de locais visitados.
"""
@app.get("/comparar")
# Define o endpoint que executa todos os algoritmos disponíveis.

"""
@app.get("/comparar")
def comparar_buscas(origem: str, destino: str):
    validar_portas(origem, destino)
    return {
        algoritmo: executar_busca(origem, destino, algoritmo)
        for algoritmo in BUSCAS
    }