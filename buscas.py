from collections import deque
import heapq

from grafo import carregar_grafo


def bfs(grafo, origem, destino):
    fila = deque([origem])
    anterior = {origem: None}
    custo = {origem: 0}
    visitados = 0

    while fila:
        atual = fila.popleft()
        visitados += 1
        if atual == destino:
            break

        for vizinho, peso in grafo[atual]:
            if vizinho in anterior:
                continue
            anterior[vizinho] = atual
            custo[vizinho] = custo[atual] + peso
            fila.append(vizinho)

    return montar_resultado(anterior, origem, destino, custo, visitados)


def dfs(grafo, origem, destino):
    pilha = [origem]
    anterior = {origem: None}
    custo = {origem: 0}
    visitados = 0

    while pilha:
        atual = pilha.pop()
        visitados += 1
        if atual == destino:
            break

        for vizinho, peso in reversed(grafo[atual]):
            if vizinho in anterior:
                continue
            anterior[vizinho] = atual
            custo[vizinho] = custo[atual] + peso
            pilha.append(vizinho)

    return montar_resultado(anterior, origem, destino, custo, visitados)


def criar_heuristica(grafo, destino):
    """Calcula a distância, em número de arestas, até o destino."""
    reverso = {no: [] for no in grafo}
    for no, vizinhos in grafo.items():
        for vizinho, _ in vizinhos:
            reverso.setdefault(vizinho, []).append(no)

    distancias = {destino: 0}
    fila = deque([destino])
    while fila:
        atual = fila.popleft()
        for vizinho in reverso.get(atual, []):
            if vizinho in distancias:
                continue
            distancias[vizinho] = distancias[atual] + 1
            fila.append(vizinho)

    return distancias


def gulosa(grafo, origem, destino):
    atual = origem
    anterior = {origem: None}
    custo = {origem: 0}
    visitados = 0
    heuristica = criar_heuristica(grafo, destino)

    while True:
        visitados += 1
        if atual == destino:
            break

        candidatos = [
            (heuristica.get(vizinho, float("inf")), peso, vizinho)
            for vizinho, peso in grafo[atual]
            if vizinho not in anterior
        ]
        if not candidatos:
            return [], None, visitados

        _, peso, proximo = min(candidatos)
        anterior[proximo] = atual
        custo[proximo] = custo[atual] + peso
        atual = proximo

    return montar_resultado(anterior, origem, destino, custo, visitados)


def dijkstra(grafo, origem, destino):
    distancia = {ponto: float("inf") for ponto in grafo}
    anterior = {origem: None}
    distancia[origem] = 0
    fila = [(0, origem)]
    finalizadas = set()

    while fila:
        custo_atual, atual = heapq.heappop(fila)
        if atual in finalizadas:
            continue

        finalizadas.add(atual)
        if atual == destino:
            break

        for vizinho, peso in grafo[atual]:
            novo_custo = custo_atual + peso
            if novo_custo < distancia[vizinho]:
                distancia[vizinho] = novo_custo
                anterior[vizinho] = atual
                heapq.heappush(fila, (novo_custo, vizinho))

    if destino not in anterior:
        return [], None, len(finalizadas)

    return montar_resultado(
        anterior, origem, destino, distancia, len(finalizadas)
    )


def montar_resultado(anterior, origem, destino, custo, visitados):
    if destino not in anterior:
        return [], None, visitados

    caminho = []
    atual = destino
    while atual is not None:
        caminho.append(atual)
        atual = anterior[atual]

    caminho.reverse()
    return caminho, custo[destino], visitados


if __name__ == "__main__":
    grafo = carregar_grafo()
    origem = "LABTEC"
    destino = "SAIDA_ANEXO"

    for nome, busca in (
        ("BFS", bfs),
        ("DFS", dfs),
        ("Gulosa", gulosa),
        ("Dijkstra", dijkstra),
    ):
        caminho, custo, visitados = busca(grafo, origem, destino)
        print(nome, caminho,"peso percorrido (passos):", custo, "locais visitados:", visitados)
