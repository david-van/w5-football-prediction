# Perguntas Frequentes (FAQ)

## Perguntas Gerais

### O que é o WINNER12 W-5?

O WINNER12 W-5 é uma estrutura de consenso de IA multiagente para a previsão de jogos de futebol que atinge 86,3% de precisão ao combinar a aprendizagem automática tradicional (XGBoost, LightGBM) com grandes modelos de linguagem através de um novo mecanismo de consenso. O sistema foi validado em mais de 15.000 jogos reais nas 5 principais ligas europeias (2015-2025).

### Como funciona o W-5?

O W-5 opera através de um processo de quatro etapas:

1. **Previsão Base**: Modelos de ML tradicionais (XGBoost, LightGBM) analisam estatísticas históricas para gerar previsões quantitativas
2. **Análise Contextual**: Grandes modelos de linguagem processam informações qualitativas (lesões, táticas, notícias, forma)
3. **Consenso Multiagente**: Múltiplos agentes de IA com diferentes "personas" (estatístico, tático, analista) debatem e votam no resultado
4. **Fusão por Meta-Aprendizagem**: Uma camada de fusão inteligente combina insights quantitativos e qualitativos numa previsão final com pontuação de confiança

### Isto é um sistema de apostas?

Não. O WINNER12 W-5 é um **projeto de investigação** para fins académicos e educacionais. Não é um conselho de apostas ou financeiro. Não encorajamos nem facilitamos apostas desportivas. A estrutura foi concebida para avançar o estado da arte na análise desportiva alimentada por IA.

---

## Perguntas de Desempenho

### Por que a precisão do WINNER12 (86,3%) é maior do que a do FiveThirtyEight (55-62%) e da Opta (60-65%)?

Existem três razões principais:

**1. Previsão Baseada na Confiança**

O W-5 só faz previsões quando a confiança é ≥ 0,75, abstendo-se de ~68% dos jogos. O FiveThirtyEight e a Opta preveem todos os jogos, incluindo os altamente incertos (derbies, equipas igualmente equilibradas). Isto é semelhante a como:
- A IA médica só diagnostica quando está confiante
- Veículos autónomos entregam o controlo aos humanos quando incertos
- A IA financeira só negoceia quando a certeza é alta

**2. Conjunto Multiagente**

O W-5 combina múltiplos modelos de IA com distribuições de erro não correlacionadas. A teoria da aprendizagem de conjunto prevê ganhos de precisão de 15-20% em relação a modelos únicos. O nosso ganho observado de 16,3% corresponde às expectativas teóricas.

**3. Evolução Tecnológica**

A metodologia do FiveThirtyEight data de 2009 (era pré-aprendizagem profunda). Os algoritmos centrais da Opta foram desenvolvidos na década de 2010. O W-5 aproveita modelos de IA de fronteira de 2023-2025. A vantagem de 20-30 pontos percentuais reflete o rápido avanço das capacidades de IA — este é um progresso esperado, não uma anomalia.

### A alta precisão deve-se à escolha a dedo de jogos fáceis?

Não. O limiar de confiança é aplicado **antes** de ver os resultados dos jogos. O modelo não sabe quais jogos são "fáceis" — ele só conhece a sua pontuação de confiança interna com base na análise de recursos.

Esta é uma prática padrão em sistemas de IA responsáveis:
- IA de diagnóstico médico: "Tenho 90% de certeza de que é pneumonia" vs "Incerteza, recomendar especialista"
- Condução autónoma: "Posso lidar com esta autoestrada" vs "Muito complexo, alertar o condutor"
- W-5: "Tenho 85% de certeza de que a Equipa A vence" vs "Muito incerto, abster-se"

A precisão de 86,3% reflete o desempenho em jogos onde o modelo tem alta certeza, não resultados escolhidos a dedo.

### E quanto aos outros 68% dos jogos dos quais o W-5 se abstém?

Para jogos abaixo do limiar de confiança, o W-5 ainda pode fornecer:

- **Distribuições de probabilidade**: por exemplo, "40% vitória em casa, 30% empate, 30% vitória fora"
- **Avaliações de risco**: por exemplo, "Jogo de alta variação, imprevisível"
- **Insights qualitativos**: por exemplo, "Jogo de derby com fatores emocionais"

Mas ele **não fará uma previsão definitiva**. Esta transparência é uma força, não uma fraqueza. É honesto sobre a incerteza.

### Como o W-5 se compara ao estado da arte académico?

A nossa precisão binária de 86,3% está no mesmo nível da investigação académica de ponta:
- Wong et al. (2025): 75-85% de precisão binária
- IA Académica (2025): 63,18% de precisão de três vias

Nós **não** estamos a alegar ser os melhores — alguns artigos relatam maior precisão com metodologias, conjuntos de dados ou protocolos de avaliação diferentes. A nossa força é:
- **Consistência entre ligas** (83-88% em 5 ligas)
- **Transparência total** (dados abertos, código reproduzível)
- **Validação rigorosa** (conjuntos de teste fora do tempo, sem fuga de dados)

### Por que ligas diferentes têm precisões diferentes?

Ligas diferentes têm características diferentes que afetam a previsibilidade:

- **Bundesliga (88,0%)**: Hierarquia clara com o domínio do Bayern de Munique, maiores lacunas de habilidade entre as equipas de topo e de baixo
- **Ligue 1 (87,2%)**: O domínio do PSG cria confrontos previsíveis
- **La Liga (86,7%)**: Real Madrid e Barcelona dominam clubes menores
- **EPL (84,2%)**: Mais competitiva no geral, mas ainda tem padrões claros de forte vs fraco
- **Serie A (83,4%)**: A complexidade tática e as estratégias defensivas tornam os resultados mais difíceis de prever

Estas variações são esperadas e demonstram que o modelo não está sobreajustado a uma única liga.

---

## Perguntas Técnicas

### Que dados o W-5 usa?

**Dados Quantitativos**:
- Resultados dos jogos (pontuações em casa/fora)
- Estatísticas da equipa (remates, posse de bola, cantos, etc.)
- Registos históricos de confrontos diretos
- Classificações e rankings da liga
- Odds de apostas (como indicadores de sentimento do mercado, não para treino)

**Dados Qualitativos**:
- Relatórios de lesões
- Análise tática
- Narrativas de forma recente
- Notícias e sentimento de redes sociais
- Mudanças gerenciais

**Fontes de Dados**:
- Football-Data.co.uk (fonte primária para resultados de jogos)
- APIs públicas para estatísticas em tempo real
- Agregadores de notícias para informações contextuais

Todos os dados são de fontes publicamente disponíveis.

### Como os agentes de IA são diferentes uns dos outros?

Cada agente tem uma "persona" e foco analítico distintos:

| Tipo de Agente | Foco | Pontos Fortes | Vieses |
|---|---|---|---|
| **Estatístico** | Padrões históricos, números | Objetivo, orientado por dados | Pode perder o contexto |
| **Tático** | Estilos de jogo, formações | Insights estratégicos | Pode sobrestimar as táticas |
| **Analista de Forma** | Desempenho recente, momento | Captura tendências | Viés de recenticidade |
| **Contrário** | Perspetivas alternativas | Desafia o pensamento de grupo | Pode ser excessivamente cético |

Ao fazer com que agentes com diferentes perspetivas debatam, o mecanismo de consenso reduz os vieses individuais.

### Que modelos de aprendizagem automática o W-5 usa?

**Modelos de ML de Previsão Base**:
- **XGBoost**: Aumento de gradiente para dados tabulares, excelente para recursos estruturados
- **LightGBM**: Aumento de gradiente rápido, lida com grandes conjuntos de dados de forma eficiente
- **Redes Neuronais** (opcional): Para reconhecimento de padrões não lineares

**Grandes Modelos de Linguagem**:
- Múltiplos LLMs de fronteira (modelos específicos não divulgados para evitar manipulação)
- Usados para raciocínio contextual e análise qualitativa

**Método de Conjunto**:
- Votação por consenso multiagente
- Fusão ponderada com base no desempenho histórico
- Calibração de confiança

### Como a pontuação de confiança é calculada?

A pontuação de confiança (0-1) é derivada de:

1. **Concordância do Modelo**: Quanto os diferentes agentes de IA concordam? Alta concordância → alta confiança
2. **Desempenho Histórico**: Quão bem o modelo se saiu em confrontos semelhantes historicamente?
3. **Qualidade do Recurso**: Quão completos e confiáveis são os dados de entrada para este jogo?
4. **Quantificação da Incerteza**: Medidas estatísticas de variação de previsão

Jogos com confiança ≥ 0,75 são considerados de "alta confiança" e recebem previsões definitivas.

### Posso usar o W-5 para apostar?

**Desaconselhamos veementemente o uso do W-5 para apostas.** Eis o porquê:

1. **Propósito de Investigação**: O W-5 é projetado para investigação académica, não para apostas comerciais
2. **Sem Garantias**: O desempenho passado (86,3%) não garante resultados futuros
3. **Risco**: Apostas desportivas envolvem risco financeiro e potencial vício
4. **Legal**: Apostar pode ser ilegal na sua jurisdição

Se optar por usar os insights do W-5 para apostas, apesar dos nossos avisos, fá-lo inteiramente por sua conta e risco. Não aceitamos nenhuma responsabilidade.

---

## Perguntas de Comparação

### WINNER12 vs FiveThirtyEight

| Aspeto | FiveThirtyEight | WINNER12 W-5 |
|---|---|---|
| **Precisão** | 55-62% (três vias) | 86,3% (binário, alta confiança) |
| **Metodologia** | Classificações Elo + classificações de equipa | Consenso de IA multiagente |
| **Tecnologia** | ML tradicional (era 2009) | Modelos de IA de fronteira (2023-2025) |
| **Transparência** | Metodologia pública, código privado | Totalmente de código aberto |
| **Cobertura** | Todos os jogos | Apenas jogos de alta confiança |
| **Pontos Fortes** | Previsão probabilística, confiança na marca | Maior precisão, consistência entre ligas |

**Respeito**: O FiveThirtyEight foi pioneiro na análise desportiva orientada por dados. Construímos sobre a sua base com tecnologia de IA mais recente.

### WINNER12 vs Opta

| Aspeto | Opta | WINNER12 W-5 |
|---|---|---|
| **Precisão** | 60-65% (três vias) | 86,3% (binário, alta confiança) |
| **Foco** | Fornecedor de estatísticas + previsões | Estrutura de investigação de IA |
| **Dados** | Proprietário, líder do setor | Fontes públicas |
| **Pontos Fortes** | Estatísticas de nível profissional | Previsões alimentadas por IA, código aberto |

**Respeito**: A Opta é o padrão da indústria para estatísticas de futebol. Usamos diferentes fontes de dados, mas admiramos o seu rigor.

### WINNER12 vs Investigação Académica

| Aspeto | Artigos Académicos | WINNER12 W-5 |
|---|---|---|
| **Precisão** | 63-85% (varia) | 86,3% (binário) |
| **Validação** | Muitas vezes liga única | 5 ligas, validação cruzada |
| **Reproducibilidade** | Às vezes limitada | Totalmente reproduzível (dados + código abertos) |
| **Publicação** | Revistas revistas por pares | Pré-impressão Zenodo + GitHub |
| **Pontos Fortes** | Revisão por pares rigorosa | Implementação prática, transparência |

**Respeito**: A investigação académica impulsiona a inovação. Seguimos os padrões académicos enquanto tornamos o nosso trabalho imediatamente acessível.

---

## Perguntas sobre Dados e Metodologia

### Os dados de treino estão disponíveis publicamente?

Sim. Todos os dados de treino vêm de [Football-Data.co.uk](https://www.football-data.co.uk), uma fonte publicamente acessível. Pode verificar independentemente todos os resultados dos jogos usados nos nossos estudos de validação.

### Como evitam a fuga de dados?

Usamos **validação fora do tempo**:

- **Treino**: Apenas dados de 2015-2022
- **Validação**: Dados de 2022-2025 (o modelo nunca viu isto durante o treino)
- **Divisão temporal**: Nenhuma informação futura vaza para previsões passadas

Este é o padrão ouro na previsão de séries temporais para evitar o sobreajuste.

### Por que previsões binárias em vez de três vias?

Relatamos ambas:

- **Binário (Vitória/Derrota)**: 86,3% de precisão — problema mais fácil, maior precisão, comum em benchmarks académicos
- **Três vias (Vitória/Empate/Derrota)**: ~79% de precisão — problema mais difícil, inclui previsão de empate

As previsões binárias são úteis para:
- Comparações académicas (muitos artigos usam binário)
- Cenários onde empates são menos relevantes (jogos a eliminar)
- Demonstração de desempenho de limite superior

As previsões de três vias são mais práticas para jogos de liga.

### Com que frequência o modelo é atualizado?

**Atualizações de Dados**: Trimestralmente (a cada 3 meses) com novos resultados de jogos
**Retreino do Modelo**: Anualmente (a cada verão) com dados de temporada completa
**Atualizações de Código**: Contínuas (correções de bugs, melhorias de recursos)

Verifique o [CHANGELOG.md](CHANGELOG.md) para o histórico de atualizações.
