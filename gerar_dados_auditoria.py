import pandas as pd
from fpdf import FPDF

def gerar_dados():
    # 1. GERAR CSV DO SIGA (Extração rica com várias linhas para agrupar)
    dados_siga = [
        {"CBO": "ENFERMEIRO", "Procedimento": "CONSULTA ENFERMEIRO ESF", "Quantidade": 1300, "Estabelecimento": "UBS JARDIM NELIA"},
        {"CBO": "ENFERMEIRO", "Procedimento": "CONSULTA ENFERMEIRO ESF", "Quantidade": 100, "Estabelecimento": "UBS JARDIM NELIA"},
        {"CBO": "MEDICO DA ESTRATEGIA DE SAUDE DA FAMILIA", "Procedimento": "CONSULTA MEDICA ESF", "Quantidade": 3800, "Estabelecimento": "UBS JARDIM NELIA"},
        {"CBO": "AGENTE COMUNITÁRIO DE SAÚDE", "Procedimento": "VISITAS DOMICILIARES ACS", "Quantidade": 9700, "Estabelecimento": "UBS JARDIM NELIA"},
        {"CBO": "CIRURGIAO DENTISTA", "Procedimento": "ATENDIMENTO ODONTO (MOD I)", "Quantidade": 424, "Estabelecimento": "UBS JARDIM NELIA"},
        {"CBO": "FARMACEUTICO", "Procedimento": "CONSULTA FARMACEUTICA", "Quantidade": 30, "Estabelecimento": "UBS JARDIM NELIA"},
        {"CBO": "PSICOLOGO", "Procedimento": "CONSULTA PSICOLOGIA", "Quantidade": 71, "Estabelecimento": "UBS JARDIM NELIA"},
    ]
    df_siga = pd.DataFrame(dados_siga)
    df_siga.to_csv('extracao_siga.csv', index=False, encoding='utf-8')
    print("✅ Ficheiro 'extracao_siga.csv' atualizado com sucesso!")

    # 2. GERAR PDF DO GESTOR (Com metas e variações de status)
    dados_pdf = [
        # Descritivo, Meta, Gestor
        ["CONSULTA ENFERMEIRO ESF", "1800", "1423"], # Superfaturado (SIGA=1400)
        ["CONSULTA MEDICA ESF", "4160", "3978"],      # Superfaturado (SIGA=3800)
        ["VISITAS DOMICILIARES ACS", "11600", "9700"],# Validado perfeito (SIGA=9700)
        ["ATENDIMENTO ODONTO (MOD I)", "264", "424"], # Validado perfeito (SIGA=424)
        ["CONSULTA FARMACEUTICA", "48", "25"],        # Subnotificado (Gestor diz 25, SIGA tem 30)
        ["CONSULTA PSICOLOGIA", "60", "71"],          # Validado perfeito (SIGA=71)
    ]
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(90, 10, "Descritivo_Meta", border=1, align='C')
    pdf.cell(40, 10, "Meta_Prevista", border=1, align='C')
    pdf.cell(50, 10, "Producao_Gestor", border=1, ln=True, align='C')

    pdf.set_font("Arial", '', 10)
    for linha in dados_pdf:
        pdf.cell(90, 10, linha[0], border=1)
        pdf.cell(40, 10, linha[1], border=1, align='C')
        pdf.cell(50, 10, linha[2], border=1, ln=True, align='C')

    pdf.output("relatorio_os.pdf")
    print("✅ Ficheiro 'relatorio_os.pdf' atualizado com sucesso!")

if __name__ == "__main__":
    gerar_dados()
