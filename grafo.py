# Define o tipo do grafo: cada local possui uma lista de vizinhos e pesos.
Grafo = dict[str, list[tuple[str, int]]]

# A função carregar_grafo lê um arquivo de texto contendo as conexões entre os locais e constrói o grafo correspondente.
"""
grafo: Grafo = {}  # Cria um dicionário vazio para armazenar o grafo.

with open(caminho, encoding="utf-8") as arq:
    # Abre o arquivo de conexões usando a codificação UTF-8.
for linha in arq:
    # Percorre o arquivo uma linha por vez.
if not linha.strip():
    continue  # Ignora linhas vazias.
a, b, peso = linha.split()
# Separa a linha em local de origem, local de destino e peso da conexão.

peso = int(peso)  # Converte o peso, que veio como texto, para número inteiro.

grafo.setdefault(a, []).append((b, peso))
# Adiciona b como vizinho de a com o peso da conexão.

grafo.setdefault(b, []).append((a, peso))
# Adiciona a como vizinho de b. Isso torna o grafo não direcionado.

Ao final, a função retorna o dicionário com todos os locais e suas conexões.
"""
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

# Ajusta a contagem de arestas em um grafo não direcionado, considerando que cada conexão repete.
"""
sum(len(vizinhos) for vizinhos in grafo.values())
# Conta todas as conexões armazenadas nas listas de vizinhos.

Como cada conexão é adicionada duas vezes no grafo não direcionado, uma vez
para cada sentido, o resultado é dividido por 2 para obter a quantidade real
de arestas.
"""
def numero_de_arestas(grafo: Grafo) -> int:
    return sum(len(vizinhos) for vizinhos in grafo.values()) // 2



# Esta parte carrega todo o grafo e exibe informações sobre ele quando o arquivo é executado diretamente.

"""
grafo = carregar_grafo()  # Carrega as conexões do arquivo arestas.txt.

len(grafo) # Conta quantos locais, ou portas, existem no grafo.
numero_de_arestas(grafo) # Conta quantas conexões existem entre os locais.

Os comandos print exibem no terminal a quantidade de portas, a quantidade de
arestas e o dicionário completo com os vizinhos de cada local.
"""
if __name__ == "__main__":
    grafo = carregar_grafo()  
    print(f"Portas: {len(grafo)}")  
    print(f"Arestas: {numero_de_arestas(grafo)}")  
    print(f"Vizinhos de A: {grafo}") 
