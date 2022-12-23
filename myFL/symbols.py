from myFL import Symbol
from myFL import mySet

class Epsilon(Symbol):
    def __init__(self) -> None:
        super().__init__('ε')


class Star(Symbol):
    def __init__(self) -> None:
        super().__init__('*')


class Add(Symbol):
    def __init__(self) -> None:
        super().__init__('*')


class LPara(Symbol):
    def __init__(self) -> None:
        super().__init__('(')


class RPara(Symbol):
    def __init__(self) -> None:
        super().__init__(')')


eps = Epsilon()
star = Star()
add = Add()
lPara = LPara()
rPara = RPara()
nullSet = mySet()
