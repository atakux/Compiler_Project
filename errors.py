class MissingArg(SyntaxError):
	""" Class for any Missing Arguments in the grammar """

	def __init__(self, missing_arg='', position=0, misspelled='', var_name=''):
		""" When errors.MissingArg() is called do the following depending on arguments passed """

		# initialize reserved words and operators
		reserved_words = ['program', 'var', 'begin', 'end.', 'integer', 'display']
		operators = [':', ';', ',', '.', '=', '(', ')']

		# missing an operator
		if missing_arg in operators:
			print(
				f"\nSyntaxError: {missing_arg} is missing at position {position} of your file."
			)
			exit()

		# either missing or misspelled a reserved word
		elif missing_arg in reserved_words:
			# if not misspelled, most likely missing:
			if misspelled == '':
				print(
					f"\nSyntaxError: {missing_arg} is expected at position {position} of your file."
				)

			elif misspelled == missing_arg:
				print(
					f"\nSyntaxError: {missing_arg} is expected at position {position} of your file."
				)

			# if misspelled suggest correct spelling
			else:
				print(
					f"\nThere is no attribute '{misspelled}'. Did you mean: '{missing_arg}' ?"
				)
			exit()

		# undefined variable
		else:
			for v in var_name:
				print(f"\nunknown identifier. variable '{v}' is not defined.")
			exit()


class InvalidExpression(ValueError):
	""" Class to for invalid expressions """

	def __init__(self):
		""" When errors.InvalidExpression is passed do the following """

		print(
			"\nInvalidExpression: Arithmetic is invalid. Perhaps you are missing an operator."
		)
		exit()
