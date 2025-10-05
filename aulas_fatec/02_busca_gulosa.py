import math
import matplotlib
matplotlib.use('Agg')   # backend sem janelas
import matplotlib.pyplot as plt
import networkx as nx
import heapq

# --- Montagem do grafo original (arestas com pesos dados) ---
G_game = nx.Graph()

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

for nome, pos in locais.items():
    G_game.add_node(nome, pos=pos)

# arestas originais (weights "custos" definidos por você)
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

# --- utilitários ---
def euclid(a, b):
    pa = G_game.nodes[a]['pos']
    pb = G_game.nodes[b]['pos']
    return math.hypot(pa[0] - pb[0], pa[1] - pb[1])

def custo_por_pesos(grafo, caminho):
    """Soma dos weights das arestas ao longo do caminho (assume caminho lista de nós)."""
    if not caminho or len(caminho) < 2:
        return 0.0
    total = 0.0
    for a, b in zip(caminho, caminho[1:]):
        total += grafo[a][b].get('weight', 0.0)
    return total

def custo_euclidiano_along_path(grafo, caminho):
    """Soma das distâncias euclidianas entre nós consecutivos do caminho."""
    if not caminho or len(caminho) < 2:
        return 0.0
    total = 0.0
    for a, b in zip(caminho, caminho[1:]):
        pa = grafo.nodes[a]['pos']
        pb = grafo.nodes[b]['pos']
        total += math.hypot(pa[0]-pb[0], pa[1]-pb[1])
    return total

# --- Plot padrão que você pediu (igual ao anterior) ---
def plot_mapa_path(grafo, caminho_encontrado=None, titulo='Mapa do reino', arquivo_saida='mapa.png'):
    pos = nx.get_node_attributes(grafo, 'pos')
    pesos = nx.get_edge_attributes(grafo, 'weight')

    plt.figure(figsize=(15, 10))
    labels = {node: node.replace(' ', '\n') for node in grafo.nodes()}

    # Cor dos nós: vermelho se estiver no caminho, senão cinza claro
    node_colors = ['red' if (caminho_encontrado and node in caminho_encontrado) else 'lightgray' for node in grafo.nodes()]

    # Desenha nós e arestas de base
    nx.draw_networkx_nodes(grafo, pos, node_size=1000, node_color=node_colors)
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
    plt.savefig(arquivo_saida)
    print(f"Arquivo salvo: {arquivo_saida}")
    plt.close()

# --- Busca Gulosa (Greedy Best-First) sobre o grafo original ---
def busca_gulosa(grafo, inicio, objetivo):
    """Greedy best-first: prioridade = heuristica(estado, objetivo). Retorna caminho (ou None)."""
    visited = set()
    pq = []
    # (prioridade, nó_atual, caminho)
    heapq.heappush(pq, (euclid(inicio, objetivo), inicio, [inicio]))

    while pq:
        pri, nodo, caminho = heapq.heappop(pq)
        if nodo == objetivo:
            return caminho
        if nodo in visited:
            continue
        visited.add(nodo)
        for viz in grafo[nodo]:
            if viz not in visited:
                novo_caminho = caminho + [viz]
                heapq.heappush(pq, (euclid(viz, objetivo), viz, novo_caminho))
    return None

# --- Funções pré-existentes: linha reta direta e grafo completo / A* (mantive elas) ---
def plot_mapa_com_linha_direta(grafo, inicio, destino, arquivo_saida='mapa_direto.png'):
    pos = nx.get_node_attributes(grafo, 'pos')
    pesos = nx.get_edge_attributes(grafo, 'weight')

    plt.figure(figsize=(14,9))
    labels = {n: n.replace(' ', '\n') for n in grafo.nodes()}

    # desenha nós
    node_colors = ['lightgray' for _ in grafo.nodes()]
    nx.draw_networkx_nodes(grafo, pos, node_size=900, node_color=node_colors)

    # desenha arestas originais atenuadas (para referência)
    nx.draw_networkx_edges(grafo, pos, width=1.0, alpha=0.4, edge_color='gray')

    # desenha labels e pesos (opcionais)
    nx.draw_networkx_labels(grafo, pos, labels=labels, font_size=10, font_weight='bold',
                            bbox=dict(facecolor='lightblue', alpha=0.5, edgecolor='none', boxstyle='round,pad=0.2'))
    nx.draw_networkx_edge_labels(grafo, pos, edge_labels=pesos, font_size=7, label_pos=0.5)

    # linha reta direta entre inicio e destino (destaca: cor vermelha)
    p_ini = pos[inicio]
    p_dst = pos[destino]
    distancia_direta = math.hypot(p_ini[0]-p_dst[0], p_ini[1]-p_dst[1])

    # desenha a linha (solid, mais grossa)
    plt.plot([p_ini[0], p_dst[0]], [p_ini[1], p_dst[1]], color='red', linewidth=3, linestyle='-')

    # destaca os nós inicio/destino em vermelho
    nx.draw_networkx_nodes(grafo, pos, nodelist=[inicio, destino], node_size=1100, node_color='red')

    # anota o custo (distância) próximo ao meio da linha
    meio_x = (p_ini[0] + p_dst[0]) / 2.0
    meio_y = (p_ini[1] + p_dst[1]) / 2.0
    plt.text(meio_x, meio_y, f'{distancia_direta:.2f}', fontsize=12, fontweight='bold', color='black',
             bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', boxstyle='round,pad=0.2'))

    plt.title(f'Linha reta entre \"{inicio}\" e \"{destino}\" — custo (euclid) = {distancia_direta:.2f}')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(arquivo_saida)
    print(f"Gerado: {arquivo_saida} (distância direta = {distancia_direta:.2f})")
    plt.close()

def criar_grafo_completo_e_astar(grafo_original, inicio, destino, arquivo_saida='mapa_grafo_completo.png'):
    # monta grafo completo (cada par de nós conectado com peso = distância euclidiana)
    Gc = nx.Graph()
    pos = nx.get_node_attributes(grafo_original, 'pos')
    for n, p in pos.items():
        Gc.add_node(n, pos=p)
    nodes = list(Gc.nodes())
    for i in range(len(nodes)):
        for j in range(i+1, len(nodes)):
            a = nodes[i]; b = nodes[j]
            d = math.hypot(pos[a][0]-pos[b][0], pos[a][1]-pos[b][1])
            Gc.add_edge(a, b, weight=d)

    # heurística euclidiana
    def h(u, v):
        pu = Gc.nodes[u]['pos']; pv = Gc.nodes[v]['pos']
        return math.hypot(pu[0]-pv[0], pu[1]-pv[1])

    try:
        caminho = nx.astar_path(Gc, inicio, destino, heuristic=h, weight='weight')
        custo = nx.astar_path_length(Gc, inicio, destino, heuristic=h, weight='weight')
        print("A* no grafo completo — caminho:", caminho)
        print("Custo (A* no completo):", custo)
    except nx.NetworkXNoPath:
        print("A* no grafo completo: nenhum caminho encontrado")
        caminho = []
        custo = float('inf')

    # plot — se o caminho for direto entre inicio e destino, a aresta será desenhada automaticamente porque existe no grafo completo
    pos = nx.get_node_attributes(Gc, 'pos')
    plt.figure(figsize=(14,9))
    labels = {n: n.replace(' ', '\n') for n in Gc.nodes()}
    nx.draw_networkx_nodes(Gc, pos, node_size=900, node_color='lightgray')
    # todas as arestas do grafo completo em alpha baixo
    nx.draw_networkx_edges(Gc, pos, width=0.7, alpha=0.2, edge_color='gray')

    # destaca arestas do caminho A* (se houver)
    if caminho and len(caminho) >= 2:
        path_edges = list(zip(caminho, caminho[1:]))
        nx.draw_networkx_edges(Gc, pos, edgelist=path_edges, width=3.5, edge_color='red')
    nx.draw_networkx_labels(Gc, pos, labels=labels, font_size=10, font_weight='bold',
                            bbox=dict(facecolor='lightblue', alpha=0.5, edgecolor='none', boxstyle='round,pad=0.2'))

    plt.title(f'A* sobre grafo completo — custo = {custo:.2f}')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(arquivo_saida)
    print(f"Gerado: {arquivo_saida}")
    plt.close()

# --- Execução: define inicio/destino e roda as opções ---
if __name__ == '__main__':
    inicio = 'Castelo do heroi'
    destino = 'Caminho da Bruxa'

    # 1) Desenhar a linha reta direta (opcional, mantém compatibilidade)
    plot_mapa_com_linha_direta(G_game, inicio, destino, arquivo_saida='mapa_direto.png')

    # 2) A* sobre grafo completo (opcional)
    criar_grafo_completo_e_astar(G_game, inicio, destino, arquivo_saida='mapa_grafo_completo.png')

    # 3) Busca Gulosa sobre o grafo original
    caminho_gulosa = busca_gulosa(G_game, inicio, destino)
    if caminho_gulosa:
        custo_weights = custo_por_pesos(G_game, caminho_gulosa)
        custo_euclid = custo_euclidiano_along_path(G_game, caminho_gulosa)
        print("\n--- Busca Gulosa (Greedy) ---")
        print("Caminho (gulosa):", caminho_gulosa)
        print(f"Custo total (soma dos weights): {custo_weights:.2f}")
        print(f"Distância euclidiana total ao longo do caminho: {custo_euclid:.2f}")

        # Plota o mapa no mesmo estilo do anterior e inclui custo no título
        titulo = f'Gulosa — custo weights={custo_weights:.2f} | euclid_total={custo_euclid:.2f}'
        plot_mapa_path(G_game, caminho_encontrado=caminho_gulosa, titulo=titulo, arquivo_saida='mapa_gulosa.png')
    else:
        print("Gulosa - Nenhum caminho encontrado")
