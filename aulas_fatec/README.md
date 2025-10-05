---

# Projetos de Inteligência Artificial

Este repositório contém diversos projetos e exemplos desenvolvidos em **Python** focados em Inteligência Artificial, como algoritmos de busca, sistemas de regras e outros.

## 🚀 Como Rodar o Projeto

O projeto é configurado para rodar em um contêiner **Docker** para garantir um ambiente de execução consistente, sem a necessidade de instalar as dependências diretamente no seu sistema.

### Pré-requisitos

Para rodar o projeto, você precisa ter o **Docker** e o **Docker Compose** instalados na sua máquina.

1. **Docker:** [Instalar o Docker](https://www.docker.com/products/docker-desktop/)
2. **Docker Compose:** Geralmente vem incluído no Docker em versões mais recentes.

### ⚙️ Inicialização do Ambiente

O ambiente é definido pelos arquivos `Dockerfile` e `docker-compose.yml`.

1. **Construa e Inicie o Contêiner:**
   Execute este comando no diretório raiz do projeto (onde estão o `docker-compose.yml` e seus arquivos Python). Ele irá construir a imagem e iniciar o serviço em segundo plano (`-d`).

   ```bash
   docker compose up -d
   ```
2. **Verifique se o Contêiner Está Rodando:**

   ```bash
   docker compose ps
   ```

---

## ▶️ Executando os Arquivos de Projeto

O comando de execução é flexível e permite que você rode **qualquer arquivo Python** que esteja no diretório, mesmo que adicione novos futuramente.

O serviço definido no seu `docker-compose.yml` é chamado de `sistema`. Usaremos o comando `docker compose run --rm` para rodar um arquivo de forma isolada, garantindo que o contêiner se encerre após a execução (`--rm`).

Para rodar **qualquer arquivo Python** no diretório:

1. **Substitua `<nome_do_arquivo.py>` pelo arquivo desejado** (por exemplo, `03_algoritmo_a_star.py`).

   ```bash
   docker compose run --rm sistema python <nome_do_arquivo.py>
   ```

   **Exemplo (para rodar o arquivo de Forward e Backward Chaining):**

   ```bash
   docker compose run --rm sistema python 04_forward_e_backward.py
   ```

### Lista de Arquivos Atualmente Disponíveis

| Nome do Arquivo              | Descrição                                                                                  |
| :--------------------------- | :------------------------------------------------------------------------------------------- |
| `01_busca_em_largura.py`   | Implementação de algoritmo de Busca em Largura (BFS).                                      |
| `02_busca_gulosa.py`       | Implementação de algoritmo de Busca Gulosa (Greedy Search).                                |
| `03_algoritmo_a_star.py`   | Implementação do Algoritmo A\*.                                                            |
| `04_forward_e_backward.py` | Exemplo de sistema de regras com encadeamento para frente (Forward) e para trás (Backward). |

---

## 🗑️ Parando e Removendo o Ambiente

Quando terminar de trabalhar e quiser liberar os recursos, execute este comando no diretório raiz:

```bash
docker compose down
```
