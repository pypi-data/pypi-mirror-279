"""
Definition of the Latex2MathML extension.
"""

import re

from latex2mathml import converter

from markdown import Extension
from markdown.blockprocessors import BlockProcessor
from markdown.inlinepatterns import Pattern


# pylint: disable=too-few-public-methods
class LaTeX2MathMLExtension(Extension):
    """
    The Latex2MathMLExtension class.
    """

    _RE_LATEX = r"\$([^$]+)\$"

    # pylint: disable=invalid-name
    def extendMarkdown(self, md):
        """
        Extend the specified markdown instance with a pattern for inline
        LaTex and a parser for blocks of LaTeX, to be converted to MathML.
        """
        md.inlinePatterns.register(
            LatexPattern(self._RE_LATEX), "latex-inline", 170)
        md.parser.blockprocessors.register(
            LatexBlockProcessor(md.parser), 'latex-block', 170)


# pylint: disable=too-few-public-methods
class LatexPattern(Pattern):
    """
    A pattern for inline LaTeX.
    """

    # pylint: disable=invalid-name
    def handleMatch(self, m):
        """
        Convert inline LaTeX to MathML.
        """
        return converter.convert_to_element(m.group(2))


# pylint: disable=too-few-public-methods
class LatexBlockProcessor(BlockProcessor):
    """
    A processor for blocks of LaTeX.
    """

    _RE_LATEX_START = [
        r"^\s*\${2}",
        r"^\s*\\\["
    ]

    _RE_LATEX_END = [
        r"\${2}\s*$",
        r"\\\]\s*$"
    ]

    def __init__(self, parser):
        super().__init__(parser)

        self._mode = 0

    def test(self, _, block):
        """
        Indicated whether the specified block starts a block of LaTeX.
        """
        for i, start in enumerate(self._RE_LATEX_START):
            if not re.search(start, block):
                continue

            self._mode = i
            return True

        return False

    def run(self, parent, blocks):
        """
        Convert all subsequent blocks of LaTeX to MathML. Cancel conversion
        in case no ending block is found.
        """

        start = self._RE_LATEX_START[self._mode]
        end = self._RE_LATEX_END[self._mode]

        for i, block in enumerate(blocks):
            if not re.search(start, block):
                continue

            text = "\n".join([blocks.pop(j) for j in range(0, i + 1)])
            text = re.sub(start, "", text)
            text = re.sub(end, "", text)

            converter.convert_to_element(text, display="block", parent=parent)

            return True

        return False
