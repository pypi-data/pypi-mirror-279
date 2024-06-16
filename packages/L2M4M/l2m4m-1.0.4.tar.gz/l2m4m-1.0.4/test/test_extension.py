"""
Test case for the Latex2MathML markdown extension.
"""

import re
from unittest import TestCase

from markdown import Markdown
from l2m4m import LaTeX2MathMLExtension


class TestExtension(TestCase):
    """
    Tests for the Latex2MathML markdown extension.
    """

    def setUp(self):
        self.markdown = Markdown(extensions=[LaTeX2MathMLExtension()])

    # pylint: disable=invalid-name
    def assertHTMLEqualsMarkdown(self, html, markdown):
        """
        Assert that the specified Markdown coverts to HTML identical to the
        specified HTML. Whitespace surrounding newlines in the specified
        HTML are discarded.
        """
        self.assertEqual(
            re.sub(r"\s*\n\r?\s*", "", html),
            re.sub(r"\s*\n\r?\s*", "", self.markdown.convert(markdown))
        )

    def test_no_latex_no_conversion(self):
        """
        Assert that markdown conversion still works as expected.
        """
        self.assertHTMLEqualsMarkdown(
            "<p>Spam, bacon, eggs.</p>",
            "Spam, bacon, eggs."
        )

    def test_inline_latex_converted(self):
        """
        Assert that inline LaTeX math is converted as expected.
        """
        self.assertHTMLEqualsMarkdown(
            """
<p>
    Spam, bacon, eggs. <math display="inline" xmlns="
                            http://www.w3.org/1998/Math/MathML">
        <mrow>
            <mi>a</mi>
            <mo>&#x0002B;</mo>
            <mi>b</mi>
            <mo>&#x0003D;</mo>
            <mi>c</mi>
        </mrow>
    </math>. Sausage, ham.
</p>
            """,
            "Spam, bacon, eggs. $a + b = c$. Sausage, ham."
        )

    def test_block_latex_converted(self):
        """
        Assert that Latex math blocks are converted as expected.
        """
        self.assertHTMLEqualsMarkdown(
            """
<math display="block" xmlns="http://www.w3.org/1998/Math/MathML">
    <mrow>
        <mi>a</mi>
        <mo>&#x0002B;</mo>
        <mi>b</mi>
        <mo>&#x0003D;</mo>
        <mi>c</mi>
    </mrow>
</math>
            """,
            "$$a + b = c$$"
        )

    def test_block_latex_alt_converted(self):
        """
        Assert that Latex math blocks using the alternative notation are
        converted as expected.
        """
        self.assertHTMLEqualsMarkdown(
            """
<math display="block" xmlns="http://www.w3.org/1998/Math/MathML">
<mrow>
    <mi>a</mi>
    <mo>&#x0002B;</mo>
    <mi>b</mi>
    <mo>&#x0003D;</mo>
    <mi>c</mi>
</mrow>
</math>
            """,
            "\\[a + b = c\\]"
        )

    def test_block_multiline_latex_converted(self):
        """
        Assert that LaTeX math blocks of multiple lines are converted as
        expected.
        """
        self.assertHTMLEqualsMarkdown(
            """
<math display="block" xmlns="http://www.w3.org/1998/Math/MathML">
    <mrow>
        <mi>a</mi>
        <mo>&#x0002B;</mo>
        <mi>b</mi>
        <mo>&#x0003D;</mo>
        <mi>c</mi>
        <mspace linebreak="newline"></mspace>
        <mi>c</mi>
        <mo>&#x0003D;</mo>
        <mi>a</mi>
        <mo>&#x02212;</mo>
        <mi>b</mi>
    </mrow>
</math>
            """,
            """
$$
a + b = c\\\\
c = a - b
$$
            """
        )

    def test_block_multiple_latex_converted(self):
        """
        Assert that multiple LaTeX math blocks are converted as expected.
        """
        self.assertHTMLEqualsMarkdown(
            """
<p>Bacon, eggs, ham.</p>
<math display="block" xmlns="http://www.w3.org/1998/Math/MathML">
    <mrow>
        <mfrac>
            <mrow>
                <mi>a</mi>
            </mrow>
            <mrow>
                <mi>b</mi>
            </mrow>
        </mfrac>
        <mo>&#x0003D;</mo>
        <mi>c</mi>
    </mrow>
</math>
<p>Spam, spam, bacon, spam.</p>
<math display="block" xmlns="http://www.w3.org/1998/Math/MathML">
    <mrow>
        <msub>
            <mo>&#x02211;</mo>
            <mi>a</mi>
        </msub>
        <mo>&#x0003D;</mo>
        <mi>b</mi>
        <mo>&#x0002B;</mo>
        <mi>c</mi>
    </mrow>
</math>
            """,
            """
Bacon, eggs, ham.

$$
\\frac{a}{b} = c
$$

Spam, spam, bacon, spam.

$$
\\sum_a = b + c
$$
            """
        )

    def test_block_subsequent_latex_converted(self):
        """
        Assert that subsequent LaTeX blocks of math are converted as expected.
        """
        self.assertHTMLEqualsMarkdown(
            """
<math display="block" xmlns="http://www.w3.org/1998/Math/MathML">
    <mrow>
        <mfrac>
            <mrow>
                <mi>a</mi>
            </mrow>
            <mrow>
                <mi>b</mi>
            </mrow>
        </mfrac>
        <mo>&#x0003D;</mo>
        <mi>c</mi>
    </mrow>
</math>
<math display="block" xmlns="http://www.w3.org/1998/Math/MathML">
    <mrow>
        <msub>
            <mo>&#x02211;</mo>
            <mi>a</mi>
        </msub>
        <mo>&#x0003D;</mo>
        <mi>b</mi>
        <mo>&#x0002B;</mo>
        <mi>c</mi>
    </mrow>
</math>
            """,
            """
$$
\\frac{a}{b} = c
$$

$$
\\sum_a = b + c
$$
                """
            )
