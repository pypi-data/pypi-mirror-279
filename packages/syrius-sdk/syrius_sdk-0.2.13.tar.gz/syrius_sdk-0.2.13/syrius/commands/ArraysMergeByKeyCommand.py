from typing import Any

from syrius.commands.abstract import Command, AbstractCommand


class ArraysMergeByKeyCommand(Command):
    """ """
    id: int = 1
    initial: list[dict[str, Any]] | AbstractCommand
    to_combine: list[dict[str, Any]] | AbstractCommand
    key: str | AbstractCommand
