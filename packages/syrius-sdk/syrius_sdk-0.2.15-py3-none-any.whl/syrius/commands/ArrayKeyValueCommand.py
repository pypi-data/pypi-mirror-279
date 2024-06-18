from typing import Any, ClassVar

from syrius.commands.abstract import Command, AbstractCommand


class ArrayKeyValueCommand(Command):
    """ """
    id: int = 26
    kvstore: dict[str, Any] | AbstractCommand
