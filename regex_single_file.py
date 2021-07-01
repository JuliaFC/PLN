import sys
import re

# Usage: python regex_single_file.py "file_path"

output_file = None

class Entity:
    
    def __init__(self, input_filepath, output_filepath):
        self.answers = []
        self.ents = []
        self.input_filepath = input_filepath
        self.output_filepath = output_filepath

    def trim_whitespace_and_newline(self, answer):
        if answer:
            while answer[0] == " ":
                answer = answer[1:]
            while answer[-1] == "\n":
                answer = answer[:-1]
        return answer

    def scan_answer(self, line):
        regex = "(?<=\?).([^,]+.*)"
        answers = re.search(regex, line)
        trimmed_answers = []
        if answers:
            answers = answers.group()
            answers = answers.split(',')
            for answer in answers:
                trimmed_answers.append(self.trim_whitespace_and_newline(answer))
            self.answers.append(self.format_answers(trimmed_answers))
    
    def scan_ent(self, line):
        regex = r"\b[A-Z].[\w']+\b(.*)\b[A-Z].[\w']+\b"
        question = line.split('?')
        question = question[0]
        ent = re.search(regex, question)
        if ent:
            ent = ent.group()
            self.ents.append(ent)

    def format_answers(self, list):
        formatted_answers = ''
        for answer in list:
            formatted_answers = formatted_answers + answer + ','
        formatted_answers = formatted_answers[:-1]
        return formatted_answers

    def fetch_answers(self):
        with open(self.input_filepath, 'r', encoding="utf8") as input_file:
            while input_file:
                line = input_file.readline()
                if not line:
                    break
                self.scan_ent(line)
                self.scan_answer(line)
        with open(self.output_filepath, 'w+', encoding="utf8") as  output_file:
            for (ent, answers) in zip(self.ents, self.answers):
                output_file.write(f'{ent}\t{answers}\n')

        input_file.close()
        output_file.close()

def main(): 
    if len(sys.argv) != 2:
        sys.exit("Erro: Precisamos de um arquivo como argumento.")
    
    input_filepath = sys.argv[1]
    output_filepath = input_filepath[:-4]
    output_filepath += "_output.txt" # output_filepath is like 'filename_output.txt'

    mt = Entity(input_filepath, output_filepath)
    mt.fetch_answers()

if __name__ == "__main__":
    main()