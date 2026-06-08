# Relatorio de status do TP01 - Agente inteligente em labirinto

Este relatorio cruza o enunciado `tp01_CSI457_2026-1.pdf` com o estado atual do repositorio. A matriz completa esta em `reports/status_trabalho_tp01.csv`.

## Resumo executivo

O projeto ja possui uma base funcional forte: geracao/leitura de mapas, buscas classicas, busca local, busca online, CSVs experimentais e notebooks de analise. O principal risco para entrega nao e falta total de codigo, mas sim conformidade experimental e documentacao final.

Pontos mais urgentes:

- Regenerar resultados do `Online A*` apos a correcao recente do algoritmo. O CSV atual cobre apenas 25 de 50 mapas e tem razoes `online/offline < 1`, o que indica resultado antigo ou inconsistente.
- Completar resultados de `DFS`: ha 44 linhas, 43 mapas unicos, 1 `maze_id` nulo e 7 mapas faltantes.
- Corrigir/explicar metricas: nao existe `nos explorados` separado de `expandidos`, e `fronteira` em alguns algoritmos parece contar insercoes acumuladas, nao tamanho maximo.
- Completar `uso_ia.md`, README e relatorio tecnico em PDF.
- Exportar graficos/imagens dos notebooks ou incorporar os graficos no PDF final.

## Parte I - Projeto do agente inteligente

### O que o PDF pede

- Modelagem PEAS: Performance, Environment, Actuators, Sensors.
- Classificacao do agente, no minimo como agente baseado em objetivos com modelo interno.
- Na parte online, atualizacao de modelo interno do ambiente.

### O que ja esta feito

- `notebooks/parte_01_agente_peas_formulacao.ipynb` contem estrutura textual para PEAS, classificacao e formulacoes.
- `src/utils/Maze.py` representa labirintos em matriz, gera mapas, salva e abre mapas.
- O agente online possui mapa interno em `src/utils/buscas/online/online_a_star.py`.

### O que falta

- Consolidar texto no relatorio tecnico final.
- Justificar formalmente a funcao de desempenho e pesos.
- Melhorar README para reproduzir execucao e experimentos.

## Parte II - Busca classica

### O que o PDF pede

- Formulação formal `<S,A,T,s0,G,c>`.
- Implementar BFS, DFS, UCS, Busca Gulosa e A*.
- Usar/justificar heuristica Manhattan em buscas heuristicas.
- Registrar: sucesso, custo, tamanho do caminho, nos explorados, nos expandidos, tempo e tamanho maximo da fronteira.
- Responder seis questoes de analise.

### O que ja esta feito

- Implementacoes:
  - `src/utils/buscas/classicas/bfs.py`
  - `src/utils/buscas/classicas/dfs.py`
  - `src/utils/buscas/classicas/ucs.py`
  - `src/utils/buscas/classicas/greedy.py`
  - `src/utils/buscas/classicas/a_star.py`
- Heuristica Manhattan em `src/utils/buscas/auxiliar_busca.py`.
- CSVs:
  - BFS: 50/50 mapas.
  - UCS: 50/50 mapas.
  - Gulosa: 50/50 mapas.
  - A*: 50/50 mapas.
  - DFS: 43/50 mapas unicos, com 1 linha sem `maze_id`.
- `notebooks/parte_02_busca_classica_analise.ipynb` gera tabelas e graficos.

### O que falta

- Regenerar DFS para cobrir os 50 mapas corretamente.
- Adicionar ou justificar `nos explorados`.
- Corrigir `fronteira` para tamanho maximo, se for usar essa metrica literalmente.
- Escrever a analise final no relatorio.

## Parte III - Busca local com coletas

### O que o PDF pede

- Representar solucao como ordem dos pontos `C`.
- Custo da rota `A -> C... -> B` usando menor caminho entre pares, calculado por A* ou UCS.
- Implementar Hill Climbing e Simulated Annealing.
- Justificar vizinhanca.
- Medir melhor/pior custo, custo medio, tempo medio, iteracoes medias, curva de convergencia e taxa de sucesso.
- Incluir grafico `iteracao x melhor custo`.
- Responder seis questoes de analise.

### O que ja esta feito

- Hill Climbing: `src/utils/buscas/local/hill_climbing.py`.
- Simulated Annealing: `src/utils/buscas/local/simulated_annealing.py`.
- Menores caminhos entre pontos via UCS: `src/utils/menor_caminho.py`.
- Resultados:
  - `datasets/resultados_hill_climbing.csv`: 493 linhas, 50 mapas unicos.
  - `datasets/resultados_simulated_annealing.csv`: 495 linhas, 50 mapas unicos.
- `notebooks/parte_03_busca_local_analise.ipynb` calcula metricas e curva de convergencia.

### O que falta

- Salvar `temp_inicial` e `taxa_resfriamento` no CSV de Simulated Annealing, ou documentar manualmente os valores usados.
- Escrever a justificativa da vizinhanca por troca de dois pontos.
- Exportar o grafico de convergencia.
- Explicar se/como Hill Climbing parou em minimo local. O objeto tem `minimo_local`, mas o CSV nao salva essa coluna.

## Parte IV - Busca online

### O que o PDF pede

- Mapa real no simulador e mapa interno parcial para o agente.
- Ciclo a cada passo: perceber -> atualizar mapa interno -> planejar -> agir.
- Implementar uma estrategia: Replanning com A* ou Online DFS.
- Medir sucesso, movimentos totais, custo real, celulas reveladas, revisitadas, replanejamentos e comparacao com caminho otimo offline.
- Calcular razao `online/offline`.
- Responder seis questoes de analise.

### O que ja esta feito

- Online A*: `src/utils/buscas/online/online_a_star.py`.
- O algoritmo foi corrigido para:
  - usar coordenadas consistentes `(x,y)`;
  - replanejar a cada ciclo;
  - evitar atravessar paredes descobertas.
- CSV online atual: `datasets/resultado_online_a_star.csv`, com 25 mapas unicos.
- Notebook: `notebooks/parte_04_busca_online_analise.ipynb`.

### O que falta

- Regenerar `resultado_online_a_star.csv` apos a correcao do algoritmo.
- Completar cobertura dos 50 mapas ou justificar por que alguns foram filtrados por tamanho.
- Recalcular razao `online/offline`. O CSV atual tem 21 casos com razao menor que 1, o que nao deveria acontecer.
- Salvar mapa interno final ou snapshots se quiser comprovar convergencia do mapa interno.

## Visualizacao obrigatoria

### O que o PDF pede

- Mostrar mapa original.
- Mostrar caminho encontrado.
- Mostrar nos expandidos ou visitados.
- Mostrar trajetoria online passo a passo.
- Mostrar rota otimizada da busca local.

### O que ja esta feito

- `src/menus/menu_simulacao.py` permite criar labirinto temporario e assistir a execucao no terminal.
- `notebooks/parte_05_visualizacao_obrigatoria.ipynb` desenha mapa original, caminho A*, frame online e rota local.

### O que falta

- Os algoritmos nao salvam a lista de nos expandidos/visitados, apenas contagens e caminho final. Para cumprir literalmente essa visualizacao, e preciso registrar historico de visitados/expandidos.
- Exportar imagens/graficos ou inserir no relatorio tecnico.

## Uso de IA

### O que o PDF pede

`uso_ia.md` deve conter:

1. ferramentas utilizadas;
2. principais prompts;
3. trechos de codigo sugeridos por IA;
4. sugestoes rejeitadas;
5. erros cometidos pela IA;
6. como o grupo validou a solucao;
7. modificacoes feitas pelo grupo.

### Estado atual

`uso_ia.md` esta incompleto: lista ferramentas e inicia a secao de prompts, mas nao cobre todos os itens obrigatorios.

## Entregaveis finais

### Feitos ou quase feitos

- Codigo-fonte Python.
- Mapas utilizados.
- CSVs experimentais.
- Notebooks de analise.
- Visualizacao no terminal/notebook.

### Pendentes

- Relatorio tecnico PDF de 6 a 10 paginas.
- README completo e correto.
- `uso_ia.md` completo.
- Graficos exportados ou inseridos no PDF.
- Apresentacao/roteiro de defesa.

## Ordem recomendada de acao

1. Regenerar resultados do Online A* corrigido.
2. Regenerar DFS e remover linha com `maze_id` nulo.
3. Corrigir metricas de `fronteira` e adicionar `explorados`, se houver tempo.
4. Executar notebooks e exportar graficos.
5. Completar `uso_ia.md`.
6. Atualizar README.
7. Escrever e exportar relatorio tecnico PDF.
8. Preparar apresentacao.
