def has_operators(expression, expected_variables):
	""" Check if a given expression with expected variables is a valid mathematical expression """

	expr_str = '\n'.join(expression)

	with open('math.txt', 'w') as m:
		m.write(expr_str)

	code = compile(expr_str, 'math.py', "exec")

	try:
		exec(code)
		return True
	except:
		return False


def get_expressions(text):
	""" Get all expressions from a given string of text and separate them by white space """

	# initialize
	expressions = []
	stop_reading = False
	operators = ['+', '-', '*', '/', '=', '(', ')']

	# get all expressions in the text
	for word in text:

		# when word is begin, we can grab all expressions
		if word == 'begin':
			k = text.index(word)
			for w in range(k + 1, len(text)):

				# skip everything to do with display
				if 'display' in text[w]:
					stop_reading = True

				elif ';' in text[w]:
					stop_reading = False
					expressions.append(';')
				elif text[w] == 'end.':
					break

				# append everything else to the expressions list
				elif not stop_reading:
					expressions.append(text[w])

	# remove all semicolons from the expressions
	expressions = ''.join(expressions)
	expressions = expressions.split(';')

	# remove any extra spaces in the list
	while "" in expressions:
		expressions.remove("")

	# space out the expressions by operator
	spaced_exprs = []

	for expr in expressions:
		for op in operators:
			expr = expr.split(op)
			expr = f' {op} '.join(expr)
		spaced_exprs.append(expr)

	# return spaced out expressions
	return spaced_exprs
