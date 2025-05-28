import os
import numpy as np
import matplotlib.pyplot as plt

# paht
data_folder = r"./Suppl data/Spectra/µ-RS spectra"

# function to read txt file
def read_raman_file(file_path):
    data = []
    with open(file_path, "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 2:
                try:
                    wavenumber, intensity = float(parts[0]), float(parts[1])
                    data.append((wavenumber, intensity))
                except ValueError:
                    continue
    return np.array(data)

# palettes
unheated_colors = {
    "Serpentine": "#009E73",
    "Olivine": "#56B4E9",
    "Magnetite": "#FFC400",
}
heated_colors = {
    "Primary olivine": "#56B4E9",
    "Secondary olivine": "#0072B2",
    "Hematite": "#D55E00",
}

# common parameters for graphs
def plot_group(ax, groups, colors, legend_order, prefix_to_remove, offset_adjustment=0, label_indices=None):
    group_offset = 0
    group_spacing = 2
    internal_spacing = 0.2
    label_counter = 0
    label_total = len(label_indices) if label_indices else 0

    for group_name, filenames in groups.items():
        color = colors[group_name]

        normal_spectra = [f for f in filenames if f not in ["olivine", "antigorite", "magnetite", "diopside", "hematite"]]
        reference_spectrum = next((f for f in filenames if f in ["olivine", "antigorite", "magnetite", "diopside", "hematite"]), None)

        if reference_spectrum:
            file_path = os.path.join(data_folder, reference_spectrum + ".txt")
            if os.path.exists(file_path):
                data = read_raman_file(file_path)
                if data.size > 0:
                    data[:, 1] /= np.max(data[:, 1])
                    data[:, 1] += group_offset - internal_spacing + offset_adjustment
                    ax.plot(data[:, 0], data[:, 1], linestyle="--", color=color)

        for i, filename in enumerate(normal_spectra):
            file_path = os.path.join(data_folder, filename + ".txt")
            if os.path.exists(file_path):
                data = read_raman_file(file_path)
                if data.size > 0:
                    data[:, 1] /= np.max(data[:, 1])
                    offset = group_offset + (i * internal_spacing) + offset_adjustment
                    data[:, 1] += offset
                    ax.plot(data[:, 0], data[:, 1], linestyle="-", color=color)
                    index = label_indices[label_counter] if label_indices else label_counter + 1
                    label = f"{label_total - index + 1:02}"
                    ax.text(data[-1, 0] + 10, offset + 0.05, label, fontsize=10, color=color)
                    label_counter += 1

        ax.plot([], [], linestyle="-", color=color, label=group_name)
        group_offset += group_spacing

    ax.plot([], [], linestyle="--", color="gray", label="Reference spectrum")

    handles, labels = ax.get_legend_handles_labels()
    order = [labels.index(group) for group in legend_order if group in labels]
    ax.legend([handles[idx] for idx in order], [labels[idx] for idx in order],
              loc="upper right", fontsize=14, frameon=True)

    ax.set_xlabel("Wavenumber (cm⁻¹)", fontsize=16)
    ax.set_ylabel("Normalised Raman intensity (arb. unit)", fontsize=16)
    ax.grid(True, which="both", linestyle="--", linewidth=0.5)
    ax.set_xlim(200, 1200)

# display options
unheated_groups = {
    "Serpentine": ["MS43B_05", "MS43B_06", "antigorite"],
    "Olivine": ["MS43B_03", "MS43B_04", "olivine"],
    "Magnetite": ["MS43B_01", "MS43B_02", "magnetite"],
}

heated_groups = {
    "Secondary olivine": ["MS43Bred_05", "MS43Bred_06"],
    "Primary olivine": ["MS43Bred_03", "MS43Bred_04", "olivine"],
    "Hematite": ["MS43Bred_01", "MS43Bred_02", "hematite"],
}

# legend
unheated_order = ["Magnetite", "Olivine", "Serpentine", "Reference spectrum"]
heated_order = ["Hematite", "Primary olivine", "Secondary olivine", "Reference spectrum"]

# plotting
fig, axes = plt.subplots(1, 2, figsize=(18, 8), sharey=True)

plot_group(axes[0], unheated_groups, unheated_colors, unheated_order, prefix_to_remove="MS43B_", label_indices=[1, 2, 3, 4, 5, 6])
axes[0].set_title("Unheated sample", fontsize=18)

plot_group(axes[1], heated_groups, heated_colors, heated_order, prefix_to_remove="MS43Bred_", offset_adjustment=-0.25, label_indices=[1, 2, 3, 4, 5, 6])
axes[1].set_title("Heated sample", fontsize=18)

# Final layout adjustment and display
plt.tight_layout()
plt.show()
