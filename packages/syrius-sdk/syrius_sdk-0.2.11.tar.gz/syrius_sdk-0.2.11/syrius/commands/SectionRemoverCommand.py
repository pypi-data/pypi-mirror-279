from typing import Any, ClassVar

from syrius.commands.abstract import Command, AbstractCommand


class SectionRemoverCommand(Command):
    """ """
    id: int = 24
    words: list[dict[str, Any]] | AbstractCommand
    text: str | AbstractCommand
