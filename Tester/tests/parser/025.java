x & y
x && y
x | y
x || y
EOF
1	1	IDENT	x	x
1	3	OPERATION	&	OpType.AND_ONE
1	5	IDENT	y	y
2	1	IDENT	x	x
2	3	OPERATION	&&	OpType.AND
2	6	IDENT	y	y
3	1	IDENT	x	x
3	3	OPERATION	|	OpType.OR_ONE
3	5	IDENT	y	y
4	1	IDENT	x	x
4	3	OPERATION	||	OpType.OR
4	6	IDENT	y	y