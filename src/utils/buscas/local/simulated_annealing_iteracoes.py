from src.utils.buscas.local.simulated_annealing import simulated_annealing

# 1. Nova assinatura: recebe o objeto do labirinto e a maleta de dados
def rodar_bateria_simulated_annealing(maze_obj, num_execucoes, temp_inicial, taxa_resfriamento):
    
    # A lista de coletáveis já vem pronta dentro dos dados_adicionais
    # (nós montamos ela no menu antes de chamar essa função)
    
    resultados = []
    
    print(f"⏳ Rodando {num_execucoes} simulações de Hill Climbing. Aguarde...")
    
    for _ in range(num_execucoes):
        # 2. Chama a nova função orientada a objetos
        res = simulated_annealing(maze_obj, temp_inicial, taxa_resfriamento)
        resultados.append(res)
        
    # 3. Acesso aos dados como atributos do objeto (r.atributo)
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
    
    # Pega o objeto da melhor execução
    melhor_execucao = next(r for r in resultados if r.custo == melhor_custo)
    
    # 4. Converte a rota_macro (que tem tuplas) para string para poder imprimir
    print(" -> ".join(map(str, melhor_execucao.rota_macro)))
    
    # 5. Salva automaticamente a melhor execução no CSV para você gerar o gráfico depois!
    if hasattr(melhor_execucao, 'salvarResultado'):
        melhor_execucao.salvarResultado(id_labirinto=maze_obj.id)
        print(f"\n💾 Melhor curva de convergência salva no CSV com sucesso (ID: {maze_obj.id})!")
    
    return melhor_execucao