# slope_gdp.py
import matplotlib.pyplot as plt

# Dades de la gràfica
groups = ['G7', 'G20 (excl. G7)', 'Rest of world']
share_2023 = [29.48, 43.54, 26.80]
share_2029 = [27.01, 45.72, 26.95]

#Config. de la gràfica

fig, ax = plt.subplots(figsize=(8, 5))
ax.set_title("Change in Global GDP Share by Country Group (2023–2029)", fontsize=13, fontweight='bold')
ax.set_xlim(0, 3)
ax.set_xticks([0, 2])
ax.set_xticklabels(["2023", "2029"], fontsize=11)
ax.set_ylabel("Share of Global GDP (%)", fontsize=11)
ax.set_ylim(20, 50)

# Colors per grup

colors = {
    'G7': '#0072B2',              # Azul
    'G20 (excl. G7)': '#D55E00',  # Naranja rojizo
    'Rest of world': '#999999'    # Gris
}

# Dibuixem linees i etiquetes
for i, group in enumerate(groups):
    plt.plot([0, 2], [share_2023[i], share_2029[i]], color=colors[group], linewidth=2.5)
    plt.text(-0.05, share_2023[i], f"{group} {share_2023[i]}%", color=colors[group], ha='right', va='center', fontsize=10)
    plt.text(2.05, share_2029[i], f"{share_2029[i]}%", color=colors[group], ha='left', va='center', fontsize=10)

# Neteja estetica
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.tick_params(left=False, bottom=False)
ax.grid(axis='y', linestyle='--', alpha=0.3)

# Guardem resultat
plt.tight_layout()
plt.savefig("slope_gdp.png", dpi=300, bbox_inches='tight')
plt.show()
