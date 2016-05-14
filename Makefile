.PHONY: program test

test: program example.os
	python osmium.py example.os

program: parser.py osmium.py

parser.py: osmium.ebnf
	grako osmium.ebnf >parser.py

