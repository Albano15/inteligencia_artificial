import matplotlib
matplotlib.use('Agg')   # backend sem janelas (gera arquivos PNG)
import matplotlib.pyplot as plt
import networkx as nx
from collections import deque
import heapq

# Criar os grafos
G_game = nx.Graph()

# Criar o mapa
locais = {
    'Castelo do heroi': (50, 400),
    'Vila dos Elfos': (110, 450),
    'Floresta dos desafios': (100, 300),
    'Glassard Cay': (20, 250),
    'Stamkasing Isle': (175, 500),
    'Bonafail Cay': (250, 200),
    'Belllams Holm': (100, 50),
    'Walllants Reef': (175, 430),
    'Depar Holm': (300, 500),
    'Flemdwell Key': (275, 325),
    'Caminho da Bruxa': (375, 200),
    'Caverna da Bruxa': (500, 450),
}

# Conexões entre os nós (Arestas)
G_game.add_edge('Castelo do heroi', 'Vila dos Elfos', weight=10)
G_game.add_edge('Castelo do heroi', 'Floresta dos desafios', weight=15)
G_game.add_edge('Vila dos Elfos', 'Glassard Cay', weight=20)
G_game.add_edge('Floresta dos desafios', 'Glassard Cay', weight=25)
G_game.add_edge('Floresta dos desafios', 'Stamkasing Isle', weight=12)
G_game.add_edge('Stamkasing Isle', 'Bonafail Cay', weight=17)
G_game.add_edge('Stamkasing Isle', 'Vila dos Elfos', weight=35)
G_game.add_edge('Glassard Cay', 'Belllams Holm', weight=16)
G_game.add_edge('Belllams Holm', 'Walllants Reef', weight=20)
G_game.add_edge('Belllams Holm', 'Depar Holm', weight=10)
G_game.add_edge('Walllants Reef', 'Depar Holm', weight=15)
G_game.add_edge('Depar Holm', 'Flemdwell Key', weight=10)
G_game.add_edge('Flemdwell Key', 'Caminho da Bruxa', weight=15)
G_game.add_edge('Caminho da Bruxa', 'Caverna da Bruxa', weight=20)
G_game.add_edge('Bonafail Cay','Caverna da Bruxa', weight=40)

# Adicionando as posições nos eixos X e Y
for local, pos in locais.items():
    G_game.nodes[local]['pos'] = pos

# Função Plot Mapa
def plot_mapa(grafo, caminho_encontrado, titulo='Mapa do reino'):
    pos = nx.get_node_attributes(grafo, 'pos')
    pesos = nx.get_edge_attributes(grafo, 'weight')

    plt.figure(figsize=(15, 10))

    # Labels com quebra de linha para caber melhor
    labels = {node: node.replace(' ', '\n') for node in grafo.nodes()}

    # Cor dos nós: vermelho se estiver no caminho, senão cinza claro
    node_colors = ['red' if (caminho_encontrado and node in caminho_encontrado) else 'lightgray' for node in grafo.nodes()]

    # Desenha nós (sem labels por enquanto)
    nx.draw_networkx_nodes(grafo, pos, node_size=1000, node_color=node_colors)

    # Desenha todas as arestas em cinza claro
    nx.draw_networkx_edges(grafo, pos, width=1.0, alpha=0.6, edge_color='lightgray')

    # Se houver caminho, desenha as arestas do caminho em vermelho e mais grossas
    if caminho_encontrado and len(caminho_encontrado) >= 2:
        path_edges = list(zip(caminho_encontrado, caminho_encontrado[1:]))
        nx.draw_networkx_edges(grafo, pos, edgelist=path_edges, width=3.5, edge_color='red')
        print("Existe um caminho e foi destacado em vermelho.")
    else:
        print("Nenhum caminho para destacar.")

    # Desenha labels (com caixa leve)
    nx.draw_networkx_labels(grafo, pos, labels=labels, font_size=10, font_weight='bold',
                            bbox=dict(facecolor='lightblue', alpha=0.5, edgecolor='none', boxstyle='round,pad=0.2'))

    # Desenha os pesos das arestas
    nx.draw_networkx_edge_labels(grafo, pos, edge_labels=pesos, font_size=8, label_pos=0.5)

    plt.title(titulo)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig("mapa.png")
    print("Arquivo salvo: mapa.png")


# Função BFS
def bfs_game(grafo, inicio, objetivo):
    visitados = set()
    fila = deque([(inicio, [inicio], 0)])  # nó, caminho até aqui, custo até aqui

    while fila:
        no_atual, caminho, custo_total = fila.popleft()

        if no_atual == objetivo:
            return caminho, custo_total

        if no_atual not in visitados:
            visitados.add(no_atual)
            for vizinho in grafo[no_atual]:
                if vizinho not in visitados:
                    novo_custo = custo_total + grafo[no_atual][vizinho]['weight']
                    novo_caminho = list(caminho)
                    novo_caminho.append(vizinho)
                    fila.append((vizinho, novo_caminho, novo_custo))
    return None, float('inf')


# Teste do BFS
inicio_heroi = 'Castelo do heroi'
objetivo_heroi = 'Caverna da Bruxa'
caminho_bfs, custo_bfs = bfs_game(G_game, inicio_heroi, objetivo_heroi)

if caminho_bfs:
    print(f"Caminho encontrado: {caminho_bfs}")
    print(f"Custo total: {custo_bfs}")
else:
    print("Deu errado - nenhum caminho encontrado")

# Gera o mapa com o caminho encontrado destacado
plot_mapa(G_game, caminho_bfs, titulo='Mapa do Reino - Caminho do Herói')

## Busca Gulosa