import pandas as pd
from os import listdir
from os.path import isfile, join

mypath = '..\movieqa\questions\wiki_entities\intentions'

def main():
    intent_files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    texts = []
    intents = []
    for file in intent_files:
        with open(mypath + '/{}'.format(file)) as f:
            read_lines = f.readlines()
            for line in read_lines:
                line_elements = line.split('\t')
                texts.append(line_elements[0])
                intents.append(line_elements[3])
    df = pd.DataFrame()
    df['texts'] = texts
    df['intents'] = intents
    df.to_csv('intents.csv')