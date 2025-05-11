#!/bin/bash

# Inferência do sexo genético com base na razão de cobertura entre os cromossomos Y e X.
# A análise utiliza samtools idxstats sobre o arquivo .cram já indexado.

set -e

source config.sh

mkdir -p "$RESULTS_DIR"

IDXSTATS_FILE="$RESULTS_DIR/idxstats.txt"
SEXO_FILE="$RESULTS_DIR/sexo_inferido.txt"

# Gera estatísticas de alinhamento por cromossomo
samtools idxstats "$CRAM" > "$IDXSTATS_FILE"

# Processa a razão entre Y e X e infere o sexo com base em um limiar simples
awk '
  $1 == "X" {x = $3}
  $1 == "Y" {y = $3}
  END {
    if (x > 0) {
      ratio = y / x
      printf "Razão Y/X: %.4f\n", ratio > "'"$SEXO_FILE"'"
      if (ratio > 0.05) {
        print "Provável sexo: MASCULINO" >> "'"$SEXO_FILE"'"
      } else {
        print "Provável sexo: FEMININO" >> "'"$SEXO_FILE"'"
      }
    } else {
      print "Cobertura no X insuficiente para inferência." > "'"$SEXO_FILE"'"
    }
  }
' "$IDXSTATS_FILE"

echo "Resultado salvo em: $SEXO_FILE"
