import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
file_path_archeo = r"./Suppl data/Tabular data/suppl data pMS.xlsx"
df_archeo = pd.read_excel(file_path_archeo)

# Filter and process archaeological data
df_filtered = df_archeo[df_archeo["vase_type"].isin(["Blue vases", "Red vases"])][["Sample ID", "vase_type", "SI"]]
df_median = df_filtered.groupby(["vase_type", "Sample ID"], as_index=False)["SI"].median()
df_filtered = df_median.copy()
df_filtered['vase_type'] = pd.Categorical(
    df_filtered['vase_type'],
    categories=["Blue vases", "Red vases"],
    ordered=True
)
palette = {
    "Blue vases": "#3273FF",
    "Red vases": "#FF3B26"
}

# Set up figure and axis
fig, ax1 = plt.subplots(figsize=(6, 6))

# Boxplot
sns.boxplot(data=df_filtered, y="SI", hue="vase_type", palette=palette, legend=False, ax=ax1)

# Custom legend
num_analyses = df_filtered.groupby('vase_type')['SI'].count()
handles = [plt.Line2D([0], [0], marker='s', color='w', markersize=10, markerfacecolor=palette[v]) for v in num_analyses.index]
labels = [f"{v.capitalize()} (n = {num})" for v, num in num_analyses.items()]
ax1.legend(handles, labels, title_fontsize=14, fontsize=12, loc='upper right')

# Axis labels and ticks
ax1.set_ylabel(r'Magnetic susc. (SI ×10$^3$)', fontsize=14)
ax1.tick_params(axis='both', labelsize=12)
# Layout
plt.tight_layout()
plt.show()
