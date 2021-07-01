import sys
import re

# Usage: python regex_single_file.py "file_path"

output_file = None

class MovieTitles:
    def __init__(self, input_filepath, output_filepath):
        self.movies = []
        self.input_filepath = input_filepath
        self.output_filepath = output_filepath

    def trim_whitespace_and_newline(self, movie):
        while movie[0] == " ":
            movie = movie[1:]
        while movie[-1] == "\n":
            movie = movie[:-1]
        return movie

    def scan_answer(self, line):
        regex = "(?<=\t).([^,]+.*)"
        movie_titles = re.search(regex, line)
        if movie_titles:
            movie_titles = movie_titles.group()
            movie_titles = movie_titles.split(',')
            for movie in movie_titles:
                movie = self.trim_whitespace_and_newline(movie)
                self.movies.append(movie)


    def fetch_movies(self):
        with open(self.input_filepath, 'r', encoding="utf8") as input_file:
            while input_file:
                line = input_file.readline()
                if not line:
                    break
                self.scan_answer(line)
        with open(self.output_filepath, 'w+', encoding="utf8") as  output_file:
            for movie in self.movies:
                output_file.write(f'{movie}\n')
        input_file.close()
        output_file.close()
        

def main(): 
    if len(sys.argv) != 2:
        sys.exit("Erro: Precisamos de um arquivo como argumento.")
    
    input_filepath = sys.argv[1]
    output_filepath = input_filepath[:-4]
    output_filepath += "_output.txt" # output_filepath is like 'filename_output.txt'

    mt = MovieTitles(input_filepath, output_filepath)
    mt.fetch_movies()

if __name__ == "__main__":
    main()