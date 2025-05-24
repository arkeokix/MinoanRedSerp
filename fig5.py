import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from matplotlib.colors import ListedColormap

# Load data from file (replace with your actual path)
file_path_data_crete = r"suppl data pXRF.xlsx"
df_crete = pd.read_excel(file_path_data_crete)
df_crete = df_crete[(df_crete['Sum_of_oxydes_before_normalization'] >= 80) &
                    (df_crete['Sum_of_oxydes_before_normalization'] <= 120)]

# Apply calibration corrections
def accuracy_calib(df):
    df_corrected = df.copy()
    df_corrected['SiO2'] *= 0.87
    df_corrected['CaO'] *= 0.90
    df_corrected['Al2O3'] *= 0.87
    df_corrected['MgO'] *= 0.92
    df_corrected['Ni'] *= 0.89
    return df_corrected

df_crete = accuracy_calib(df_crete)
df_heating = df_crete[df_crete['Type'] == "Experimental heating"]
df_archeo = df_crete[df_crete['Type'] != "Experimental heating"].copy()

# Join facies data
path_facies = r"C:\Users\kregnier\OneDrive - UCL\Articles_perso\red serp\facies.xlsx"
df_facies = pd.read_excel(path_facies)
df_archeo = df_archeo.merge(df_facies[['Sample ID', 'Facies']], on='Sample ID', how='left')
unmatched_samples = df_archeo[df_archeo['Facies'].isna()]['Sample ID'].unique()
if len(unmatched_samples) != 0:
    print("WARNING !!! Sample IDs not matched with facies:", unmatched_samples)

df_archeo.to_excel("archeo_with_facies.xlsx")

# Load worldwide serpentinite data
file_path_data_compil_serp = r"C:\Users\kregnier\OneDrive - UCL\GEODATA\serp_world_data.xlsx"
df_world_serp = pd.read_excel(file_path_data_compil_serp)
df_world_serp['ratio_normalised'] = 100 / df_world_serp['Total']
columns_to_multiply = ['SiO2', 'TiO2', 'Al2O3', 'Cr2O3', 'Fe2O3T', 'MnO', 'NiO', 'MgO', 'CaO', 'Na2O', 'K2O', 'P2O5']
for col in columns_to_multiply:
    if pd.api.types.is_numeric_dtype(df_world_serp[col]):
        df_world_serp[col] *= df_world_serp['ratio_normalised']
    else:
        df_world_serp[col] = pd.to_numeric(df_world_serp[col], errors='coerce')

df_world_serp['MgOSiO2'] = df_world_serp['MgO'] / df_world_serp["SiO2"]
required_columns = ["MgOSiO2", "SiO2", "CaO", "TiO2", "Ni", "MgO"]
df_world_serp[required_columns] = df_world_serp[required_columns].apply(pd.to_numeric, errors='coerce')

# Filter for facies 1 and 6
df_facies = df_archeo[df_archeo['Facies'].isin([1, 6])]
df_facies_1 = df_archeo[df_archeo['Facies'] == 1]
df_facies_6 = df_archeo[df_archeo['Facies'] == 6]

# Plotting
axes_pairs = [("SiO2", "MgO"), ("CaO", "MgO"), ("TiO2", "MgO"), ("Ni", "MgO")]
fig, axes = plt.subplots(2, 2, figsize=(10, 10))  # Square graphs
n = 0
n_list = ['a', 'b', 'c', 'd']

for ax, (axe_y, axe_x) in zip(axes.flat, axes_pairs):
    cmap = ListedColormap(sns.color_palette("Greys", n_colors=256)[100:])
    if axe_y == "TiO2" or axe_x in ["Cr", "Zn"]:
        df_world_serp_filtered = df_world_serp.dropna(subset=[axe_x if axe_x in df_world_serp else axe_y])
        sns.scatterplot(data=df_world_serp_filtered, x=axe_x, y=axe_y, color="grey",
                        marker='o', legend=False, alpha=0.1, ax=ax)
    else:
        sns.scatterplot(data=df_world_serp, x=axe_x, y=axe_y, color="grey",
                        marker='o', legend=False, alpha=0.1, ax=ax)

    df_medians = df_facies.groupby(['Sample ID', 'Facies'])[[axe_x, axe_y]].median().reset_index()

    sns.scatterplot(data=df_facies, x=axe_x, y=axe_y, hue='Facies', palette={1: 'blue', 6: 'red'},
                    edgecolor='black', marker='o', facecolor='none', legend=False, alpha=0.1, ax=ax)
    sns.scatterplot(data=df_medians, x=axe_x, y=axe_y, hue='Facies', palette={1: 'blue', 6: 'red'},
                    edgecolor='black', marker='o', facecolor='none', legend=False, ax=ax)

    df_heating_medians = df_heating.groupby(['Sample ID'])[[axe_x, axe_y]].median().reset_index()
    df_heating_min = df_heating.groupby(['Sample ID'])[[axe_x, axe_y]].min().reset_index()
    df_heating_max = df_heating.groupby(['Sample ID'])[[axe_x, axe_y]].max().reset_index()
    sns.scatterplot(data=df_heating_medians, x=axe_x, y=axe_y, color="gold",
                    edgecolor='black', marker='s', legend=False, ax=ax)

    for i, row in df_heating_medians.iterrows():
        min_value = df_heating_min.loc[i, [axe_x, axe_y]].values
        max_value = df_heating_max.loc[i, [axe_x, axe_y]].values
        ax.errorbar(x=row[axe_x], y=row[axe_y],
                    xerr=[[row[axe_x] - min_value[0]], [max_value[0] - row[axe_x]]],
                    yerr=[[row[axe_y] - min_value[1]], [max_value[1] - row[axe_y]]],
                    fmt='o', color='black', capsize=5, elinewidth=0.5, alpha=0.5)

    # Axis labels and customizations
    ax.set_xlabel(f"{axe_x} wt. % (anhydrous)", fontsize=14)
    if axe_y == "Ni":
        ax.set_ylabel(f"{axe_y} ppm", fontsize=14)
    else:
        ax.set_ylabel(f"{axe_y} wt. % (anhydrous)", fontsize=14)

    if axe_y == "SiO2":
        ax.set_ylim(30, 50)
    if axe_y == "CaO":
        ax.set_yscale('log')
        ax.set_yticks([0.01, 0.1, 1, 10])
        ax.set_yticklabels(['0.01', '0.1', '1', '10'])
    if axe_y == "TiO2":
        ax.set_yscale('log')
        ax.set_yticks([0.01, 0.1, 1])
        ax.set_yticklabels(['0.01', '0.1', '1'])
    if axe_x == "MgO":
        ax.set_xlim(left=20, right=55)

    ax.text(-0.12, 1.05, n_list[n] + '.', transform=ax.transAxes, fontsize=16, fontweight='bold',
            va='top', ha='right')
    n += 1

# Add legend only on the last subplot
legend_elements = [
    plt.Line2D([0], [0], marker='o', color='blue', linestyle='', alpha=0.3, label="All blue vase data"),
    plt.Line2D([0], [0], marker='o', color='red', linestyle='', alpha=0.3, label="All red vase data"),
    plt.Line2D([0], [0], marker='o', color='blue', linestyle='', markeredgecolor="black", label="Median per blue vase"),
    plt.Line2D([0], [0], marker='o', color='red', linestyle='', markeredgecolor="black", label="Median per red vase"),
    plt.Line2D([0], [0], marker='o', color='grey', linestyle='', alpha=0.2, label="Worldwide serpentinite data"),
    plt.Line2D([0], [0], marker='s', color='#7F6B00', markersize=10, markeredgecolor="black",
               linewidth=2, linestyle='', alpha=0.5, label="Experimental heating samples")
]
axes[1, 1].legend(handles=legend_elements, loc='upper right', fontsize=12)

plt.subplots_adjust(wspace=0.5)
# Final layout adjustment and display
plt.tight_layout()
plt.show()
