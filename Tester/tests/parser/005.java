class Main {
}
EOF
digraph astgraph {
  node [shape=circle, fontsize=12, fontname="Courier", height=.1];
  ranksep=.3;
  edge [arrowsize=.5]
  node1 [label="CompUnit"]
  node2 [label="Class"]
  node3 [label="Main"]
  node2 -> node3[label=name]
  node4 [label="Block"]
  node2 -> node4[label=fields]
  node1 -> node2[label=class_]
}