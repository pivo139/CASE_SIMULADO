# 📊 Análise de Desempenho e Indicadores — Programa Grandes Talentos

## 📌 Visão Geral do Projeto

Este projeto consiste na consolidação, tratamento e visualização analítica dos dados do programa de formação de gestores **"Grandes Talentos"**.

A solução resolveu a descentralização dos dados provenientes de múltiplos gestores (Valentina, Vanderleia e Enzo), padronizou inconsistências cadastrais de CPFs, unificou a contagem de frequência e estruturou um modelo relacional no **Power BI** para acompanhamento dos principais indicadores de desempenho (KPIs) por Diretoria de Ensino.

## 🔢 Números Gerais da Análise (Base Tratada)

| Métrica / KPI | Valor Consolidado | Descrição / Regra | 
| ----- | ----- | ----- | 
| **Total de Inscritos** | **75.781** | Base final oficial auditada e sem duplicidades cadastrais. | 
| **Total de Certificados** | **69.043** | Cursistas com frequência maior ou igual a 75%. | 
| **Total de Evadidos** | **6.250** | Cursistas com frequência zerada (0%), sujeitos a suspensão de 1 ano. | 
| **Total de Não Certificados** | **488** | Cursistas com frequência maior que 0% e menor que 75%. | 
| **Taxa de Efetividade** | **91,1%** | Percentual líquido de aprovação (Certificados dividido pelo Total de Inscritos). | 
| **Diretorias de Ensino** | **91** | Cobertura total de diretorias analisadas no estado. | 

## 🛠️ Trilha de Tratamento & Engenharia de Dados

### 1. Seleção das Bases Cronológicas (Regra de Negócio)

Para garantir a temporalidade mais recente e evitar divergências de versão entre planilhas descentralizadas:

* **Valentina & Enzo:** Adotadas as versões com data limite de **05/12**.
* **Vanderleia:** Adotada a versão com data limite de **04/12**.

### 2. Higienização e Padronização de CPFs

* **Desafio:** CPFs com 10 dígitos (perda de zero à esquerda pelo Excel), 12 dígitos (sufixos decimais `.0`) e notação científica.
* **Solução:** Limpeza via regex em Python (`tratamento_dados.py`) e padronização final no Power Query via fórmula M:

  ```m
  Text.PadStart(Text.Remove([CPF_limpo], {"."}), 11, "0")
  ```

## 📐 Medidas DAX Implementadas no Power BI

```dax
// 1. Total de Inscritos
Total_Inscritos = COUNTROWS('base_tratada_grandes_talentos')

// 2. Total de Certificados
Total_Certificados = 
CALCULATE(
    COUNTROWS('base_tratada_grandes_talentos'),
    'base_tratada_grandes_talentos'[Status_Oficial] = "Certificado"
)

// 3. Total de Evadidos
Total_Evadidos = 
CALCULATE(
    COUNTROWS('base_tratada_grandes_talentos'),
    'base_tratada_grandes_talentos'[Status_Oficial] = "Evadido (Suspenso 1 ano)"
)

// 4. Total de Não Certificados
Total_Nao_Certificados = 
CALCULATE(
    COUNTROWS('base_tratada_grandes_talentos'),
    'base_tratada_grandes_talentos'[Status_Oficial] = "Não Certificado"
)

// 5. Taxa de Efetividade (%)
Taxa_Efetividade = 
DIVIDE(
    [Total_Certificados],
    [Total_Inscritos],
    0
)
```

## 🏆 Top 10 Diretorias em Absoluto de Certificados

 1. **D.E.REG. MAUA:** 1.138 certificados
 2. **D.E.REG. SOROCABA:** 1.130 certificados
 3. **D.E.REG. RIBEIRAO PRETO:** 1.118 certificados
 4. **D.E.REG. CAMPINAS OESTE:** 1.094 certificados
 5. **D.E.REG. SUL 3:** 1.069 certificados
 6. **D.E.REG. SANTOS:** 1.062 certificados
 7. **D.E.REG. SUL 2:** 1.021 certificados
 8. **SÃO PAULO:** 981 certificados
 9. **D.E.REG. SUL 1:** 947 certificados
10. **D.E.REG. JUNDIAI:** 927 certificados

## 🔄 Status Atual e Próximos Passos (Amanhã)

* [x] Tratamento de dados via Python finalizado e validado (`base_tratada_grandes_talentos.xlsx`).
* [x] Importação e tratamento de tipo de dados (CPF com 11 dígitos) no Power Query.
* [x] Criação do modelo de medidas DAX essenciais.
* [x] Estruturação dos cartões de KPI e ranking Top 10 em gráfico de barras horizontais no Dark Mode.
* [ ] **Refinamento de UI/UX (Amanhã):**
  * Implementar cabeçalho profissional com títulos e filtros por Cargo/Diretoria.
  * Adicionar gráfico de distribuição de status (Rosca) para preencher a lateral direita.
  * Renomear rótulos dos cartões e desativar eixo X redundante no gráfico de barras.

---
*Projeto desenvolvido para o desafio técnico de análise de dados Grandes Talentos.*