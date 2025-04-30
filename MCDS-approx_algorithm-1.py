import random
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from collections import deque

# ───── Parameters ─────
NUM_NODES     = 15
K_DISK_RADIUS = 25
GRID_SIZE     = 100
T0_DELAY      = 1

WHITE, GRAY, YELLOW, BLACK = 'WHITE','GRAY','YELLOW','BLACK'

# ───── Node Class ─────
class Node:
    def __init__(self, node_id, pos):
        self.id         = node_id
        self.pos        = pos
        self.state      = WHITE
        self.dominator  = None
        self.rank       = None
        self.round_idle = 0
        self.Wu         = set()
        self.msg_queue  = deque()
        self.children   = set()
    def __repr__(self):
        return f"{self.id}:{self.state}"

# ───── Build a connected geometric graph ─────
def generate_connected_graph(n, r):
    while True:
        pos = {i:(random.uniform(0,GRID_SIZE), random.uniform(0,GRID_SIZE)) for i in range(n)}
        G = nx.random_geometric_graph(n, r, pos=pos)
        if nx.is_connected(G):
            return G

# ───── Messaging and state transitions ─────
def broadcast_messages(G, nodes, t):
    for u,node in nodes.items():
        if   node.state==BLACK:   tag='dominator'
        elif node.state==GRAY:    tag='dominatee'
        elif node.state==YELLOW:  tag='active'
        else:                     continue

        for v in G.neighbors(u):
            if tag=='active' and nodes[v].state not in (WHITE,YELLOW):
                continue
            nodes[v].msg_queue.append((t, tag, u, node.rank))

def process_round(G, nodes, t):
    changed = False
    # 1) Process all messages
    for u,node in nodes.items():
        while node.msg_queue:
            _, msg, s, rnk = node.msg_queue.popleft()

            if msg=='dominator' and node.state in (WHITE,YELLOW):
                node.state      = GRAY
                node.dominator  = s
                node.rank       = rnk+1
                nodes[s].children.add(u)
                node.round_idle = 0
                changed = True

            elif msg=='dominatee' and node.state==WHITE:
                node.state      = YELLOW
                node.dominator  = s
                node.rank       = rnk+1
                nodes[s].children.add(u)
                node.round_idle = 0
                changed = True

            elif msg=='active':
                node.Wu.add(s)

    # 2) Elect next BLACK pair
    cands = [u for u,n in nodes.items() if n.state==YELLOW and n.round_idle>=T0_DELAY]
    if cands:
        u = min(cands)
        grays = [v for v in G.neighbors(u) if nodes[v].state==GRAY]
        if grays:
            v = min(grays)
            nodes[u].state = nodes[v].state = BLACK
            nodes[u].children.add(v)
            nodes[v].children.add(u)
            nodes[u].round_idle = 0
            nodes[u].Wu.clear()
            changed = True

    # 3) Advance idle
    for n in nodes.values():
        if n.state==YELLOW:
            n.round_idle += 1

    # 4) Step 8
    for u,n in nodes.items():
        if n.state==BLACK and not n.children:
            n.state = GRAY
            changed = True

    return changed

# ───── Simulator with key‐binding ─────
class CDS_Stepper:
    def __init__(self):
        self.G     = generate_connected_graph(NUM_NODES, K_DISK_RADIUS)
        self.nodes = {i: Node(i, self.G.nodes[i]['pos']) for i in self.G.nodes()}
        leader = min(self.nodes)
        self.nodes[leader].state = BLACK
        self.nodes[leader].rank  = 0
        self.pos   = nx.get_node_attributes(self.G, 'pos')
        self.t     = 0
        self.changed = True

        # figure + button
        self.fig, self.ax = plt.subplots()
        plt.subplots_adjust(bottom=0.2)
        btn_ax = self.fig.add_axes([0.85, 0.05, 0.1, 0.075])
        self.button = Button(btn_ax, '→')
        self.button.on_clicked(self.next_step)

        # bind right‐arrow key
        self.fig.canvas.mpl_connect('key_press_event', self.on_key)

        # draw initial
        self.log_state()
        self.draw_state()
        plt.show()

    def log_state(self):
        by = {WHITE:[],GRAY:[],YELLOW:[],BLACK:[]}
        for u,n in self.nodes.items():
            by[n.state].append(u)
        print(f"Round {self.t:2d}: W={sorted(by[WHITE])}  "
              f"G={sorted(by[GRAY])}  Y={sorted(by[YELLOW])}  B={sorted(by[BLACK])}")

    def draw_state(self):
        self.ax.clear()
        cmap = {WHITE:'lightgray',GRAY:'gray',YELLOW:'orange',BLACK:'black'}
        colors = [cmap[self.nodes[u].state] for u in self.G.nodes()]
        nx.draw(self.G, self.pos, ax=self.ax,
                node_color=colors, with_labels=True,
                node_size=400, edge_color='lightblue')
        self.ax.set_title(f"Algorithm I – Round {self.t}")
        self.fig.canvas.draw_idle()

    def next_step(self, event=None):
        if not self.changed:
            print("No more changes.")
            return
        broadcast_messages(self.G, self.nodes, self.t)
        self.changed = process_round(self.G, self.nodes, self.t)
        self.t += 1
        self.log_state()
        self.draw_state()

    def on_key(self, event):
        if event.key == 'right':
            self.next_step()

# ───── Run ─────
stepper = CDS_Stepper()
