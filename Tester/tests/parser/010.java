class Main {
    int[] a;
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
  node6 [label="Array"]
  node7 [label="int"]
  node6 -> node7[label=type_]
  node5 -> node6[label=type_]
  node8 [label="a"]
  node5 -> node8[label=name]
  node9 [label="None"]
  node5 -> node9[label=value]
  node4 -> node5[label=children]
  node2 -> node4[label=fields]
  node1 -> node2[label=class_]
}