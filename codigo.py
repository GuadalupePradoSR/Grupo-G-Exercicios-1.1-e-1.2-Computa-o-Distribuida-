import math
import random
import matplotlib.pyplot as plt
import pandas as pd

# 1. CÁLCULO ANALÍTICO
def disponibilidade_analitica(n, k, p):
    disponibilidade_total = 0
    for i in range(k, n + 1):
        combinacao = math.comb(n, i)
        prob_i_sucessos = combinacao * (p ** i) * ((1 - p) ** (n - i))
        disponibilidade_total += prob_i_sucessos
    return disponibilidade_total

# 2. SIMULADOR ESTOCÁSTICO
def disponibilidade_simulada(n, k, p, rodadas=5000):
    rodadas_sucesso = 0
    
    for _ in range(rodadas):
        servidores_disponiveis = 0
        for _ in range(n):
            if random.random() <= p:
                servidores_disponiveis += 1
                
        if servidores_disponiveis >= k:
            rodadas_sucesso += 1
            
    return rodadas_sucesso / rodadas

# 3. TABELA DE RESULTADOS
def gerar_dados_disponibilidade(valores_n):
    """Gera dados iterando sobre múltiplos valores de n"""
    dados = []
    valores_p = [x / 20.0 for x in range(21)]  # de 0.0 a 1.0 (passo 0.05)
    
    for n in valores_n:
        casos_k = [1, n//2, n]  # k=1 (consulta), k=n/2 (maioria), k=n (atualização estrita)
        
        for k in casos_k:
            for p in valores_p:
                analitico = disponibilidade_analitica(n, k, p)
                simulado = disponibilidade_simulada(n, k, p, rodadas=5000)
                erro_relativo = abs(analitico - simulado) / analitico if analitico != 0 else 0
                
                dados.append({
                    'n': n,
                    'k': k,
                    'p': round(p, 2),
                    'Analítico': round(analitico, 6),
                    'Simulado': round(simulado, 6),
                    'Erro (%)': round(erro_relativo * 100, 2)
                })
    
    return pd.DataFrame(dados)

def salvar_tabela_csv(dataframe, nome_arquivo='disponibilidade_resultados.csv'):
    dataframe.to_csv(nome_arquivo, index=False)
    print(f"Tabela completa salva em: {nome_arquivo}")


# 4. GERAÇÃO DE DADOS E GRÁFICOS
def plotar_graficos(valores_n):
    valores_p = [x / 20.0 for x in range(21)]
    cores = ['blue', 'green', 'red']
    
    fig, axes = plt.subplots(1, len(valores_n), figsize=(5 * len(valores_n), 5), sharey=True)
    
    if len(valores_n) == 1:
        axes = [axes]
        
    for i, n in enumerate(valores_n):
        ax = axes[i]
        casos_k = [1, n//2, n]
        
        for idx, k in enumerate(casos_k):
            analitico_y = [disponibilidade_analitica(n, k, p) for p in valores_p]
            simulado_y = [disponibilidade_simulada(n, k, p, rodadas=5000) for p in valores_p]
            
            ax.plot(valores_p, analitico_y, label=f'Analítico (k={k})', color=cores[idx], linestyle='-')
            ax.scatter(valores_p, simulado_y, label=f'Simulado (k={k})', color=cores[idx], marker='x', alpha=0.7)

        ax.set_title(f'Disponibilidade para n = {n}')
        ax.set_xlabel('Probabilidade do Servidor (p)')
        if i == 0:
            ax.set_ylabel('Disponibilidade do Serviço')
        ax.set_xlim(0, 1.05)
        ax.set_ylim(-0.05, 1.05)
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.legend()
        
    plt.tight_layout()
    plt.savefig('graficos_disponibilidade.png', dpi=150, bbox_inches='tight')
    print("Gráfico unificado salvo em: graficos_disponibilidade.png\n")
    plt.show()


if __name__ == "__main__":
    print("\n" + "="*80)
    print("EXERCÍCIO 1.2 - DISPONIBILIDADE DE SERVIÇO REPLICADO")
    print("="*80 + "\n")

    valores_de_n_para_testar = [4, 6, 10]

    print("Simulando rodadas e processando os dados.")
    df_resultados = gerar_dados_disponibilidade(valores_de_n_para_testar)

    salvar_tabela_csv(df_resultados)

    plotar_graficos(valores_de_n_para_testar)