# 📊 Portfólio de Soluções de Dados e IA - ADE SAMPA
**Prova Técnica Prática (Edital 005/2026) - Cargo: Assistente II (Dados e IA)**

Este repositório contém a resolução de **dois problemas estratégicos** da gestão municipal de São Paulo, abordando desde a auditoria financeira na Saúde até à inteligência territorial para fomento económico.

---

## 📌 1. Títulos dos Projetos
*   **Solução 1:** Painel Executivo de Auditoria - SIGA vs Organizações Sociais (OS).
*   **Solução 2:** Radar Empreendedor Territorial - Mapeamento e Inteligência (APIs).

## ❗ 2. Descrição dos Problemas Identificados
*   **Problema 1 (Saúde):** A validação mensal do cumprimento de metas das Organizações Sociais exige um cruzamento exaustivo entre os relatórios declarados em PDF e as extrações brutas do sistema SIGA/BPA. Esta validação manual atrasa a deteção de gargalos operacionais ou possíveis "superfaturamentos" nas faturas enviadas à Prefeitura.
*   **Problema 2 (Desenvolvimento Económico):** A identificação rápida de territórios estratégicos para alocar recursos de fomento ao microempreendedor (como novos espaços Teia ou unidades do Cate) carece de ferramentas ágeis que convertam um simples código postal (CEP) num perfil socioeconómico geolocalizado em tempo real.

## 📖 3. Contexto e Justificativa da Escolha
A eficiência na alocação do dinheiro público é o pilar de ambas as soluções. Na **Solução 1**, automatizar a auditoria protege o erário municipal de repasses indevidos por serviços não prestados. Na **Solução 2**, o uso de inteligência geográfica garante que as políticas de microcrédito e qualificação profissional da ADE SAMPA cheguem aos bairros periféricos que mais necessitam, com base em dados concretos e não em suposições empíricas.

## 🏛️ 4. Secretarias e Áreas Municipais Relacionadas
*   **Solução 1:** Secretaria Municipal da Saúde (SMS) - Gestão de Contratos com Organizações Sociais de Saúde.
*   **Solução 2:** Agência São Paulo de Desenvolvimento (ADE SAMPA) e Secretaria Municipal de Desenvolvimento Económico e Trabalho (SMDET).

## 💻 5. Descrição das Soluções Desenvolvidas
*   **Painel de Auditoria (`app.py`):** Aplicação web de *parsing* e reconciliação. Cruza um PDF gerencial com um CSV oficial, calculando linha a linha a diferença entre a meta exigida, a produção declarada e o lastro real encontrado no sistema municipal, gerando alertas de inconsistência.
*   **Radar Territorial (`app_territorio.py`):** Ferramenta web conectada à *cloud*. O utilizador insere um CEP e o sistema consome APIs públicas para devolver a morada exata, renderizar um mapa com coordenadas GPS precisas e apresentar um painel de indicadores sobre a atividade de Microempreendedores Individuais (MEIs) na região.

## 👥 6. Público e Área da Gestão Beneficiada
Auditores de faturamento do SUS, Coordenadores de Unidades Básicas de Saúde (UBS), Analistas de Inteligência de Mercado da ADE SAMPA e formuladores de políticas públicas de microcrédito.

## ⚙️ 7. Principais Funcionalidades
*   *Parsing* automatizado de grelhas em ficheiros PDF não estruturados.
*   Cruzamento de *DataFrames* para identificação de desvios padrão (subnotificação e superfaturamento).
*   Consumo em cascata de duas APIs públicas (Brasil API + OpenStreetMap).
*   Visualização geográfica interativa nativa e painéis de indicadores (KPIs).
*   Exportação automática de relatórios de discrepância em formato CSV.

## 🔍 8. Fontes Pesquisadas
*   Modelos de Relatórios de Medição de Produção Mensal (OS Santa Marcelina - Supervisão Itaim Paulista).
*   Documentação da **Brasil API** (Dados abertos brasileiros).
*   Documentação da API **Nominatim / OpenStreetMap**.
*   Conceitos de espacialização das plataformas GeoSampa e IBGE.

## 📊 9. Dados Utilizados
*   **Ficheiros Locais:** Leitura de `.csv` e `.pdf` submetidos pelo utilizador.
*   **Rede (APIs):** Respostas JSON contendo dados de logradouros, bairros, municípios e coordenadas (Latitude/Longitude).

## ⚠️ 10. Indicação Clara de Dados Sintéticos e Simulados
Para proteção de dados reais de utentes do SUS e sigilo empresarial (LGPD), **esta prova utiliza dados sintéticos**:
*   **Na Solução 1:** Foi desenvolvido o script `gerar_dados_auditoria.py` que gera um CSV e um PDF com desvios matemáticos intencionais para demonstrar o mecanismo de alerta de fraudes/gargalos do sistema.
*   **Na Solução 2:** Enquanto as coordenadas geográficas e os endereços são **100% reais e dinâmicos** (oriundos das APIs), os indicadores de "Densidade de MEI" e o "Gráfico de Setores" são gerados com base em regras de negócio simuladas para exemplificar o cruzamento de bases.

## ⚖️ 11. Justificativa das Principais Escolhas Realizadas
*   A escolha do ecossistema **Streamlit** justifica-se pela rapidez em entregar uma interface executiva (UI/UX) focada em dados, sem a necessidade de manter complexos servidores *front-end*.
*   O uso de dupla API no Radar Territorial garante resiliência: se a Brasil API não devolver a geolocalização exata, o sistema possui um *fallback* inteligente para buscar as coordenadas via OpenStreetMap.

## 🛠️ 12. Metodologia e Tecnologias (Stack Tecnológico)
*   **Linguagem:** Python 3.
*   **Framework Web:** Streamlit.
*   **Manipulação de Dados:** Pandas.
*   **Extração de Documentos:** pdfplumber, fpdf (para geração da simulação).
*   **Integração Web:** Requests.
*   **Visualização:** Plotly Express.

## 🤖 13. Utilização de Inteligência Artificial Generativa
Ferramentas de IA (LLMs) foram empregues em regime de *vibe coding* nas seguintes etapas:
*   Criação da lógica geradora de dados sintéticos (para o PDF e CSV de teste).
*   Estruturação do *parsing* das respostas JSON provenientes das APIs públicas.
*   Refatoração estética da interface, organizando o código Streamlit em separadores (*tabs*) e otimizando a distribuição dos gráficos.

## 🚧 14. Limitações Identificadas
*   O motor de leitura de PDFs (`pdfplumber`) é sensível a grandes alterações na formatação das grelhas submetidas pela Organização Social.
*   O serviço gratuito do OpenStreetMap possui *rate limits* (limite de requisições), o que pode gerar instabilidade se dezenas de agentes realizarem procuras no exato mesmo segundo.

## 🚀 15. Possíveis Melhorias ou Evoluções
*   **Integração de Base de Dados:** Ligar o sistema diretamente ao PostgreSQL/MySQL municipal, dispensando o *upload* manual de ficheiros CSV.
*   **Substituição de Mockups:** No Radar Territorial, ligar o painel à API oficial da Receita Federal (CNPJ) para trazer o número absoluto de MEIs ativos no bairro, em tempo real.

---

## 💻 16. Instruções para Instalação e Execução

O projeto encontra-se pronto para avaliação e deve ser executado localmente.

**Requisitos do Ambiente:**
*   Python 3.9 ou superior.
*   Conexão estável à Internet (para consumo de APIs e bibliotecas).

**1. Instalação das Dependências:**
Abra o seu terminal (Linha de Comandos) no diretório do projeto e instale as bibliotecas necessárias:
```bash
python -m pip install streamlit pandas plotly pdfplumber fpdf requests
