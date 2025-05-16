# Pipeline-WES-QC

Pipeline automatizado para controle de qualidade de dados de Whole Exome Sequencing (WES), implementado com Bash e Python. 
Este projeto foi desenvolvido como parte de um desafio técnico no InCor – Instituto do Coração, FMUSP,  
no âmbito do Laboratory of Genetics and Molecular Cardiology (LGMC).
---

## Autor

**Victor Fernandes de Oliveira**  
Bioinformata

---

## Descrição do pipeline

Este pipeline executa um fluxo completo de controle de qualidade em dados WES, utilizando um arquivo `.cram` de exoma completo proveniente do projeto 1000 Genomes. As etapas incluem:

1. **Download e verificação dos arquivos**  
2. **Cálculo de cobertura nas regiões exônicas**  
3. **Inferência do sexo genético**  
4. **Estimativa de contaminação por DNA exógeno**  
5. **Geração de relatório final em PDF**

---

## Estrutura de diretórios

```
pipeline_wes_qc/
├── assets/           # Logo do InCor
├── data/             # Arquivos .cram, .crai e BED
├── reference/        # Referência genômica (.fa e .fai)
├── results/          # Saídas e relatórios
│   ├── figures/      # Gráficos gerados pelo Python
│   └── relatorio_qc_wes.pdf
├── logs/             # Logs das execuções
├── scripts/          # Scripts do pipeline
├── config.sh         # Arquivo com os parâmetros
└── README.md
```

---

## Dados utilizados
Os dados de entrada são públicos e não estão incluídos no repositório. Eles são baixados automaticamente de

- Arquivo `.cram`: [1000 Genomes](https://ftp.1000genomes.ebi.ac.uk/vol1/ftp/data_collections/1000_genomes_project/data/CEU/NA06994/exome_alignment/NA06994.alt_bwamem_GRCh38DH.20150826.CEU.exome.cram)
- Arquivo `.crai`: [1000 Genomes](https://ftp.1000genomes.ebi.ac.uk/vol1/ftp/data_collections/1000_genomes_project/data/CEU/NA06994/exome_alignment/NA06994.alt_bwamem_GRCh38DH.20150826.CEU.exome.cram.crai)
- Arquivo BED das regiões exônicas do hg38: [Twist Bioscience](https://www.twistbioscience.com/sites/default/files/resources/2022-12/hg38_exome_v2.0.2_targets_sorted_validated.re_annotated.bed)
- Referência GRCh38 com HLA e decoys: [1000 Genomes – Reference](https://ftp.1000genomes.ebi.ac.uk/vol1/ftp/technical/reference/GRCh38_reference_genome)

> A referência GRCh38 utilizada inclui regiões HLA e sequências “decoy”, e corresponde exatamente à versão utilizada para o mapeamento do arquivo `.cram` fornecido. A consistência entre o alinhamento original e a referência utilizada é fundamental para garantir a validade dos resultados das análises (como o cálculo de cobertura).


> A ferramenta escolhida para a estimativa de contaminação por DNA exógeno foi o **VerifyBamID2**, desenvolvida pelo Broad Institute of MIT. Ela é amplamente utilizada para detectar contaminação em amostras de DNA humano a partir de arquivos BAM/CRAM, utilizando painéis de SNPs populacionais e decomposição por componentes principais (PCA). A principal vantagem do VerifyBamID2 é sua capacidade de estimar com precisão a fração de contaminação (FREEMIX), mesmo em amostras de baixa cobertura ou com ancestrais mistos, sem exigir identificação de genótipos conhecidos da amostra. Além disso, a ferramenta possui painéis pré-calculados disponíveis para GRCh38, compatíveis com o arquivo `.cram` utilizado neste desafio, o que garante consistência com o mapeamento da amostra.

---

## Dependências

### Ambiente recomendado via Conda:

```bash
conda create -n pipeline_wes python=3.12 -c bioconda -c conda-forge
conda activate pipeline_wes
conda install samtools wget verifybamid2 matplotlib pandas reportlab pillow seaborn -c bioconda -c conda-forge

```
---

## Instruções de uso

1. **Clone o repositório:**

```bash
git clone https://github.com/VictorUSP/pipeline_wes_qc.git
cd pipeline_wes_qc
```
2. **Dê permissão de execução aos scripts:**

```bash
chmod +x scripts/*.sh
chmod +x run_pipeline.sh

```

3. **Crie e ative o ambiente Conda:**

```bash
conda create -n pipeline_wes python=3.12 -c bioconda -c conda-forge
conda activate pipeline_wes
```

4. **Instale as dependências:**

```bash
conda install samtools wget verifybamid2 matplotlib pandas reportlab pillow seaborn -c bioconda -c conda-forge
```

5. **Edite config.sh se desejar alterar nomes de arquivos ou URLs**

6. **Execute o pipeline completo:**

```bash
./scripts/run_pipeline.sh
```
> O script é interativo: para cada etapa já executada (por exemplo, se os arquivos já estiverem baixados), será perguntado se deseja pular ou reexecutar. Ou e preferir, pode executar separadamente os scripts com os comandos no item 6 abaixo.


7. **(Opcional) Executar os scripts individualmente:**

```bash
bash scripts/01_download_data.sh             # Baixa arquivos e genoma de referência
bash scripts/02_calcular_cobertura.sh        # Calcula profundidade média e cobertura ≥10x/30x
bash scripts/03_inferir_sexo.sh              # Estima sexo com base em X/Y
bash scripts/04_estimar_contaminacao.sh      # Estima contaminação com VerifyBamID2
python scripts/05_relatorio_qc.py            # Gera gráficos da cobertura
python scripts/06_gerar_relatorio_pdf.py     # Compila o relatório final em PDF

```

7. **Relatório final:**

O relatório final será salvo em:

```bash
results/relatorio_qc_wes.pdf
```


