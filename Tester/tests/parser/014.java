class Main {
    int a = 1 + 1;
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
  node5 [label="Var"]
  node6 [label="int"]
  node5 -> node6[label=type_]
  node7 [label="a"]
  node5 -> node7[label=name]
  node8 [label="+"]
  node9 [label="1"]
  node8 -> node9[label=left]
  node10 [label="1"]
  node8 -> node10[label=right]
  node5 -> node8[label=value]
  node4 -> node5[label=children]
  node2 -> node4[label=fields]
  node1 -> node2[label=class_]
}