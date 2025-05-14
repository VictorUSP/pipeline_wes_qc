#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Diretórios
RESULTS_DIR = "results"
FIGURES_DIR = os.path.join(RESULTS_DIR, "figures")
os.makedirs(FIGURES_DIR, exist_ok=True)

# === 1. Cobertura por base (depth.txt) ===
depth_path = os.path.join(RESULTS_DIR, "depth.txt")
depth_df = pd.read_csv(depth_path, sep='\t', header=None, names=["chr", "pos", "depth"])

# Gráfico 1: Histograma da profundidade
plt.figure(figsize=(10, 5))
sns.histplot(depth_df["depth"], bins=100, kde=False, color="steelblue")
plt.title("Distribuição da profundidade por base")
plt.xlabel("Profundidade (x)")
plt.ylabel("Número de bases")
plt.xlim(0, min(200, depth_df["depth"].max()))
plt.tight_layout()
plt.savefig(os.path.join(FIGURES_DIR, "histograma_profundidade.png"))

# Gráfico 2: Curva acumulada de cobertura
thresholds = [1, 5, 10, 20, 30, 50, 100]
coverage = [(depth_df["depth"] >= t).mean() * 100 for t in thresholds]

plt.figure(figsize=(8, 4))
sns.lineplot(x=thresholds, y=coverage, marker="o")
plt.title("Cobertura acumulada")
plt.xlabel("Profundidade mínima (x)")
plt.ylabel("Porcentagem de bases cobertas (%)")
plt.ylim(0, 100)
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(FIGURES_DIR, "cobertura_acumulada.png"))

# === 2. Relatório resumido ===
print("\n📄 Relatório de Cobertura (coverage_report.txt):\n")
with open(os.path.join(RESULTS_DIR, "coverage_report.txt")) as f:
    print(f.read())

# === 3. Inferência de sexo ===
print("\n📄 Inferência de Sexo (sexo_inferido.txt):\n")
with open(os.path.join(RESULTS_DIR, "sexo_inferido.txt")) as f:
    print(f.read())

# === 4. Estimativa de contaminação (VerifyBamID2) ===
selfsm_path = os.path.join(RESULTS_DIR, "verifybamid2.selfSM")

if os.path.exists(selfsm_path):
    try:
        selfsm = pd.read_csv(selfsm_path, sep='\t', comment='#')
        # Tenta localizar a coluna que contenha 'FREEMIX'
        freemix_col = [col for col in selfsm.columns if "FREEMIX" in col.upper()]
        if freemix_col:
            freemix_value = selfsm[freemix_col[0]].values[0]
            print(f"\n📄 Contaminação estimada ({freemix_col[0]}): {freemix_value:.6f}")
        else:
            print("\n⚠️  Coluna 'FREEMIX' não encontrada no arquivo selfSM.")
            print("🧪 Colunas detectadas:", selfsm.columns.tolist())
    except Exception as e:
        print("\n❌ Erro ao ler o arquivo selfSM:", str(e))
else:
    print("\n⚠️  Arquivo verifybamid2.selfSM não encontrado.")

