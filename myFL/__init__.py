from functools import reduce
from typing import Hashable, Iterable


class mySet(set[Hashable]):
    def __hash__(self) -> int:
        hash_tuple = tuple(sorted(hash(item) for item in self))
        return hash(hash_tuple)
    
    def __repr__(self) -> str:
        return repr(set(self))

    def __str__(self) -> str:
        ret = ''
        items = tuple(self)
        if len(items) >= 1:
            ret += str(items[0])
        for item in items[1:]:
            ret += f', {str(item)}'
        return '{' + ret + '}'


class Symbol:
    def __init__(self, symbol_str) -> None:
        if isinstance(symbol_str, str):
            self.symbol_str = symbol_str
        else :
            self.symbol_str = str(symbol_str)

    def __str__(self) -> str:
        return self.symbol_str

    def __repr__(self) -> str:
        return f'Symbol({self.symbol_str})'

    def __hash__(self) -> int:
        return hash(self.symbol_str)

    def __eq__(self, __o: object) -> bool:
        assert isinstance(__o, Symbol)
        return hash(self) == hash(__o)


class String(list):
    def __init__(self, arg) -> None:
        if isinstance(arg, str):
            self.__init__(Symbol(symbol) for symbol in arg)
        elif isinstance(arg, Iterable):
            super().__init__(arg)
        else:
            assert 0

    def __str__(self) -> str:
        string = reduce(lambda base, sym: base + str(sym), self, '')
        return string

    def __repr__(self) -> str:
        return f'String({str(self)})'

    def __hash__(self) -> int:
        hash_tuple = tuple(sorted(hash(item) for item in self))
        return hash(hash_tuple)

