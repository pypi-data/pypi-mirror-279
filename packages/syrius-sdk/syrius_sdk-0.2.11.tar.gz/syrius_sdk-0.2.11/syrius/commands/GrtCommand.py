from typing import ClassVar

from syrius.commands.abstract import Command, AbstractCommand


class GrtCommand(Command):
    """ """
    id: int = 7
    number: int | AbstractCommand
    greater: int | AbstractCommand
