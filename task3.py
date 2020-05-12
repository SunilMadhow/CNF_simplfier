from grammar_brain import *

string = read_input()
if string != "" and string != "0":
	grammar = parse(string)
	g_prime = remove_lambda(grammar)
	g_prime = remove_unit_productions(g_prime)
	g_prime = cnf(g_prime)
	print_grammar(g_prime)