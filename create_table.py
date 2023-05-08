from tabulate import tabulate


def initialize_parsing_table():
	""" Initialize already calculated parsing table """

	parsing_table = [[' ' for x in range(31)] for y in range(23)]

	# state P := <prog>
	# row P, col program
	parsing_table[0][25] = 'program I ; var H begin G end.'

	# state I := <identifier>
	# row I, cols p, q, r, s
	for i in range(21, 25):
		parsing_table[1][i] = 'L J'

	# state J from removing left-recursion
	# row J, cols ;, :, ,
	for i in range(0, 3):
		parsing_table[2][i] = 'lamb'
	# row J, col )
	parsing_table[2][4] = 'lamb'
	# row J, col =, +, -, *, /
	for i in range(6, 11):
		parsing_table[2][i] = 'lamb'
	# row J, cols 0-9
	for i in range(11, 21):
		parsing_table[2][i] = 'D J'
	# row J, cols p, q, r, s
	for i in range(21, 25):
		parsing_table[2][i] = 'L J'

	# state H := <dec-list>
	# row H, cols p, q, r, s
	for i in range(21, 25):
		parsing_table[3][i] = 'C : Y ;'

	# state C := <dec>
	# row C, cols p, q, r, s
	for i in range(21, 25):
		parsing_table[4][i] = 'I K'

	# state K from removing left-recursion
	# row K, col :
	parsing_table[5][1] = 'lamb'
	# row K, col ,
	parsing_table[5][2] = ', K'
	# row K, cols p, q, r, s
	for i in range(21, 25):
		parsing_table[5][i] = 'I K'

	# state Y := <type>
	# row Y, col integer
	parsing_table[6][29] = 'integer'

	# state G := <stat-list>
	# row G, cols p, q, r, s
	for i in range(21, 25):
		parsing_table[7][i] = 'S O'
	# row G, col display
	parsing_table[7][30] = 'S O'

	# state O from removing left-recursion
	# row O, cols p, q, r, s
	for i in range(21, 25):
		parsing_table[8][i] = 'lamb'
	# row O, col end.
	parsing_table[8][28] = 'lamb'
	# row O, col display
	parsing_table[8][30] = 'lamb'

	# state S := <stat>
	# row S, col p, q, r, s
	for i in range(21, 25):
		parsing_table[9][i] = 'A S'
	# row S, col display
	parsing_table[9][30] = 'W S'

	# state W := <write>
	# row W, col display
	parsing_table[10][30] = 'display ( B ) ;'

	# state B from removing left-recursion
	# row B, col "value="
	parsing_table[11][5] = '"value=" , I'
	# row B, col p, q, r, s
	for i in range(21, 25):
		parsing_table[11][i] = 'I'

	# state A := <assign>
	# row A, col p, q, r, s
	for i in range(21, 25):
		parsing_table[12][i] = 'I = E ;'

	# state E := <expr>
	# row E, col )
	parsing_table[13][3] = 'T Q'
	# row E, col +
	parsing_table[13][7] = '+ T Q'
	# row E, col -
	parsing_table[13][8] = '- T Q'
	# row E, col 0-9, p, q, r, s
	for i in range(11, 25):
		parsing_table[13][i] = 'T Q'

	# state Q from removing left-recursion
	# row Q, col ;
	parsing_table[14][0] = 'lamb'
	# row Q, col )
	parsing_table[14][4] = 'lamb'
	# row Q, col +
	parsing_table[14][7] = '+ T Q'
	# row Q, col -
	parsing_table[14][8] = '- T Q'

	# state T := <term>
	# row T, col (
	parsing_table[15][3] = 'F R'
	# row T, col *
	parsing_table[15][9] = '* F R'
	# row T, col /
	parsing_table[15][10] = '/ F R'
	# row T, col 0-9, p, q, r, s
	for i in range(11, 25):
		parsing_table[15][i] = 'F R'

	# state R from removing left-recursion
	# row R, col ;
	parsing_table[16][0] = 'lamb'
	# row R, col )
	parsing_table[16][4] = 'lamb'
	# row R, col +
	parsing_table[16][7] = 'lamb'
	# row R, col -
	parsing_table[16][8] = 'lamb'
	# row R, col *
	parsing_table[16][9] = '* F R'
	# row R, col /
	parsing_table[16][10] = '/ F R'

	# state F := <factor>
	# row F, col (
	parsing_table[17][3] = '( E )'
	# row F, col +
	parsing_table[17][7] = 'N'
	# row F, col -
	parsing_table[17][8] = 'N'
	# row F, cols 0-9
	for i in range(11, 21):
		parsing_table[17][i] = 'N'
	# row F, cols p, q, r, s
	for i in range(21, 25):
		parsing_table[17][i] = 'I'

	# state N := <number>
	# row N, cols +, -
	for i in range(7, 9):
		parsing_table[18][i] = 'U M'
	# row N, cols 0-9
	for i in range(11, 21):
		parsing_table[18][i] = 'M'

	# state M from removing left-recursion
	# row M, col ;
	parsing_table[19][0] = 'lamb'
	# row M, col )
	parsing_table[19][4] = 'lamb'
	# row M, cols +, -, *, /
	for i in range(7, 11):
		parsing_table[19][i] = 'lamb'
	# row M, cols 0-9
	for i in range(11, 21):
		parsing_table[19][i] = 'D M'

	# state U := <sign>
	# row U, col +
	parsing_table[20][7] = '+'
	# row U, col -
	parsing_table[20][8] = '-'
	# row U, cols 0-9
	for i in range(11, 21):
		parsing_table[20][i] = 'lamb'

	# state D := <digit>
	# row D, cols 0-9
	for i in range(11, 21):
		digit = i - 11
		parsing_table[21][i] = digit

	# state L := <letter>
	# row L, col p
	parsing_table[22][21] = 'p'
	# row L, col q
	parsing_table[22][22] = 'q'
	# row L, col p
	parsing_table[22][23] = 'r'
	# row L, col p
	parsing_table[22][24] = 's'

	# saving a nice looking version of the table

	nonterminals = [
		'P', 'I', 'J', 'H', 'C', 'K', 'Y', 'G', 'O', 'S', 'W', 'B', 'A', 'E', 'Q',
		'T', 'R', 'F', 'N', 'M', 'U', 'D', 'L'
	]

	pretty_table = tabulate(parsing_table,
													headers=[
														';', ':', ',', '(', ')', '"value="', '=', '+', '-',
														'*', '/', '0', '1', '2', '3', '4', '5', '6', '7',
														'8', '9', 'p', 'q', 'r', 's', 'program', 'var',
														'begin', 'end.', 'integer', 'display'
													],
													showindex=nonterminals,
													tablefmt="grid")
	# save to txt
	with open('parsing_table.txt', 'w') as f:
		f.write(pretty_table)

	# return parsing_table so we can use it to check grammar
	return parsing_table
