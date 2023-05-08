from settingUp import *
set_up_file()

from grammar import *
from create_table import *
from convertPython import *
from outputPython import *

# initialize file to be read and parsing table to be used
text = txt_tostr('finalp2.txt')
parsing_table = initialize_parsing_table()

# check grammar of text in file
result = check_grammar(parsing_table, text)

if result:
  print("\nAccept\n")  # grammar was valid
  print("\nAfter conversion to Python3: \n")

  # call code to translate to python here
  toPython()
  # call converted code here
  eval(pull_function() + "()")

else:
  print("\nNot Accept")  # grammar was invalid
