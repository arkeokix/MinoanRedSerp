import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from skimage import color
from adjustText import adjust_text
from matplotlib.lines import Line2D

# Download data
file_path_archeo = r"./Suppl data/Tabular data/suppl data Munsell.xlsx"
df = pd.read_excel(file_path_archeo)

# Conversion HEX -> HSV
def hex_to_hsv(hex_color):
    hex_color = hex_color.lstrip("#")
    rgb = np.array([int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4)])
    hsv = color.rgb2hsv(rgb.reshape(1, 1, 3))[0, 0]
    return hsv

df["HSV"] = df["Hex"].apply(hex_to_hsv)
df["Hue"] = df["HSV"].apply(lambda x: x[0] * 360)
df["Saturation"] = df["HSV"].apply(lambda x: x[1])
df["Value"] = df["HSV"].apply(lambda x: x[2])

# Point styles and colors
marker_dict = {
    "Unheated sample": "X",
    "Heated sample": "X",
    "Blue vase": "D",
    "Red vase": "D"
}
color_dict = {
    "Unheated sample": "#264de4",   # Darker blue
    "Heated sample": "#e01b1b",     # Darker red
    "Blue vase": "#76a7ff",         # Light blue
    "Red vase": "#ff7b61"           # Light red
}

# Figure division
fig, axes = plt.subplots(1, 2, figsize=(20, 10))

texts_hue_sat = []
texts_hue_val = []

# Hue vs Saturation
for sample_type, marker in marker_dict.items():
    subset = df[df["Type"] == sample_type]
    sns.scatterplot(
        data=subset, x="Hue", y="Saturation",
        marker=marker, s=200, edgecolor="black", ax=axes[0],
        color=color_dict[sample_type]
    )
    for i in range(len(subset)):
        text = axes[0].text(subset["Hue"].iloc[i], subset["Saturation"].iloc[i],
                            subset["Sample ID"].iloc[i], fontsize=12, ha='right')
        texts_hue_sat.append(text)

axes[0].set_title("Hue vs Saturation", fontsize=25)
axes[0].set_xlabel("Hue [0-360°]", fontsize=22)
axes[0].set_ylabel("Saturation [0-1]", fontsize=22)
axes[0].tick_params(axis='both', labelsize=20)
axes[0].grid(linewidth=0.7)

# Hue vs Value
for sample_type, marker in marker_dict.items():
    subset = df[df["Type"] == sample_type]
    sns.scatterplot(
        data=subset, x="Hue", y="Value",
        marker=marker, s=200, edgecolor="black", ax=axes[1],
        color=color_dict[sample_type]
    )
    for i in range(len(subset)):
        text = axes[1].text(subset["Hue"].iloc[i], subset["Value"].iloc[i],
                            subset["Sample ID"].iloc[i], fontsize=12, ha='right')
        texts_hue_val.append(text)

axes[1].set_title("Hue vs Luminosity", fontsize=25)
axes[1].set_xlabel("Hue [0-360°]", fontsize=22)
axes[1].set_ylabel("Brightness [0-1]", fontsize=22)
axes[1].tick_params(axis='both', labelsize=20)
axes[1].grid(linewidth=0.7)

# Text
adjust_text(texts_hue_sat, ax=axes[0], expand=(1.2, 1.2), arrowprops=dict(arrowstyle="-", lw=0.8))
adjust_text(texts_hue_val, ax=axes[1], expand=(1.2, 1.2), arrowprops=dict(arrowstyle="-", lw=0.8))

# Legend
legend_elements = [
    Line2D([0], [0], marker='X', color='w', markerfacecolor='#264de4', markeredgecolor='black',
           markersize=14, label="Unheated sample"),
    Line2D([0], [0], marker='X', color='w', markerfacecolor='#e01b1b', markeredgecolor='black',
           markersize=14, label="Heated sample"),
    Line2D([0], [0], marker='D', color='w', markerfacecolor='#76a7ff', markeredgecolor='black',
           markersize=14, label="Blue vase"),
    Line2D([0], [0], marker='D', color='w', markerfacecolor='#ff7b61', markeredgecolor='black',
           markersize=14, label="Red vase")
]
axes[1].legend(handles=legend_elements, loc="upper right", fontsize=18, title="", frameon=True)

plt.tight_layout()
plt.subplots_adjust(wspace=0.15)
plt.show()
