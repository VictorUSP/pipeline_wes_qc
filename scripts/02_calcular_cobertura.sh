#!/bin/bash

# Calcula a cobertura nas regiões exônicas a partir do arquivo .cram
# Gera um relatório com profundidade média e percentual de cobertura ≥10x e ≥30x

set -e

source config.sh

mkdir -p "$RESULTS_DIR"

DEPTH_FILE="$RESULTS_DIR/depth.txt"
REPORT_FILE="$RESULTS_DIR/coverage_report.txt"

# Calcula profundidade por posição nas regiões do BED usando samtools
samtools depth -a -b "$BED" --reference "$REF_FASTA" "$CRAM" > "$DEPTH_FILE"

# Processa o arquivo de profundidade e calcula estatísticas básicas
awk '
BEGIN {
  total = 0;
  soma = 0;
  acima10 = 0;
  acima30 = 0;
}
{
  d = $3;
  soma += d;
  total++;
  if (d >= 10) acima10++;
  if (d >= 30) acima30++;
}
END {
  media = (total > 0) ? soma / total : 0;
  p10 = (total > 0) ? (acima10 / total) * 100 : 0;
  p30 = (total > 0) ? (acima30 / total) * 100 : 0;
  printf "Profundidade média: %.2fx\n", media;
  printf "Cobertura ≥10x: %.2f%%\n", p10;
  printf "Cobertura ≥30x: %.2f%%\n", p30;
}
' "$DEPTH_FILE" > "$REPORT_FILE"

echo "Relatório de cobertura salvo em: $REPORT_FILE"

