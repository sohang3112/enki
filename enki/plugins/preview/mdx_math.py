# -*- coding: utf-8 -*-

'''
Math extension for Python-Markdown
==================================

Adds support for displaying math formulas using [MathJax](http://www.mathjax.org/).

Author: 2015, Dmitry Shachnev <mitya57@gmail.com>.
Source: https://github.com/mitya57/python-markdown-math,
commit db12837790a0e260c87da4edd9dc276361501897 plus some fixes.
'''

import markdown


class MathExtension(markdown.extensions.Extension):

    def __init__(self, *args, **kwargs):
        self.config = {
            'enable_dollar_delimiter': [False, 'Enable single-dollar delimiter'],
        }
        super(MathExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md):
        def handle_match_inline(m):
            node = markdown.util.etree.Element('script')
            node.set('type', 'math/tex')
            node.text = markdown.util.AtomicString(m.group(3))
            return node

        def handle_match(m):
            node = markdown.util.etree.Element('script')
            node.set('type', 'math/tex; mode=display')
            if '\\begin' in m.group(2):
                node.text = markdown.util.AtomicString(m.group(2) + m.group(4) + m.group(5))
            else:
                node.text = markdown.util.AtomicString(m.group(3))
            return node

        inlinemathpatterns = (
            markdown.inlinepatterns.Pattern(r'(?<!\\|\$)(\$)([^\$]+)(\$)'),  # $...$
            markdown.inlinepatterns.Pattern(r'(?<!\\)(\\\()(.+?)(\\\))')     # \(...\)
        )
        mathpatterns = (
            markdown.inlinepatterns.Pattern(r'(?<!\\)(\$\$)([^\$]+)(\$\$)'),  # $$...$$
            markdown.inlinepatterns.Pattern(r'(?<!\\)(\\\[)(.+?)(\\\])'),    # \[...\]
            markdown.inlinepatterns.Pattern(r'(?<!\\)(\\begin{([a-z]+?\*?)})(.+?)(\\end{\3})')
        )
        if not self.getConfig('enable_dollar_delimiter'):
            inlinemathpatterns = inlinemathpatterns[1:]

        PRIORITY_LT_ESCAPE = 185     # less priority than 'escape' (180), more than 'backtick' (190) ; NOTE: higher priority has lower numeric value
        for i, pattern in enumerate(inlinemathpatterns):
            pattern.handleMatch = handle_match_inline
            md.inlinePatterns.register('math-inline-%d' % i, pattern, PRIORITY_LT_ESCAPE)  # '<escape')
        for i, pattern in enumerate(mathpatterns):
            pattern.handleMatch = handle_match
            md.inlinePatterns.register('math-%d' % i, pattern, PRIORITY_LT_ESCAPE)   # '<escape')


def makeExtension(*args, **kwargs):
    return MathExtension(*args, **kwargs)
