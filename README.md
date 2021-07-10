### To run the parser:

usage: parser_utils.py [-h] [-f FILE] [-m MATCH] [-i] [-e] [-d DIRECTORY]

options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Pick which file you want to parse. | usage: -f filename
  -m MATCH, --match MATCH
                        Accepts only the files whose ending match with '_match.txt'. | usage: -m dev || test || train
  -i, --intentions      Use it to generate intentions files from the parser | usage: -i
  -e, --entities        Use it to generate entities files from the parser | usage: -e
  -d DIRECTORY, --directory DIRECTORY
                        Pick which directory you want to parse | usage: -d directory

### Parsing intentions:

**wiki-entities_qa_actor_to_movie_dev.txt**

    1 what movies did Temuera Morrison act in?    Once Were Warriors, Tracker, River Queen

**wiki-entities_qa_actor_to_movie_dev_intentions.txt**

    what movies did Temuera Morrison act in?		Once Were Warriors,Tracker,River Queen	actor_to_movie

### Parsing entities:
**In development**

