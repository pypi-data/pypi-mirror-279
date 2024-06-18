from typing import ClassVar

from syrius.commands.abstract import Command, AbstractCommand


class PdfHighlighterCommand(Command):
    """ """
    id: int = 27
    filename: str | AbstractCommand
    bucket: str | AbstractCommand
    access_key: str | AbstractCommand
    secret_key: str | AbstractCommand
    texts: list[str] | AbstractCommand
