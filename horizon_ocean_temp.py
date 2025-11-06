# horizon_ocean_temp.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1) CÀRREGA DE DADES
df = pd.read_csv("ocean_temp_daily.csv", sep=None, engine="python")

# Neteja de noms de columnes
df.columns = df.columns.str.strip()

# Parseig de la data
df["date"] = pd.to_datetime("2000-" + df["date"].astype(str).str.strip().str.replace("/", "-", regex=False),
                            format="%Y-%d-%m", errors="coerce")
df = df.sort_values("date").reset_index(drop=True)

# Converteix totes les columnes numèriques
for col in df.columns:
    if col != "date":
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Columnes d'anys disponibles
ordre_anys = ["2022", "2023", "2024", "2025"]
years = [y for y in ordre_anys if y in df.columns]

# Baseline
baseline = df["baseline"].to_numpy()

# 2) FUNCIÓ HORIZON
def plot_horizon(ax, series, baseline, n_bands=4, cmap_pos="#d73027", cmap_neg="#4575b4"):
    """
    Dibuixa un horizon chart per a 'series' respecte a 'baseline'.
    n_bands controla quantes bandes d'intensitat s'apilen.
    """
    anomalies = series - baseline

    # Escala robusta per a valors extrems (percentil 95)
    max_abs = np.nanpercentile(np.abs(anomalies), 95)
    if not np.isfinite(max_abs) or max_abs == 0:
        max_abs = 1.0
    band = max_abs / n_bands
    x = np.arange(len(series))

    # Positives (rogues) i negatives (blaves), apilades
    for i in range(n_bands, 0, -1):
        lower, upper = (i - 1) * band, i * band

        # positives
        band_vals = np.clip(anomalies, lower, upper) - lower
        band_vals[anomalies < lower] = 0
        ax.fill_between(x, 0, band_vals, color=cmap_pos, alpha=0.25 + 0.15 * (i - 1), linewidth=0)

        # negatives
        band_vals_neg = -np.clip(-anomalies, lower, upper) + lower
        band_vals_neg[anomalies > -lower] = 0
        ax.fill_between(x, 0, band_vals_neg, color=cmap_neg, alpha=0.25 + 0.15 * (i - 1), linewidth=0)

    ax.set_xlim(0, len(series) - 1)
    ax.axhline(0, color="#888", linewidth=0.6)
    ax.set_yticks([])
    ax.set_xticks([])

# 3) DIBUIX
rows = len(years)
fig, axes = plt.subplots(rows, 1, figsize=(12, 6), sharex=True)
if rows == 1:
    axes = [axes]

for ax, y in zip(axes, years):
    plot_horizon(ax, df[y].to_numpy(), baseline, n_bands=4)
    ax.set_ylabel(y, rotation=0, ha="right", va="center", fontsize=10, labelpad=15)

# Eix X amb mesos (posició al dia 1 de cada mes)
xticks, xlabels = [], []
for m in range(1, 13):
    idx = df.index[df["date"].dt.month.eq(m) & df["date"].dt.day.eq(1)]
    if len(idx):
        xticks.append(idx[0])
        xlabels.append(pd.Timestamp(2000, m, 1).strftime("%b"))
axes[-1].set_xticks(xticks)
axes[-1].set_xticklabels(xlabels)

fig.suptitle("Daily Global Average Sea Surface Temperature — anomalies vs. 1982–2010 baseline",
             fontsize=13, fontweight="bold")
fig.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig("horizon_ocean_temp.png", dpi=300, bbox_inches="tight")
plt.show()
