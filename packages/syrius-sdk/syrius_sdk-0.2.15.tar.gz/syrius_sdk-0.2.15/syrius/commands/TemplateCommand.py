from typing import Any, ClassVar

from syrius.commands.abstract import Command, AbstractCommand


class TemplateCommand(Command):
    """ """
    id: int = 21
    variables: dict[str, Any] | AbstractCommand
    text: str | AbstractCommand
