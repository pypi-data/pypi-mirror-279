from typing import ClassVar

from syrius.commands.abstract import Command, AbstractCommand


class UnstructuredCommand(Command):
    """ """
    id: int = 23
    text: str | AbstractCommand
