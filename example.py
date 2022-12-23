from myFL.FA import *
from graphviz import Digraph

# 输入 ε-NFA
S = [State(i) for i in range(25)]
Q = mySet(S[1:])
a = Symbol('a')
b = Symbol('b')
c = Symbol('c')
Sigma = mySet({a,b,c})
q0 = S[1]
F = mySet({S[24]})
delta = TransferFunction()
delta.add_edges([
    (S[1], S[2], eps),
    (S[1], S[8], eps),
    (S[2], S[3], eps),
    (S[2], S[5], eps),
    (S[3], S[4], a),
    (S[4], S[7], eps),
    (S[5], S[6], b),
    (S[6], S[7], eps),
    (S[7], S[2], eps),
    (S[7], S[8], eps),
    (S[8], S[9], a),
    (S[9], S[10], eps),
    (S[9], S[16], eps),
    (S[10], S[11], eps),
    (S[10], S[13], eps),
    (S[11], S[12], b),
    (S[12], S[15], eps),
    (S[13], S[14], c),
    (S[14], S[15], eps),
    (S[15], S[16], eps),
    (S[15], S[10], eps),
    (S[16], S[17], b),
    (S[17], S[18], eps),
    (S[17], S[24], eps),
    (S[18], S[19], eps),
    (S[18], S[20], eps),
    (S[19], S[21], a),
    (S[20], S[22], c),
    (S[21], S[23], eps),
    (S[22], S[23], eps),
    (S[23], S[18], eps),
    (S[23], S[24], eps)
])
eps_nfa = eps_NFA(Q, Sigma, delta, q0, F)
# 将自动机输出为graphviz图像
dot_eps_nfa = Digraph("eps_nfa", format="jpg")
eps_nfa.create_digraph(dot_eps_nfa)
dot_eps_nfa.render(filename="dot/eps_nfa")


# ε-NFA转DFA
dfa = eps_nfa.to_DFA()

dot_dfa = Digraph("dfa", format="jpg")
dfa.create_digraph(dot_dfa)
dot_dfa.render(filename="dot/dfa")


# 最小化DFA
min_dfa = dfa.minimized_dfa()

dot_min_dfa = Digraph("min_dfa", format="jpg")
min_dfa.create_digraph(dot_min_dfa)
dot_min_dfa.render(filename="dot/min_dfs")
