import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pdfplumber

st.set_page_config(page_title="Auditoria SIGA vs OS - APS", page_icon="📊", layout="wide")

st.title("📊 Painel Executivo de Auditoria: SIGA vs Organização Social")
st.markdown("Plataforma de reconciliação de dados da Atenção Primária à Saúde para validação de metas contratuais.")

# --- UPLOAD DE FICHEIROS ---
st.sidebar.header("📁 Carregamento de Dados")
ficheiro_siga = st.sidebar.file_uploader("1. Extração SIGA (CSV/XLSX)", type=['csv', 'xlsx'])
ficheiro_pdf = st.sidebar.file_uploader("2. Relatório Gestor OS (PDF)", type=['pdf'])

@st.cache_data
def processar_pdf_gestor(ficheiro_pdf):
    linhas_tabela = []
    with pdfplumber.open(ficheiro_pdf) as pdf:
        for pagina in pdf.pages:
            tabela = pagina.extract_table()
            if tabela:
                linhas_tabela.extend(tabela[1:])
    df_pdf = pd.DataFrame(linhas_tabela, columns=['Descritivo_Meta', 'Meta_Prevista', 'Producao_Gestor'])
    df_pdf['Meta_Prevista'] = pd.to_numeric(df_pdf['Meta_Prevista'], errors='coerce').fillna(0)
    df_pdf['Producao_Gestor'] = pd.to_numeric(df_pdf['Producao_Gestor'], errors='coerce').fillna(0)
    return df_pdf

if ficheiro_siga is not None and ficheiro_pdf is not None:
    if ficheiro_siga.name.endswith('.csv'):
        df_siga = pd.read_csv(ficheiro_siga)
    else:
        df_siga = pd.read_excel(ficheiro_siga)

    df_pdf = processar_pdf_gestor(ficheiro_pdf)
    
    # Processamento e Cruzamento
    producao_siga_agrupada = df_siga.groupby(['Procedimento'])['Quantidade'].sum().reset_index()
    producao_siga_agrupada.rename(columns={'Procedimento': 'Descritivo_Meta', 'Quantidade': 'Producao_SIGA'}, inplace=True)
    
    df_cruzamento = pd.merge(df_pdf, producao_siga_agrupada, on="Descritivo_Meta", how="left")
    df_cruzamento['Producao_SIGA'] = df_cruzamento['Producao_SIGA'].fillna(0)
    
    df_cruzamento['Diferenca_Declarada'] = df_cruzamento['Producao_SIGA'] - df_cruzamento['Producao_Gestor']
    
    def avaliar_status(row):
        if row['Diferenca_Declarada'] < 0:
            return 'Superfaturamento OS' 
        elif row['Diferenca_Declarada'] > 0:
            return 'Subnotificado OS' 
        else:
            return 'Validado'
            
    df_cruzamento['Status Auditoria'] = df_cruzamento.apply(avaliar_status, axis=1)

    # --- SEPARADORES (TABS) DA APLICAÇÃO ---
    tab1, tab2, tab3 = st.tabs(["📈 Dashboard Executivo", "📊 Análise Comparativa por CBO", "⚙️ Reconciliação e Exportação"])

    with tab1:
        st.subheader("Visão Geral do Desempenho e Auditoria")
        
        # KPIs Principais
        total_meta = df_cruzamento['Meta_Prevista'].sum()
        total_gestor = df_cruzamento['Producao_Gestor'].sum()
        total_siga = df_cruzamento['Producao_SIGA'].sum()
        perdas_financeiras = abs(df_cruzamento[df_cruzamento['Diferenca_Declarada'] < 0]['Diferenca_Declarada'].sum())

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Meta Contratual Global", f"{total_meta:,.0f}")
        col2.metric("Produção Reportada (OS)", f"{total_gestor:,.0f}")
        col3.metric("Produção Auditada (SIGA)", f"{total_siga:,.0f}", delta=f"{total_siga - total_gestor:,.0f} vs Relatório", delta_color="inverse")
        col4.metric("Desvios de Produção", f"{perdas_financeiras:,.0f} atendimentos")

        st.divider()

        # Gráficos do Dashboard
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Saúde da Auditoria (Volume de Status)**")
            fig_pie = px.pie(df_cruzamento, names="Status Auditoria", hole=0.4, 
                             color="Status Auditoria",
                             color_discrete_map={"Validado": "#2ca02c", "Superfaturamento OS": "#d62728", "Subnotificado OS": "#ff7f0e"})
            st.plotly_chart(fig_pie, use_container_width=True)

        with c2:
            st.markdown("**Alcance de Metas por Procedimento (%)**")
            df_cruzamento['% Alcance SIGA'] = (df_cruzamento['Producao_SIGA'] / df_cruzamento['Meta_Prevista']) * 100
            # Limita a 100% no gráfico para melhor visualização
            df_cruzamento['% Visual'] = df_cruzamento['% Alcance SIGA'].apply(lambda x: 100 if x > 100 else x)
            fig_bar_perc = px.bar(df_cruzamento, x='% Visual', y='Descritivo_Meta', orientation='h',
                                  text=df_cruzamento['% Alcance SIGA'].apply(lambda x: f"{x:.1f}%"),
                                  color='% Visual', color_continuous_scale="Blues")
            fig_bar_perc.update_layout(xaxis_title="% de Alcance Real", yaxis_title="")
            st.plotly_chart(fig_bar_perc, use_container_width=True)

    with tab2:
        st.subheader("Comparativo de Apontamentos: SIGA vs Relatório OS")
        st.markdown("Este gráfico compara lado a lado o volume exigido (Meta), o volume declarado pela OS e o lastro real encontrado no SIGA.")
        
        # Gráfico de Barras Agrupadas
        fig_comparativo = go.Figure()
        fig_comparativo.add_trace(go.Bar(x=df_cruzamento['Descritivo_Meta'], y=df_cruzamento['Meta_Prevista'], name='Meta Prevista', marker_color='lightgrey'))
        fig_comparativo.add_trace(go.Bar(x=df_cruzamento['Descritivo_Meta'], y=df_cruzamento['Producao_Gestor'], name='Declarado (OS)', marker_color='#ff7f0e'))
        fig_comparativo.add_trace(go.Bar(x=df_cruzamento['Descritivo_Meta'], y=df_cruzamento['Producao_SIGA'], name='Real (SIGA)', marker_color='#1f77b4'))
        
        fig_comparativo.update_layout(barmode='group', xaxis_tickangle=-45, legend_title="Fonte de Dados")
        st.plotly_chart(fig_comparativo, use_container_width=True)

    with tab3:
        st.subheader("Matriz de Reconciliação e Ação Administrativa")
        st.markdown("Analise as discrepâncias linha a linha. Exporte a grelha para solicitar correções contratuais ou operacionais à Organização Social.")
        
        # Formatação Condicional
        def destacar_erros(row):
            if row['Status Auditoria'] == 'Superfaturamento OS':
                return ['background-color: #ffcccc'] * len(row)
            elif row['Status Auditoria'] == 'Subnotificado OS':
                return ['background-color: #fff3cd'] * len(row)
            return [''] * len(row)

        colunas = ['Descritivo_Meta', 'Meta_Prevista', 'Producao_Gestor', 'Producao_SIGA', 'Diferenca_Declarada', 'Status Auditoria']
        st.dataframe(
            df_cruzamento[colunas].style.apply(destacar_erros, axis=1),
            use_container_width=True,
            hide_index=True
        )

        csv_export = df_cruzamento[df_cruzamento['Status Auditoria'] != 'Validado'].to_csv(index=False).encode('utf-8')
        st.download_button(label="📥 Exportar Inconsistências (CSV)", data=csv_export, file_name='inconsistencias_os.csv', mime='text/csv')

else:
    st.info("👈 Por favor, faça o carregamento do arquivo CSV (SIGA) e do PDF (Relatório da OS) no menu lateral para gerar o dashboard.")
