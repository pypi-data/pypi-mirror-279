from typing import Any, ClassVar

from syrius.commands.abstract import Command, AbstractCommand


class ArrayReduceByKeyCommand(Command):
    """ """
    id: int = 32
    array: list[Any] | AbstractCommand
    key: str | AbstractCommand
    value: str | AbstractCommand
