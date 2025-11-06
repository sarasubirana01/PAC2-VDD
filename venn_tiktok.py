# venn_tiktok.py
from matplotlib import pyplot as plt
from matplotlib_venn import venn3


venn = venn3(
    subsets = (
        300,  # TikTok Shop
        240,  # Shein
        140,  # TikTok & Shein
        200,  # Temu
        120,  # TikTok & Temu
        90,   # Shein & Temu
        60    # TikTok & Shein & Temu
    ),
    set_labels = ('TikTok Shop', 'Shein', 'Temu')
)


# Colores personalizados
venn.get_patch_by_id('100').set_color('#ff0050')  # TikTok (rosa fucsia)
venn.get_patch_by_id('010').set_color('#00aaff')  # Shein (azul)
venn.get_patch_by_id('001').set_color('#ff6600')  # Temu (naranja)
plt.title('Overlap of TikTok Shop, Shein, and Temu Users (Simulated)', fontsize=14)

# Guardar el resultado
plt.savefig("venn_tiktokshop.png", dpi=300, bbox_inches='tight')
plt.show()
