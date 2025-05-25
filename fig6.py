import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from scipy.stats import pearsonr
import statsmodels.api as sm
from matplotlib.ticker import FuncFormatter

# Load data for the first graph
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

# Load data for the second graph
file_path_serp = r"./Suppl data/Tabular data/suppl data pMS world compil.xlsx"
df_serp_compil = pd.read_excel(file_path_serp)
x = df_serp_compil['m (%)']
y = df_serp_compil['K SI']
x_np = x.values
y_np = y.values

# Set up figure and axes
fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(12, 6), gridspec_kw={'width_ratios': [1.5, 2]})

# First plot: boxplot
sns.boxplot(data=df_filtered, y="SI", hue="vase_type", palette=palette, legend=False, ax=ax1)

# Custom legend
num_analyses = df_filtered.groupby('vase_type')['SI'].count()
handles = [plt.Line2D([0], [0], marker='s', color='w', markersize=10, markerfacecolor=palette[v]) for v in num_analyses.index]
labels = [f"{v.capitalize()} (n = {num})" for v, num in num_analyses.items()]
ax1.legend(handles, labels, title_fontsize=14, fontsize=12, loc='upper right')

# Axis labels and ticks
ax1.set_ylabel('Magnetic susc. (SI)', fontsize=14)
ax1.tick_params(axis='both', labelsize=12)

# Second Y-axis on ax1
def SI_to_m(SI):
    return 0.18350183134625886 + (47.621322186139174 * SI)

def m_to_SI(m):
    return -7.420217690514569e-05 + 0.018771549627447405 * m

ax1_sec = ax1.twinx()
all_v_ticks = np.arange(1, 17)
all_si_ticks = [m_to_SI(v) for v in all_v_ticks]
visible_labels = {1, 5, 10, 15}
ax1_sec.set_yticks(all_si_ticks)
ax1_sec.set_yticklabels([f"{v}%" if v in visible_labels else "" for v in all_v_ticks], fontsize=12)
ax1_sec.set_ylim(ax1.get_ylim())
ax1_sec.set_ylabel('Magnetite Volume Fraction', fontsize=14)
ax1_sec.tick_params(axis='both', labelsize=12)

# Second plot: scatter and regression
X = sm.add_constant(x_np)
model_sm = sm.OLS(y_np, X)
results = model_sm.fit()

x_reshaped = x_np.reshape(-1, 1)
model = LinearRegression()
model.fit(x_reshaped, y_np)
corr_coef, _ = pearsonr(x_np, y_np)

x_grid = np.linspace(min(x_np), max(x_np), 100)
X_grid = sm.add_constant(x_grid)
y_grid_pred = results.predict(X_grid)

results_robust = model_sm.fit(cov_type='HC3')
y_grid_pred_robust = results_robust.predict(X_grid)
y_grid_pred_ci_robust = results_robust.get_prediction(X_grid).conf_int(alpha=0.32)

ax2.scatter(x_np, y_np, color='grey', alpha=0.5, label=f'Worldwide serpentinite (n = {len(x_np)})')
ax2.plot(x_grid, y_grid_pred, color='grey', linestyle="--", label=f'r²={results.rsquared:.2f}')
ax2.fill_between(x_grid, y_grid_pred_ci_robust[:, 0], y_grid_pred_ci_robust[:, 1],
                 color='grey', alpha=0.2, label='1σ confidence interval (68%)')

# Axis labels and ticks
ax2.set_xlabel('Magnetite Volume Fraction', fontsize=14)
ax2.set_ylabel('Magnetic susc. (SI)', fontsize=14)
ax2.tick_params(axis='both', labelsize=12)

formatter = FuncFormatter(lambda x, _: f'{x:.2f}')
ax2.yaxis.set_major_formatter(formatter)
ax2.set_xticks(np.arange(0, 8))
ax2.set_xticklabels([f'{v}%' for v in np.arange(0, 8)], fontsize=12)

ax2.legend(fontsize=12)

# Harmonize Y-axis range
y_min_ax1 = df_archeo['SI'].min()
y_max_ax1 = df_archeo['SI'].max()
y_min_ax2 = min(y_np)
y_max_ax2 = max(y_np)
global_y_min = min(y_min_ax1, y_min_ax2)
global_y_max = max(y_max_ax1, y_max_ax2)
margin = 0.05 * (global_y_max - global_y_min)
global_y_min -= margin
global_y_max += margin
ax1.set_ylim(global_y_min, global_y_max)
ax2.set_ylim(global_y_min, global_y_max)
ax1_sec.set_ylim(ax1.get_ylim())

# Subplot annotations
ax1.text(-0.1, 1.05, 'a.', transform=ax1.transAxes, fontsize=16, fontweight='bold', va='top', ha='right')
ax2.text(-0.1, 1.05, 'b.', transform=ax2.transAxes, fontsize=16, fontweight='bold', va='top', ha='right')

# Final layout adjustment and display
plt.subplots_adjust(wspace=0.4)
plt.tight_layout()
plt.show()
