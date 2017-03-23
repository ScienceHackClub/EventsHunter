# -*- coding: utf-8 -*-
#!usr/bin/env python

##
## Extracts Named Entities with NLTK
## Autor: Jean-Francois Kener
##

import nltk
from nltk.tokenize import sent_tokenize # para separar frases

# Load trained POS-tagger + NE chunker
tagger_rss = nltk.data.load('../data/kenerator_aubt.pickle')
chunker_rss = nltk.data.load('../data/kenerator_NaiveBayes.pickle')
tagger_twitter = nltk.data.load('../data/kenerator_aubt.pickle')
chunker_twitter = nltk.data.load('../data/kenerator_NaiveBayes.pickle')


# Extract entity from tree
def extract_ents(t, en_type):
    entity_names = []
    if hasattr(t, 'label') and t.label:
        if t.label() == en_type:
            entity_names.append(' '.join([child[0] for child in t]))
        else:
            for child in t:
                entity_names.extend(extract_ents(child, en_type))

    return entity_names

# Extractor v0.00001 ultra-alpha :)
def nltk_extract(text, text_type="twitter"):
    global tagger
    global chunker

    data = {
        "loc" : [],
        "date" : [],
        "time" : [],
        "person" : [],
        "price" : [],
        "title" : [], # Only for twitter, as RSS already provides it
        "org" : []
    }

    sents = sent_tokenize(text)
    sents = sents[:3] # Relevant infos should be shown first

    for sent in sents:
        if text_type=="twitter":
            print "Parsing twit..."
            str_tags = tagger_twitter.tag(nltk.word_tokenize(sent))
            str_chunks = chunker_twitter.parse(str_tags)
        elif text_type=="rss":
            print "Parsing rss..."
            str_tags = tagger_rss.tag(nltk.word_tokenize(sent))
            str_chunks = chunker_rss.parse(str_tags)

        data['loc'].extend(extract_ents(str_chunks,'LOC'))
        data['org'].extend(extract_ents(str_chunks,'ORG'))
        data['date'].extend(extract_ents(str_chunks,'DATE'))
        data['time'].extend(extract_ents(str_chunks,'TIME'))
        data['person'].extend(extract_ents(str_chunks,'PER'))
        data['price'].extend(extract_ents(str_chunks,'PRICE'))

    #print data['date']
    return data
