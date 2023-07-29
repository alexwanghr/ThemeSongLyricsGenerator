import json
import spacy
from spacy import displacy
import textacy
import syllables
import random
from pathlib import Path
import nltk
from nltk import word_tokenize
import tracery
from tracery.modifiers import base_english
    
theme_titles = ["Spiderman","Star Wars", "Pirates of the Caribbean"]
data_file = "_parse.json"
#parse data storing path
parse_path = Path("parse")
# make sure the folder exists
parse_path.mkdir(parents=True, exist_ok=True)
output_path = Path("output")
# make sure the folder exists
output_path.mkdir(parents=True, exist_ok=True)

parse_dict ={}

for theme in theme_titles:
    file_name = theme+data_file
    file = parse_path / file_name
    with open(file) as json_file:
        data = json.load(json_file)
        parse_dict[theme]=data


def get_format(size):
    if size>5:
        format_list=["NOUN VERB NOUN", "NOUN VERB NOUN", "PROPN VERB NOUN", "PROPN VERB PROPN", "PROPN VERB ADJ", "ADJ NOUN VERB"]
    else:
        format_list=["PRON AJD", "VERB NOUN","ADJ NOUN","ADV ADJ","NOUN VERB"]
    return random.choice(format_list)
    
    
def get_combine(size):
    times=0
    paragraph = str(get_format(size))
    
    while check_format(size,paragraph)==False:
        times=times+1
        paragraph = str(get_format(size))
        if(times>15):
            break
    
    return paragraph
    
        
# Check that this line has all required parts of speech
def check_orgin(orgin,paragraph):
    format_str = word_tokenize(paragraph)
    for word in format_str:
        if word in orgin.keys():
            continue
        else:
            return False
    return True
    
    
def check_format(size,paragraph):
    global orgin
    times=0
    
    while True:
        if times>30:
            return False
        orgin = random.choice(parse_data)
        if check_orgin(orgin,paragraph)==False:
            times=times+1
            orgin = random.choice(parse_data)
            continue
        else:
            if len(get_syllables_dict(size,orgin,paragraph))== 0:
                times=times+1
                continue
            else:
                return True
    return False


def get_syllables_dict(size,orgin,paragraph):
    global syllables_dict
    format_str = word_tokenize(paragraph)
    length=len(format_str)
    if length==1:
        for key in orgin[format_str[0]].keys():
            one_word_dict={}
            if abs(key-size)<=2:
                one_word_dict[format_str[0]]=key
                syllables_dict.append(one_word_dict)
    if length==2:
        syllables_dict=two_sum(size,orgin,format_str)
    if length==3:
        syllables_dict=three_sum(size,orgin,format_str)
                   
    return syllables_dict


def two_sum(sum,orgin,format_str):
    list_dict=[]
    list1 = list(orgin[format_str[0]].keys())
    list1 = sort_intlist(list1)
    list2 = list(orgin[format_str[1]].keys())
    list2 = sort_intlist(list2)
    
    for l1 in list1:
        for l2 in list2:
            if abs(sum-l1-l2)<=1:
                result={}
                result[format_str[0]]=l1
                result[format_str[1]]=l2
                list_dict.append(result)
    return list_dict

def three_sum(sum,orgin,format_str):
    list_dict=[]
    list1 = list(orgin[format_str[0]].keys())
    list1 = sort_intlist(list1)
    list2 = list(orgin[format_str[1]].keys())
    list2 = sort_intlist(list2)
    list3 = list(orgin[format_str[2]].keys())
    list3 = sort_intlist(list3)
    
    for l1 in list1:
        newsum=sum-l1
        for l2 in list2:
            for l3 in list3:
                if abs(newsum-l3-l2)<=1:
                    result={}
                    result[format_str[0]]=l1
                    result[format_str[1]]=l2
                    result[format_str[2]]=l3
                    list_dict.append(result)
    return list_dict

def sort_intlist(stringlist):
    newlist=[]
    for s in stringlist:
        newlist.append(int(s))
    newlist.sort()
    return newlist



def to_Tracery(syllables_list,orgin_dict):
    rules = {}
    rules_orgin=[]

    for pair in syllables_list:
        orgin_str=""
        for k,v in pair.items():
            key=str(k)+str(v)
            rules[key]=orgin_dict[k][str(v)]
            orgin_str=orgin_str+"#" + key +"# "
        rules_orgin.append(orgin_str)
    
    rules["origin"] = rules_orgin
    
    grammar = tracery.Grammar(rules) # create a grammar object from the rules
    grammar.add_modifiers(base_english)
    output_line = grammar.flatten("#origin#")
    
    return output_line


output_data = []
output_dict={}
for theme in theme_titles:
    output_dict[theme] = output_data

output_data = []
each_line=[9,8,4,4,8,7,2,9,6,7,7]
parse_data = parse_dict['Spiderman']
for i in range(30):
    for count in each_line:
        get_combine(count)
        output = to_Tracery(syllables_dict,orgin)
        output_data.append(output)
    output_dict['Spiderman'].append(output_data)
    
output_data = []
each_line=[9,9,8,7,8,9,9,8,7,8]
parse_data = parse_dict['Star Wars']
for i in range(30):
    for count in each_line:
        get_combine(count)
        output = to_Tracery(syllables_dict,orgin)
        output_data.append(output)
output_dict['Star Wars'] = output_data
    
output_data = []
each_line=[10,10,7,6,4,4,5,5]
parse_data = parse_dict['Pirates of the Caribbean']
for i in range(30):
    for count in each_line:
        get_combine(count)
        output = to_Tracery(syllables_dict,orgin)
        output_data.append(output)
output_dict['Pirates of the Caribbean'] = output_data
    

for theme in theme_titles:
    file_name = theme+'.json'
    file_path = output_path / file_name
    data = output_dict[theme] 
    with open(file_path, 'w') as outfile:
        json_string = json.dumps(data)
        outfile.write(json_string)
    
