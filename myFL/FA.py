from queue import Queue
from typing import Any, Dict
from itertools import product
from myFL import mySet, Symbol
from myFL.symbols import eps
from myFL.state import *
from graphviz import Digraph


class StateSymbolPair:
    def __init__(self, state: State, symbol: Symbol) -> None:
        self.state = state
        self.symbol = symbol

    def __str__(self) -> str:
        return f'({self.state}, {self.symbol})'

    def __repr__(self) -> str:
        return repr(self)

    def __hash__(self) -> int:
        return hash((self.state, self.symbol))

    def __eq__(self, __o: object) -> bool:
        assert isinstance(__o, StateSymbolPair)
        return hash(self) == hash(__o)


class TransferFunction:
    def __init__(self) -> None:
        self.transfer_function: Dict[StateSymbolPair, mySet[State]] = dict()

    def union(self, transfer_function: Dict[StateSymbolPair, mySet[State]]) -> None:
        self.transfer_function.update(transfer_function)

    def set(self, key: StateSymbolPair, value: mySet[State]):
        self.transfer_function[key] = value

    def insert_state_symbol_pair(self, key: StateSymbolPair, state: State):
        if key in self.transfer_function.keys():
            self.transfer_function[key].add(state)
        else:
            self.transfer_function[key] = mySet((state,))

    def set_transfer_table(self, transfer_table):
        for src, dst_set in transfer_table.items():
            for symbol, dst in dst_set.items():
                self.insert_state_symbol_pair(StateSymbolPair(src, symbol), dst)

    def add_edge(self, src_state: State, dst_state: State, symbol: Symbol):
        self.insert_state_symbol_pair(StateSymbolPair(src_state, symbol), dst_state)

    def add_edges(self, edge_list):
        for edge in edge_list:
            self.add_edge(*edge)

    def get_state_symbol_pair(self, key: StateSymbolPair):
        if key in self.transfer_function.keys():
            return self.transfer_function[key]
        else:
            return mySet()

    def get(self, state: State, symbol: Symbol) -> mySet[State]:
        return self.get_state_symbol_pair(StateSymbolPair(state, symbol))

    def eps_closure_set(self, states: mySet[State]) -> mySet[State]:
        closure = mySet(states)
        while True:
            new_clusure = mySet(closure)
            for state in closure:
                new_clusure |= self.get(state, eps)
            if new_clusure == closure:
                break
            closure = new_clusure
        return closure

    def eps_closure(self, states: Any) -> mySet[State]:
        if isinstance(states, State):
            return self.eps_closure_set(mySet((states,)))
        elif isinstance(states, mySet):
            return self.eps_closure_set(states)
        else:
            assert 0

    def move(self, states: mySet[State], symbol: Symbol) -> mySet[State]:
        ret = mySet()
        for state in states:
            ret |= self.get(state, symbol)
        return ret


class FiniteAutomata:
    def __init__(self,
                 Q: mySet,
                 Sigma: mySet,
                 delta: TransferFunction,
                 q0: State,
                 F: mySet
                 ) -> None:
        self.Q = Q
        self.Sigma = Sigma
        self.delta = delta
        self.q0 = q0
        self.F = F

    def create_digraph(self, dot: Digraph):
        id_map = {
            state: f'S{id}' for (id, state) in enumerate(self.Q)
        }
        for state in self.Q:
            dot.node(
                name=id_map[state],
                label=str(state),
                shape='doublecircle' if state in self.F else 'circle'
            )
        dot.node(name='', color='white')
        dot.edge('', id_map[self.q0], label='', arrowhead='normal')

        def dot_add_edge(src, dst_set, symbol):
            for dst in dst_set:
                dot.edge(
                    tail_name=id_map[src],
                    head_name=id_map[dst],
                    label=str(symbol),
                    arrowhead='normal'
                )

        for state in self.Q:
            dot_add_edge(state, self.delta.get(state, eps), eps)
            for symbol in self.Sigma:
                dot_add_edge(state, self.delta.get(state, symbol), symbol)


class DFA(FiniteAutomata):
    def __init__(self, *args) -> None:
        super(DFA, self).__init__(*args)
        self.adjacency_table = {}
        for (src_symbol_pair, dst) in self.delta.transfer_function.items():
            self.adjacency_table[(src_symbol_pair.state, dst)] = src_symbol_pair.symbol

    def add_dead_state(self):
        dead = StateStr('dead')
        updated = False
        for state, symbol in product(self.Q, self.Sigma):
            if not self.delta.get(state, symbol):
                self.delta.add_edge(state, dead, symbol)
                updated = True
        if updated:
            self.Q.add(dead)
            for symbol in self.Sigma:
                self.delta.add_edge(dead, dead, symbol)

    def product(self, other, finish_filter):
        Q = mySet(product(self.Q, other.Q))
        Sigma = self.Sigma
        delta = TransferFunction()
        q0 = (self.q0, other.q0)
        F = mySet(filter(finish_filter, Q))
        pass
        # TODO


    def minimized_dfa(self):
        self.add_dead_state()
        eq_pairs = mySet()
        not_accepted_states = self.Q - self.F
        for S1, S2 in product(not_accepted_states, not_accepted_states):
            eq_pairs.add((S1, S2))
        for S1, S2 in product(self.F, self.F):
            eq_pairs.add((S1, S2))

        def eq_judge(S1, S2):
            for symbol in self.Sigma:
                S1_nxt_set = self.delta.get(S1, symbol)
                S2_nxt_set = self.delta.get(S2, symbol)
                for S1_nxt, S2_nxt in product(S1_nxt_set, S2_nxt_set):
                    if (S1_nxt, S2_nxt) not in eq_pairs:
                        return False
            return True

        while True:
            delete_pairs = mySet()
            for S1, S2 in eq_pairs:
                if not eq_judge(S1, S2):
                    delete_pairs.add((S1, S2))
            if not delete_pairs:
                break
            eq_pairs -= delete_pairs

        state_eq_set_map = dict()

        for state in self.Q:
            if state in state_eq_set_map.keys():
                continue
            eq_set = mySet()
            for other in self.Q:
                if (state, other) in eq_pairs:
                    eq_set.add(other)
            for item in eq_set:
                state_eq_set_map[item] = eq_set

        Q = mySet[State](state_eq_set_map.values())
        Sigma = self.Sigma
        delta = TransferFunction()
        q0 = state_eq_set_map[self.q0]
        F = mySet[State]({state_eq_set_map[f] for f in self.F})

        for state, symbol in product(self.Q, self.Sigma):
            for transferred in self.delta.get(state, symbol):
                delta.add_edge(
                    src_state=state_eq_set_map[state],
                    dst_state=state_eq_set_map[transferred],
                    symbol=symbol
                )

        return DFA(Q, Sigma, delta, q0, F)

    def is_empty(self):
        reachable = {self.q0}
        queue = Queue()
        queue.put(self.q0)
        while not queue.empty():
            now = queue.get()
            for symbol in self.Sigma:
                for dst in self.delta.get(now, symbol):
                    if dst not in reachable:
                        reachable.add(dst)
                        queue.put(dst)
        return not any(state in self.F for state in reachable)



class eps_NFA(FiniteAutomata):
    def to_DFA(self) -> DFA:
        Q = mySet[State]()
        Sigma = self.Sigma
        delta = TransferFunction()
        q0 = self.delta.eps_closure(self.q0)
        F = mySet[State]()

        cal_queue = Queue[mySet[State]]()
        cal_queue.put(q0)
        Q.add(q0)

        while not cal_queue.empty():
            sub_set = cal_queue.get()
            if sub_set & self.F:
                F.add(sub_set)
            for symbol in self.Sigma:
                transferred_set = self.delta.eps_closure(
                    self.delta.move(sub_set, symbol)
                )
                if not transferred_set:
                    continue
                delta.add_edge(sub_set, transferred_set, symbol)
                if transferred_set not in Q:
                    Q.add(transferred_set)
                    cal_queue.put(transferred_set)

        return DFA(Q, Sigma, delta, q0, F)


class NFA(eps_NFA):
    pass
