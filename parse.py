from __future__ import unicode_literals
from pattern.en import parse
from pattern.en import pprint
import nltk
import json
import spacy
from spacy import displacy
import textacy
from pattern.en import sentiment
import syllables
from pathlib import Path

plot_path = Path("plot")
data_file = "_plot.json"
theme_titles = ["Spiderman","Star Wars", "Pirates of the Caribbean"]
# collect parse data storing path
parse_path = Path("parse")
# make sure the folder exists
parse_path.mkdir(parents=True, exist_ok=True)

plot_dict ={}
for theme in theme_titles:
    file_name = theme+data_file
    file = plot_path / file_name
    with open(file) as json_file:
        data = json.load(json_file)
        plot_dict[theme]=data
        

nlp = spacy.load("en_core_web_sm")

# Named Entity Recognition (NER) with Spacy
def get_ner_dict(key):
    NER = spacy.load("en_core_web_sm")
    ner_dict={}
    ner_data=plot_dict[key]
    for line in ner_data:
        doc= NER(line)
        for ent in doc.ents:
            ner = []
            if ent.label_ in ner_dict.keys():
                ner = ner_dict[ent.label_]
            ner.append(ent.text)
            ner_dict[ent.label_]=ner

#     displacy.serve(doc, style="ent")
    return remove_dup(ner_dict)
    

def get_verb_list(key):
    verb_list=[]
    verb_data=plot_dict[key]
    
    lemmatizer = nlp.get_pipe("lemmatizer")
    
    pattern = [{'POS': 'VERB', 'OP': '?'},
               {'POS': 'ADV', 'OP': '*'},
               {'POS': 'VERB', 'OP': '+'}]

    for line in verb_data:
        sentence = line
        doc = nlp(sentence)
        lists = textacy.extract.token_matches(doc, pattern)
        for verb in lists:
            verb_list.append(verb.lemma_)
    return verb_list


# Part-of-speech tagging
def get_pos_dict(key):
    pos_list=[]
    pos_data=plot_dict[key]
    pos = []
    
    for line in pos_data:
        pos_dict={}
        doc= nlp(line)
        for token in doc:
            if token.pos_ in pos_dict.keys():
                pos = pos_dict[token.pos_]
            else:
                pos=[]
                
            if token.is_stop is False:
                pos.append(token.lemma_)
                
            pos_dict[token.pos_]=pos
        pos_list.append(remove_dup(pos_dict))

    return pos_list
    
    
def remove_dup(pos_dict):
    # remove duplicates
    for k in pos_dict.keys():
        l1 = pos_dict[k]
        l2 = []
        [l2.append(i) for i in l1 if not i in l2]
        pos_dict[k] = l2
    return pos_dict

#Store the syllable information of each word as a dictionary
def get_syllables(word):
    return syllables.estimate(word)

def store_syllables(word_list):
    syllables_dict={}
    syllables_list=[]
    for word in word_list:
        count = get_syllables(word)
        if count in syllables_dict:
            syllables_list = syllables_dict[count]
        else:
            syllables_list=[]
        syllables_list.append(word)
        syllables_dict[count]=syllables_list
    return syllables_dict


def get_parse(orgin_dict):
    parse_dict={}
    
    for k,v in orgin_dict.items():
        parse_dict[k] = store_syllables(v)
    return parse_dict


def get_parse_dict(key):
    
    parse_list=[]
    
    pos_list = get_pos_dict(key)
    verb_list=get_verb_list(key)
    ner_dict = get_ner_dict(key)
    
    for pos in pos_list:
        parse_dict_foreach = get_parse(pos)
        parse_list.append(get_parse(pos))

    return parse_list

    
for theme in theme_titles:
    file_name = theme+'_parse.json'
    file_path = parse_path / file_name
    parse_data = get_parse_dict(theme) 
    with open(file_path, 'w') as outfile:
        json_string = json.dumps(parse_data)
        outfile.write(json_string)

print('test')
print(get_parse_dict('Spiderman'))
