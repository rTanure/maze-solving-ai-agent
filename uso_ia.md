# Uso de IA no Projeto

## Contexto

Modelagem da classe `Maze`, manipulacao de arquivos e correcoes no menu de geracao em lote.

## Ferramentas utilizadas

- Google Gemini
- Codex (autocomplete)

## Principais prompts utilizados

- "TypeError: can't multiply sequence by non-int of type 'float'" [envio de codigo do metodo `create` e log de erro]
- "IndexError: index 1 is out of bounds for axis 0 with size 1" [envio de log de erro de execucao]
- "Esse randint esta deixando passar valor menor que o minHeight" [envio de codigo do `menu_gerar_labirintos_lotes`]
- "Por qu essa funcao nao acha caminho nos labirintos geraos:" [envio de codigo da funcao `bfs` e da classe `Maze`]
- "FAca com que ele salve no arquivo uma string mas quando montar a classe ele gere o vetor"
- "me fala apenas as linhas que eu tenho que mudar psl"
- "pq esse exit = true n funciona?" [envio de codigo do `menu_principal`]

## Trechos de codigo sugeridos por IA e correcoes solicitadas

### A. Tipagem e sanitizacao preventiva (`Maze.create`)

Inclusao de rotinas de conversao explicita de tipos no topo do metodo gerador para evitar que dados vindos da interface quebrassem os modulos nativos do Python:

```python
@classmethod
def create(cls, width, height, collectibles=0, cicles=0.1):
    # --- GARANTE A TIPAGEM CORRETA DOS INPUTS ---
    width = int(width)
    height = int(height)
    collectibles = int(collectibles)
    cicles = float(str(cicles).replace(',', '.'))
    # --------------------------------------------
```

### B. Trava de seguranca e tratamento de inputs (`menu_gerador.py`)

Desenvolvimento de logica de ordenacao e imposicao de limites minimos para evitar que o algoritmo gerador entrasse em colapso com dimensoes invalidas:

```python
# Correcao solicitada: evitar inversao de valores se digitados errados pelo usuario
if min_width > max_width:
    min_width, max_width = max_width, min_width
if min_height > max_height:
    min_height, max_height = max_height, min_height

# Correcao solicitada: impor barreira fisica para dimensoes funcionais minimas
if min_width < 5:
    min_width = 5
if max_width < 5:
    max_width = 5
if min_height < 5:
    min_height = 5
if max_height < 5:
    max_height = 5
```

### C. Ajuste estrutural de persistencia e instanciacao (`Maze.py`)

Modificacoes pontuais divididas nos metodos da classe para garantir o salvamento em modo texto plano (`str`) e a reconstrucao instantanea em formato de matriz (`list` de `list`) ao carregar.

No construtor (`__init__`):

```python
# Se receber uma string, por exemplo do arquivo de texto,
# converte em matriz de caracteres.
if isinstance(maze, str):
    self.maze = [list(linha) for linha in maze.split("\n") if linha]
else:
    self.maze = maze
```

No metodo de salvamento (`save_all`):

```python
# Converte a matriz interna de volta para string visual com quebras de linha
# ao gravar o arquivo fisico.
with open(caminho_txt, "w", encoding="utf-8") as arquivo_txt:
    if isinstance(maze.maze, list):
        string_labirinto = "\n".join(["".join(linha) for linha in maze.maze])
    else:
        string_labirinto = str(maze.maze)
    arquivo_txt.write(string_labirinto)
```

No metodo de fabrica (`open`):

```python
# Le o texto cru e reconstroi as linhas do vetor bidimensional de caracteres.
with open(caminho_txt, "r", encoding="utf-8") as arquivo_txt:
    conteudo_txt = arquivo_txt.read()
    maze_vetor = [list(linha) for list_linha in conteudo_txt.split("\n") if (linha := list_linha.strip())]
```

### D. Controle de escopo de menu em expressoes inline (`menu_principal.py`)

Substituicao da atribuicao ilegal de variavel interna em funcoes `lambda` por uma flag de retorno booleano ou interrupcao limpa:

```python
choices = {
    "Gerar em lote": lambda: (menu_gerar_labirintos_lotes(), False)[1],
    "Sair": lambda: True  # Retorna True indicando que deve encerrar o loop recursivo
}
deve_sair = choices.get(escolha, lambda: False)()
if not deve_sair:
    menu_principal()
```

## Sugestoes rejeitadas

Uso de tupla indexada estendida em menus: a IA sugeriu estruturar todas as chamadas do dicionario de menus utilizando a sintaxe `(funcao(), False)[1]`. O grupo rejeitou parte dessa padronizacao por considerar que o codigo perdia legibilidade e optou por isolar apenas a logica do encerramento ou utilizar modulos nativos como `sys.exit()`.

## Erros cometidos pela IA

### Instanciacao com incompatibilidade de tipos (`TypeError`)

A IA estruturou a recepcao dos dados do menu sem validar a tipagem. Com isso, strings ou decimais (`float`) coletados da interface foram repassados diretamente a funcao `random.sample(..., min(collectibles, ...))`, provocando um erro interno de multiplicacao de sequencias.

### Estouro de indice por sorteio em limite critico (`IndexError`)

A logica inicial da IA para forcar valores impares no gerador permitia que o `random.randint` definisse dimensoes finais iguais a 3. Em matrizes de tamanho 3, as checagens de vizinhos ultrapassavam o tamanho real da malha, gerando excecoes de eixos fora de limite (`axis 0 with size 1`) no Numpy.

### Corrupcao de tipo para algoritmos de busca

A IA converteu a matriz do labirinto em uma unica string continua persistida no atributo do objeto. Isso fez com que a funcao de busca em largura (`bfs`) falhasse, pois tentava varrer vizinhos usando indices bi-indexados `grid[y][x]` em uma estrutura linear de caracteres.

## Como o grupo validou a solucao

### Analise dirigida de tracebacks

Captura e leitura minuciosa dos logs de erro emitidos pelo interpretador Python no terminal para identificar os pontos de estouro de escopo e tipagem incorreta.

### Testes de caixa preta no console

Execucao sistematica do menu inserindo intencionalmente valores vazios, valores fora das faixas estipuladas e ranges invertidos, com minimo maior que maximo, para verificar o comportamento das travas e fallbacks.

### Auditoria de arquivos locais

Abertura e checagem visual direta do arquivo de tabelas `datasets/mazes.csv` e dos respectivos mapas gerados individualmente na pasta `datasets/mazes/` para validar a formatacao do texto e das tuplas de coordenadas salvos pela aplicacao.

## Modificacoes feitas pelo grupo

### Sanitizacao de strings monetarias/decimais

Inclusao de rotinas adaptativas `.replace(',', '.')` nas variaveis do tipo `float` no codigo antes de submete-las ao construtor para evitar quebras por digitacao regionalizada de virgulas.

### Implementacao de clausulas de barreira

Adicao manual de travas condicionais forcando um valor minimo estrito (`< 5`) para largura e altura dos labirintos no arquivo do menu, garantindo que o algoritmo de DFS do gerador sempre opere em dimensoes matematicamente seguras.

### Refatoracao no inicializador da classe

Modificacao no metodo `__init__` da classe `Maze` para introduzir uma validacao do tipo `isinstance(maze, str)`. Isso permitiu conferir inteligencia a classe, que passou a saber o momento exato em que deve quebrar strings de arquivos e transforma-las em vetores nativos.

---

## Contexto: Ajuste e formatacao de visualizacoes de dados

O objetivo desta interacao foi resolver problemas de layout, rotacao e visibilidade de rotulos (`labels`) em graficos de matrizes de transicao (`heatmaps`) gerados com Seaborn e Matplotlib no Python. O foco foi garantir a legibilidade das labels dos eixos e subplots sem comprometer a integridade e a exibicao dos dados estatisticos do projeto.

## Ferramenta utilizada nesta interacao

- Google Gemini

## Principais prompts utilizados nesta interacao

- "Como eu consigo colocar essa label da esquerda na horizontal?" [enviado junto com imagem inicial do codigo e dos graficos desalinhados]
- "O inicial ficou na horizontal mas o label do heatmap nao" [identificando que as categorias internas do eixo Y continuavam rotacionadas incorretamente]
- "Sumiu o label" [alerta de regressao visual apos tentativa de rotacao que causou o desaparecimento dos textos nos subplots compartilhados]

## Trechos de codigo sugeridos por IA e correcoes solicitadas nesta interacao

### Correcao 1: Alinhamento e rotacao da label geral do eixo Y (`ylabel`)

Problema: a label principal `"Inicial"` estava disposta verticalmente e colidindo visualmente com os textos das categorias do heatmap.

Codigo sugerido:

```python
ax.set_ylabel("Inicial" if lang == LANGS[0] else "", rotation=0, ha="right", labelpad=25)
```

Explicacao: o codigo rotaciona a label para a horizontal (`rotation=0`), ajusta a ancoragem a direita (`ha="right"`) para evitar sobreposicao e adiciona um espacamento (`labelpad=25`) para afastar o texto do grafico de forma limpa.

### Correcao 2: Rotacao das categorias internas do heatmap (`yticklabels`)

Problema: as labels especificas das linhas do heatmap, como `"Contrary"`, `"Favorable"` e `"Inconclusive"`, permaneciam na vertical.

Codigo sugerido:

```python
ax.set_yticklabels(ax.get_yticklabels(), rotation=0)
```

Explicacao: tentativa inicial de aplicar a rotacao diretamente nos marcadores textuais recuperados do eixo atual.

### Correcao 3: Correcao de sumico e fix de warnings do Matplotlib

Problema: devido ao uso de `sharey=True`, os subplots seguintes tinham labels vazias, o que causou o desaparecimento dos textos na tela. Alem disso, a modificacao direta de ticks sem fixar o formatador gerava avisos no console do Python.

Codigo sugerido:

```python
ax.set_yticks(ax.get_yticks())  # Fix para evitar o warning de FixedFormatter
ax.set_yticklabels(ax.get_yticklabels(), rotation=0, va="center")
```

Explicacao: a solucao fixa explicitamente as posicoes numericas do eixo Y antes de extrair e modificar as labels de texto, aplicando o alinhamento vertical centralizado (`va="center"`) para que todas as categorias voltem a aparecer alinhadas nos subplots correspondentes.

## Sugestoes rejeitadas nesta interacao

Nenhuma sugestao foi rejeitada neste chat. As abordagens propostas evoluiram sequencialmente conforme o comportamento do layout do Matplotlib era refinado pelo usuario.

## Erros cometidos pela IA nesta interacao

### Erro de estouro de escopo/efeito colateral

A IA falhou em prever, na segunda resposta, que o uso de `ax.get_yticklabels()` em uma figura configurada com compartilhamento de eixos (`sharey=True`) causaria o desaparecimento ou limpeza das labels nos subplots adjacentes, como Ingles e Italiano. A instrucao direta resultou em um comportamento inesperado de ocultacao de dados visuais antes de ser corrigida com a fixacao explicita de `set_yticks`.

## Como o grupo validou a solucao nesta interacao

A validacao foi inteiramente visual e em tempo de execucao dentro do ambiente interativo do Python, como Jupyter Notebook ou IPython. O usuario executou as celulas de codigo modificadas apos cada instrucao da IA, analisando diretamente a renderizacao da imagem gerada pelo bloco `plt.show()` para inspecionar o alinhamento de texto, colisoes e persistencia dos dados nos eixos.

## Modificacoes feitas pelo grupo nesta interacao

O usuario realizou de forma autonoma a integracao das linhas de estilizacao dentro do laco de repeticao `for ax, lang in zip(axes, LANGS):` ja existente na arquitetura do script, garantindo que as regras de exibicao fossem aplicadas uniformemente a todas as linguagens avaliadas no projeto sem quebrar a funcao personalizada de salvamento `save_fig`.

---

## Contexto: Otimizacao de estrutura de classes, monitoramento de performance e persistencia dinamica de dados

O objetivo desta interacao foi melhorar a estrutura das classes de resultado dos algoritmos de busca em labirintos, medir tempos de execucao com maior precisao e persistir dados dinamicos em arquivos CSV usando Pandas.

## Ferramenta utilizada nesta interacao

- Google Gemini
- Gemini 1.5 Pro, via interface de chat academico/profissional, em junho de 2026

## Principais prompts utilizados nesta interacao

- "QUal o problema dessa clasese?" [enviando snippet inicial com erros de sintaxe e logica na classe `Resultado`]
- "Como criar uma funcao start e um finish para calcular o tempo"
- "Como criar uma classe ResultadoBFS que herda o que tem na Resultado mas me deixa colocar novos parametros"
- "Como definir um metodo abstrado em resultado que deve ser sobrescrito e tambem deixar a resultado uma classe abstrata"
- "FAca um codigo que use o pandas para salvar uma nova coluna com os resultados em um csv que existe na raiz/datasets/resultado_a_star.csv. Se o arquivo nao existir ele deve criar"
- "Assim ta certo?" [enviando proposta de refatoracao usando heranca e `pd.concat`]
- "esse tempo deve ser em milesegundos. o mais preciso que o pcs tiver"
- "Como gerar UUID"
- "Como concatenar dois dicionarios em python"
- "Como fazer com que, quando eu adicioar um novo campo em um csv que ja existe el identifique que o dicionario possui um atributo novo no header e cadastre ele no header do csv?"
- "Ajuste essa funcao" [enviando metodo `_salvaResultado` utilizando `mode='a'` com dicionarios compostos]
- "Traceback... pandas.errors.ParserError: Error tokenizing data. C error: Expected 6 fields in line 5, saw 7" [enviando log de erro de parseamento de arquivos]
- "Assim funciona para ele sempre criar um novo csv do zero para manter a integridade?" [enviando proposta com `read_csv` sem condicional e sem `index=False`]
- "Voce esta alucinando. eu quero que ele olhe para o csv atual, adicione a nova linha e se a nova linha tiver algum parametro que o csv original nao tenha, ele tem que adiciona. com isso, ele altera todas as linhas para colocar null"
- "ma o csv esta [valor] e nao valor"
- "como deixar um metodo privado"

## Trechos de codigo sugeridos por IA e correcoes solicitadas nesta interacao

### Correcao de sintaxe da classe base (`Resultado`)

Remocao de virgulas acidentais que transformavam atributos em tuplas, como `False,`, substituicao de chaves `{}` por indentacao padrao Python e inclusao do parametro `self` no metodo `expandir`.

### Calculo de tempo com alta precisao (`time.perf_counter`)

Implementacao dos metodos `start()` e `finish()` utilizando o relogio de hardware de maior resolucao do sistema, com conversao matematica para milissegundos por meio de `* 1000`.

### Abstracao e heranca com o modulo `abc`

Demontracao de uso de `from abc import ABC, abstractmethod` para impedir a instanciacao da classe base e forcar as classes filhas, como `ResultadoBFS` e `ResultadoAStar`, a implementar comportamentos obrigatorios.

### Persistencia incremental dinamica com mapeamento de novas colunas (Pandas)

```python
def _salvaResultado(self, file, additionalData):
    dados = self.getResultado() | additionalData
    df_dados = pd.DataFrame(dados, index=[0])

    pasta = os.path.dirname(file)
    if pasta and not os.path.exists(pasta):
        os.makedirs(pasta)

    if os.path.exists(file):
        df_atual = pd.read_csv(file)
        df_concat = pd.concat([df_atual, df_dados], ignore_index=True)
    else:
        df_concat = df_dados

    df_concat.to_csv(file, index=False)
```

Resolucao: este bloco resolveu a necessidade de ler o CSV anterior, identificar novos parametros de forma flexivel em tempo de execucao, alinhar as colunas preenchendo as linhas do historico com nulos (`NaN`/`null`) e sobrescrever o arquivo de maneira integra.

## Sugestoes rejeitadas nesta interacao

### Gravacao via modo append (`mode='a'`)

A IA sugeriu inicialmente otimizar a escrita utilizando a gravacao direta no fim do arquivo para poupar memoria do sistema. Esta abordagem foi rejeitada e descartada pelo usuario porque impossibilitava a alteracao retroativa do cabecalho (`header`) do arquivo quando chaves ineditas fossem passadas no dicionario.

## Erros cometidos pela IA nesta interacao

### Tipagem incorreta na construcao do DataFrame

Para evitar que o Pandas gerasse erro de inicializacao por falta de indices, a IA sugeriu fazer um mapeamento por compreensao de dicionario transformando os valores brutos em listas de um unico elemento: `{k: [v] for k, v in dados.items()}`.

Impacto do erro: o codigo executou sem travar, mas gravou os dados no arquivo CSV poluidos visualmente, encapsulados por colchetes, como `[True]`, `[10]` e `[Manhattan]`, em vez de salvar as constantes limpas. O erro foi admitido pela IA e corrigido substituindo a logica pelo argumento estrutural `pd.DataFrame(dados, index=[0])`.

## Como o grupo validou a solucao nesta interacao

### Analise de logs de erros (`Tracebacks`)

Identificacao e isolamento do erro critico de parseamento `ParserError` gerado pelo Pandas no terminal durante a tentativa de ler um CSV com colunas desalinhadas.

### Inspecao visual de artefatos

Verificacao direta da integridade dos arquivos gerados dentro do diretorio `datasets/resultado_a_star.csv`, analisando a formatacao das celulas de texto e a correta insercao de nulos (`NaN`) em linhas que registraram execucoes anteriores a criacao de novos parametros.

## Modificacoes feitas pelo grupo nesta interacao

### Encapsulamento e restricao de acesso

O usuario solicitou explicitamente a conversao de metodos de salvamento e escrita interna para o escopo estrito de metodos privados (`__metodo`). Isso garante que componentes externos do motor de simulacao do labirinto nao alterem o arquivo ou corrompam os logs por acidente.

### Modularizacao arquitetural de arquivos

Ajuste na arvore de diretorios do projeto para isolar a infraestrutura de relatorios dentro de pacotes utilitarios (`src.utils.resultados`), importando-os nos scripts de teste atraves do sistema de empacotamento do Python (`python -m`).

---

## Contexto: Visualizacao e plotagem de series temporais com Seaborn

Este relatorio documenta a interacao tecnica realizada com assistente de IA generativa para suporte ao desenvolvimento e documentacao do projeto Maze Solving AI Agent, com foco em suporte, revisao e sugestao de melhorias arquiteturais e de visualizacao.

## Ferramentas utilizadas nesta interacao

- Google Gemini
- Assistente de desenvolvimento de software, analise de dados e documentacao tecnica

## Principais prompts utilizados nesta interacao

- "Como plotar uma setie temporal no seaborn"
- "Atue como um assistente de desenvolvimento de software e documentacao tecnica. Preciso que voce gere um relatorio detalhado sobre a nossa conversa atual para que eu possa prestar contas sobre o uso de IA Generativa no meu trabalho academico (Projeto: Maze Solving AI Agent)..."

## Trechos de codigo sugeridos por IA e correcoes solicitadas nesta interacao

Durante a sessao, foi solicitada orientacao sobre a plotagem de series temporais. A IA sugeriu um pipeline padrao utilizando `pandas` e `seaborn` para evitar erros comuns de encavalamento de strings e eixos temporais incorretos.

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Exemplo conceitual de estrutura de dados estruturada
dados = {
    'data': ['2026-01-01', '2026-01-02', '2026-01-03', '2026-01-04', '2026-01-05'],
    'vendas': [100, 120, 115, 140, 135]
}
df = pd.DataFrame(dados)

# Correcao conceitual sugerida: conversao explicita para datetime
df['data'] = pd.to_datetime(df['data'])

# Configuracao do ambiente grafico e plotagem
sns.set_theme(style="darkgrid")
plt.figure(figsize=(10, 5))
sns.lineplot(data=df, x='data', y='vendas', marker='o', color='b')

plt.title('Evolucao de Vendas Over Time')
plt.xlabel('Data')
plt.ylabel('Vendas (R$)')
plt.xticks(rotation=45)

plt.tight_layout()
```

Melhoria resolvida pelo bloco: tratamento do eixo X como tipo temporal (`datetime`) no Pandas, impedindo que o Seaborn trate strings de datas de forma puramente categorica e desordenada. O exemplo tambem inclui boas praticas de rotacao de rotulos (`xticks`) para evitar poluicao visual.

## Sugestoes rejeitadas nesta interacao

Nenhuma sugestao foi rejeitada neste chat. O escopo concentrou-se na consulta de sintaxe e estrutura base para plotagem de series temporais e na formatacao do documento de prestacao de contas.

## Erros cometidos pela IA nesta interacao

Nenhum erro tecnico foi detectado. O codigo sintatico fornecido para Seaborn e Pandas seguiu o padrao estrutural esperado, sem falhas de digitacao, imports ou logica de tipos.

## Como o grupo validou a solucao nesta interacao

### Ambiente de execucao Python

Execucao do script localmente via terminal ou em ambientes interativos como Jupyter Notebook.

### Inspecao visual

Verificacao se a janela do Matplotlib renderiza a curva continua corretamente ordenada por data.

### Validacao de tipos

Utilizacao do comando `df.dtypes` no terminal para garantir que a coluna temporal foi devidamente convertida para `datetime64[ns]` antes da plotagem.

## Modificacoes feitas pelo grupo nesta interacao

### Mapeamento de metricas do agente

Substituicao dos dados ficticios estruturados pelos arrays reais de logs coletados do agente de busca, como passos executados, taxa de acerto ou tempo de convergencia por iteracao/epoca.

### Sanitizacao de logs

Tratamento previo de strings de data coletadas diretamente do sistema de arquivos ou outputs do algoritmo para evitar excecoes de parser no `pd.to_datetime()`.

### Persistencia em disco

Substituicao do metodo interativo `plt.show()` por `plt.savefig('caminho/grafico.png')` para salvamento automatizado dos relatorios de execucao diretamente na pasta de assets do projeto academico.

---

# Contexto: Revisao, implementacao e documentacao do projeto Maze Solving AI Agent

## 1. Ferramentas Utilizadas

* Codex, assistente de desenvolvimento de software baseado em GPT-5.
* Terminal local do projeto para leitura de arquivos, validacao de sintaxe, inspecao de notebooks e execucao de testes rapidos.
* Ferramentas de linha de comando como `rg`, `sed`, `tail`, `pdftotext`, `git status` e Python em ambiente virtual.
* Bibliotecas ja existentes no projeto ou utilizadas nos notebooks, como `pandas`, `matplotlib` e `seaborn`.

## 2. Principais Prompts Utilizados

* "Avalie a implementacao desse projeto e busque por possiveis bugs e melhorias."
* "No menu principal, implemente uma funcionalidade que me permite criar um labirinto temporario para ver uma simulacao da execucao do algoritmo."
* "So coloque o `?` nas buscas que nao tem acesso ao mapa completo. Veja no pdf que ele pede um em especifico."
* "Pela definicao do trabalho, a busca online A* deve pegar os coletaveis?"
* "Altere os algoritmos que nao precisam olhar para `C` para tratar eles como celulas livres."
* "Verifique a implementacao do Online A*. Acho que ele so esta indo para baixo e para a direita."
* "Implemente um notebook para cada analise solicitada pelo professor. Separe por partes igual o professor separou por partes no trabalho."
* "Faca um relatorio completo com tudo que precisa fazer em cada parte do trabalho e o que ja esta feito. Crie um CSV com essas informacoes."
* "O notebook `notebooks/aaaaa.ipynb` tem um grafico tamanho x custo. Crie um array de graficos com custo, passos, tempo, expandidos e fronteiras."
* "Remova o de passos, mantenha apenas o de custo."
* "Mantenha os outros 4. Remova apenas o de passos. Falei errado."
* "Preciso que voce gere um relatorio detalhado sobre a nossa conversa atual para que eu possa prestar contas sobre o uso de IA Generativa."

## 3. Trechos de Codigo Sugeridos por IA e Correcoes Solicitadas

### Inclusao da simulacao no menu principal

Foi sugerida a inclusao de uma nova opcao no menu principal para abrir uma simulacao temporaria de labirinto sem depender dos arquivos persistidos do projeto.

```python
from src.menus.menu_simulacao import menu_simulacao_temporaria

opcoes = {
    # Demais opcoes ja existentes
    "Simular labirinto temporario": lambda: (menu_simulacao_temporaria(), False)[1],
}
```

Correcao ou melhoria resolvida: adiciona uma entrada no fluxo interativo principal para gerar um labirinto temporario, escolher um algoritmo e assistir a execucao no terminal.

### Tratamento de coletaveis como celulas livres para algoritmos que nao usam `C`

Foi sugerida uma separacao entre algoritmos que precisam considerar coletaveis e algoritmos que devem tratar `C` como caminho livre.

```python
ALGORITMOS_COM_COLETAVEIS = {
    "Hill Climbing",
    "Simulated Annealing",
}

def _maze_tratando_coletaveis_como_livres(maze):
    grid = [
        [" " if celula == "C" else celula for celula in linha]
        for linha in maze.grid
    ]

    maze_simulado = deepcopy(maze)
    maze_simulado.grid = grid
    return maze_simulado
```

Correcao ou melhoria resolvida: os metodos classicos e o Online A* deixam de interpretar coletaveis como objetivos obrigatorios quando a especificacao do algoritmo nao exige isso.

### Visualizacao no terminal com caminho, posicao atual e regioes desconhecidas

Foi sugerida uma funcao de animacao para mostrar a trajetoria no terminal usando `.` para caminho visitado, `@` para a posicao atual e `?` apenas quando o algoritmo nao possui acesso ao mapa completo.

```python
def _renderizar_estado(maze, caminho_visitado, posicao_atual, usar_desconhecido=False):
    for y, linha in enumerate(maze.grid):
        caracteres = []

        for x, celula in enumerate(linha):
            posicao = (x, y)

            if posicao == posicao_atual:
                caracteres.append("@")
            elif posicao in caminho_visitado:
                caracteres.append(".")
            elif usar_desconhecido and posicao not in caminho_visitado:
                caracteres.append("?")
            else:
                caracteres.append(celula)

        print("".join(caracteres))
```

Correcao ou melhoria resolvida: atende ao requisito visual da simulacao e respeita a restricao posterior de usar `?` somente nas buscas sem conhecimento completo do mapa, especialmente a busca online indicada no PDF.

### Correcao da busca Online A*

Foi revisada a implementacao do Online A* porque havia indicios de movimento enviesado e comportamento incorreto em mapas com obstaculos. A correcao principal foi padronizar coordenadas como `(x, y)`, replanejar a cada ciclo e impedir movimento para paredes reais.

```python
if (nx, ny) not in celulas_conhecidas:
    estado_real = grid_real[ny][nx]
    grid_interno[ny][nx] = estado_real
    celulas_conhecidas.add((nx, ny))

resultado.replanejamentos += 1
caminho_planejado = _a_star_replanejamento(grid_interno, posicao_atual, objetivo)

proximo_x, proximo_y = caminho_planejado[1]

if grid_real[proximo_y][proximo_x] == "#":
    grid_interno[proximo_y][proximo_x] = "#"
    continue

posicao_atual = (proximo_x, proximo_y)
```

Correcao ou melhoria resolvida: evita mistura entre `(x, y)` e `(y, x)`, reduz comportamento preso a direcoes especificas e impede que o agente atravesse paredes desconhecidas.

### Criacao de notebooks por parte do trabalho

Foram sugeridos notebooks separados por secoes do enunciado para organizar as analises solicitadas pelo professor.

```text
notebooks/parte_01_agente_peas_formulacao.ipynb
notebooks/parte_02_busca_classica_analise.ipynb
notebooks/parte_03_busca_local_analise.ipynb
notebooks/parte_04_busca_online_analise.ipynb
notebooks/parte_05_visualizacao_obrigatoria.ipynb
```

Correcao ou melhoria resolvida: separa a documentacao e a analise experimental de acordo com as partes do trabalho, facilitando revisao e prestacao de contas.

### Relatorio e CSV de status do trabalho

Foi sugerida a geracao de um relatorio e de um CSV com itens do enunciado, status, evidencias e pendencias.

```text
reports/status_trabalho_tp01.csv
reports/relatorio_status_trabalho_tp01.md
```

Correcao ou melhoria resolvida: cria um inventario rastreavel do que esta feito, parcial ou pendente em relacao ao PDF do trabalho.

### Ajuste do notebook `aaaaa.ipynb`

Foi sugerida a alteracao do grafico original `tamanho x custo` para uma grade com quatro metricas, removendo apenas `passos` apos a correcao do escopo feita pelo usuario.

```python
metricas = {
    "custo": "Custo",
    "tempo_segundos": "Tempo (s)",
    "expandidos": "Nos expandidos",
    "fronteira": "Fronteira",
}

fig, axes = plt.subplots(2, 2, figsize=(16, 11), sharex=True)

for ax, (coluna, titulo) in zip(axes.flat, metricas.items()):
    sns.scatterplot(
        data=df_grafico,
        x="tamanho",
        y=coluna,
        hue="tipo_busca",
        style="tipo_busca",
        size="cicles",
        sizes=(40, 260),
        alpha=0.75,
        ax=ax,
    )
```

Correcao ou melhoria resolvida: mantem custo, tempo, expandidos e fronteira no mesmo painel comparativo, usando cor e marcador por tipo de busca e tamanho da bolha pela probabilidade de ciclos.

## 4. Sugestoes Rejeitadas

Nenhuma sugestao foi rejeitada neste chat. Houve refinamentos de escopo feitos pelo usuario, como limitar o uso de `?` apenas as buscas sem mapa completo, tratar `C` como livre em algoritmos que nao coletam itens e remover somente a metrica `passos` do notebook. Esses pontos foram incorporados como correcoes de requisito, nao como rejeicoes de uma abordagem.

## 5. Erros Cometidos pela IA

* A primeira interpretacao da visualizacao no terminal foi ampla demais, pois aplicava `?` de forma generica. O usuario corrigiu que o `?` deveria aparecer apenas em buscas sem acesso ao mapa completo, conforme o PDF.
* A primeira alteracao solicitada no notebook foi interpretada como remocao de todos os graficos exceto `custo`. O usuario esclareceu que queria remover apenas `passos` e manter custo, tempo, expandidos e fronteira.
* Durante a validacao por terminal, alguns comandos de inspecao e execucao precisaram ser ajustados por contexto de diretorio, escape de shell ou ausencia de dependencias como `pytest`.
* A revisao do Online A* inicialmente partiu da suspeita de que o algoritmo so andava para baixo e para a direita, mas a analise mostrou tambem problemas mais concretos de coordenadas e planejamento. A correcao final tratou a causa tecnica encontrada.

## 6. Como o Grupo Validou a Solucao

As sugestoes foram validadas por inspecao direta dos arquivos do projeto e por execucoes locais no ambiente Python.

Foram usados comandos como:

```bash
pdftotext tp01_CSI457_2026-1.pdf -
rg --files
git status --short
.venv/bin/python -m compileall -q main.py src
```

Tambem foram feitos testes rapidos com Python para executar buscas como BFS, UCS, A* e Online A* em mapas controlados, incluindo um caso de desvio forcado para confirmar que o Online A* nao atravessava parede desconhecida apos a correcao.

Os notebooks foram validados por leitura como JSON, garantindo que os arquivos `.ipynb` gerados ou alterados permanecessem estruturalmente validos. O notebook `notebooks/aaaaa.ipynb` tambem foi conferido com execucao parcial da celula de carregamento e montagem do dataframe para verificar as colunas esperadas e os tipos de busca presentes.

O CSV e o relatorio de status foram conferidos com `pandas`, incluindo contagem de linhas e distribuicao de status, para garantir que os arquivos gerados tinham estrutura tabular consistente.

## 7. Modificacoes Feitas pelo Grupo

Nenhuma modificacao manual feita pelo usuario foi registrada diretamente neste chat. O usuario atuou principalmente refinando requisitos e apontando ajustes necessarios.

As principais decisoes de adaptacao solicitadas pelo usuario foram:

* Restringir o caractere `?` as buscas sem conhecimento completo do mapa.
* Definir que a busca Online A* nao deveria obrigatoriamente coletar celulas `C`, pois seu objetivo no trabalho e encontrar uma rota ate a saida em ambiente parcialmente conhecido.
* Tratar `C` como celula livre em algoritmos que nao precisam considerar coletaveis.
* Revisar o Online A* por suspeita de movimento enviesado.
* Separar os notebooks por partes do enunciado.
* Manter no notebook `aaaaa.ipynb` os graficos de custo, tempo, expandidos e fronteira, removendo apenas passos.

---

# Contexto: Análise de Desempenho, Geração de Gráficos Comparativos e Refatoração do Algoritmo A* Online

## 1. Ferramentas Utilizadas

* **IA Generativa:** Gemini (Google)
* **Ambiente de Contexto do Usuário:** Python, Jupyter Notebook, Nix-shell, bibliotecas de análise e visualização de dados (Pandas, Seaborn, Matplotlib).

## 2. Principais Prompts Utilizados

* Solicitação para criar um gráfico relacionando Custo da Solução, Nós Expandidos e Área do labirinto.
* Solicitação para implementar em Python uma fórmula matemática de desempenho extraída de uma imagem ($Score = \alpha C - \beta N - \gamma Ne - \delta Mi - \epsilon Cr$).
* Pedido de ajuda para calcular a distância Euclidiana a partir de coordenadas em formato de string `"(1,1)"`.
* Resolução de erros de infraestrutura do Jupyter no Nix-shell (`HTTP 403: Forbidden` e `HTTP 404: Kernel does not exist`).
* Solicitação para refazer códigos de plotagem integrando novas colunas (`celulas_revisitadas` e `replanejamentos`) para avaliar a busca Online A*.
* Pedido para gerar um grid com 6 subgráficos variando os pesos da fórmula de desempenho, mantendo um padrão visual rigoroso (cores hexadecimais específicas, `darkgrid`).
* Pedido de refatoração do código da classe `ResultadoOnlineAStar` e da função `online_a_star` para salvar o "custo real percorrido".
* Solicitação para criar e explicar um gráfico de "Razão de Competitividade" (Custo Online / Custo Offline).
* Solicitações para formatar e gerar textos analíticos em estilo de "relatório acadêmico" para interpretar as visualizações geradas.
* Dúvida conceitual pedindo explicação detalhada sobre a otimização de memória ("Lazy Deletion") no uso do `heapq` para o A*.

## 3. Trechos de Código Sugeridos por IA e Correções Solicitadas

* **Limpeza e Cálculo Euclidiano:** Foi sugerida a função `converter_string_para_tupla` utilizando `.replace().split()` para tratar as strings de coordenadas sujas e permitir o cálculo via Teorema de Pitágoras com `np.sqrt()`.
* **Resolução de Autenticação do Jupyter:** Sugestão de comandos de terminal (ex: `jupyter notebook --no-browser --NotebookApp.token=''`) e limpeza de metadados de `kernelspec` no arquivo `.ipynb` para resolver bloqueios de CSRF/Tokens antigos no VS Code com Nix.
* **Cálculo de Score Consolidado:** O código base de pontuação da performance foi implementado utilizando pesos multiplicativos `(alpha, beta, gamma...)`.
* **Custo Real no A* Online:** O código do ciclo "Perceber-Planejar-Agir" foi modificado pela IA para incluir `resultado.custo_real = len(caminho_percorrido) - 1`, garantindo que retrocessos físicos (backtracking) fossem registrados no dataset final.
* **Ajuste de Overlap na Legenda (Matplotlib):** Sugestão das propriedades `bbox_to_anchor=(1.02, 0.5)` e `tight_layout(rect=[0, 0, 0.85, 1])` para espremer o eixo X e forçar a caixa da legenda a renderizar na margem externa do `.png` sem sobrepor os dados.

## 4. Sugestões Rejeitadas

* **Interpretação literal da fórmula de subtrações:** O usuário enviou uma fórmula onde todas as penalidades eram subtraídas ($Score = Custo - Nós - Tempo$). A IA inicialmente implementou as subtrações e aplicou um multiplicador `*-1` para o gráfico fazer sentido. Posteriormente, essa abordagem foi abandonada e alterada de forma consensual para uma *soma* das penalidades matemáticas, facilitando a visualização em escala logarítmica.
* **Visualização via Bubble Chart 3D/Complexo:** Nas primeiras interações, a IA sugeriu abstrair métricas demais em tamanho/cor, mas o usuário redirecionou a abordagem exigindo um grid estrito de painéis (6 subgráficos) e esquemas de cores pré-determinados, o que foi prontamente adotado e substituiu a ideia original da IA.

## 5. Erros Cometidos pela IA

* **Estouro e Falta de Tipagem/Tratamento de Nulos (`NaN`):** Ao criar o código de comparação consolidada entre o A* Offline e o A* Online, a IA inicialmente não previu que a junção dos DataFrames geraria valores `NaN` (nulos) na coluna de `replanejamentos` para o A* Offline. Isso quebraria a fórmula matemática. O erro foi mitigado nas versões seguintes através da introdução do método `.get('coluna', pd.Series(0)).fillna(0)`.
* **Inconsistência de Escala em Eixos:** No primeiro código do grid de 6 gráficos, a IA aplicou um multiplicador baixo para a variável de "Tempo". Como o tempo geralmente é avaliado na casa de $0.00x$ segundos, a variável se tornava estatisticamente invisível perto da contagem de nós, requerendo um ajuste para `peso = 1000` sugerido a posteriori para balancear o cálculo visual.

## 6. Como o Grupo Validou a Solução

* **Teste em Ambiente Nix:** As correções do Jupyter Server foram validadas rodando os comandos diretamente no gerenciador de pacotes isolado (`nix-shell`) e verificando a conexão via IDE (VS Code).
* **Inspeção Visual (DataViz):** Todos os trechos de visualização de dados foram validados a partir da plotagem real e análise das imagens `.png` salvas no diretório `figs/`. A comprovação da eficiência das heurísticas ocorreu pela verificação de sobreposição, formação de clusters e tamanho das bolhas nos gráficos resultantes.
* **Revisão Teórica (Desk Check):** A lógica interna de replanejamento (`_a_star_replanejamento`) e o controle do `g_cost` (`heapq`) foram auditados teoricamente na conversa para assegurar que não quebravam a otimalidade de Busca em Grafos esperada pela literatura.

## 7. Modificações Feitas pelo Grupo

* **Injeção de Caminhos e Estruturas Locais:** O usuário interveio nos exemplos genéricos da IA forçando a utilização de caminhos absolutos do próprio ambiente local (`/home/pedroalves/faculdade/...`), assegurando que a leitura dos `.csv` conversasse com a estrutura real do repositório.
* **Padronização Estética (UI/UX dos Dados):** O usuário foi o responsável por travar e injetar o dicionário completo de cores hexadecimais (ex: `"#FF0055"` para o BFS/0.1), os tamanhos dos marcadores (`sizes=(40, 260)`) e a imposição da ordem dos *hues* para manter a identidade visual alinhada aos padrões de formatação do relatório final que o grupo entregará à universidade.
* **Importação das Classes customizadas:** O usuário adaptou a lógica orientada a objetos (uso de `super()._getResultado()` e caminhos de classes como `src.utils.resultados...`) provando que a lógica algorítmica sugerida pela IA foi encapsulada na arquitetura de *tracking* de métricas previamente construída pelo grupo.

---

# Contexto: Análise e Otimização de Algoritmos de Busca Local (Hill-Climbing e Simulated Annealing) no Projeto Maze Solving AI Agent

## 1. Ferramentas Utilizadas

* Inteligência Artificial: Gemini (modelo de linguagem grande).

## 2. Principais Prompts Utilizados

* "Mas é que meu csv executa pro mesmo labirinto várias vezes" (Discussão sobre a estrutura de dados e agregação).
* "Porque está ficando assim nessa primeira parte, mostrando apenas hill-climbing" (Investigação sobre a leitura de arquivos e visualização com `.head()`).
* "Porque a taxa do SA está aparecendo 0 aqui sendo que tem taxa" (Depuração de lógica de métricas).
* "Porque seus resultados do SA estão sendo piores que do Hill Climbing, ele não era pra ser melhor?" (Discussão teórica sobre o comportamento das meta-heurísticas).
* "Faça a mesma coisa, só que agora para essas tabelas [de parâmetros diferentes]" (Solicitação de estruturação de dados comparativos para o relatório).
* "Classifique os agentes do hill-climbing e do simulated annealing para eu adicionar ao relatório" (Solicitação de fundamentação teórica baseada em IA).

## 3. Trechos de Código Sugeridos por IA e Correções Solicitadas

* **Cálculo da Taxa de Sucesso:** Sugeri uma função `taxa_sucesso_5pct_corrigida` que utiliza o `min()` absoluto do custo para normalizar a comparação entre algoritmos, evitando distorções quando o Hill-Climbing encontrava um ótimo global muito superior ao Simulated Annealing.
* **Agregação de Dados (`agg`):** Refinei a estrutura de agregação dos DataFrames usando `groupby("algoritmo")` para garantir que o resumo estatístico contivesse colunas consistentes (`melhor_custo`, `tempo_medio`, etc.) aptas para visualização em gráficos `barplot` e `boxplot`.
* **Ajuste de Parâmetros de Resfriamento:** Orientei a lógica de ajuste das taxas de resfriamento ($\alpha$ de 0.95 para 0.999) para permitir uma convergência mais robusta e menos prematura.

## 4. Sugestões Rejeitadas

* Nenhuma sugestão foi rejeitada neste chat. O usuário acatou as diretrizes lógicas para a correção das métricas e para o ajuste dos hiperparâmetros.

## 5. Erros Cometidos pela IA

* Inicialmente, sugeri nomes de colunas no `.agg()` (`tempo_medio_bateria`) que não correspondiam exatamente às chaves utilizadas no `sns.barplot`, gerando um `ValueError`. O erro foi corrigido na interação seguinte ao alinhar os identificadores das colunas entre o processamento de dados e a camada de visualização.

## 6. Como o Grupo Validou a Solução

* A validação foi realizada através de testes incrementais no ambiente Jupyter Notebook:
    * Execução de blocos de código para inspeção via `local.head()` e `local.tail()` para verificar se ambos os algoritmos estavam presentes no DataFrame consolidado.
    * Verificação de tabelas resumo (`resumo.round(4)`) comparando os resultados estatísticos gerados.
    * Inspeção visual dos gráficos de convergência (`matplotlib`) para confirmar que a curva do SA apresentava o comportamento esperado de "descida suave" comparado ao HC.

## 7. Modificações Feitas pelo Grupo

* O usuário realizou a higienização dos arquivos `.csv` na pasta `datasets` para garantir que as baterias de teste não contivessem dados corrompidos.
* O usuário ajustou manualmente a ordem dos parâmetros na definição da função `rodar_bateria_simulated_annealing` para corrigir um erro de posicionamento de argumentos padrão (`num_execucoes`), garantindo conformidade com a assinatura da função.
* O usuário implementou a lógica de `Path` para garantir que o carregamento dos arquivos fosse independente do diretório de trabalho do terminal, evitando falhas de carregamento de datasets.
