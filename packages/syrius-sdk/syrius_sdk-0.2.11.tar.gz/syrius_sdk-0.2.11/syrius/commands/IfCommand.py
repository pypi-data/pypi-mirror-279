from typing import Any

from syrius.commands.abstract import Logical


class IfCommand(Logical):
    """ """
    id: int = 1
    condition: Any
    then: list[Any]
