import os
import time
import numpy as np
import matplotlib.pyplot as plt
import heapq
import random

# --- Funções do Algoritmo A* (Mantidas) ---

def heuristica(a, b):
    """Heurística de Distância de Manhattan."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star_grid(grid, start, goal):
    """
    Implementação do Algoritmo A* com medição de desempenho.
    Retorna: (path, path_length, time_taken, nodes_explored)
    """
    start_time = time.time()
    rows, cols = len(grid), len(grid[0])
    open_heap = [(0, start)]
    came_from = {}
    g_score = {start: 0}
    nodes_explored = 0

    while open_heap:
        f, current = heapq.heappop(open_heap)
        nodes_explored += 1 
        
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            
            end_time = time.time()
            time_taken = end_time - start_time
            path_length = len(path) - 1
            
            return path[::-1], path_length, time_taken, nodes_explored 

        for dx, dy in [(0,1), (0,-1), (1,0), (-1,0)]:
            neighbor = (current[0]+dx, current[1]+dy)
            
            if (0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols
                and grid[neighbor[0]][neighbor[1]] == 0):
                
                tentative_g = g_score[current] + 1
                
                if tentative_g < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f = tentative_g + heuristica(neighbor, goal)
                    heapq.heappush(open_heap, (f, neighbor))
    
    end_time = time.time()
    time_taken = end_time - start_time
    return None, 0, time_taken, nodes_explored


# --- Funções de Criação de Cenários ---

def create_scenario_random(size, obs_density, seed, name):
    """Cria um cenário aleatório (mantido do código original)."""
    np.random.seed(seed)
    grid = np.zeros((size, size))
    grid[np.random.rand(size, size) < obs_density] = 1 

    free_cells = list(zip(*np.where(grid == 0)))
    if len(free_cells) < 2:
         return None, name, "Células insuficientes"
         
    start = random.choice(free_cells)
    goal = random.choice(free_cells)
    while goal == start:
        goal = random.choice(free_cells)
        
    grid[start] = 0
    grid[goal] = 0
    return grid, start, goal, name

def create_scenario_dense_labyrinth(size, name):
    """Cenário 1: O Labirinto Densa (30% obstáculos)."""
    return create_scenario_random(size, 0.3, 100, name) 

def create_scenario_bottleneck(size, name):
    """Cenário 2: O Gargalo (Caminho estreito)."""
    grid = np.zeros((size, size))
    grid[:, size//2 - 2] = 1
    grid[:, size//2 + 2] = 1
    grid[size//2 - 5:size//2 + 5, size//2 - 2] = 0
    grid[size//2 - 5:size//2 + 5, size//2 + 2] = 0
    
    start = (size//2, 1)
    goal = (size//2, size - 2)
    return grid, start, goal, name

def create_scenario_dead_end(size, name):
    """
    Cenário 3: O Poço Sem Saída.
    Força o A* a explorar o beco, pois ele parece ser o caminho mais curto.
    """
    grid = np.zeros((size, size))
    
    # 1. Definir o beco sem saída (Dead End)
    BECK_WIDTH = size // 5
    BECK_START_COL = size // 4
    
    # Parede superior e inferior do beco
    grid[size // 4, BECK_START_COL:BECK_START_COL + BECK_WIDTH] = 1
    grid[size * 3 // 4, BECK_START_COL:BECK_START_COL + BECK_WIDTH] = 1
    
    # Parede de fundo do beco (fecha)
    grid[size // 4 : size * 3 // 4, BECK_START_COL + BECK_WIDTH - 1] = 1
    
    # 2. Criar a passagem lateral (o caminho ideal)
    # Abre um espaço na parede superior para o caminho contornar por cima
    grid[size // 8, size//2] = 0
    grid[size // 8, size//2 - 1] = 0

    # 3. Definir Start e Goal
    # Start: Na entrada do beco (parece ser o caminho mais direto)
    start = (size // 2, BECK_START_COL - 1)
    
    # Goal: Longe, além da parede de fundo (BECK_START_COL + BECK_WIDTH)
    goal = (size // 2, BECK_START_COL + BECK_WIDTH + 5)
    
    # Garantir que Start e Goal não sejam obstáculos
    grid[start[0], start[1]] = 0
    grid[goal[0], goal[1]] = 0
    
    return grid, start, goal, name

def create_scenario_unreachable(size, name):
    """Cenário 4: Inalcançável (Barreira sólida)."""
    grid = np.zeros((size, size))
    grid[:, size//2] = 1
    start = (size//4, size//2 - 1)
    goal = (size//4, size//2 + 1)
    return grid, start, goal, name

# --- Execução e Visualização (Mantidas) ---

def run_test_scenario(scenario_func, size, name):
    """Executa o A* para um dado cenário e retorna os resultados."""
    grid, start, goal, _ = scenario_func(size, name)
    
    grid_list = grid.tolist()
    grid_list[start[0]][start[1]] = 0
    grid_list[goal[0]][goal[1]] = 0
    
    path, length, time_t, explored = a_star_grid(grid_list, start, goal)
    
    results = {
        "Nome": name,
        "Caminho": path,
        "Tamanho da Grade": size,
        "Início": start,
        "Fim": goal,
        "Comprimento do Caminho (L)": length,
        "Tempo de Execução (T)": time_t,
        "Nós Explorados (NE)": explored,
        "Grid": grid
    }
    return results

def visualize_results(all_results, filename):
    """Gera o gráfico e imprime a tabela de resultados."""
    num_scenarios = len(all_results)
    fig, axes = plt.subplots(1, num_scenarios, figsize=(5 * num_scenarios, 6))

    if num_scenarios == 1:
        axes = [axes]

    for idx, res in enumerate(all_results):
        g = res["Grid"]
        path = res["Caminho"]
        start = res["Início"]
        goal = res["Fim"]

        axes[idx].imshow(g, cmap='gray_r', origin='upper')
        
        if path:
            y, x = zip(*path)
            axes[idx].plot(x, y, color='blue', linewidth=1)
        
        axes[idx].scatter(start[1], start[0], c='grey', s=50, label='Start')
        axes[idx].scatter(goal[1], goal[0], c='green', s=50, label='Goal')
        
        title = f"{res['Nome']}\nL={res['Comprimento do Caminho (L)'] or 'N/A'}, T={res['Tempo de Execução (T)']:.4f}s"
        axes[idx].set_title(title, fontsize=10)
        axes[idx].axis('off')

    plt.tight_layout()
    output_file = os.path.join(os.getcwd(), filename)
    plt.savefig(output_file, dpi=150)
    print(f"\nImagem salva em: {output_file}")


def print_metrics_table(all_results):
    """Imprime uma tabela formatada com os resultados."""
    print("\n" + "="*80)
    print("                      RESUMO DAS MÉTRICAS DO ALGORITMO A*")
    print("="*80)
    
    header = f"| {'Cenário':<20} | {'Tamanho':<10} | {'L (Passos)':<12} | {'T (Segundos)':<12} | {'NE (Nós Expl.)':<16} |"
    print(header)
    print("-" * 80)
    
    for res in all_results:
        length = res["Comprimento do Caminho (L)"]
        if length == 0 and res["Caminho"] is None:
             length_str = "INALCANÇÁVEL"
        else:
             length_str = str(length)

        row = f"| {res['Nome']:<20} | {res['Tamanho da Grade']:<10} | {length_str:<12} | {res['Tempo de Execução (T)']:.6f}s | {res['Nós Explorados (NE)']:<16} |"
        print(row)
    print("="*80)

# --- Execução Principal ---

if __name__ == "__main__":
    
    GRID_SIZE = 50 
    
    scenarios_to_test = [
        lambda size, name: create_scenario_random(size, 0.2, 42, "Aleatório Simples 1"),
        lambda size, name: create_scenario_dense_labyrinth(size, "Labirinto Densa"),
        lambda size, name: create_scenario_bottleneck(size, "Gargalo (Bottleneck)"),
        lambda size, name: create_scenario_dead_end(size, "Poço Sem Saída"),
        lambda size, name: create_scenario_unreachable(size, "Inalcançável"),
    ]

    all_results = []

    for scenario_func in scenarios_to_test:
        name = scenario_func(GRID_SIZE, "Placeholder")[3] 
        print(f"Executando teste: {name}...")
        results = run_test_scenario(scenario_func, GRID_SIZE, name)
        all_results.append(results)

    print_metrics_table(all_results)
    visualize_results(all_results, "a_star_test_scenarios.png")