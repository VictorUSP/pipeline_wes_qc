# Arquivos padrão usados neste projeto Pipeline-WES-QC
# Para adaptar para outras amostras, basta trocar os nomes e as URLs abaixo.

# Diretórios
DATA_DIR="data"
REFERENCE_DIR="reference"
RESULTS_DIR="results"
LOGS_DIR="logs"

# Nomes dos arquivos (editável)
CRAM_FILENAME="NA06994.alt_bwamem_GRCh38DH.20150826.CEU.exome.cram"
CRAI_FILENAME="NA06994.alt_bwamem_GRCh38DH.20150826.CEU.exome.cram.crai"
BED_FILENAME="hg38_exome_v2.0.2_targets_sorted_validated.re_annotated.bed"

# Caminhos locais
CRAM="$DATA_DIR/$CRAM_FILENAME"
CRAI="$DATA_DIR/$CRAI_FILENAME"
BED="$DATA_DIR/$BED_FILENAME"
REF_FASTA="$REFERENCE_DIR/GRCh38_full_analysis_set_plus_decoy_hla.fa"

# URLs dos arquivos (editável para outros caminhos)
CRAM_URL="http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/data_collections/1000_genomes_project/data/CEU/NA06994/exome_alignment/$CRAM_FILENAME"
CRAI_URL="http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/data_collections/1000_genomes_project/data/CEU/NA06994/exome_alignment/$CRAI_FILENAME"
BED_URL="https://www.twistbioscience.com/sites/default/files/resources/2022-12/$BED_FILENAME"

