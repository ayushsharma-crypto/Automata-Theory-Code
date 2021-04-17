import sys
import json

if __name__=='__main__':
    if len(sys.argv) != 3:
        print("Unexceptable Format!")
        quit()
    

    try:
        input_file = open(sys.argv[1])
        regular_expression = json.load(input_file)
    except:
        print("Error accessing `input_file`")