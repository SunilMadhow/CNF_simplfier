import itertools
import sys

def parse(stdin):
	array = stdin.split("\n")
	grammar = []
	for i in array:
		s = []
		production = i.split(" ")
		# print(production)
		variable = ""
		sent = production[1]
		for i in range(0, len(sent)):
			if sent[i].isupper():
				variable = variable + sent[i]
				if len(sent) == i + 1:
					s.append(variable)
					variable = ""
				elif not sent[i+1].isdigit():
					s.append(variable)
					variable = ""
			elif variable != "" and sent[i].isdigit():
				variable  = variable + sent[i]
				if not sent[i+1].isdigit():
					s.append(variable)
					variable = ""
			# elif variable != "" and sent[i].isdigit():
			# 	s.append(variable)
			# 	variable = ""
			elif sent[i].islower() or sent[i] == "_": 
				s.append(sent[i])
		grammar.append((production[0], s))


	return grammar
	# return [tuple(array[i].split(" ")) for i in range(0, len(array))]

def print_grammar(grammar):
	for i in range(0, len(grammar)):
		print("%s %s" % (grammar[i][0], "".join(grammar[i][1])))

lines = ""

line = input()
while line != "":
	lines += line
	line = input()
	if line != "":
		lines += '\n'


grammar = parse(lines)
print(grammar)
print_grammar(grammar)
print()

def find_nullable(grammar):
	array = [grammar[i][0] for i in range(0, len(grammar)) if grammar[i][1][0] == "_"]
	i = 0
	while i < len(grammar):
		if grammar[i][0] in array: 
			i = i + 1
			continue
		all_nullable = True
		for j in "".join(grammar[i][1]):
			if j not in array:
				all_nullable = False
				break
		if all_nullable: 
			array.append(grammar[i][0])
			i = -1
		i = i + 1
	return array


def remove_lambda(grammar):
	g_prime = []
	nullable = find_nullable(grammar)
	# print(nullable)
	# g_prime.append(grammar[0])
	for i in range(0, len(grammar)):
		nullable_chars = []
		string = "".join(grammar[i][1])
		for j in range(0, len(string)):
			if string[j] in nullable:
				nullable_chars.append(j)

		all_combos = []
		for r in range(0, len(nullable_chars)+1):
			 all_combos += list(itertools.combinations(nullable_chars, r))
		# print(all_combos)
		for combo in all_combos:
			# print(combo)
			newrule = [string[i] for i in range(0, len(string)) if i not in combo or string[i].islower()]
			g_prime.append((grammar[i][0], newrule))
	# print_grammar(g_prime)
	# for i in g_prime:
	# 	print(i)
	g_prime = [i for i in g_prime if len(i[1]) >= 1]
	return [i for i in g_prime if i[1][0] != "" and i[1][0] != "_"]

def variable_derivable(grammar, v):
	derivable = []
	for i in range(len(grammar)):
		n = grammar[i]
		if n[0] == v and n[1][0].isupper() and len(n[1]) == 1:
			derivable.append(n[1][0])
			i = 0
		elif (n[0] in derivable) and n[1][0].isupper() and len(n[1]) == 1 and n[1][0] != v:
			derivable.append(n[1][0])
			i = 0
	return derivable

#B C A B C p
def remove_unit_productions(grammar):	
	g_prime = grammar
	variables = {i[0] for i in grammar}	
	# print(variables)	
	dictionary = {}
	for v in variables:
		dictionary[v] = variable_derivable(grammar, v)
	# print(dictionary)
	for v in variables:
		for j in grammar:
			if (j[0] in dictionary[v]) and (any(i.islower() for i in "".join(j[1])) or len(j[1]) > 1):
				if (v, j[1]) not in g_prime:
					g_prime.append((v, j[1]))
					print("appending {}".format((v, j[1])))
	# print(g_prime)
	g_prime = [item for item in g_prime if len(item[1]) > 1 or item[1][0].islower()]
	return g_prime

def split_variable_string(production, grammar):
	# string = "".join(production[1])
	sentential = production[1]
	prev_prod = production[0]
	new_prods = []
	i = 0
	while i < len(sentential) - 2:
		prod = (prev_prod, ["V{}".format(len(grammar) + i), sentential[i * -1 - 1]])
		prev_prod = "V{}".format(len(grammar) + i)
		new_prods.append(prod)
		i  = i + 1

	new_prods.append(("V{}".format(len(grammar) + i -1), [sentential[0], sentential[1]]))
	return new_prods

def segregation(production):
	sentential = production[1]
	new_prods = []
	# print("production = {}".format(production))
	if len(sentential) > 1:
		for i in range(0, len(sentential)):
			print(sentential[i])
			if sentential[i].islower():
				production[1][i] = production[1][i].upper()
				new_prods.append((sentential[i], [sentential[i].lower()]))

	new_prods.append(production)
	
	# print(new_prods)
	# print("----")
	return new_prods


		
def cnf(grammar):
	# to_remove = []
	g_prime = []
	for production in grammar:
		if any(i.islower() for i in production[1]) and len(production[1]) > 1:
			for i in segregation(production):
				if i not in g_prime:
					g_prime.append(i)
			# to_remove.append(production)
		else:
			g_prime.append(production)
	grammar = g_prime
	# print_grammar(grammar)
	g_prime = []
	for production in grammar:
		if len(production[1]) > 2:
			g_prime += split_variable_string(production, g_prime)
			# to_remove.append(production)
		else: g_prime.append(production)
	grammar = g_prime
	# grammar = [i for i in grammar + to_remove if i in grammar and i not in to_remove]
	return grammar

g_prime = remove_lambda(grammar)
g_prime = remove_unit_productions(g_prime)
# print_grammar(g_prime)
g_prime = cnf(g_prime)
# print("------------")
# split_variable_string(("A", ["B", "C", "X", "Y", "Z", "B67"]))
print_grammar(g_prime)