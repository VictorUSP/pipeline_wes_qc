#!/bin/bash

# Download dos arquivos de entrada necessários para o pipeline de WES.
# Os nomes e URLs estão definidos no arquivo config.sh.
# Após o download, os arquivos são verificados por hash MD5.

set -e

source config.sh

mkdir -p "$DATA_DIR"

# Download dos arquivos .cram, .crai e BED
wget -O "$CRAM" "$CRAM_URL"
wget -O "$CRAI" "$CRAI_URL"
wget -O "$BED" "$BED_URL"

# Verificação da integridade dos arquivos (hashes fornecidos no enunciado do desafio técnico)
echo "3d8d8dc27d85ceaf0daefa493b8bd660  $CRAM" | md5sum -c -
echo "15a6576f46f51c37299fc004ed47fcd9  $CRAI" | md5sum -c -
echo "c3a7cea67f992e0412db4b596730d276  $BED"  | md5sum -c -

