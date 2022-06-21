import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['savefig.dpi'] = 300


def _clear_legend(leg):
  leg.get_frame().set_edgecolor('b')
  leg.get_frame().set_linewidth(0.0)
  leg.get_frame().set_facecolor('none')


x = np.linspace(-2 * np.pi, 2 * np.pi, 25)
y = np.sin(x)
cosy = np.cos(x)

fig, axd = plt.subplot_mosaic([["A", "B"]], figsize=(10, 2.5))
ax = axd["A"]
ax.set_xlabel('x label')
ax.set_ylabel('y label')
ax.set_title("Simple Plot")
ax.plot(x, y, 'o', markersize=3, label="sin(x)",
        color='black', linewidth=1, linestyle='--')
ax.plot(x, cosy, 'v', markersize=3, label="cos(x)",
        color='black', linewidth=1, linestyle='--')
ax.text(2.2, -1.5, r'$\mu=115,\ \sigma=15$')
ax.annotate('local max', xy=(2, 1), xytext=(3, 1.5),
            arrowprops=dict(facecolor='black', width=0.5, headwidth=4, shrink=0.05, headlength=4))
ax.set_ylim(-2, 2)
leg = ax.legend()
_clear_legend(leg)

ax = axd["B"]
ax.set_xlabel('x label')
ax.set_ylabel('y label')
ax.set_title("Simple Plot")

# / , \\ , | , - , + , x, o, O, ., *
ax.xaxis.set_tick_params(length=0)
ax.set_xlim(-2, 10)
ax.bar([1, 2, 3], [1, 2, 3], width=1, fill=False,
       hatch=['ooo', 'x', '...'])
ax.bar([5, 6, 7], [1, 2, 3], width=1, fill=False,
       hatch=['ooo', 'x', '...'])
ax.set_xticks([2, 6])
ax.set_xticklabels(['Write', 'Read'])
leg = ax.legend(handles=[
        mpatches.Patch(label='sqlite', hatch='ooo', fill=False), 
        mpatches.Patch(label='dqlite-raft', hatch='xx', fill=False),
        mpatches.Patch(label='dqlite-dpaxos', hatch='...', fill=False),
], loc=2)
_clear_legend(leg)

plt.savefig("plot.png", bbox_inches='tight')
