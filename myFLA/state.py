from typing import Hashable


class State:
    def __init__(self, state_val: Hashable) -> None:
        self.state_val = state_val

    def __str__(self) -> str:
        return str(self.state_val)

    def __repr__(self) -> str:
        return f'State({str(self)})'

    def __hash__(self) -> int:
        return hash(self.state_val)

    def __eq__(self, __o: object) -> bool:
        assert isinstance(__o, State)
        return hash(self) == hash(__o)


class StrValue:
    def __init__(self, val: str) -> None:
        self.val = val

    def __str__(self) -> str:
        return self.val

    def __repr__(self) -> str:
        return f'StrValue({str(self)})'

    def __hash__(self) -> int:
        return hash(self.val)

    def __eq__(self, __o: object) -> bool:
        assert isinstance(__o, StrValue)
        return hash(self) == hash(__o)


class StateStr(State):
    def __init__(self, state_str: str) -> None:
        super().__init__(StrValue(state_str))
