# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

import logging

from rich.console import Console
from rich.highlighter import RegexHighlighter
from rich.logging import RichHandler
from rich.theme import Theme


class NodeHighlighter(RegexHighlighter):
    """
    Apply style to anything that looks like an faebryk Node\n
    <*|XOR_with_NANDS.nands[2]|NAND.inputs[0]|Logic> with
      <*|TI_CD4011BE.nands[2]|ElectricNAND.inputs[0]|ElectricLogic>\n
    \t<> = Node\n
    \t|  = Type\n
    \t.  = Parent\n
    \t*  = Root
    """

    base_style = "node."
    highlights = [
        #  r"(?P<Rest>(.*))",
        r"(?P<Node>([/</>]))",
        r"[?=\|](?P<Type>([a-zA-Z_0-9]+))[?=\>]",
        r"[\.](?P<Child>([a-zA-Z_0-9]+))[?=\[]",
        r"[\|](?P<Parent>([a-zA-Z_0-9]+))[?=\.]",
        r"[?<=*.](?P<Root>(\*))",
        r"[?=\[](?P<Number>([0-9]+))[?=\]]",
    ]


theme = Theme(
    {
        "node.Node": "bold magenta",
        "node.Type": "bright_cyan",
        "node.Parent": "bright_red",
        "node.Child": "bright_yellow",
        "node.Root": "bold yellow",
        "node.Number": "bright_green",
        #   "node.Rest": "bright_black",
    }
)


def setup_basic_logging(rich: bool = True):
    logging.basicConfig(
        format="" if not rich else "%(message)s",
        level=logging.INFO,
        handlers=[
            RichHandler(
                console=Console(
                    safe_box=False,
                    theme=theme,
                ),
                highlighter=NodeHighlighter(),
            )
        ]
        if rich
        else None,
    )
