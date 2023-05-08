import sys

def toPython():
	""" Translate the grammar into Python3. """

	# open file for conversion
	with open("finalp2.txt", "r") as file:
		# returns a list of lines
		content = file.readlines()
		
	#==================================================
	# Recognize reserved words and set off flags when found
	# Namely, (program, var, begin, end) for error checking
	program_flag = False
	var_flag = False
	begin_flag = False
	empty_flag = True
	
	# Iterate through each line
	for w in range(len(content)):
		
		# Check structure of function with flags
		# two allowed scenarios:
		# 1.) program -> var [var data] -> begin [begin data] -> end
		# 2.) program -> begin [begin data] -> end
		
		# 'begin' section must not be empty 

		# Flags should not be set off if reserved word is used in quotation marks (ie. ("this program is valid"))
		
		# Assume "real" reserved words cannot be used in same line as quotations, since they are only allowed in <stat> -> <write> grammar
		if '"' in content[w]:
			pass
		# Set off flags to distiguish sections
		else:
			# Start of function declaration
			if "program" in content[w]:
				program_flag = True

			# Start of <dec-list>
			if "var" in content[w]:
				var_flag = True
				if program_flag == False:
					print("error: missing identifier 'program'")
					sys.exit()

			# Start of <stat-list>
			if "begin" in content[w]:
				begin_flag = True
				var_flag = False
				if program_flag == False:
					print("error: missing identifier 'program'")
					sys.exit()

			# End of function declaration
			if "end" in content[w]:
				if program_flag == False:
					print("error: missing identifier 'program'")
					sys.exit()
				if begin_flag == False:
					print("error: missing identifier 'begin'")
					sys.exit()
				if empty_flag == True:
					print("error: empty body is not allowed")
					sys.exit()
					
				# set all flags to default if 'end' is found
				program_flag = False
				var_flag = False
				begin_flag = False
				empty_flag = True

		# if line is in function declaration, tab the line
		if program_flag == True:
			content[w] = "\t" + content[w]
			
		# Now, you can split each line into words
		# Identify the object, extract the name, insert into python syntax
		
		# convert line string into array of words
		words = content[w].split()

		# iterate through list of words
		for i in range(len(words)):
			
			# find function name
			if words[i] == "program":
				global function_name
				function_name = words[i+1]
				#remove semicolon
				function_name = function_name.replace(';', '')
				# insert into python syntax
				content[w] = "def %s():\n" % function_name

			# identifier "var" structure does not exist in python
			# remove var from program
			if words[i] == "var":
				content[w] = ''

			# if in declaration section 'var', assume 'integer' means variable declaration
			# variable declaration does not exist in python
			# remove variable declaration
			if var_flag == True:
				if "integer" in content[w]:
					content[w] = ''

			# 'begin' has no python3 equivalent
			# remove begin
			if "begin" in content[w]:
				content[w] = ''

			# three scenarios: integer value, math. and display
			# semicolons not needed in any line in python
			if begin_flag == True:
				content[w] = content[w].replace(';', '')

				# infer if 'begin' section is empty by checking for <stat-list> indicators
				if "display" in content[w] or "=" in content[w]:
					empty_flag = False

				# Replace the syntax 'display' with python syntax 'print'
				if "display" in content[w]:
					content[w] = content[w].replace('display', 'print')

			# Give error if <stat-list> or <dec-list> found before 'begin'
			elif begin_flag == False:
				if "display" in content[w] or "=" in content[w]:
					print("error: cannot have statements before identifer 'begin'")
					sys.exit()

			# end has no python3 equivalent, remove end
			if "end" in content[w]:
				content[w] = ''
		
		#--------------------------------------------------------------
	
	# ensure enough 'end' occurances to match 'program' occurances
	if program_flag == True:
		print("error: missing identifier 'end'")
		sys.exit()

#==================================================
	# If there are no errors, write to python file
	with open("outputPython.py", "w") as out_file:
		# replace "content" with your new list
		for item in content:
			out_file.write(item)


toPython()

def pull_function():
	return(function_name)
	
