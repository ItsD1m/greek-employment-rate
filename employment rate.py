import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from datetime import datetime

# ==============================================================================
# 1. ΤΑ ΔΕΔΟΜΕΝΑ (Καθαρισμένα και έτοιμα, χωρίς αρχεία)
# ==============================================================================
data = {
    "Ημερομηνία": [
        "1995-01", "1996-01", "1997-01", "1998-01", "1999-01", "2000-01",
        "2001-01", "2002-01", "2003-01", "2004-01", "2005-01", "2006-01",
        "2007-01", "2008-01", "2009-01", "2010-01", "2011-01", "2012-01",
        "2013-01", "2014-01", "2015-01", "2016-01", "2017-01", "2018-01",
        "2019-01", "2020-01", "2021-01", "2022-01", "2023-01", "2024-01",
        "2025-01"
    ],
    "Απασχόληση": [
        4152.5, 4132.1, 4120.7, 4298.7, 4308.0, 4324.3,
        4334.4, 4440.8, 4491.1, 4606.8, 4652.0, 4742.9,
        4806.7, 4867.1, 4835.9, 4706.4, 4505.1, 4325.8,
        4300.6, 4453.7, 4322.5, 4469.5, 4446.6, 4650.3,
        4751.9, 4629.7, 4865.5, 5037.3, 5135.8, 5183.4,
        5225.9
    ]
}

df = pd.DataFrame(data)
df["Ημερομηνία"] = pd.to_datetime(df["Ημερομηνία"])

# ==============================================================================
# 2. ΚΥΒΕΡΝΗΣΗ ΑΝΑ ΗΜΕΡΟΜΗΝΙΑ
# ==============================================================================
def get_party(date):
    if date < datetime(2004, 3, 7):
        return "ΠΑΣΟΚ"
    elif date < datetime(2009, 10, 4):
        return "Νέα Δημοκρατία"
    elif date < datetime(2012, 6, 20):  
        return "ΠΑΣΟΚ" 
    elif date < datetime(2015, 1, 25):  
        return "Νέα Δημοκρατία"
    elif date < datetime(2019, 7, 7):
        return "ΣΥΡΙΖΑ"
    else:
        return "Νέα Δημοκρατία"

df["Κυβέρνηση"] = df["Ημερομηνία"].apply(get_party)

colors = {
    "ΠΑΣΟΚ": "#00FF00",          
    "Νέα Δημοκρατία": "#00BFFF", 
    "ΣΥΡΙΖΑ": "#FF1493"          
}

# ==============================================================================
# 3. ΤΕΧΝΗΤΗ ΠΥΚΝΩΣΗ ΔΕΔΟΜΕΝΩΝ
# ==============================================================================
x_numeric = df["Ημερομηνία"].map(lambda x: x.toordinal()).values
y_numeric = df["Απασχόληση"].values

x_dense_numeric = np.linspace(x_numeric.min(), x_numeric.max(), 3000)
y_dense = np.interp(x_dense_numeric, x_numeric, y_numeric)
x_dense_dates = [datetime.fromordinal(int(d)) for d in x_dense_numeric]

# ==============================================================================
# 4. ΣΧΕΔΙΑΣΗ (UI)
# ==============================================================================
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(15, 7.5))

bg_color = '#121212'
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#333333')
ax.spines['bottom'].set_color('#333333')
ax.grid(True, color='#2A2A2A', linestyle='-', linewidth=0.8, alpha=0.7)

current_party = get_party(x_dense_dates[0])
current_x = [x_dense_dates[0]]
current_y = [y_dense[0]]

def plot_glow_segment(x, y, party_name):
    color = colors[party_name]
    ax.plot(x, y, color=color, linewidth=8, alpha=0.08, zorder=1)
    ax.plot(x, y, color=color, linewidth=4.5, alpha=0.18, zorder=2)
    ax.plot(x, y, color=color, linewidth=2.5, zorder=3)

for i in range(1, len(x_dense_numeric)):
    party = get_party(x_dense_dates[i])
    if party == current_party:
        current_x.append(x_dense_dates[i])
        current_y.append(y_dense[i])
    else:
        current_x.append(x_dense_dates[i])
        current_y.append(y_dense[i])
        plot_glow_segment(current_x, current_y, current_party)
        
        current_party = party
        current_x = [x_dense_dates[i]]
        current_y = [y_dense[i]]

plot_glow_segment(current_x, current_y, current_party)

for i in range(len(df)):
    date = df["Ημερομηνία"].iloc[i]
    val = df["Απασχόληση"].iloc[i]
    party = get_party(date)
    ax.scatter(date, val, color=bg_color, edgecolor=colors[party], linewidth=1.5, s=35, zorder=5)

plt.title("Greece Total Employment by Political Era (1995–2025)", 
          fontsize=16, color='white', fontweight='bold', pad=20, loc='left')

plt.xlabel("Έτος", color='#AAAAAA', fontsize=11, labelpad=10)
plt.ylabel("Σύνολο Απασχολουμένων (Εκατομμύρια Άτομα)", color='#AAAAAA', fontsize=11, labelpad=10)

ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f'{x/1000:,.2f}M'))
ax.tick_params(colors='#AAAAAA', length=0)

legend_elements = [
    plt.Line2D([0], [0], color=colors['ΠΑΣΟΚ'], lw=3, label='ΠΑΣΟΚ'),
    plt.Line2D([0], [0], color=colors['Νέα Δημοκρατία'], lw=3, label='Νέα Δημοκρατία'),
    plt.Line2D([0], [0], color=colors['ΣΥΡΙΖΑ'], lw=3, label='ΣΥΡΙΖΑ')
]
legend = ax.legend(handles=legend_elements, loc='best', frameon=True, 
                   facecolor='#1E1E1E', edgecolor='#333333', fontsize=11)
plt.setp(legend.get_texts(), color='#DDDDDD')

ax.text(0.98, 0.03, 'Created by: @ItsD1m', 
        transform=ax.transAxes, 
        color='#666666', fontsize=13, style='italic', weight='bold',
        ha='right', va='bottom', alpha=0.7, zorder=0)

plt.tight_layout()
plt.show()