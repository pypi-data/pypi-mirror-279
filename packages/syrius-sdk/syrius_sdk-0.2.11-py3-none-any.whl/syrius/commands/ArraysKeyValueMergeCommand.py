from typing import Any

from syrius.commands.abstract import Command, AbstractCommand


class ArraysMergeByKeyCommand(Command):
    id: int = 3
    dictionaries: list[dict[str, Any]] | AbstractCommand
