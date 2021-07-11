import sys
import os
import argparse
from Parser import Parser

# Usage: run python parser_utils.py -h

def main():
    argument_parser = argparse.ArgumentParser()

    argument_parser.add_argument("-f", "--file", dest = "file",type=str, default = None, help="Pick which file you want to parse. | usage: -f filename")
    argument_parser.add_argument("-m", "--match", dest = "match",type=str, default = None, help="Accepts only the files whose ending match with '_match.txt'. | usage: -m dev || test || train")
    argument_parser.add_argument("-i", "--intentions", dest = "intentions", default = False, action='store_true', help="Use it to generate intentions files from the parser | usage: -i")
    argument_parser.add_argument("-e", "--entities", dest ="entities", default = False, action='store_true', help="Use it to generate entities files from the parser | usage: -e")
    argument_parser.add_argument("-d", "--directory",dest = "directory", type=str, default = None, help="Pick which directory you want to parse | usage: -d directory")

    args = argument_parser.parse_args()
    ending = ".txt"

    if args.match:
        ending = (args.match + ending)

    if args.directory:
        try:
            os.chdir(args.directory)

            for file in os.listdir():
                if file.endswith(ending):
                    input_filepath = f"{args.directory}\{file}"            
                    parser = Parser(input_filepath)
                    parser.parse()

                    if args.intentions:
                        parser.write_intentions()
                    if args.entities:
                        parser.write_entities()
                else:
                    pass
        except:
            sys.exit("uwu something went wrong while parsing this directory")

    if args.file:
        try:
            if (args.file).endswith(ending):       
                parser = Parser(args.file)
                parser.parse()

                if args.intentions:
                    parser.write_intentions()
                if args.entities:
                    parser.write_entities()
            else:
                sys.exit("Arquivo inválido.")
        except:
            sys.exit("uwu something went wrong while parsing this file")

    print('DONE')

if __name__ == "__main__":
    main()