import sys, gzip, csv, random
from collections import Counter
from pathlib import Path
import networkx as nx
import matplotlib.pyplot as plt

source = Path(sys.argv[1] if len(sys.argv)>1 else 'sx-mathoverflow.txt.gz')
if not source.exists():
    raise SystemExit(f'Missing {source}. Download the MathOverflow temporal interaction file from https://snap.stanford.edu/data/sx-mathoverflow.html')
G = nx.Graph()
open_fn = gzip.open if source.suffix == '.gz' else open
with open_fn(source, 'rt', encoding='utf-8') as f:
    for line in f:
        if not line.strip() or line.startswith('#'):
            continue
        fields = line.split()
        if len(fields) < 2:
            continue
        try:
            u,v = int(fields[0]),int(fields[1])
        except ValueError:
            continue
        if u != v:
            G.add_edge(u,v)

if G.number_of_edges() == 0:
    raise SystemExit('No edges parsed. Check the dataset file format.')
n,m=G.number_of_nodes(),G.number_of_edges()
lcc=max(nx.connected_components(G),key=len)
print('Nodes:',n,'Edges:',m,'Average degree:',round(2*m/n,4),'Density:',round(nx.density(G),8),'Largest component:',len(lcc))
# Louvain on the full undirected graph, with a reproducible seed.
communities=nx.community.louvain_communities(G,seed=42)
communities=sorted(communities,key=len,reverse=True)
mod=nx.community.modularity(G,communities)
print('Clusters:',len(communities),'Modularity:',round(mod,5))
print('Top 20 cluster sizes:',[len(c) for c in communities[:20]])
with open('exercise3_cluster_sizes.csv','w',newline='') as f:
    w=csv.writer(f);w.writerow(['cluster','size']);w.writerows((i,len(c)) for i,c in enumerate(communities))
with open('exercise3_nodes.csv','w',newline='') as f:
    w=csv.writer(f);w.writerow(['node_id','cluster','degree'])
    for i,c in enumerate(communities):
        for u in sorted(c):w.writerow([u,i,G.degree(u)])
# Reproducible sample of 5 real IDs from different clusters for manual profile verification.
rng=random.Random(42)
print('\nVerify these profiles manually (different clusters):')
for i,c in enumerate(communities[:5]):
    u=rng.choice(sorted(c))
    print(f'Cluster {i}: node {u}, degree {G.degree(u)}, https://mathoverflow.net/users/{u}')
# Visualize the high-degree core, retaining edges among selected nodes.
selected=sorted(G.nodes,key=lambda u:G.degree(u),reverse=True)[:250]
H=G.subgraph(selected).copy()
lookup={u:i for i,c in enumerate(communities) for u in c}
pos=nx.spring_layout(H,seed=42,iterations=60)
plt.figure(figsize=(12,9))
nx.draw_networkx_edges(H,pos,alpha=.12,width=.4)
nx.draw_networkx_nodes(H,pos,node_size=[12+3*H.degree(u) for u in H],node_color=[lookup[u] for u in H],cmap='tab20',alpha=.85)
plt.title('MathOverflow interaction network: top 250 high-degree users\nColors = Louvain communities (sampled view)')
plt.axis('off');plt.tight_layout();plt.savefig('exercise3_communities.png',dpi=200);plt.close()
print('\nSaved exercise3_cluster_sizes.csv, exercise3_nodes.csv, exercise3_communities.png')
