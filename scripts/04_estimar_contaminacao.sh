#!/bin/bash

# Estimativa de contaminação com VerifyBamID2
# Requer CRAM, referência genômica e arquivos de recurso pré-instalados com o pacote

set -e

source config.sh

mkdir -p "$RESULTS_DIR"

# Caminho base para os arquivos de referência pré-instalados com o VerifyBamID2
VERIFYBAMID2_RESOURCE="$CONDA_PREFIX/share/verifybamid2*/resource/1000g.phase3.100k.b38.vcf.gz.dat"

# Prefixo de saída
OUTPUT_PREFIX="$RESULTS_DIR/verifybamid2"

# Executa a estimativa
verifybamid2 \
  --BamFile "$CRAM" \
  --Reference "$REF_FASTA" \
  --SVDPrefix "$VERIFYBAMID2_RESOURCE" \
  --Output "$OUTPUT_PREFIX" \
  --NumThread 2
