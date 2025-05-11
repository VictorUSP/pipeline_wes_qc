#!/bin/bash

# Download dos arquivos de entrada necessários para o pipeline de WES.
# Os nomes e URLs estão definidos no arquivo config.sh.
# Após o download, os arquivos são verificados por hash MD5.

set -e

source config.sh

mkdir -p "$DATA_DIR"
mkdir -p "$REFERENCE_DIR"

# Download dos arquivos .cram, .crai e BED
wget -O "$CRAM" "$CRAM_URL"
wget -O "$CRAI" "$CRAI_URL"
wget -O "$BED" "$BED_URL"

# Download da referência genômica (mesma usada para gerar o arquivo .cram)
wget -O "$REF_FASTA" "https://ftp.1000genomes.ebi.ac.uk/vol1/ftp/technical/reference/GRCh38_reference_genome/GRCh38_full_analysis_set_plus_decoy_hla.fa"
wget -O "${REF_FASTA}.fai" "https://ftp.1000genomes.ebi.ac.uk/vol1/ftp/technical/reference/GRCh38_reference_genome/GRCh38_full_analysis_set_plus_decoy_hla.fa.fai"

# Verificação da integridade dos arquivos principais (.cram, .crai, .bed)
echo "3d8d8dc27d85ceaf0daefa493b8bd660  $CRAM" | md5sum -c -
echo "15a6576f46f51c37299fc004ed47fcd9  $CRAI" | md5sum -c -
echo "c3a7cea67f992e0412db4b596730d276  $BED"  | md5sum -c -
