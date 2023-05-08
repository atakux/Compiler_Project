import nltk

def set_up_file():
   """ Set up file for parsing. Remove blanks and comments."""
   # open the input file (finalpt1.txt)
   with open("finalp1.txt", "r") as file:
      # read content of the file
      content = file.readlines()
   
   # remove all comments, blank lines, and clean up spaces 
   new_content = []
   prevLine=""
   addedLine=""
   addLineFlag = True
   
   #iterate through the string
   for line in content:
      addedLine=line
      addLineFlag = True
   
      # remove all the comments in the form; //comment, //comment//, and block comments. *can't have aspace after*
      if addedLine.endswith("//\n") and prevLine.startswith("//"):
         addLineFlag = False
         continue
      if addedLine.endswith("// ") and prevLine.startswith("//"):
         addLineFlag = False
         continue
      if "//" in addedLine and "//" in prevLine:
         addLineFlag = True
         continue
      elif "//" in addedLine:
         addedLine = addedLine[:addedLine.index("//")]
         
      # remove all the blank lines
      if addedLine.strip() == "":
         prevLine = line
         addLineFlag = False
         continue
      
      # clean up all the spaces
      addedLine = " ".join(addedLine.split())
      
      # append the modified line to the new content
      if addLineFlag is True:
         new_content.append(addedLine)
      
      prevLine=line
      
   # open the output file
   with open("finalp2.txt", "w") as file:
      # write modified content to the output file
      file.write("\n".join(new_content))


def txt_tostr(file_name):
   """Convert text in a file to a long string"""
   
   input_text = ""
   with open(file_name, 'r') as f:
    input_text = f.read()

   return input_text


def init_text(text, inputted_rw, reserved_words, digits, letters):
   """Initialize text for parsing purposes."""
   
   input_text = []

   # split input text into separate characters
   for word in text.split():
    if word in inputted_rw or word in reserved_words:
      input_text.append(word)
    elif word == '"value=",':
      input_text.append('"value=",')
    else:
      for char in word:
         input_text.append(char)

   return input_text


def get_inputted_reserved_words(text, letters, variable_names):
   """Get inputted reserved words to check if misspelt"""
   
   # get inputted reserved words
   inputted_rw_temp = text.translate({ord(c): " " for c in '"*();:,/-=+ '})
   inputted_rw = []

   # get all inputted reserved words
   for rw in inputted_rw_temp.split():
    if rw in letters:
      continue
    elif rw == '"value=",':
      continue
    elif rw in variable_names:
      continue
    else:
      inputted_rw.append(rw)

   # remove any digits
   inputted_rw = [
    x for x in inputted_rw
    if not (x.isdigit() or x[0] == '-' and x[1:].isdigit())
   ]

   # remove any duplicates
   in_rw_no_dups = []
   [
    in_rw_no_dups.append(item) for item in inputted_rw
    if item not in in_rw_no_dups
   ]

   return in_rw_no_dups


def get_variable_names(text):
   """Get names of variables from the text after reserved word var and before reserved word begin. Include variable name of the program. """
   
   variable_names = []

   # split up input text including variable names
   for word in text.split():
    if word == 'program':
      k = text.split().index(word)
    
      for j in range(k + 1, len(text.split())):
         
         if nltk.edit_distance("var", text.split()[j]) <= 2:
          break
         else:
          if ';' in text.split()[j]:
            variable_names.append(text.split()[j].replace(';', ''))
          else:
            variable_names.append(text.split()[j])
    
    elif nltk.edit_distance("var", word) > 2:
      continue
    
    else:
      special_chars = [',', ':', ';', '=', '+', '-', '*', '/', '(', ')']
      
      k = text.split().index(word)
      
      for j in range(k + 1, len(text.split())):
      
         if text.split()[j] == 'integer' or text.split()[j].startswith('i'):
          break
         elif text.split()[j] not in ', :':
          variable_names.append(text.split()[j])
   
   return variable_names


def get_undefined_vars(text, variable_names, inputted_rw, reserved_words,
                        digits, letters):
   """Get any undefined variable for error checking"""

   # get defined variables
   defined_variables = []

   while "" in variable_names:
    variable_names.remove("")

   for varname in variable_names:
    defined_variables.append(
      varname.translate({ord(c): ""
                         for c in "*();:,/-=+ "}))

   while "" in defined_variables:
    defined_variables.remove("")

   defined_variables = set(defined_variables)

   # get undefined variables
   # parse thru everything after begin
   undefined_variables_temp = []
   undefined_variables = []

   # check all used variables after reserved word begin to see if any undefined variables are there
   for word in text.split():
    if word != 'begin':
      continue
    
    else:
      special_chars = [
         '"', 'value', ',', ':', ';', '=', '+', '-', '*', '/', '(', ')'
      ]
      
      k = text.split().index(word)
      for j in range(k + 1, len(text.split())):
         
         if text.split()[j] == 'end.':
          break
         elif text.split()[j] == 'display':
          continue
         elif text.split()[j] == '"value=",':
          continue
         elif text.split()[j] in special_chars:
          continue
         elif text.split()[j] in digits:
          continue
         else:
          for t in text.split()[j]:
            if t in digits:
               continue
          undefined_variables_temp.append(text.split()[j])
          
   for undef_var in undefined_variables_temp:
    undefined_variables.append(
      undef_var.translate({ord(c): " "
                           for c in '"*();:,/-=+'}))

   while 'value' in undefined_variables:
    undefined_variables.remove('value')

   # make sure the undefined vars dont include reserved words
   for undef_var in undefined_variables:
    if undef_var in inputted_rw or undef_var in reserved_words:
      undefined_variables.remove(undef_var)

   undefined_variables = ' '.join(undefined_variables)
   undefined_variables = undefined_variables.split()

   # remove defined variables from undefined
   for def_var in defined_variables:
    while def_var in undefined_variables:
      undefined_variables.remove(def_var)

   undefined_variables = [
    x for x in undefined_variables
    if not (x.isdigit() or x[0] == '-' and x[1:].isdigit())
   ]

   return undefined_variables
