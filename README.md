
# Connected Dominating Set Construction in Geometric k-Disk Graphs

This repository contains Python implementations of three algorithms for constructing a **Connected Dominating Set (CDS)** in **geometric k-disk graphs**, commonly used to model wireless ad hoc and sensor networks.

## 📘 Project Overview

A Connected Dominating Set (CDS) serves as a virtual communication backbone in wireless networks, helping reduce routing overhead and energy consumption. This project explores three different approaches to CDS construction and visualizes the step-by-step progression of each algorithm.

Implemented in Python using **NetworkX**, **Matplotlib**, and **interactive widgets**, this repository provides both functional and visual insights into each algorithm's behavior and performance.

---

## 📁 Algorithms Included

### 1. 📡 Distributed Approximation Algorithm (Algorithm I)

- Based on state transitions (`WHITE → GRAY → YELLOW → BLACK`)
- Follows a distributed message-passing model
- Leader-based initiation and round-wise simulation
- Includes **Step 8 optimization** (removes redundant BLACK nodes)

### 2. ⚙️ Greedy Heuristic Algorithm

- Selects nodes based on maximum **coverage** in a bipartite-style model
- Efficient but does not guarantee a minimum CDS
- Simple and centralized logic


### 3. 🧠 Brute Force MCDS

- Exhaustively checks all subsets of nodes
- Returns the **true minimum CDS**
- Only feasible for **small graphs** (≤ 15 nodes)

## 📊 Visualization

All algorithms generate live Matplotlib plots showing:
- Node state transitions
- Final CDS formation
- CDS nodes highlighted in orange or black

Interactive tools like buttons or keypress support are included for round-by-round simulation.

---

## ⚙️ Requirements

Install required packages:

pip install networkx matplotlib

# to run
python algorithm_name.py


