NEARLEYC=node_modules/.bin/nearleyc

all: cm99109-grammar.js nearley.js

nearley.js cm99109-grammar.js: ../cm99109.ne
	npm install nearley
	${NEARLEYC} $< > $@
	cp node_modules/nearley/lib/nearley.js .
