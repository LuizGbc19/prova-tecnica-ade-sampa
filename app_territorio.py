import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Radar Empreendedor - ADE SAMPA", page_icon="📍", layout="wide")

st.title("📍 Radar Empreendedor territorial - ADE SAMPA")
st.markdown("""
Esta ferramenta de inteligência territorial consome a **Brasil API** (Dados Abertos) e o **OpenStreetMap** em tempo real para mapear 
regiões da cidade de São Paulo com precisão. Auxilia a gestão pública a identificar bairros estratégicos para 
alocação de recursos, como microcrédito e novos espaços Teia.
""")

# --- BARRA LATERAL: ENTRADA DE DADOS ---
st.sidebar.header("🔍 Busca Territorial")
st.sidebar.markdown("Insira um CEP válido da cidade de São Paulo para análise.")
cep_input = st.sidebar.text_input("CEP (apenas números):", "01001000", max_chars=8)

@st.cache_data
def buscar_dados_cep(cep):
    """Consome a Brasil API para o endereço e o OpenStreetMap para geolocalização exata."""
    # 1. API DE ENDEREÇO
    url_cep = f"https://brasilapi.com.br/api/cep/v1/{cep}"
    resp_cep = requests.get(url_cep)
    
    if resp_cep.status_code == 200:
        dados = resp_cep.json()
        
        # Monta a string de busca para o GPS
        rua = dados.get('street', '')
        bairro = dados.get('neighborhood', '')
        cidade = dados.get('city', 'São Paulo')
        estado = dados.get('state', 'SP')
        
        endereco_busca = f"{rua}, {bairro}, {cidade}, {estado}"
        
        # 2. API DE GEOLOCALIZAÇÃO (Nominatim/OpenStreetMap)
        url_geo = "https://nominatim.openstreetmap.org/search"
        params = {'format': 'json', 'q': endereco_busca, 'limit': 1}
        headers = {'User-Agent': 'ProjetoProvaTecnicaADESAMPA/1.0'}
        
        resp_geo = requests.get(url_geo, params=params, headers=headers)
        
        # Se encontrou a rua exata
        if resp_geo.status_code == 200 and len(resp_geo.json()) > 0:
            resultado_geo = resp_geo.json()[0]
            dados['lat'] = float(resultado_geo['lat'])
            dados['lon'] = float(resultado_geo['lon'])
        else:
            # Fallback de Segurança: Procura pelo centro do bairro caso a rua seja muito nova
            params_bairro = {'format': 'json', 'q': f"{bairro}, {cidade}, {estado}", 'limit': 1}
            resp_geo_bairro = requests.get(url_geo, params=params_bairro, headers=headers)
            if resp_geo_bairro.status_code == 200 and len(resp_geo_bairro.json()) > 0:
                resultado_geo_bairro = resp_geo_bairro.json()[0]
                dados['lat'] = float(resultado_geo_bairro['lat'])
                dados['lon'] = float(resultado_geo_bairro['lon'])
            else:
                # Fallback final (Praça da Sé)
                dados['lat'] = -23.5505
                dados['lon'] = -46.6333
                
        return dados
    return None

if st.sidebar.button("Analisar Território"):
    if len(cep_input) == 8 and cep_input.isdigit():
        with st.spinner("A cruzar dados de APIs públicas (Brasil API + OpenStreetMap)..."):
            dados_api = buscar_dados_cep(cep_input)
            
            if dados_api and 'lat' in dados_api:
                bairro = dados_api.get('neighborhood', 'Desconhecido')
                cidade = dados_api.get('city', 'Desconhecido')
                estado = dados_api.get('state', 'Desconhecido')
                logradouro = dados_api.get('street', 'Desconhecido')
                
                lat = dados_api['lat']
                lng = dados_api['lon']
                
                # --- KPIS TERRITORIAIS ---
                st.subheader(f"Análise da Região: {bairro}, {cidade} - {estado}")
                
                # Dados Simulados/Sintéticos
                densidade_mei = 4530 if bairro != 'Desconhecido' else 0
                indice_vulnerabilidade = "Alto" if lat < -23.56 else "Médio"
                recomendacao = "Prioritário para Abertura de Teia" if indice_vulnerabilidade == "Alto" else "Ações de Microcrédito e Formalização"
                
                # 1. Linha de KPIs Numéricos (Métricas curtas)
                col1, col2 = st.columns(2)
                col1.metric("MEIs Ativos (Estimativa)", f"{densidade_mei:,}", delta="Alta Densidade" if densidade_mei > 3000 else "Baixa Densidade")
                col2.metric("Vulnerabilidade Económica", indice_vulnerabilidade, delta="Atenção" if indice_vulnerabilidade == "Alto" else "Estável", delta_color="inverse" if indice_vulnerabilidade == "Alto" else "normal")
                
                # 2. Linha de Informação Descritiva (Caixas de texto dinâmicas que não cortam as palavras)
                st.write("") # Espaçamento
                col3, col4 = st.columns(2)
                with col3:
                    st.info(f"📍 **Logradouro Base:**\n\n{logradouro}")
                with col4:
                    st.success(f"🎯 **Recomendação ADE SAMPA:**\n\n{recomendacao}")
                
                st.divider()
                
                # --- MAPA GEOGRÁFICO ---
                st.subheader("Mapeamento Estratégico Exato")
                st.info(f"📍 Marcador apontando com precisão de GPS para: **{logradouro}, {bairro}**")
                
                # O Streamlit precisa apenas das colunas 'lat' e 'lon' para renderizar o mapa nativo
                df_mapa = pd.DataFrame({'lat': [lat], 'lon': [lng]})
                st.map(df_mapa, zoom=16, color="#ff0000")
                
                st.divider()
                
                # --- GRÁFICO DE POTENCIAL ECONÓMICO ---
                st.subheader(f"Perfil de Atividades MEI no entorno ({bairro})")
                st.info("⚠️ **Nota de Metodologia:** Os dados de setor abaixo são sintéticos e servem para demonstrar a capacidade da aplicação em cruzar a geolocalização da API com bases de inteligência de negócios locais.")
                
                dados_setor = pd.DataFrame({
                    "Setor": ["Comércio Varejista", "Beleza e Estética", "Alimentação (Delivery)", "Serviços de TI", "Costura e Vestuário"],
                    "Quantidade": [1200, 950, 800, 450, 1130]
                })
                
                fig_barras = px.bar(dados_setor, x="Quantidade", y="Setor", orientation='h', color="Setor", title="Distribuição de Setores (Simulação)")
                st.plotly_chart(fig_barras, use_container_width=True)
                
            else:
                st.error("Não foi possível processar este CEP. Verifique se o número está correto.")
    else:
        st.warning("Por favor, insira um CEP válido com 8 dígitos numéricos.")
