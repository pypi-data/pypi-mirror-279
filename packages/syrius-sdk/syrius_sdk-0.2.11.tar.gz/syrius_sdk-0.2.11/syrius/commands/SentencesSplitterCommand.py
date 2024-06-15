from typing import ClassVar

from syrius.commands.abstract import Command, AbstractCommand


class SentencesSplitterCommand(Command):
    """ """
    id: int = 25
    text: str | AbstractCommand
    sentence_max_char: int | AbstractCommand
    overlap: int | AbstractCommand
