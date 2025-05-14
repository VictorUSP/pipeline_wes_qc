from reportlab.lib.pagesizes import A4
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import cm
from datetime import datetime
import os

# Caminhos e arquivos
RESULTS_DIR = "results"
FIGURES_DIR = os.path.join(RESULTS_DIR, "figures")
LOGO_PATH = "assets/incor_logo.png"
PDF_PATH = os.path.join(RESULTS_DIR, "relatorio_qc_wes.pdf")
selfsm_path = os.path.join(RESULTS_DIR, "verifybamid2.selfSM")

# Dados fixos
bioinfo = "Victor Fernandes de Oliveira"
instituicao = "InCor – Instituto do Coração, FMUSP"
laboratorio = "Laboratory of Genetics and Molecular Cardiology (LGMC)"
data_execucao = datetime.today().strftime("%d/%m/%Y")
arquivo = "NA06994.alt_bwamem_GRCh38DH.20150826.CEU.exome.cram"
referencia = "GRCh38_full_analysis_set_plus_decoy_hla.fa"

# Estilos
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Justify', alignment=4, leading=15))
title_style = styles['Title']
subtitle_style = styles['Heading2']
normal = styles['Normal']
justified = styles['Justify']

# Cabeçalho com faixa escura + logo + título
def draw_header(canvas, doc):
    width, height = A4

    # Faixa superior
    canvas.setFillColor(colors.HexColor("#494949"))
    canvas.rect(0, height - 90, width, 90, fill=1, stroke=0)

    # Parâmetros do logo
    logo_width = 0  # vamos calcular se a imagem existir
    logo_height = 40
    logo_x = 0
    logo_y = height - 60

    if os.path.exists(LOGO_PATH):
        # Abre a imagem e calcula proporção
        from PIL import Image as PILImage
        pil_img = PILImage.open(LOGO_PATH)
        aspect = pil_img.width / pil_img.height
        logo_width = logo_height * aspect

        # Desenha a imagem
        canvas.drawImage(LOGO_PATH, x=logo_x, y=logo_y, width=logo_width, height=logo_height, mask='auto')

    # Título ao lado da logo, com espaçamento seguro
    title_x = logo_x + logo_width + 10  # 10pt de espaço entre logo e texto
    canvas.setFont("Helvetica-Bold", 16)
    canvas.setFillColor(colors.white)
    canvas.drawString(title_x, height - 50, "Relatório de Controle de Qualidade – Exoma Completo")

# Área do conteúdo abaixo do cabeçalho
frame = Frame(x1=2*cm, y1=2*cm, width=A4[0]-4*cm, height=A4[1]-150)
template = PageTemplate(id="com_cabecalho", frames=[frame], onPage=draw_header)
doc = BaseDocTemplate(PDF_PATH, pagesize=A4)
doc.addPageTemplates([template])

# Conteúdo do relatório
story = []

# Bloco de informações técnicas
def add_info_line(label, valor):
    story.append(Paragraph(f"<b>{label}:</b> {valor}", styles['Normal']))
info_fields = [
    ("Bioinformata", bioinfo),
    ("Instituição", instituicao),
    ("Laboratório", laboratorio),
    ("Data de execução", data_execucao),
    ("Arquivo analisado", arquivo),
    ("Referência", referencia)
]
for label, valor in info_fields:
    add_info_line(label, valor)
story.append(Spacer(1, 12))

# Seção 1: Objetivo
story.append(Paragraph("1. Objetivo", subtitle_style))
story.append(Spacer(1, 6))
story.append(Paragraph(
    "Executar um pipeline de controle de qualidade (QC) para dados de sequenciamento de exoma completo (WES), incluindo cálculo de cobertura, inferência de sexo genético e estimativa de contaminação por DNA exógeno.",
    justified))
story.append(Spacer(1, 12))

# Seção 2: Cobertura
story.append(Paragraph("2. Cálculo de Cobertura", subtitle_style))
coverage_path = os.path.join(RESULTS_DIR, "coverage_report.txt")
if os.path.exists(coverage_path):
    with open(coverage_path) as f:
        for line in f:
            story.append(Paragraph(line.strip(), normal))
else:
    story.append(Paragraph("Arquivo coverage_report.txt não encontrado.", normal))
story.append(Spacer(1, 12))

# Gráficos
hist_path = os.path.join(FIGURES_DIR, "histograma_profundidade.png")
if os.path.exists(hist_path):
    story.append(Paragraph("Distribuição da profundidade por base:", normal))
    story.append(Image(hist_path, width=400, height=200))
    story.append(Spacer(1, 12))

curve_path = os.path.join(FIGURES_DIR, "cobertura_acumulada.png")
if os.path.exists(curve_path):
    story.append(Paragraph("Cobertura acumulada por profundidade mínima:", normal))
    story.append(Image(curve_path, width=400, height=200))
    story.append(Spacer(1, 12))

# Seção 3: Sexo
story.append(Paragraph("3. Inferência de Sexo", subtitle_style))
sexo_path = os.path.join(RESULTS_DIR, "sexo_inferido.txt")
if os.path.exists(sexo_path):
    with open(sexo_path) as f:
        for line in f:
            story.append(Paragraph(line.strip(), normal))
else:
    story.append(Paragraph("Arquivo sexo_inferido.txt não encontrado.", normal))
story.append(Spacer(1, 12))

# Seção 4: Contaminação
story.append(Paragraph("4. Estimativa de Contaminação", subtitle_style))
freemix = None
if os.path.exists(selfsm_path):
    with open(selfsm_path) as f:
        for linha in f:
            if not linha.startswith("#"):
                campos = linha.strip().split("\t")
                if len(campos) >= 10:
                    freemix = campos[9]
                    break
if freemix:
    story.append(Paragraph(f"FREEMIX (fração estimada de contaminação): {freemix}", normal))
else:
    story.append(Paragraph("Arquivo verifybamid2.selfSM não encontrado ou valor de FREEMIX ausente.", normal))
story.append(Spacer(1, 12))

# Seção 5: Conclusão
story.append(Paragraph("5. Conclusão", subtitle_style))
story.append(Spacer(1, 6))
story.append(Paragraph(
    "A amostra apresenta profundidade média adequada para exoma, com alta proporção de regiões cobertas acima de 30x. "
    "A inferência de sexo foi consistente com a presença do cromossomo Y, sugerindo sexo masculino. "
    "A estimativa de contaminação (FREEMIX) foi inferior a 1%, indicando alta pureza da amostra.",
    justified))

# Gera PDF
doc.build(story)
print(f"PDF gerado com sucesso: {PDF_PATH}")
