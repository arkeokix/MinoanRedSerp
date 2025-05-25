import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
file_path = r"./Suppl data/Tabular data/suppl data pMS.xlsx"
df = pd.read_excel(file_path)

# Filter only heated and unheated samples with necessary columns
df_heating_sample = df[df["vase_type"].isin(["Heated sample", "Unheated sample"])][["Sample ID", "vase_type", "SI"]]

# Define color palette for both categories
palette = {
    "Unheated sample": "#3273FF",
    "Heated sample": "#FF3B26"
}

# Ensure 'Unheated' appears before 'Heated' in both plot and legend
df_heating_sample['vase_type'] = pd.Categorical(
    df_heating_sample['vase_type'],
    categories=["Unheated sample", "Heated sample"],
    ordered=True
)

# Make 'Sample ID' a categorical variable to maintain order in the plot
df_heating_sample['Sample ID'] = pd.Categorical(df_heating_sample['Sample ID'], ordered=True)

# Create the plot with square aspect ratio
plt.figure(figsize=(10, 10))
ax = sns.boxplot(
    data=df_heating_sample,
    x='Sample ID',
    y="SI",
    hue="vase_type",
    palette=palette,
    legend=False,
    flierprops=dict(marker='d', markerfacecolor='grey', alpha=0.5)
)

# Define reference min-max ranges for blue and red vases
blue_min = 0.0227175
blue_max = 0.0587109
red_min = 0.0043969
red_max = 0.017212

# Add shaded reference ranges (min-max bands)
ax.axhspan(blue_min, blue_max, color='#3273FF', alpha=0.2, label='Blue vases min-max')
ax.axhspan(red_min, red_max, color='#FF3B26', alpha=0.2, label='Red vases min-max')

# Create custom legend markers for unheated and heated samples
order = ["Unheated sample", "Heated sample"]
handles = [
    plt.Line2D([0], [0], marker='s', color='w', markersize=12, markerfacecolor=palette[vase])
    for vase in order
]
labels = [f"{vase}" for vase in order]

# Add quartile patch handles to the legend
quartile_handles, quartile_labels = ax.get_legend_handles_labels()
all_handles = handles + quartile_handles
all_labels = labels + quartile_labels

# Display combined legend
plt.legend(
    all_handles,
    all_labels,
    title=None,
    fontsize=13,
    loc='upper right'
)

# Draw vertical dashed lines between sample pairs
xticks = ax.get_xticks()
for i in range(len(xticks) - 1):
    mid_point = (xticks[i] + xticks[i + 1]) / 2
    ax.axvline(x=mid_point, color='gray', linestyle='dotted', linewidth=0.7, alpha=0.7)

# Customize labels and title
plt.xlabel("Experimental Sample", fontsize=18)
plt.ylabel("Magnetic Susceptibility (SI)", fontsize=18)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)

# Final layout adjustment and display
plt.tight_layout()
plt.show()
