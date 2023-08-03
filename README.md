# Theme Song Lyrics Generator
* This is final project for COMP47410 – Computational Creativity
## Tech Stack: Python, NLP(Part-of-Speech Tagging, Named Entity Recognition, Sentiment analysis), Tracery grammer
The main idea is to input titles for series of movies, know the melody and the number of syllables needed for each lyric, then use movie database API to capture the movie plot and other related information, and then perform Natural Language Processing to analyse the proper nouns and other nouns, verbs, adjectives, etc, and mark syllables for each word. Then transformed into Tracery grammar to automatically generate some short sentences to form the lyrics of the theme song.


* DATA COLLECTION
1. Read csv file line by line, and then use the movie name in that line to get the movie information.
2. Get API key
3. Exception handling
4. Filter the content I need ("Plot")
* PARSE
1. Part-of-Speech Tagging (POS Tagging)
2. Named Entity Recognition(NER)
3. Advanced: Sentiment analysis
* GENERATE
1. Sentence composition

   eg: Format_list = 
[
Noun + Verb + Noun, 
Pronoun + Verb + Adjective, 
Noun + Verb + Adjective, 
Adjective + Noun + Verb, 
Noun + Verb + Adverb, 
Noun + Verb + Preposition + Noun, 
…
]

3. Syllable correspondence
* FUTURE WORK
1. Data collection improvement
2. More detailed and richer sentence formats
