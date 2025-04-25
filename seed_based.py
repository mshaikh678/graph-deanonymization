import networkx as nx

def load_graph(edgelist_path):
    return nx.read_edgelist(edgelist_path, nodetype=int)

def load_seeds(seed_path):
    seeds = {}
    with open(seed_path, 'r') as f:
        for line in f:
            g1, g2 = map(int, line.strip().split())
            seeds[g1] = g2
    return seeds

def propagate_matches(G1, G2, seeds):
    matches = seeds.copy()
    while True:
        new_matches = {}
        for node in G1.nodes():
            if node not in matches:
                neighbors = list(G1.neighbors(node))
                matched_neighbors = [n for n in neighbors if n in matches]
                if matched_neighbors:
                    candidates = {}
                    for candidate in G2.nodes():
                        if candidate not in matches.values():
                            score = sum(1 for n in matched_neighbors 
                                     if matches[n] in G2.neighbors(candidate))
                            if score > 0:
                                candidates[candidate] = score
                    if candidates:
                        best_match = max(candidates, key=candidates.get)
                        new_matches[node] = best_match
        if not new_matches:
            break
        matches.update(new_matches)
    return matches

if __name__ == "__main__":
    G1 = load_graph("data/seed_G1.edgelist")
    G2 = load_graph("data/seed_G2.edgelist")
    seeds = load_seeds("data/seed_mapping.txt")
    
    full_mapping = propagate_matches(G1, G2, seeds)
    
    with open("results/LastnameSeedbased.txt", "w") as f:
        for g1, g2 in full_mapping.items():
            f.write(f"{g1} {g2}\n")
