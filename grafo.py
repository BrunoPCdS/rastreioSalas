Grafo = dict[str, list[tuple[str, int]]]


def carregar_grafo(caminho: str = "arestas.txt") -> Grafo:
    grafo: Grafo = {}

    with open(caminho, encoding="utf-8") as arq:
        for linha in arq:
            if not linha.strip():
                continue

            a, b, peso = linha.split()
            peso = int(peso)
            grafo.setdefault(a, []).append((b, peso))
            grafo.setdefault(b, []).append((a, peso))

    return grafo


def numero_de_arestas(grafo: Grafo) -> int:
    return sum(len(vizinhos) for vizinhos in grafo.values()) // 2


if __name__ == "__main__":
    grafo = carregar_grafo()
    print(f"Portas: {len(grafo)}")
    print(f"Arestas: {numero_de_arestas(grafo)}")
    print(f"Vizinhos de A: {grafo}")
