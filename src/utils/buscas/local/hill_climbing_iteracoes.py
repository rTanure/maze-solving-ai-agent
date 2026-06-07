from src.utils.buscas.local.hill_climbing import executar_hill_climbing_tsp

def rodar_bateria_hill_climbing(matriz_distancias, pontos_dict, num_execucoes=100):
    lista_coletaveis = [p for p in pontos_dict.keys() if p.startswith('C')]
    
    resultados = []
    
    for _ in range(num_execucoes):
        res = executar_hill_climbing_tsp(matriz_distancias, lista_coletaveis)
        resultados.append(res)
        
    custos = [r['custo'] for r in resultados]
    tempos = [r['tempo_s'] for r in resultados]
    iteracoes = [r['iteracoes'] for r in resultados]
    
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
    melhor_execucao = next(r for r in resultados if r['custo'] == melhor_custo)
    print(" -> ".join(melhor_execucao['rota']))
    
    return melhor_execucao 