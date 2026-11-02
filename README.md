# Rotas do Prédio

Projeto da disciplina de Algoritmos e Estruturas de Dados II para encontrar
rotas em um prédio representado por um grafo.

## Integrantes

- Bruno Corrêa
- Lucas Rocha

## Estrutura do projeto

- `grafo.py`: carrega o grafo a partir do arquivo `arestas.txt`.
Este arquivo serve para montar o mapa do prédio em formato grafo.
Ou seja, ele abre o arquivo de arestas, lê cada ligalão entre duas portas, guarda em memória, Adiciona a ligação nos dois sentidos, e conta o numero de conexões.

exemplo: ENTRADA SECRETARIA 11
{
    "ENTRADA": [("SECRETARIA", 11)],
    "SECRETARIA": [("ENTRADA", 11)]
}




- `arestas.txt`: contém as conexões entre as portas e seus pesos.
documento onde fica gravado os dados do prédio.



- `buscas.py`: implementa BFS, DFS, busca gulosa e Dijkstra.
- `api.py`: disponibiliza os algoritmos por uma API FastAPI.

O grafo é não direcionado: cada conexão do arquivo pode ser percorrida nos
dois sentidos.

## Unidade do peso

O peso de cada conexão é um custo inteiro medido em **passos**. A soma dos
pesos das conexões percorridas é o custo total da rota. Esses pesos
representam uma unidade abstrata do mapa, e não uma medida em metros.

Por exemplo, a linha:

```text
ENTRADA SECRETARIA 11
```

indica que a conexão entre `ENTRADA` e `SECRETARIA` tem custo de 11 passos.

## Como executar

### Executar as buscas no terminal

Com o terminal aberto na pasta do projeto, execute:

```bash
python buscas.py
```

Esse comando compara os quatro algoritmos entre `LABTEC` e `SAIDA_ANEXO`.

Para consultar a quantidade de portas e conexões:

```bash
python grafo.py
```

### Executar a API

Instale as dependências, caso ainda não estejam instaladas:

```bash
pip install fastapi uvicorn
```

Inicie o servidor:

```bash
uvicorn api:app --reload
```

Depois, acesse a documentação interativa em:

<http://127.0.0.1:8000/docs>

Principais endpoints:

- `GET /portas`: lista todas as portas.
- `GET /vizinhos/{porta}`: mostra os vizinhos e os pesos de uma porta.
- `GET /rota?origem=LABTEC&destino=SAIDA_ANEXO&algoritmo=dijkstra`:
  calcula uma rota usando um algoritmo específico.
- `GET /comparar?origem=LABTEC&destino=SAIDA_ANEXO`: executa todos os
  algoritmos para a mesma origem e destino.

Os algoritmos disponíveis são `bfs`, `dfs`, `gulosa` e `dijkstra`.

## Exemplo de divergência entre BFS e Dijkstra

Um par de portas em que os algoritmos discordam é:

```text
Origem:  SAIDA_BIBLIOTECA
Destino: SAIDA_CANTINA
```

### BFS

```text
SAIDA_BIBLIOTECA -> ENTRADA_ANEXO -> SAIDA_CANTINA
Custo total: 127 passos
```

### Dijkstra

```text
SAIDA_BIBLIOTECA -> BIBLIOTECA -> SALA_PROFESSORES -> DIRECAO
-> LIDERANCA_ADMINISTRATIVA -> COORDENADORIA_PEDAGOGICA -> SECRETARIA_2
-> ALA_SECRETARIA -> BANHEIRO_MASCULINO -> BANHEIRO_FEMININO
-> SAIDA_PATIO_2 -> SALA203 -> SALA202 -> SALA201 -> LABTEC
-> SAIDA_PATIO_1 -> SAIDA_CANTINA
Custo total: 108 passos
```

O BFS encontra o caminho com menor quantidade de conexões, por isso escolhe
uma rota de apenas duas conexões, mas seu custo é 127 passos. O Dijkstra
considera os pesos e encontra a rota de menor custo total, mesmo que ela
tenha mais conexões: 108 passos. Portanto, BFS e Dijkstra podem retornar
caminhos diferentes quando as conexões possuem pesos diferentes.
