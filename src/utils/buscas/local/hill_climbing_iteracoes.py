from src.utils.buscas.local.hill_climbing import hill_climbing

def rodar_bateria_hill_climbing(maze_obj, num_execucoes=100 ):
    
   
    resultados = []
    
    print(f"⏳ Rodando {num_execucoes} simulações de Hill Climbing. Aguarde...")
    
    for _ in range(num_execucoes):
        res = hill_climbing(maze_obj)
        resultados.append(res)
        
    custos = [r.custo for r in resultados]
    tempos = [r.tempo for r in resultados]
    iteracoes = [r.iteracoes for r in resultados]
    
    melhor_custo = min(custos)
    pior_custo = max(custos)
    custo_medio = sum(custos) / len(custos)
    tempo_medio = sum(tempos) / len(tempos)
    iteracoes_media = sum(iteracoes) / len(iteracoes)
    
    margem_aceitavel = melhor_custo * 1.05
    sucessos = sum(1 for c in custos if c <= margem_aceitavel)
    taxa_sucesso = (sucessos / num_execucoes) * 100
    
    print("\n--- 📊 RESULTADOS DO HILL CLIMBING (100 Execuções) ---")
    print(f"Melhor Custo Encontrado: {melhor_custo}")
    print(f"Pior Custo Encontrado: {pior_custo}")
    print(f"Custo Médio: {custo_medio:.2f}")
    print(f"Tempo Médio: {tempo_medio:.6f} s")
    print(f"Iterações Médias: {iteracoes_media:.2f}")
    print(f"Taxa de Sucesso (margem 5%): {taxa_sucesso:.1f}%")
    print("\nMelhor Rota Encontrada:")
    
    melhor_execucao = next(r for r in resultados if r.custo == melhor_custo)

    melhor_execucao.pior_custo = pior_custo
    melhor_execucao.custo_medio = custo_medio
    melhor_execucao.tempo_medio = tempo_medio
    melhor_execucao.iteracoes_media = iteracoes_media
    melhor_execucao.taxa_sucesso = taxa_sucesso
    
    print(" -> ".join(map(str, melhor_execucao.rota_macro)))
    
    if hasattr(melhor_execucao, 'salvarResultado'):
        melhor_execucao.salvarResultado()
        print(f"\n💾 Melhor curva de convergência salva no CSV com sucesso (ID: {maze_obj.id})!")
    
    return melhor_execucao