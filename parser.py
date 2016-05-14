#!/usr/bin/env python
# -*- coding: utf-8 -*-

# CAVEAT UTILITOR
#
# This file was automatically generated by Grako.
#
#    https://pypi.python.org/pypi/grako/
#
# Any changes you make to it will be overwritten the next time
# the file is generated.


from __future__ import print_function, division, absolute_import, unicode_literals

from grako.parsing import graken, Parser
from grako.util import re, RE_FLAGS  # noqa


__version__ = (2016, 3, 6, 3, 55, 12, 6)

__all__ = [
    'osmiumParser',
    'osmiumSemantics',
    'main'
]


class osmiumParser(Parser):
    def __init__(self,
                 whitespace=None,
                 nameguard=None,
                 comments_re='/\\*((?!\\*/).)*\\*/',
                 eol_comments_re=None,
                 ignorecase=None,
                 left_recursion=True,
                 **kwargs):
        super(osmiumParser, self).__init__(
            whitespace=whitespace,
            nameguard=nameguard,
            comments_re=comments_re,
            eol_comments_re=eol_comments_re,
            ignorecase=ignorecase,
            left_recursion=left_recursion,
            **kwargs
        )

    @graken()
    def _program_(self):

        def block0():
            self._definition_()
        self._closure(block0)
        self._check_eof()

    @graken()
    def _definition_(self):
        with self._choice():
            with self._option():
                self._token('(')
                self._cut()
                self._arglist_()
                self.ast['in_'] = self.last_node
                self._token(')')
                self._ident_()
                self.ast['op'] = self.last_node
                self._token('(')
                self._arglist_()
                self.ast['out'] = self.last_node
                self._token(')')
                self._body_()
                self.ast['body'] = self.last_node
            with self._option():
                self._token('compound')
                self._cut()
                self._ident_()
                self.ast['name'] = self.last_node
                self._compound_body_()
                self.ast['body'] = self.last_node
            self._error('no available options')

        self.ast._define(
            ['in_', 'op', 'out', 'body', 'name'],
            []
        )

    @graken()
    def _body_(self):
        self._token('{')

        def block0():
            self._rule_()
            self.ast.setlist('@', self.last_node)
        self._closure(block0)
        self._token('}')

    @graken()
    def _compound_body_(self):
        self._token('{')

        def block0():
            self._field_()
            self.ast.setlist('@', self.last_node)
        self._closure(block0)
        self._token('}')

    @graken()
    def _field_(self):
        self._ident_()
        self.ast['type'] = self.last_node
        self._ident_()
        self.ast['name'] = self.last_node
        with self._group():
            with self._choice():
                with self._option():
                    self._token('[]')
                    self.ast['array'] = self.last_node
                with self._option():
                    pass
                self._error('expecting one of: []')
        self._token(';')

        self.ast._define(
            ['type', 'name', 'array'],
            []
        )

    @graken()
    def _rule_(self):
        with self._choice():
            with self._option():
                self._token('(')
                self._cut()
                self._arglist_()
                self.ast['in_'] = self.last_node
                self._token(')')
                self._ident_()
                self.ast['op'] = self.last_node
                self._token('(')
                self._arglist_()
                self.ast['out'] = self.last_node
                self._token(')')
            with self._option():
                self._token('native')
                self._cut()
                self._token('{')
                self._snippet_list_()
                self.ast['snippets'] = self.last_node
                self._token('}')
            self._error('no available options')

        self.ast._define(
            ['in_', 'op', 'out', 'snippets'],
            []
        )

    @graken()
    def _snippet_list_(self):

        def block0():
            self._snippet_()
            self.ast.setlist('@', self.last_node)
        self._closure(block0)

    @graken()
    def _arglist_(self):

        def block0():
            self._ident_()
            self.ast.setlist('@', self.last_node)
        self._closure(block0)

    @graken()
    def _snippet_(self):
        with self._choice():
            with self._option():
                self._ident_()
                self.ast['loop'] = self.last_node
                self._token('{')
                self._snippet_list_()
                self.ast['body'] = self.last_node
                self._token('}')
            with self._option():
                self._pattern(r'"[^"]*"')
                self.ast['constant'] = self.last_node
            with self._option():
                self._ident_()
                self.ast['insert'] = self.last_node
            self._error('expecting one of: "[^"]*"')

        self.ast._define(
            ['loop', 'body', 'constant', 'insert'],
            []
        )

    @graken()
    def _ident_(self):
        self._pattern(r'[-_+*/~!:@#$%^&a-zA-Z0-9]+')


class osmiumSemantics(object):
    def program(self, ast):
        return ast

    def definition(self, ast):
        return ast

    def body(self, ast):
        return ast

    def compound_body(self, ast):
        return ast

    def field(self, ast):
        return ast

    def rule(self, ast):
        return ast

    def snippet_list(self, ast):
        return ast

    def arglist(self, ast):
        return ast

    def snippet(self, ast):
        return ast

    def ident(self, ast):
        return ast


def main(filename, startrule, trace=False, whitespace=None, nameguard=None):
    import json
    with open(filename) as f:
        text = f.read()
    parser = osmiumParser(parseinfo=False)
    ast = parser.parse(
        text,
        startrule,
        filename=filename,
        trace=trace,
        whitespace=whitespace,
        nameguard=nameguard)
    print('AST:')
    print(ast)
    print()
    print('JSON:')
    print(json.dumps(ast, indent=2))
    print()

if __name__ == '__main__':
    import argparse
    import string
    import sys

    class ListRules(argparse.Action):
        def __call__(self, parser, namespace, values, option_string):
            print('Rules:')
            for r in osmiumParser.rule_list():
                print(r)
            print()
            sys.exit(0)

    parser = argparse.ArgumentParser(description="Simple parser for osmium.")
    parser.add_argument('-l', '--list', action=ListRules, nargs=0,
                        help="list all rules and exit")
    parser.add_argument('-n', '--no-nameguard', action='store_true',
                        dest='no_nameguard',
                        help="disable the 'nameguard' feature")
    parser.add_argument('-t', '--trace', action='store_true',
                        help="output trace information")
    parser.add_argument('-w', '--whitespace', type=str, default=string.whitespace,
                        help="whitespace specification")
    parser.add_argument('file', metavar="FILE", help="the input file to parse")
    parser.add_argument('startrule', metavar="STARTRULE",
                        help="the start rule for parsing")
    args = parser.parse_args()

    main(
        args.file,
        args.startrule,
        trace=args.trace,
        whitespace=args.whitespace,
        nameguard=not args.no_nameguard
    )
