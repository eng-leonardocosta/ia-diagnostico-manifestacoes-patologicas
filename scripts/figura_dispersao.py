"""Gera a Figura 1 (pontuação média por ficha: manifestação x causa).

Uso:  python scripts/figura_dispersao.py   ->  resultados/figura1_dispersao.png
"""
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
d = pd.read_csv(RAIZ / "dados" / "codificacao.csv")
PONTOS = {1: 1.0, 2: 0.5, 0: 0.0}
d["S_m"] = d.mpos.map(PONTOS); d["S_c"] = d.cpos.map(PONTOS)
media = d.groupby("ficha")[["S_m", "S_c"]].mean()

grupos = defaultdict(list)                      # fichas com a mesma posição dividem o ponto
for ficha, r in media.iterrows():
    grupos[(round(r.S_m, 3), round(r.S_c, 3))].append(ficha.replace("Ficha ", ""))

fig, ax = plt.subplots(figsize=(5.0, 3.95), dpi=220)
ax.fill_between([0, 1.05], [0, 1.05], [-0.05, -0.05], color="#efefef", zorder=0)
ax.plot([-0.05, 1.05], [-0.05, 1.05], color="#7a7a7a", lw=1, ls="--", zorder=1)
ax.text(0.03, 0.97, "acima da diagonal:\nacerta a causa mais do que\ndescreve a manifestação", ha="left", va="top", fontsize=7, color="#555")
ax.text(0.97, -0.035, "abaixo da diagonal:\nreconhece a manifestação\nmais do que acerta a causa", ha="right", va="bottom", fontsize=7, color="#555")
for (x, y), fs in grupos.items():
    n = len(fs); rot = ", ".join(sorted(fs))
    ax.scatter([x], [y], s=40 + 55 * (n - 1), facecolor="#3b3b3b", edgecolor="white", linewidth=1.5, zorder=3)
    if n >= 4:
        ax.text(x + 0.02, y + 0.055, rot, ha="right", va="bottom", fontsize=7, color="#222", zorder=4)
    elif x > 0.9:
        ax.text(x - 0.03, y, rot, ha="right", va="center", fontsize=7, color="#222", zorder=4)
    else:
        ax.text(x + 0.03, y, rot, ha="left", va="center", fontsize=7, color="#222", zorder=4)
t = [0, 1 / 6, 2 / 6, 3 / 6, 4 / 6, 5 / 6, 1]; rot_t = ["0", "0,17", "0,33", "0,50", "0,67", "0,83", "1"]
ax.set_xticks(t); ax.set_yticks(t); ax.set_xticklabels(rot_t); ax.set_yticklabels(rot_t)
ax.set_xlim(-0.05, 1.08); ax.set_ylim(-0.05, 1.13)
ax.grid(color="#e3e3e3", lw=0.6); ax.set_axisbelow(True)
for s in ["top", "right"]: ax.spines[s].set_visible(False)
ax.set_xlabel("Pontuação média da manifestação (0 = ausente; 1 = exata)")
ax.set_ylabel("Pontuação média da causa (0 = ausente; 1 = exata)")
fig.tight_layout()
(RAIZ / "resultados").mkdir(exist_ok=True)
fig.savefig(RAIZ / "resultados" / "figura1_dispersao.png")
print("resultados/figura1_dispersao.png")
