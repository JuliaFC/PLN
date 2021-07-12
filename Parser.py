import sys
import re

class Parser:
    
    def __init__(self, input_file):
        self.answers = []
        self.ents = []
        self.intention = None
        self.questions = []
        self.wiki_entities = self.load_wiki_entities()
        self.input_filename = input_file
        self.processed_lines = 0

    def trim_whitespace_and_newline(self, answer):
        if answer:
            while answer[0] == " ":
                answer = answer[1:]
            while answer[-1] == "\n":
                answer = answer[:-1]
        return answer

    def parse_answer(self, line):
        regex = "(?<=\?).([^,]+.*)"
        answers = re.search(regex, line)
        trimmed_answers = []
        if answers:
            answers = answers.group()
            answers = answers.split(',')
            for answer in answers:
                trimmed_answers.append(self.trim_whitespace_and_newline(answer))
            self.answers.append(self.format_answers(trimmed_answers))
    
    def parse_entity(self, line):
        regex = r"\b(?=\w*[A-Z0-9])\w*\b(.*)([A-Z0-9\'\!]+)\w*"
        line = line.split('?')[0][1:] # captures the text of the question between '1' and '?'
        line = self.trim_whitespace_and_newline(line)
        main_entity = re.search(regex, line)
        words = line.split(' ')

        entities = []
        if main_entity:
            main_entity = main_entity.group()
            main_entity_words = main_entity.split(' ')
            for word in words:
                if word in self.wiki_entities:
                    entities.append(word)
                elif word in main_entity_words and main_entity in self.wiki_entities:
                    entities.append(main_entity)
                else:
                    entities.append('0')

            self.ents.append((line, entities))
    
    def load_wiki_entities(self):
        wiki_entities_file = r'C:\Users\JuliaFC\Documents\2021\PLN\PLN\movieqa\knowledge_source\entities.txt'
        wiki_entities = set()
        with open(wiki_entities_file, 'r', encoding="utf8") as file:
            while file:
                line = file.readline()
                if not line:
                    break
                wiki_entities.add(self.trim_whitespace_and_newline(line))
        return wiki_entities
 
    def parse_intention_from_filename(self):
        regex = r"(?<=_qa_)(.*)(?=_dev)"
        intention = re.search(regex, self.input_filename)
        if intention:
            intention = intention.group()
            self.intention = intention

    def parse_questions(self, line):
        regex = r"[A-Za-z].(.*)(?=[\t])"
        question = re.search(regex, line)
        if question:
            question = question.group()
            self.questions.append(question)

    def format_answers(self, list):
        formatted_answers = ''
        for answer in list:
            formatted_answers = formatted_answers + answer + ','
        formatted_answers = formatted_answers[:-1]
        return formatted_answers

    def parse(self):
        self.parse_intention_from_filename()
        with open(self.input_filename, 'r', encoding="utf8") as input_file:
            while input_file:
                line = input_file.readline()
                if not line:
                    break
                self.parse_entity(line)
                self.parse_answer(line)
                self.parse_questions(line)
                self.processed_lines = self.processed_lines + 1

    def write_entities(self):
        output_filename = self.create_output_filename("entities")
        with open(output_filename, 'w+', encoding="utf8") as output_file:
            for ent in self.ents:
                question = ent[0]
                entities = ent[1]
                output_file.write(f'{question}\t{entities}\n')

    def write_intentions(self):
        output_filename = self.create_output_filename("intentions")
        with open(output_filename, 'w+', encoding="utf8") as output_file:
            for (questions, answers) in zip(self.questions, self.answers):
                output_file.write(f'{questions}\t{answers}\t{self.intention}\n')

    def create_output_filename(self, identifier):
        if self.input_filename is None:
            sys.exit("Erro: Não há o input_filename.")
        filename = self.input_filename[:-4]
        filename += f"_{identifier}.txt"
        return filename


def main(): 
    if len(sys.argv) != 2:
        sys.exit("Erro: Precisamos de um arquivo como argumento.")
    
    input_file = sys.argv[1]
   
    parser = Parser(input_file)
    parser.parse()

if __name__ == "__main__":
    main()