import sys
import os
import re
from regex_single_file import *

# Usage: python regex.py "directory"

def main(): 
    if len(sys.argv) != 2:
        sys.exit("Erro: Precisamos de um diretório como argumento.")
    
    directory = sys.argv[1]
    os.chdir(directory)

    for file in os.listdir():
        if file.endswith(".txt"):
            input_filepath = f"{directory}\{file}"            
            output_filepath = input_filepath[:-4]
            output_filepath += "_output.txt"

            ent = Entity(input_filepath, output_filepath)
            ent.fetch_answers()

if __name__ == "__main__":
    main()