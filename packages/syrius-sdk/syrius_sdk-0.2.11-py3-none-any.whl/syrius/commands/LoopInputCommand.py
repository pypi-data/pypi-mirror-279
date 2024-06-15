from syrius.api import SyriusAPI
from syrius.commands.abstract import LocalCommand
from syrius.exceptions import FlowException


class LoopInputCommand(LocalCommand):
    """ """

    def run(self) -> str:
        """ """
        return "ref@index"
