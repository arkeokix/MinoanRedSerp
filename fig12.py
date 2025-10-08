import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from pathlib import Path


# path data XRD
data_folder = "./Suppl data/Spectra/XRD spectra"

# XRD peaks for minerals
peaks = {
    "Olivine": ([17.2, 22.8, 35.5, 52.2], "#56B4E9"),  # yellow
    "Serpentine": ([12.1, 19.4, 24.6], "#009E73"),  # Vert
    "Magnetite": ([37.3], "#FFC400"),  # Bleu clair
    "Hematite": ([33.2], "#D55E00")
}

files_no_red = []
files_red = []

for filename in os.listdir(data_folder):
    if filename.endswith(".txt"):
        full_path = os.path.join(data_folder, filename)
        if "red" in filename.lower():
            files_red.append(full_path)
        else:
            files_no_red.append(full_path)

# function to read XRD spectra
def read_xrd_file(file_path):
    data = []
    with open(file_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            try:
                parts = line.strip().split()
                if len(parts) == 2:
                    theta, intensity = float(parts[0]), float(parts[1])
                    data.append((theta, intensity))
            except ValueError:
                continue
    return np.array(data)


fig, axes = plt.subplots(2, 1, figsize=(14, 10), sharex=True)

colors = ['#0072B2', '#009E73', '#CC79A7', '#F0E442', '#56B4E9', '#D55E00']

# top graph (unheated)
for i, file in enumerate(files_no_red):
    data = read_xrd_file(file)
    if data.size > 0:
        # Normaliser l'intensité et ajouter un décalage
        normalized_intensity = data[:, 1] / np.max(data[:, 1]) * 1000
        axes[0].plot(data[:, 0], normalized_intensity + i * 1000, label=None, color=colors[i % len(colors)])

axes[0].set_title("Unheated samples",fontsize=20)
axes[0].set_ylabel("Lin (counts)",fontsize=18)

# bottom graph (heated)
for i, file in enumerate(files_red):
    data = read_xrd_file(file)
    if data.size > 0:
        # Normaliser l'intensité et ajouter un décalage
        normalized_intensity = data[:, 1] / np.max(data[:, 1]) * 1000
        axes[1].plot(data[:, 0], normalized_intensity + i * 1000, label=None, color=colors[i % len(colors)])


## display options ##
axes[1].set_title("Heated samples",fontsize=20)
axes[1].set_xlabel("2θ (°)",fontsize=18)
axes[1].set_ylabel("Lin (counts)",fontsize=18)

used_colors = set()
mineral_legend_elements = []

for ax in axes:
    for mineral, (positions, color) in peaks.items():
        for peak in positions:
            # Tracer les lignes en pointillés sans label
            ax.axvline(x=peak, color=color, linestyle="--", alpha=0.7)

        # Ajouter le minéral à la légende uniquement si sa couleur n'a pas déjà été utilisée
        if color not in used_colors:
            mineral_legend_elements.append(
                mlines.Line2D([], [], color=color, linestyle='--',
                              label=mineral)
            )
            used_colors.add(color)

# graduations
for ax in axes:
    ax.xaxis.set_major_locator(plt.MultipleLocator(5))
    ax.xaxis.set_minor_locator(plt.MultipleLocator(1))

sample_legend_elements = [
    plt.Line2D([0], [0], color='#0072B2', lw=2, label="MS01B"),
    plt.Line2D([0], [0], color='#009E73', lw=2, label="MS02B"),
    plt.Line2D([0], [0], color='#CC79A7', lw=2, label="MS43B")
]


for ax in axes:
    ax.set_xlim(left=5, right=55)

# first legend
mineral_legend = axes[0].legend(handles=mineral_legend_elements,
                            title="Mineral Peaks",
                            loc='upper left',
                            framealpha=0.9,
                                fontsize=18,
                                title_fontsize=20)  # Fond légèrement transparent

# second legend
sample_legend = axes[1].legend(handles=sample_legend_elements,
                           title="Samples",
                           loc='upper left',
                           framealpha=0.9,
                               fontsize=18,
                               title_fontsize=20)  # Fond légèrement transparent

# add labels
axes[0].text(-0.02, 1.06, 'a.', transform=axes[0].transAxes,
             fontsize=16, fontweight='bold', va='top', ha='left')
axes[1].text(-0.02, 1.06, 'b.', transform=axes[1].transAxes,
             fontsize=16, fontweight='bold', va='top', ha='left')

# Final layout adjustment and display
plt.tight_layout()
plt.show()
