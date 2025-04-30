import random
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

# ───── Parameters ─────
NUM_NODES     = 15
K_DISK_RADIUS = 25
GRID_SIZE     = 100

WHITE, GRAY, BLACK = 'WHITE', 'GRAY', 'BLACK'

class GreedyCDS_Stepper:
    def __init__(self):
        # Generate and store graph
        self.G = self._generate_connected_graph(NUM_NODES, K_DISK_RADIUS, GRID_SIZE)
        self.pos = nx.get_node_attributes(self.G, 'pos')
        
        # CDS set and dominated set
        self.C = set()
        self.dominated = set()
        
        # Step counter
        self.step = 0
        self.finished = False
        
        # Set up plot
        self.fig, self.ax = plt.subplots()
        plt.subplots_adjust(bottom=0.2)
        btn_ax = self.fig.add_axes([0.85, 0.05, 0.1, 0.075])
        self.button = Button(btn_ax, 'Next →')
        self.button.on_clicked(self.next_step)
        
        # Initial draw
        self._log_state()
        self._draw()
        plt.show()
    
    def _generate_connected_graph(self, n, r, size):
        while True:
            pos = {i: (random.uniform(0, size), random.uniform(0, size)) for i in range(n)}
            G = nx.random_geometric_graph(n, r, pos=pos)
            if nx.is_connected(G):
                return G
    
    def _compute_covering_numbers(self, eligible):
        cov = {}
        for v in eligible:
            # neighbors not yet dominated
            cov[v] = sum(1 for u in self.G.neighbors(v) if u not in self.dominated)
        return cov
    
    def _select_next(self):
        # Determine eligible nodes: 
        if self.step == 0:
            eligible = list(self.G.nodes())
        else:
            # nodes not in C that have a neighbor in C
            eligible = [v for v in self.G.nodes() 
                        if v not in self.C and any(u in self.C for u in self.G.neighbors(v))]
        
        if not eligible:
            return None
        
        cov = self._compute_covering_numbers(eligible)
        # pick max covering number, tie-break by highest ID
        max_cov = max(cov.values())
        candidates = [v for v, c in cov.items() if c == max_cov]
        return max(candidates)
    
    def next_step(self, event=None):
        if self.finished:
            print("Algorithm completed.")
            return
        
        v = self._select_next()
        if v is None:
            self.finished = True
            print("No eligible nodes remaining.")
            return
        
        # Add to CDS
        self.C.add(v)
        # Mark dominated: v and its neighbors
        self.dominated.add(v)
        for u in self.G.neighbors(v):
            self.dominated.add(u)
        
        self.step += 1
        self._log_state()
        self._draw()
        
        if len(self.dominated) == self.G.number_of_nodes():
            self.finished = True
            print("All nodes dominated. CDS:", sorted(self.C))
    
    def _log_state(self):
        white = [v for v in self.G.nodes() if v not in self.dominated]
        gray = [v for v in self.dominated if v not in self.C]
        black = sorted(self.C)
        print(f"Step {self.step}: CDS={black}, Dominated={sorted(self.dominated)}")
    
    def _draw(self):
        self.ax.clear()
        # Assign colors
        color_map = {WHITE:'lightgray', GRAY:'gray', BLACK:'orange'}
        node_colors = []
        for v in self.G.nodes():
            if v in self.C:
                node_colors.append(color_map[BLACK])
            elif v in self.dominated:
                node_colors.append(color_map[GRAY])
            else:
                node_colors.append(color_map[WHITE])
        
        nx.draw(self.G, self.pos, 
                node_color=node_colors, 
                with_labels=True, 
                node_size=500, 
                edge_color='lightblue',
                ax=self.ax)
        self.ax.set_title(f"Greedy MCDS – Step {self.step}")
        self.fig.canvas.draw_idle()

# Instantiate and run
stepper = GreedyCDS_Stepper()


