import numpy as np
import pyarrow.parquet as pq
import matplotlib.pyplot as plt
from muon_sim.mcmc import EPS

plt.rc('font', size=10) #controls default text size
plt.rc('axes', titlesize=20) #fontsize of the title
plt.rc('axes', labelsize=20) #fontsize of the x and y labels
plt.rc('xtick', labelsize=15) #fontsize of the x tick labels
plt.rc('ytick', labelsize=15) #fontsize of the y tick labels
plt.rc('legend', fontsize=15) #fontsize of the legend

tab = pq.read_table("test.pq")
print(tab.to_pandas().head(10).to_latex(index=False, float_format="{:0.2f}".format, bold_rows=False, columns=["x0", "y0", "z0", "theta", "phi", "E"]))
x = np.linspace(np.pi - np.pi / 2 + 1e-5, np.pi, 100)
y = np.power(np.cos(x + np.pi), 1.9)
# y = np.cos(x + np.pi)

#plt.plot(x, y)
plt.hist(tab["phi"], bins=100, density=True, label=r"$cos(x + \pi)^{1.9}$")
plt.title(f"Echantillons angle verticaux muons ({len(tab['phi'])} valeurs)")
plt.xlabel("x")
plt.ylabel(r"$\phi$")
plt.legend()
plt.show()

