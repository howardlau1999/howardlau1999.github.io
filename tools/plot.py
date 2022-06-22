import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams["legend.edgecolor"] = '1'
plt.rcParams["legend.fancybox"] = False
plt.rcParams["legend.framealpha"] = 0
plt.rcParams['savefig.dpi'] = 300
plt.rcParams["errorbar.capsize"] = 4


def _clear_legend(leg):
  leg.get_frame().set_edgecolor('b')
  leg.get_frame().set_linewidth(0.0)
  leg.get_frame().set_facecolor('none')


x = np.linspace(-2 * np.pi, 2 * np.pi, 25)
y = np.sin(x)
cosy = np.cos(x)

fig, axd = plt.subplot_mosaic([["A", "B"], ["C", "."]], figsize=(10, 5), constrained_layout=True)
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
ax.set_xlabel('Transaction Type')
ax.set_ylabel('Avg. Latency (ms)')
ax.set_title("")

# / , \\ , | , - , + , x, o, O, ., *
ax.xaxis.set_tick_params(length=0)
ax.set_xlim(0, 8)
ax.bar([1, 2, 3], [1.64, 2.64, 2.44], width=1, fill=False, yerr=[[0.24, 1.58, 1.26], [0.18, 0.84, 0.66]], error_kw=dict(elinewidth=1),
       hatch=['ooo', 'xxx', '...'])
ax.bar([5, 6, 7], [1.21, 2.35, 2.24], width=1, fill=False, yerr=[[0.12, 0.78, 0.68], [0.08, 0.54, 0.44]], error_kw=dict(elinewidth=1),
       hatch=['ooo', 'xxx', '...'], )
ax.set_xticks([2, 6])
ax.set_yticks(np.linspace(0, 3, 5))
ax.set_xticklabels(['read-write', 'read-only'])
leg = ax.legend(handles=[
    mpatches.Patch(label='sqlite', hatch='ooo', fill=False),
    mpatches.Patch(label='dqlite-raft', hatch='xxx', fill=False),
    mpatches.Patch(label='dqlite-dpaxos', hatch='...', fill=False),
], loc='upper center', bbox_to_anchor=(0., 1.02, 1., .102), ncol=3, mode='expand', borderaxespad=0)
_clear_legend(leg)

ax = axd["C"]
ax.set_xlabel('Transaction Type')
ax.set_ylabel('Avg. Latency (ms)')
ax.set_title("")

# / , \\ , | , - , + , x, o, O, ., *
ax.xaxis.set_tick_params(length=0)
ax.set_xlim(0, 8)
ax.bar([2, 3], [232.64, 143.44], width=1, fill=False, yerr=[[11.58, 10.26], [8.84, 7.66]], error_kw=dict(elinewidth=1),
       hatch=['xxx', '...'])
ax.bar([5, 6], [224.35, 12.24], width=1, fill=False, yerr=[[0.78, 0.68], [0.54, 0.44]], error_kw=dict(elinewidth=1),
       hatch=['xxx', '...'], )
ax.set_xticks([2.5, 5.5])
ax.set_yticks(np.linspace(0, 250, 5))
ax.set_xticklabels(['read-write', 'read-only'])
leg = ax.legend(handles=[
    mpatches.Patch(label='dqlite-raft', hatch='xxx', fill=False),
    mpatches.Patch(label='dqlite-dpaxos', hatch='...', fill=False),
], loc='upper center', bbox_to_anchor=(0., 1.02, 1., .102), ncol=2, mode='expand', borderaxespad=0)
_clear_legend(leg)

plt.savefig("plot.pdf", bbox_inches='tight')
