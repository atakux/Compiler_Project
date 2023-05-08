import errors
from settingUp import *
from create_table import *
from check_arithmetic import *


def check_grammar(parsing_table, text):
	""" Check grammar of a given text using a given parsing table """

	# initialize stack, counter for parsing, reserved_words, digits, and letters
	stack = []
	i = 0
	reserved_words = [
		'program', 'var', 'begin', 'end.', 'display', 'integer', '"value=",'
	]
	digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
	letters = ['p', 'q', 'r', 's']

	# prepare text for parsing, call all settingUp functions except for file based ones
	# get variable names, inputted reserved words, undefined variables, as well as the input text
	variable_names = get_variable_names(text)
	inputted_rw = get_inputted_reserved_words(text, letters, variable_names)
	undefined_variables = get_undefined_vars(text, variable_names, inputted_rw,
																					 reserved_words, digits, letters)
	input_text = init_text(text, inputted_rw, reserved_words, digits, letters)

	# if there are undefined variables in the text, raise an error
	if undefined_variables:
		raise errors.MissingArg('', 0, '', undefined_variables)

	# begin tracing
	stack.append('P')  # push P

	print(f"current stack: {stack}")
	current = stack.pop()  # pop P

	# parse thru entire input_text
	while i < len(input_text):
		print(f"\nreading {input_text[i]}")
		print(f"just popped {current}")

		# state P
		if current == 'P':
			# case: [row P, col program I val H begin G]
			if input_text[i] == reserved_words[0]:
				for j in range(len(parsing_table[0][25].split()) - 1, -1, -1):
					stack.append(parsing_table[0][25].split()[j])

				print(f"current stack: {stack}")
				current = stack.pop()  # pop program

			else:
				raise errors.MissingArg('program', i, inputted_rw[0])

		# state I
		elif current == 'I':
			# case: [row I, col p, q, r, s]
			if input_text[i] in letters:
				stack.append(parsing_table[1][21].split()[1])  # push J
				stack.append(parsing_table[1][21].split()[0])  # push L

				print(f"current stack: {stack}")
				current = stack.pop()  # pop L
			else:
				# identifier started with a number
				if input_text[i].isdigit():
					print("The start of an identifier cannot be numerical.")
				elif input_text[i] in '[@_!#$%^&*()<>?/\|}{~:]':
					print(
						"The start of an identifier cannot contain special characters.")
				elif input_text[i] == ';':
					raise errors.MissingArg('', i)
				return False

		# state J
		elif current == 'J':
			# case: [row J, col p, q, r, s]
			if input_text[i] in letters:
				stack.append(parsing_table[2][21].split()[1])  # push J
				stack.append(parsing_table[2][21].split()[0])  # push L

				print(f"current stack: {stack}")
				current = stack.pop()  # pop L

			# case: [row J, col ; : , ) = * /]
			elif input_text[i] in '; : , ) = + - * /':
				stack.append(parsing_table[2][0].split()[0])  # push lambda

				print(f"current stack: {stack}")
				current = stack.pop()  # pop lambda

			# case: [row J, col 0-9]
			elif input_text[i] in digits:
				stack.append(parsing_table[2][11].split()[1])  # push J
				stack.append(parsing_table[2][11].split()[0])  # push D

				print(f"current stack: {stack}")
				current = stack.pop()  # pop D

			else:
				if input_text[i] not in letters or list(
						input_text[i])[0] not in digits:
					if input_text[i] == 'var':
						raise errors.MissingArg(';', i)
					elif input_text[i] == 'integer':
						raise errors.MissingArg(':', i)
					elif list(input_text[i - 1])[0] in letters or list(
							input_text[i - 1])[0] in digits:
						if input_text[i] not in '+ -':
							raise errors.MissingArg('=', i)
				return False

		# state H
		elif current == 'H':
			# case: [row H, col p, q, r, s]
			if input_text[i] in letters:
				stack.append(parsing_table[3][21].split()[3])  # push ;
				stack.append(parsing_table[3][21].split()[2])  # push Y
				stack.append(parsing_table[3][21].split()[1])  # push :
				stack.append(parsing_table[3][21].split()[0])  # push C

				print(f"current stack: {stack}")
				current = stack.pop()  # pop C

			else:
				if input_text[i] == 'integer':
					raise errors.MissingArg(':', i)
				else:
					print("Variable names must begin with an alphabetical character.")
				return False

		# state C
		elif current == 'C':
			# case: [row C, col p, q, r, s]
			if input_text[i] in letters:
				stack.append(parsing_table[4][21].split()[1])  # push K
				stack.append(parsing_table[4][21].split()[0])  # push I

				print(f"current stack: {stack}")
				current = stack.pop()  # pop I

			else:
				if input_text[i] == ' ':
					raise errors.MissingArg('', i)
				else:
					print("Variable names must begin with an alphabetical character.")
				return False

		# state K
		elif current == 'K':
			# case: [row K, col :]
			if input_text[i] == ':':
				stack.append(parsing_table[5][1].split()[0])  # push lambda

				print(f"current stack: {stack}")
				current = stack.pop()  # pop lambda

			elif input_text[i] == ',':
				stack.append(parsing_table[5][2].split()[1])  # push K
				stack.append(parsing_table[5][2].split()[0])  # push ,

				print(f"current stack: {stack}")
				current = stack.pop()  # pop ,

			# case: [row K, col p, q, r, s]
			elif input_text[i] in letters:
				stack.append(parsing_table[5][21].split()[1])  # push K
				stack.append(parsing_table[5][21].split()[0])  # push I

				print(f"current stack: {stack}")
				current = stack.pop()  # pop I

			else:
				raise errors.MissingArg(',', i)

		# state Y
		elif current == 'Y':
			# case: [row Y, col integer]
			if input_text[i] == 'integer':
				stack.append(parsing_table[6][29].split()[0])  # push integer

				print(f"current stack: {stack}")
				current = stack.pop()  # pop integer

			else:
				raise errors.MissingArg('integer', i, inputted_rw[2])

		# state G
		elif current == 'G':
			# case: [row G, col p, q, r, s]
			if input_text[i] in letters:
				stack.append(parsing_table[7][21].split()[1])  # push O
				stack.append(parsing_table[7][21].split()[0])  # push S

				print(f"current stack: {stack}")
				current = stack.pop()  # pop S

			elif input_text[i] == 'display':
				stack.append(parsing_table[7][30].split()[0])  # push O
				stack.append(parsing_table[7][30].split()[0])  # push S

				print(f"current stack: {stack}")
				current = stack.pop()  # pop S

			else:
				if input_text[i] not in letters:
					raise errors.MissingArg('display', i, inputted_rw[4])
				return False

		# state O
		elif current == 'O':
			# case: [row O, col p, q, r, s]
			if input_text[i] in letters:
				stack.append(parsing_table[8][21].split()[0])  # push lambda

				print(f"current stack: {stack}")
				current = stack.pop()  # pop lambda

			elif input_text[i] == 'display':
				stack.append(parsing_table[8][30].split()[0])  # push lambda

				print(f"current stack: {stack}")
				current = stack.pop()  # pop lambda

			elif input_text[i] == 'end.':
				stack.append(parsing_table[8][28].split()[0])  # push lambda

				print(f"current stack: {stack}")
				current = stack.pop()  # pop lambda

			else:

				if input_text[i] not in letters:
					if input_text[i] != 'display':
						raise errors.MissingArg('end.', i, inputted_rw[5])
					else:
						raise errors.MissingArg('display', i, inputted_rw[4])

		# state S
		elif current == 'S':
			# case: [row S, col p, q, r, s]
			if input_text[i] in letters:
				stack.append(parsing_table[9][21].split()[1])  # push S
				stack.append(parsing_table[9][21].split()[0])  # push A

				print(f"current stack: {stack}")
				current = stack.pop()  # pop A

			elif input_text[i] == 'display':
				stack.append(parsing_table[9][30].split()[1])  # push S
				stack.append(parsing_table[9][30].split()[0])  # push W

				print(f"current stack: {stack}")
				current = stack.pop()  # pop display

			elif input_text[i] == 'end.':
				stack.append(parsing_table[8][28].split()[0])  # push lambda

				print(f"current stack: {stack}")
				current = stack.pop()  # pop lambda

			else:
				if input_text[i] == 'end':
					raise errors.MissingArg('.', 'the end')
				elif input_text[i].startswith('e'):
					raise errors.MissingArg('end.', i, inputted_rw[6])
				elif input_text[i].startswith('d'):
					raise errors.MissingArg('display', i, inputted_rw[4])
				elif input_text[i] == '(':
					raise errors.MissingArg('display', i, inputted_rw[4])
				return False

		# state W
		elif current == 'W':
			# case: [row W, col display]
			if input_text[i] == 'display':
				stack.append(parsing_table[10][30].split()[4])  # push ;
				stack.append(parsing_table[10][30].split()[3])  # push )
				stack.append(parsing_table[10][30].split()[2])  # push B
				stack.append(parsing_table[10][30].split()[1])  # push (
				stack.append(parsing_table[10][30].split()[0])  # push display

				print(f"current stack: {stack}")
				current = stack.pop()  # pop display
			else:
				raise errors.MissingArg('display', i, inputted_rw[4])

		# state B
		elif current == 'B':
			# case: [row B, col "value="]
			if input_text[i] == '"value=",':
				stack.append(parsing_table[11][5].split()[2])  # push I
				stack.append(''.join(
					parsing_table[11][5].split()[0:2]))  # push "value=",

				print(f"current stack: {stack}")
				current = stack.pop()  # pop "value=",

			# case: [row B, col p q r s]
			elif input_text[i] in letters:
				stack.append(parsing_table[11][21].split()[0])  # push I

				print(f"current stack: {stack}")
				current = stack.pop()  # pop I

			else:
				return False

		# state A
		elif current == 'A':
			# case: [row A, col p q r s]
			if input_text[i] in letters:
				stack.append(parsing_table[12][21].split()[3])  # push ;
				stack.append(parsing_table[12][21].split()[2])  # push E
				stack.append(parsing_table[12][21].split()[1])  # push =
				stack.append(parsing_table[12][21].split()[0])  # push I

				print(f"current stack: {stack}")
				current = stack.pop()  # pop I

			else:
				raise errors.MissingArg('', i)

		# state E
		elif current == 'E':
			# case: [row E, col p, q, r, s]
			if input_text[i] in letters:
				stack.append(parsing_table[13][21].split()[1])  # push Q
				stack.append(parsing_table[13][21].split()[0])  # push T

				print(f"current stack: {stack}")
				current = stack.pop()  # pop T

			# case: [row E, col + - (]
			elif input_text[i] in '+ - (':
				print(parsing_table[13][3].split())
				stack.append(parsing_table[13][3].split()[1])  # push Q
				stack.append(parsing_table[13][3].split()[0])  # push T

				print(f"current stack: {stack}")
				current = stack.pop()  # pop T

			# case: [row E, col 0-9]
			elif input_text[i] in digits:
				stack.append(parsing_table[13][11].split()[1])  # push Q
				stack.append(parsing_table[13][11].split()[0])  # push T

				print(f"current stack: {stack}")
				current = stack.pop()  # pop T

			else:
				raise errors.MissingArg('(', i)

		# state Q
		elif current == 'Q':
			# case: [row Q, col ;]
			if input_text[i] == ';':
				stack.append(parsing_table[14][0].split()[0])  # push lambda

				print(f"current stack: {stack}")
				current = stack.pop()  # pop lambda

			# case: [row Q, col )]
			elif input_text[i] == ')':
				stack.append(parsing_table[14][4].split()[0])  # push lambda

				print(f"current stack: {stack}")
				current = stack.pop()  # pop lambda

			# case: [row Q, col +]
			elif input_text[i] == '+':
				stack.append(parsing_table[14][7].split()[2])  # push Q
				stack.append(parsing_table[14][7].split()[1])  # push T
				stack.append(parsing_table[14][7].split()[0])  # push +

				print(f"current stack: {stack}")
				current = stack.pop()  # pop +

			# case: [row Q, col -]
			elif input_text[i] == '-':
				stack.append(parsing_table[14][8].split()[2])  # push Q
				stack.append(parsing_table[14][8].split()[1])  # push T
				stack.append(parsing_table[14][8].split()[0])  # push -

				print(f"current stack: {stack}")
				current = stack.pop()  # pop -

			else:
				return False

		# state T
		elif current == 'T':
			# case: [row T, col p, q, r, s]
			if input_text[i] in letters:
				stack.append(parsing_table[15][21].split()[1])  # push R
				stack.append(parsing_table[15][21].split()[0])  # push F

				print(f"current stack: {stack}")
				current = stack.pop()  # pop F

			# case: [row T, col + - (]
			elif input_text[i] in '+ - (':
				stack.append(parsing_table[15][3].split()[1])  # push R
				stack.append(parsing_table[15][3].split()[0])  # push F

				print(f"current stack: {stack}")
				current = stack.pop()  # pop F

			# case: [row T, col 0-9]
			elif input_text[i] in digits:
				stack.append(parsing_table[15][11].split()[1])  # push R
				stack.append(parsing_table[15][11].split()[0])  # push F

				print(f"current stack: {stack}")
				current = stack.pop()  # pop F

			else:
				return False

		# state R
		elif current == 'R':
			# case: [row R, col ;]
			if input_text[i] == ';':
				stack.append(parsing_table[16][0].split()[0])  # push lambda

				print(f"current stack: {stack}")
				current = stack.pop()  # pop lambda

			# case: [row R, col )]
			elif input_text[i] == ')':
				stack.append(parsing_table[16][4].split()[0])  # push lambda

				print(f"current stack: {stack}")
				current = stack.pop()  # pop lambda

			# case: [row R, col +]
			elif input_text[i] == '+':
				stack.append(parsing_table[16][7].split()[0])  # push lambda

				print(f"current stack: {stack}")
				current = stack.pop()  # pop lambda

			# case: [row R, col -]
			elif input_text[i] == '-':
				stack.append(parsing_table[16][8].split()[0])  # push lambda

				print(f"current stack: {stack}")
				current = stack.pop()  # pop lambda

			# case: [row R, col *]
			elif input_text[i] == '*':
				stack.append(parsing_table[16][9].split()[2])  # push R
				stack.append(parsing_table[16][9].split()[1])  # push F
				stack.append(parsing_table[16][9].split()[0])  # push *

				print(f"current stack: {stack}")
				current = stack.pop()  # pop *

			# case: [row R, col /]
			elif input_text[i] == '/':
				stack.append(parsing_table[16][10].split()[2])  # push R
				stack.append(parsing_table[16][10].split()[1])  # push F
				stack.append(parsing_table[16][10].split()[0])  # push /

				print(f"current stack: {stack}")
				current = stack.pop()  # pop /

			else:
				return False

		# state F
		elif current == 'F':
			# case: [row F, col (]
			if input_text[i] == '(':
				stack.append(parsing_table[17][3].split()[2])  # push )
				stack.append(parsing_table[17][3].split()[1])  # push E
				stack.append(parsing_table[17][3].split()[0])  # push (

				print(f"current stack: {stack}")
				current = stack.pop()  # pop (

			# case: [row F, col + -]
			elif input_text[i] in '+ -':
				stack.append(parsing_table[17][7].split()[0])  # push N

				print(f"current stack: {stack}")
				current = stack.pop()  # pop N

			# case: [row F, col 0-9]
			elif input_text[i] in digits:
				stack.append(parsing_table[17][11].split()[0])  # push N

				print(f"current stack: {stack}")
				current = stack.pop()  # pop N

			# case: [row F, col p q r s]
			elif input_text[i] in letters:
				stack.append(parsing_table[17][21].split()[0])  # push I

				print(f"current stack: {stack}")
				current = stack.pop()  # pop I

			else:
				raise errors.MissingArg('(', i)

		# state N
		elif current == 'N':
			# case: [row N, col + -]
			if input_text[i] in '+ -':
				stack.append(parsing_table[18][7].split()[1])  # push M
				stack.append(parsing_table[18][7].split()[0])  # push U

				print(f"current stack: {stack}")
				current = stack.pop()  # pop U

			# case: [row N, col 0-9]
			elif input_text[i] in digits:
				stack.append(parsing_table[18][11].split()[0])  # push M

				print(f"current stack: {stack}")
				current = stack.pop()  # pop M

			else:
				return False

		# state M
		elif current == 'M':
			# case: [row M, col ;]
			if input_text[i] == ';':
				stack.append(parsing_table[19][0].split()[0])  # push lambda

				print(f"current stack: {stack}")
				current = stack.pop()  # pop lambda

			# case: [row M, col )]
			elif input_text[i] == ')':
				stack.append(parsing_table[19][4].split()[0])  # push lambda

				print(f"current stack: {stack}")
				current = stack.pop()  # pop lambda

			# case: [row M, col +]
			elif input_text[i] == '+':
				stack.append(parsing_table[19][7].split()[0])  # push lambda

				print(f"current stack: {stack}")
				current = stack.pop()  # pop lambda

			# case: [row M, col -]
			elif input_text[i] == '-':
				stack.append(parsing_table[19][8].split()[0])  # push lambda

				print(f"current stack: {stack}")
				current = stack.pop()  # pop lambda

			# case: [row M, col *]
			elif input_text[i] == '*':
				stack.append(parsing_table[19][9].split()[0])  # push lambda

				print(f"current stack: {stack}")
				current = stack.pop()  # pop lambda

			# case: [row M, col /]
			elif input_text[i] == '/':
				stack.append(parsing_table[19][10].split()[0])  # push lambda

				print(f"current stack: {stack}")
				current = stack.pop()  # pop lambda

			# case: [row M, col 0-9]
			elif input_text[i] in digits:
				stack.append(parsing_table[19][11].split()[1])  # push M
				stack.append(parsing_table[19][11].split()[0])  # push D

				print(f"current stack: {stack}")
				current = stack.pop()  # pop D

			else:
				if list(input_text[i - 1])[0] in digits and list(
						input_text[i - 1])[0] in letters:
					raise errors.MissingArg(';', i)
				elif input_text[i] == 'display':
					raise errors.MissingArg(';', i)
				return False

		# state U
		elif current == 'U':
			# case: [row U, col +]
			if input_text[i] == '+':
				stack.append(parsing_table[20][7].split()[0])  # push +

				print(f"current stack: {stack}")
				current = stack.pop()  # pop +

			# case: [row U, col -]
			elif input_text[i] == '-':
				stack.append(parsing_table[20][8].split()[0])  # push -

				print(f"current stack: {stack}")
				current = stack.pop()  # pop -

			# case: [row U, col 0-9]
			elif input_text[i] in digits:
				stack.append(parsing_table[20][11].split()[0])  # push lambda

				print(f"current stack: {stack}")
				current = stack.pop()  # pop lambda

			else:
				return False

		# state D
		elif current == 'D':
			# case: [row D, col 0-9]
			if input_text[i] in digits:
				# check which digit is being read
				for digit in digits:
					if digit == input_text[i]:
						stack.append(parsing_table[21][int(digit) + 11])  # push digit
				print(f"current stack: {stack}")
				current = stack.pop()  # pop digit

			else:
				return False

		# state L
		elif current == 'L':
			if input_text[i] == 'p':
				stack.append(parsing_table[22][21].split()[0])  # push p
				print(f"current stack: {stack}")
				current = stack.pop()

			elif input_text[i] == 'q':
				stack.append(parsing_table[22][22].split()[0])  # push q
				print(f"current stack: {stack}")
				current = stack.pop()

			elif input_text[i] == 'r':
				stack.append(parsing_table[22][23].split()[0])  # push r
				print(f"current stack: {stack}")
				current = stack.pop()

			elif input_text[i] == 's':
				stack.append(parsing_table[22][24].split()[0])  # push s
				print(f"current stack: {stack}")
				current = stack.pop()

			else:
				if input_text[i + 1] in reserved_words:
					raise errors.MissingArg(';', i)
				return False

		# what was popped is what we are reading
		elif str(current) == input_text[i]:
			print(f"matched {input_text[i]}")
			print(f"current stack: {stack}")

			# if we are at the end of the file and there were no errors,
			# check arithmetic to prepare for translation to python
			if current == input_text[i] and input_text[i] == 'end.':
				# check for any missing operators, to be able to convert txt to py
				expressions = get_expressions(input_text)
				res = has_operators(expressions, variable_names)

				# if the arithmetic is good, we can conclude check_grammar and return True
				if res:
					return True
				# otherwise, invalid arithmetic, return False
				else:
					raise errors.InvalidExpression()

			# if we arent at the end of the file, keep popping and reading
			else:
				current = stack.pop()  # pop next item
				i += 1

		# if the current item that was popped is lambda, pop again
		elif current == 'lamb':
			print(f"current stack: {stack}")
			current = stack.pop()

		# double check that no errors were missed if we arent in any current state
		else:
			if current == 'var':
				raise errors.MissingArg('var', i, inputted_rw[1])
			elif current == 'integer':
				raise errors.MissingArg('integer', i, inputted_rw[2])
			elif current == 'begin':
				raise errors.MissingArg('begin', i, inputted_rw[3])
			elif current == 'display':
				raise errors.MissingArg('display', i, inputted_rw[4])
			elif current == 'end.':
				raise errors.MissingArg('end.', i, inputted_rw[5])
			elif current == '=':
				raise errors.MissingArg('=', i)
			elif current == 'end':
				raise errors.MissingArg('.', i)
			elif current == ';':
				raise errors.MissingArg(';', i)
			elif current == ':':
				raise errors.MissingArg(':', i)
			elif current == ')':
				raise errors.MissingArg(')', i)
			elif current == '(':
				raise errors.MissingArg('(', i)
			elif current == ',':
				raise errors.MissingArg(',', i)

			return False
