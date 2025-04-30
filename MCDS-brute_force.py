# Correcting the constant unpacking error

import random
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from itertools import combinations

# ───── Parameters ─────
NUM_NODES     = 20
K_DISK_RADIUS = 30
GRID_SIZE     = 100

WHITE, GRAY, BLACK = 'WHITE', 'GRAY', 'BLACK'

# ───── Generate connected geometric graph ─────
def generate_connected_graph(n, r, size):
    while True:
        pos = {i: (random.uniform(0, size), random.uniform(0, size)) for i in range(n)}
        G = nx.random_geometric_graph(n, r, pos=pos)
        if nx.is_connected(G):
            return G, pos

# ───── Check if a subset is a dominating set ─────
def is_dominating(G, subset):
    dominated = set(subset)
    for node in subset:
        dominated.update(G.neighbors(node))
    return len(dominated) == len(G)

# ───── Check if subset induces a connected subgraph ─────
def is_connected_subset(G, subset):
    subG = G.subgraph(subset)
    return nx.is_connected(subG)

# ───── Find Minimum Connected Dominating Set ─────
def brute_force_mcds(G):
    nodes = list(G.nodes())
    for k in range(1, len(nodes) + 1):
        for subset in combinations(nodes, k):
            if is_dominating(G, subset) and is_connected_subset(G, subset):
                return set(subset)  # smallest valid CDS

# ───── Visualizer Class ─────
class BruteForceCDSVisualizer:
    def __init__(self):
        self.G, self.pos = generate_connected_graph(NUM_NODES, K_DISK_RADIUS, GRID_SIZE)
        self.cds = brute_force_mcds(self.G)
        self.fig, self.ax = plt.subplots()
        plt.subplots_adjust(bottom=0.2)
        btn_ax = self.fig.add_axes([0.85, 0.05, 0.1, 0.075])
        self.button = Button(btn_ax, 'Show CDS')
        self.button.on_clicked(self.draw)
        self._draw_initial()
        plt.show()

    def _draw_initial(self):
        self.ax.clear()
        nx.draw(self.G, self.pos, with_labels=True, node_color='lightgray',
                edge_color='lightblue', node_size=500, ax=self.ax)
        self.ax.set_title("Initial k-Disk Graph")
        self.fig.canvas.draw_idle()

    def draw(self, event=None):
        self.ax.clear()
        node_colors = []
        for v in self.G.nodes():
            if v in self.cds:
                node_colors.append('orange')
            else:
                node_colors.append('gray')
        nx.draw(self.G, self.pos, with_labels=True, node_color=node_colors,
                edge_color='lightblue', node_size=500, ax=self.ax)
        self.ax.set_title(f"Brute-Force MCDS: {sorted(self.cds)}")
        self.fig.canvas.draw_idle()

# ───── Run ─────
visualizer = BruteForceCDSVisualizer()
