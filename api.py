from pathlib import Path

from fastapi import FastAPI, HTTPException, Query

from buscas import bfs, dfs, dijkstra, gulosa
from grafo import carregar_grafo


app = FastAPI(title="API de Rotas")
grafo = carregar_grafo(str(Path(__file__).with_name("arestas.txt")))

BUSCAS = {
    "bfs": bfs,
    "dfs": dfs,
    "gulosa": gulosa,
    "dijkstra": dijkstra,
}


def validar_portas(*portas):
    for porta in portas:
        if porta not in grafo:
            raise HTTPException(
                status_code=404,
                detail=f"Porta não encontrada: {porta}",
            )


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


@app.get("/portas")
def listar_portas():
    return {"portas": sorted(grafo)}


@app.get("/vizinhos/{porta}")
def listar_vizinhos(porta: str):
    validar_portas(porta)
    return {
        "porta": porta,
        "vizinhos": [
            {"porta": vizinho, "peso": peso}
            for vizinho, peso in grafo[porta]
        ],
    }


@app.get("/rota")
def buscar_rota(
    origem: str,
    destino: str,
    algoritmo: str = Query("bfs"),
):
    validar_portas(origem, destino)
    return executar_busca(origem, destino, algoritmo)


@app.get("/comparar")
def comparar_buscas(origem: str, destino: str):
    validar_portas(origem, destino)
    return {
        algoritmo: executar_busca(origem, destino, algoritmo)
        for algoritmo in BUSCAS
    }