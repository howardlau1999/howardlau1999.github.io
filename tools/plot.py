import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['savefig.dpi'] = 300

x = np.linspace(-2 * np.pi, 2 * np.pi, 25)
y = np.sin(x)
cosy = np.cos(x)

# fig, axd = plt.subplot_mosaic
fig, ax = plt.subplots(figsize=(5, 2.7), layout='constrained')
ax.set_xlabel('x label')
ax.set_ylabel('y label')
ax.set_title("Simple Plot")
ax.plot(x, y, 'o', markersize=3, label="sin(x)", color='black', linewidth=1, linestyle='--')
ax.plot(x, cosy, 'v', markersize=3, label="cos(x)", 
        color='black', linewidth=1, linestyle='--')
ax.text(2.2, -1.5, r'$\mu=115,\ \sigma=15$')
ax.annotate('local max', xy=(2, 1), xytext=(3, 1.5),
            arrowprops=dict(facecolor='black', width=0.5, headwidth=4, shrink=0.05, headlength=4))
ax.set_ylim(-2, 2)
leg = ax.legend()
leg.get_frame().set_edgecolor('b')
leg.get_frame().set_linewidth(0.0)
leg.get_frame().set_facecolor('none')
plt.savefig("plot.png", bbox_inches='tight')
