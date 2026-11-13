import pandas as pd

# 1. Carregando o arquivo Excel
caminho_arquivo = 'CASE- Analista de Dados.xlsx'
excel_file = pd.ExcelFile(caminho_arquivo)

print("--- LENDO AS BASES OFICIAIS ---")

# Carregando as bases que o gestor indicou como confiáveis
df_inscritos = pd.read_excel(caminho_arquivo, sheet_name='Inscritos no Curso')
df_diretorias = pd.read_excel(caminho_arquivo, sheet_name='Diretorias')

# Exibindo uma prévia do tamanho e das colunas
print(f"Total de Inscritos oficiais: {len(df_inscritos)} registros")
print(f"Colunas de Inscritos: {list(df_inscritos.columns)}")
print("-" * 40)
print(f"Total de Diretorias oficiais: {len(df_diretorias)} registros")
print(f"Colunas de Diretorias: {list(df_diretorias.columns)}")


print("\n--- LENDO AS PLANILHAS DOS GESTORES ---")

# Carregando as planilhas dos gestores
# (Para a Valentina e Vanderleia, vamos pegar as versões mais recentes.)
df_valentina = pd.read_excel(caminho_arquivo, sheet_name='05.12.2025 Valentina')
df_vanderleia = pd.read_excel(caminho_arquivo, sheet_name='04.12.2025 Vanderleia')
df_enzo = pd.read_excel(caminho_arquivo, sheet_name='05.12.2025 Enzo')

print(f"Registros Valentina (05.12): {len(df_valentina)}")
print(f"Registros Vanderleia (04.12): {len(df_vanderleia)}")
print(f"Registros Enzo (05.12): {len(df_enzo)}")

# Vamos exibir as colunas de uma delas para conferir a estrutura
print(f"Colunas das planilhas dos gestores: {list(df_valentina.columns)}")



print("\n--- CONSOLIDANDO E CRUZANDO OS DADOS ---")

# 1. Unindo as planilhas dos três gestores em uma única base de frequência
df_gestores_consolidado = pd.concat([df_valentina, df_vanderleia, df_enzo], ignore_index=True)
print(f"Total de registros consolidados dos gestores: {len(df_gestores_consolidado)}")

# 2. Convertendo CPF para string limpa em ambas as bases para garantir um cruzamento sem falhas de ponto flutuante (.0)
df_inscritos['CPF_limpo'] = df_inscritos['CPF'].astype(str).str.split('.').str[0].str.zfill(11)
df_gestores_consolidado['CPF_limpo'] = df_gestores_consolidado['CPF'].astype(str).str.split('.').str[0].str.zfill(11)

# 3. Fazendo o merge (cruzamento) com a base oficial de inscritos (Left Join para manter todos os 75.781 inscritos)
df_final = pd.merge(df_inscritos, df_gestores_consolidado[['CPF_limpo', 'Diretoria de Ensino', '% Frequência', 'Resultado Final', 'Emitir Certificado']], on='CPF_limpo', how='left')

# Exibindo uma amostra do resultado do cruzamento
print(f"Total de linhas na base final cruzada: {len(df_final)}")
print("Amostra das primeiras linhas:")
print(df_final[['Nome completo do Cursista', 'Cargo', 'Diretoria de Ensino', '% Frequência', 'Resultado Final']].head(3))


print("\n--- TRATANDO EVADIDOS E CALCULANDO MÉTRICAS ---")

# 4. Quem tem Frequência NaN na verdade teve 0% de frequência (Evadidos)
df_final['% Frequência'] = df_final['% Frequência'].fillna(0.0)

# 5. Definindo a regra de negócio oficial da certificação
def regra_certificacao(freq):
    if freq >= 0.75:
        return 'Certificado'
    elif freq == 0.0:
        return 'Evadido (Suspenso 1 ano)'
    else:
        return 'Não Certificado'

df_final['Status_Oficial'] = df_final['% Frequência'].apply(regra_certificacao)

# 6. Contando quantos ficaram em cada categoria
print("\nDistribuição dos resultados finais:")
print(df_final['Status_Oficial'].value_counts())

# 7. Salvando a base tratada em um novo arquivo Excel para o Power BI
caminho_saida = 'base_tratada_grandes_talentos.xlsx'
df_final.to_excel(caminho_saida, index=False)
print(f"\nBase tratada salva com sucesso em: {caminho_saida}")