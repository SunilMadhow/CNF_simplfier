import itertools

def parse(stdin):
	array = stdin.split("\n")
	return [tuple(array[i].split(" ")) for i in range(0, len(array))]

def print_grammar(grammar):
	for i in range(0, len(grammar)):
		print("%s %s" % (grammar[i][0], grammar[i][1]))

grammar = parse("S ABCd\nA BC\nB bB\nB _\nC _\nC cC")
print(grammar)
print_grammar(grammar)
print()

def find_nullable(grammar):
	array = [grammar[i][0] for i in range(0, len(grammar)) if grammar[i][1] == "_"]
	i = 0
	while i < len(grammar):
		if grammar[i][0] in array: 
			i = i + 1
			continue
		all_nullable = True
		for j in grammar[i][1]:
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
	print(nullable)
	# g_prime.append(grammar[0])
	for i in range(0, len(grammar)):
		nullable_chars = []
		string = grammar[i][1]
		for j in range(0, len(string)):
			if string[j] in nullable:
				nullable_chars.append(j)

		all_combos = []
		for r in range(0, len(nullable_chars)+1):
			 all_combos += list(itertools.combinations(nullable_chars, r))
		print(all_combos)
		for combo in all_combos:
			print(combo)
			newrule = "".join([string[i] for i in range(0, len(string)) if i not in combo or string[i].islower()])
			g_prime.append((grammar[i][0], newrule))
	
	g_prime = [i for i in g_prime if i[1] != "" and i[1] != "_"]

	print_grammar(g_prime)

remove_lambda(grammar)