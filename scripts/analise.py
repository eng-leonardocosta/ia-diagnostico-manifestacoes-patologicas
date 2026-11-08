"""Reproduz todos os números do artigo a partir de dados/codificacao.csv.

Uso:  python scripts/analise.py
Saídas: resultados/resultados.json e tabelas CSV em resultados/.
Dependências: numpy, pandas, scipy (ver requirements.txt).
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import binomtest, chi2

RAIZ = Path(__file__).resolve().parents[1]
OUT = RAIZ / "resultados"
OUT.mkdir(exist_ok=True)

d = pd.read_csv(RAIZ / "dados" / "codificacao.csv")
FERR = {"G": "Claude", "H": "ChatGPT", "I": "Gemini"}
PONTOS = {1: 1.0, 2: 0.5, 0: 0.0}           # 1 = acerto pleno, 2 = parcial, 0 = erro
d["manif_exata"] = (d.mpos == 1).astype(int)
d["causa_exata"] = (d.cpos == 1).astype(int)
d["causa_hipoteses"] = (d.cpos > 0).astype(int)
d["grupo_ok"] = (d.grupo_ia == d.grupo_ref).astype(int)
d["S_m"] = d.mpos.map(PONTOS)
d["S_c"] = d.cpos.map(PONTOS)
UMIDADE = d.grupo_ref.str.startswith("Umidade") | (d.grupo_ref == "Vazamento de instalações")


# ---------- coeficientes de concordância (duas fontes, categorias nominais) ----------
def _tabela(a, b):
    cats = sorted(set(a) | set(b))
    pa = pd.Series(a).value_counts(normalize=True).reindex(cats, fill_value=0)
    pb = pd.Series(b).value_counts(normalize=True).reindex(cats, fill_value=0)
    po = float(np.mean(np.asarray(a) == np.asarray(b)))
    return cats, pa, pb, po

def kappa_cohen(a, b):
    """kappa = (po - pe) / (1 - pe); pe = soma(prop. referência x prop. ferramenta)."""
    _, pa, pb, po = _tabela(a, b)
    pe = float((pa * pb).sum())
    return (po - pe) / (1 - pe), po, pe

def pi_scott(a, b):
    _, pa, pb, po = _tabela(a, b)
    pe = float((((pa + pb) / 2) ** 2).sum())
    return (po - pe) / (1 - pe)

def alfa_krippendorff(a, b):
    n = len(a)                                  # 2 avaliadores, sem faltantes, nominal
    vals = list(a) + list(b)
    cats = sorted(set(vals))
    nc = pd.Series(vals).value_counts().reindex(cats, fill_value=0)
    N = 2 * n
    do = float(np.mean(np.asarray(a) != np.asarray(b)))
    de = (N * N - (nc ** 2).sum()) / (N * (N - 1))
    return 1 - do / de

def ac1_gwet(a, b):
    cats, pa, pb, po = _tabela(a, b)
    pi = (pa + pb) / 2
    q = len(cats)
    pe = float((pi * (1 - pi)).sum() / (q - 1))
    return (po - pe) / (1 - pe)

def ic_bootstrap(sub, semente=2026, B=2000):
    """IC 95% do Kappa por reamostragem das fichas (casos), com reposição."""
    rng = np.random.default_rng(semente)
    fichas = sorted(sub.ficha.unique())
    idx = {f: np.where(sub.ficha.values == f)[0] for f in fichas}
    vals = []
    for _ in range(B):
        s = rng.choice(fichas, len(fichas), replace=True)
        bs = sub.iloc[np.concatenate([idx[x] for x in s])]
        k = kappa_cohen(bs.grupo_ref, bs.grupo_ia)[0]
        if np.isfinite(k):
            vals.append(k)
    return [float(x) for x in np.percentile(vals, [2.5, 97.5])]

def faixa_landis_koch(k):
    for lim, nome in [(0, "Pobre"), (0.20, "Leve"), (0.40, "Razoável"), (0.60, "Moderada"), (0.80, "Substancial")]:
        if k <= lim:
            return nome
    return "Quase perfeita"

# ---------- desempenho por ferramenta (Tabela 1) ----------
linhas = []
for cod, sub in list(d.groupby("codigo")) + [("Conjunto", d)]:
    k, po, pe = kappa_cohen(sub.grupo_ref, sub.grupo_ia)
    li, ls = ic_bootstrap(sub)
    linhas.append({
        "ferramenta": FERR.get(cod, "Conjunto"), "codigo": cod, "n": len(sub),
        "manif_exata": sub.manif_exata.mean(), "causa_exata": sub.causa_exata.mean(),
        "causa_entre_hipoteses": sub.causa_hipoteses.mean(),
        "po_grupo": po, "pe_acaso": pe, "kappa": k, "kappa_ic95": [li, ls], "faixa": faixa_landis_koch(k),
        "pi_scott": pi_scott(sub.grupo_ref, sub.grupo_ia),
        "alfa_krippendorff": alfa_krippendorff(sub.grupo_ref, sub.grupo_ia),
        "ac1_gwet": ac1_gwet(sub.grupo_ref, sub.grupo_ia),
    })
T1 = pd.DataFrame(linhas)
T1.to_csv(OUT / "tabela1_desempenho.csv", index=False)

# ---------- reconhecer x diagnosticar (McNemar exato) ----------
b = int(((d.manif_exata == 1) & (d.causa_exata == 0)).sum())   # só manifestação
c = int(((d.manif_exata == 0) & (d.causa_exata == 1)).sum())   # só causa
mcnemar_p = binomtest(b, b + c, 0.5).pvalue
tab2x2 = {"ambas": int(((d.manif_exata == 1) & (d.causa_exata == 1)).sum()), "so_manifestacao": b,
          "so_causa": c, "nenhuma": int(((d.manif_exata == 0) & (d.causa_exata == 0)).sum())}

# ---------- diferença entre ferramentas na causa exata (Q de Cochran) ----------
w = d.pivot(index="ficha", columns="codigo", values="causa_exata")
k_ = w.shape[1]; Cj = w.sum(axis=0); Ri = w.sum(axis=1); N = Cj.sum()
Q = (k_ - 1) * (k_ * (Cj ** 2).sum() - N ** 2) / (k_ * N - (Ri ** 2).sum())
cochran_p = float(chi2.sf(Q, k_ - 1))

# ---------- grupos de causa (Tabela 2) e umidade ----------
T2 = d.groupby("grupo_ref").agg(casos=("ficha", "nunique"), causa_exata=("causa_exata", "mean"),
                                 causa_entre_hipoteses=("causa_hipoteses", "mean"))
T2.sort_values("causa_exata", ascending=False).to_csv(OUT / "tabela2_grupos_de_causa.csv")
umid = {"umidade_causa_exata": d[UMIDADE].causa_exata.mean(), "demais_causa_exata": d[~UMIDADE].causa_exata.mean(),
        "n_umidade": int(UMIDADE.sum()), "n_demais": int((~UMIDADE).sum())}

# ---------- confiança declarada ----------
conf = (d.groupby(["ferramenta", "confianca"]).size().unstack(fill_value=0)).to_dict(orient="index")
alta_I = d[(d.codigo == "I") & (d.confianca == "A")]
sobreconf = d[(d.confianca == "A") & (d.cpos == 0)][["ficha", "ferramenta"]].values.tolist()

# ---------- pontuação média por ficha (Figura 1) ----------
fig = d.groupby("ficha")[["S_m", "S_c"]].mean().round(3)
fig.to_csv(OUT / "figura1_pontuacao_por_ficha.csv")

res = {"tabela1": linhas, "mcnemar_manif_x_causa": {"tabela": tab2x2, "p_exato": mcnemar_p},
       "cochran_q_causa_exata": {"Q": float(Q), "gl": k_ - 1, "p": cochran_p}, "umidade": umid,
       "confianca": conf, "ferramenta_I_alta": {"n": len(alta_I), "causa_exata": int(alta_I.causa_exata.sum())},
       "confianca_alta_sem_causa": sobreconf}
json.dump(res, open(OUT / "resultados.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2, default=float)

pd.set_option("display.width", 200)
print(T1[["ferramenta", "manif_exata", "causa_exata", "causa_entre_hipoteses", "po_grupo", "pe_acaso", "kappa",
          "kappa_ic95", "faixa", "pi_scott", "alfa_krippendorff", "ac1_gwet"]].round(3).to_string(index=False))
print(f"\nMcNemar (manifestação x causa): {tab2x2}  p exato = {mcnemar_p:.3f}")
print(f"Q de Cochran (causa exata, 3 ferramentas): Q = {Q:.2f}; p = {cochran_p:.2f}")
print(f"Umidade: {umid['umidade_causa_exata']:.1%} x demais {umid['demais_causa_exata']:.1%}")
print(f"Ferramenta I, confiança alta: {len(alta_I)} respostas, causa exata em {int(alta_I.causa_exata.sum())}")
print(f"Confiança alta com causa ausente: {sobreconf}")
