from typing import Any, ClassVar

from syrius.commands.abstract import Command, AbstractCommand


class ArrayLengthCommand(Command):
    """ """
    id: int = 2
    array: list[Any] | AbstractCommand
