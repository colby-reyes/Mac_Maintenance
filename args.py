import sys
import getopt

def get_args():
  import getopt
  import sys

  # Remove the first argument( the filename)
  all_args = sys.argv[1:]
  
  try:
    # Gather the arguments
    print(f"arg: {all_args}")
    # Should have exactly two options
    if len(opts) != 2:
      print ('usage: args_demo.py -x <first_value> -b <second_value>')
    else:
      # Iterate over the options and values
      for opt, arg_val in opts:
        prod *= int(arg_val)
      print('Product of the two numbers is {}'.format(prod))

  except:
    print ('usage: args_demo.py -a <first_value> -b <second_value>')
    sys.exit(2)
      

import argparse

# Construct an argument parser
all_args = argparse.ArgumentParser(description='Example for one positional arguments',
formatter_class=argparse.ArgumentDefaultsHelpFormatter)

# Add arguments to the parser
all_args.add_argument("-x", "--Value1", metavar='Value1', required=False,
   help="first Value")
all_args.add_argument("-y", "--Value2", metavar='Value2', required=False,
   help="second Value")
all_args.add_argument('titles', metavar='titles', type=int, help='GrandSlam Titles')

args = vars(all_args.parse_args())

print(f"args: {args}")
print(args.titles)