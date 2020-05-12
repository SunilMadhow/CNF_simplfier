from grammar_brain import *
import sys
# string = read_input()
# string = sys.stdin.readlines()
string = input()
# print(string)
# string = sys.stdin.read()
# string = "3\nS aT54321b\nT54321 x\nT54321 _"
if string != "" and string != "0":
	grammar = parse(string)
	# print(grammar)
	g_prime = remove_lambda(grammar)
	print_grammar_mentor(g_prime)
