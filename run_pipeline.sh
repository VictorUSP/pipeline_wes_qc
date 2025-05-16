#!/bin/bash

# Pipeline mestre para controle de qualidade de dados WES
# Autor: Victor Fernandes de Oliveira
# Instituição: InCor – FMUSP - LGCM

set -e
source config.sh

function prompt_skip() {
    local step_name="$1"
    local condition="$2"

    if eval "$condition"; then
        read -p "$step_name já foi executado. Deseja pular? [s/N]: " resp
        [[ "$resp" =~ ^[Ss]$ ]] && return 1
    fi
    return 0
}

mkdir -p logs

# Etapa 1: Download
if prompt_skip "Etapa 1 (Download dos dados)" "[ -f \"$CRAM\" ] && [ -f \"$CRAI\" ] && [ -f \"$BED\" ] && [ -f \"$REF_FASTA\" ]"; then
    bash scripts/01_download_data.sh | tee logs/01_download_data.log
fi

# Etapa 2: Cobertura
if prompt_skip "Etapa 2 (Cálculo de cobertura)" "[ -f results/coverage_report.txt ]"; then
    bash scripts/02_calcular_cobertura.sh | tee logs/02_calcular_cobertura.log
fi

# Etapa 3: Inferência de sexo
if prompt_skip "Etapa 3 (Inferência de sexo)" "[ -f results/sexo_inferido.txt ]"; then
    bash scripts/03_inferir_sexo.sh | tee logs/03_inferir_sexo.log
fi

# Etapa 4: Contaminação
if prompt_skip "Etapa 4 (Estimativa de contaminação)" "[ -f results/verifybamid2.selfSM ]"; then
    bash scripts/04_estimar_contaminacao.sh | tee logs/04_estimar_contaminacao.log
fi

# Etapa 5: Gráficos
if prompt_skip "Etapa 5 (Geração de gráficos)" "[ -f results/figures/histograma_profundidade.png ] && [ -f results/figures/cobertura_acumulada.png ]"; then
    python scripts/05_relatorio_qc.py
fi

# Etapa 6: PDF
if prompt_skip "Etapa 6 (Geração do PDF final)" "[ -f results/relatorio_qc_wes.pdf ]"; then
    python scripts/06_gerar_relatorio_pdf.py
fi

echo "Pipeline concluído com sucesso."
