from collections import deque
import heapq

from grafo import carregar_grafo


# A busca em largura (BFS) percorre o grafo por níveis, começando pela origem.
# A fila garante que os locais descobertos primeiro sejam processados antes dos
# locais dos níveis seguintes. O dicionário "anterior" registra o caminho e
# "custo" soma os pesos das conexões percorridas.

"""
fila = deque([origem])  # Inicia criando uma fila e colocando nela o primeiro local que será analisado.
anterior = {origem: None}  # Guarda que a origem não possui um local anterior no caminho.
custo = {origem: 0}  # Define o custo inicial da origem como zero.
visitados = 0  # Inicia o contador de locais retirados da fila para análise.

No laço while, enquanto ainda existirem locais aguardando análise, o algoritmo retira o primeiro local da fila, registra que ele foi analisado e verifica se é o destino. Se não for, percorre todos os vizinhos conectados ao local atual, ignorando aqueles que já foram descobertos. Para cada vizinho novo, registra o local atual como predecessor, soma o peso da conexão ao custo acumulado e coloca o vizinho no final da fila.

No for, percorre todos os vizinhos conectados ao local atual, ignorando aqueles que já foram descobertos. Para cada vizinho novo, registra o local atual como predecessor, soma o peso da conexão ao custo acumulado e coloca o vizinho no final da fila.

No final, a função monta o caminho percorrido usando os predecessores registrados, calcula o custo total e retorna o caminho, o custo e a quantidade de locais visitados.
"""

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


# A busca em profundidade (DFS) segue o caminho mais recente até não encontrar
# novos vizinhos. A pilha controla essa ordem e "anterior" evita visitar o
# mesmo local novamente, permitindo reconstruir o caminho ao final.


"""
pilha = [origem]  # Cria uma pilha e coloca nela a origem.
anterior = {origem: None}  # Guarda que a origem não possui um local anterior.
custo = {origem: 0}  # Define o custo inicial da origem como zero.
visitados = 0  # Inicia o contador de locais analisados.

No laço while, enquanto houver locais na pilha, o algoritmo retira o último
local inserido. Isso faz a busca seguir primeiro por um caminho mais profundo.
Depois, verifica se o local retirado é o destino. Caso não seja, percorre seus
vizinhos, ignora os que já foram descobertos, registra o predecessor, atualiza
o custo e coloca o novo vizinho na pilha.

O reversed faz os vizinhos serem inseridos na ordem inversa. Como a pilha
retira o último item inserido, isso ajuda a preservar a ordem original dos
vizinhos durante a busca.

No final, a função monta o caminho usando os predecessores e retorna o caminho,
o custo total e a quantidade de locais visitados.
"""

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



"""
reverso = {no: [] for no in grafo}  # Cria um grafo com as ligações invertidas.

O primeiro for percorre todos os locais e o segundo percorre seus vizinhos.
Para cada ligação, o local atual é armazenado como entrada do vizinho no
grafo reverso. Assim, é possível descobrir quais locais chegam a cada destino.

distancias = {destino: 0}  # A distância do destino até ele mesmo é zero.
fila = deque([destino])  # Inicia uma busca em largura a partir do destino.

Enquanto houver locais na fila, o algoritmo retira um local e visita os locais
que levam até ele. Cada novo local recebe a distância do atual mais uma aresta.
No final, retorna a quantidade de arestas até o destino para cada local.
Essa informação é usada como heurística pela busca gulosa.
"""


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


# A busca gulosa escolhe, a cada passo, o vizinho que parece estar mais perto
# do destino segundo a heurística. A heurística é calculada pela quantidade de
# arestas até o destino; por isso, o algoritmo pode chegar rapidamente ao fim,
# mas não garante o menor custo total quando os pesos são diferentes.

"""
atual = origem  # Começa a busca na origem.
anterior = {origem: None}  # Guarda que a origem inicia o caminho.
custo = {origem: 0}  # Define o custo inicial como zero.
heuristica = criar_heuristica(grafo, destino)  # Calcula a distância estimada.

No laço while, o algoritmo verifica se chegou ao destino. Caso ainda não tenha
chegado, cria uma lista com os vizinhos não visitados. Cada candidato recebe
três valores: a estimativa até o destino, o peso da conexão e o nome do local.

min(candidatos) escolhe o candidato com a menor estimativa. Em seguida, o
algoritmo registra o predecessor, soma o peso ao custo acumulado e avança para
o local escolhido. Como a busca considera primeiro a estimativa, ela pode não
encontrar a rota de menor custo total.
"""

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


# Dijkstra mantém uma fila de prioridade com os caminhos de menor custo
# conhecido. Sempre que encontra um caminho mais barato para um vizinho, ele
# atualiza a distância e o predecessor. Assim, com pesos não negativos, retorna
# a rota de menor custo total.

"""
distancia = {ponto: float("inf") for ponto in grafo}
# Inicializa todos os locais com custo infinito, pois ainda não foram alcançados.
anterior = {origem: None}  # A origem não possui predecessor.
distancia[origem] = 0  # O custo para sair da origem é zero.
fila = [(0, origem)]  # Cria a fila de prioridade com a origem.
finalizadas = set()  # Guarda os locais cujo menor custo foi confirmado.

Enquanto houver caminhos na fila, heapq.heappop retira o caminho de menor
custo. Se o local já foi finalizado, a entrada antiga é ignorada. Caso contrário,
o local é finalizado e seus vizinhos são analisados.

Para cada vizinho, novo_custo soma o custo atual ao peso da conexão. Se esse
valor for menor que o custo conhecido, a distância e o predecessor são
atualizados, e o novo caminho é inserido na fila com heapq.heappush.

Quando o destino é finalizado, o algoritmo pode parar. Como sempre escolhe o
menor custo conhecido, Dijkstra encontra a rota de menor custo com pesos não
negativos.
"""

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
