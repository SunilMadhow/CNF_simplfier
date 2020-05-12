from grammar_brain import *

string = read_input()
if string != "" and string != "0":
	grammar = parse(string)
	# print(grammar)
	g_prime = remove_lambda(grammar)
	g_prime = remove_unit_productions(g_prime)
	g_prime = cnf(g_prime)
	print_grammar_mentor(g_prime)