# -*- coding: utf-8 -*-
#!usr/bin/env python

##
## Extracts Named Entities with NLTK
## Autor: Jean-Francois Kener
##

import nltk, re
from nltk.tokenize import sent_tokenize # para separar frases

# config
max_len = 200 # to implement

# Load trained POS-tagger + NE chunker
tagger_rss = nltk.data.load('../data/kener-rss-tagger.pickle')
chunker_rss = nltk.data.load('../data/kener-rss-chunker.pickle')
tagger_twitter = nltk.data.load('../data/kener-twitter-tagger.pickle')
chunker_twitter = nltk.data.load('../data/kener-twitter-chunker.pickle')


# Gets len of part of tree
def tree_len(t, l=0):
    for child in t:
        if type(child) is not nltk.Tree:
            l += len(child[0]) + 1
        else:
            l += tree_len(child, l)
    return l

# Extract entity from tree
def extract_ents(t, en_type, pos=0):
    entity_names = []
    for child in t:
        if type(child) is nltk.Tree:
            entity_names.extend(extract_ents(child, en_type, pos))
            if hasattr(t, 'label') and t.label:
                if child.label() == en_type:
                    ne = ' '.join([_child[0] for _child in child])
                    entity_names.append((ne, pos))
        pos+=tree_len(child)
    return entity_names
'''
def extract_ents(t, en_type, pos=0):
    entity_names = []
    if hasattr(t, 'label') and t.label:
        if t.label() == en_type:
            ne = ' '.join([child[0] for child in t])
            entity_names.append((ne, pos))
        else:
            for child in t:
                entity_names.extend(extract_ents(child, en_type,pos))
                pos+=tree_len(child)
    return entity_names
'''

# Extractor v0.00001 ultra-alpha :)
def nltk_extract(text, text_type="twitter"):
    global max_len
    global tagger
    global chunker

    print "Parsing " + text_type

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

    # index keep track for tags restoration
    index_text = 0
    index_sent = 0
    sentslen = [len(sent) for sent in sents]

    # Separate commas and other punctuation
    for sent in sents:
        sent = re.sub(r'([\!\¡\¿\?\,\'\"\(\)\.\-])', r' \1 ', sent)
        sent = re.sub(r'\.\ \.\ \.\ ','...', sent)
        sent = re.sub(r'[\s]{2,}',' ', sent)

    # Extract NEs
    for sent in sents:
        if text_type=="twitter":
            str_tags = tagger_twitter.tag(nltk.word_tokenize(sent))
            str_chunks = chunker_twitter.parse(str_tags)
            data['title'].extend(extract_ents(str_chunks,'MAIN'))
        elif text_type=="rss":
            str_tags = tagger_rss.tag(nltk.word_tokenize(sent))
            str_chunks = chunker_rss.parse(str_tags)

        data['loc'].extend(extract_ents(str_chunks,'LOC',index_text))
        data['org'].extend(extract_ents(str_chunks,'ORG',index_text))
        data['date'].extend(extract_ents(str_chunks,'DATE',index_text))
        data['time'].extend(extract_ents(str_chunks,'TIME',index_text))
        data['person'].extend(extract_ents(str_chunks,'PER',index_text))
        data['price'].extend(extract_ents(str_chunks,'PRICE',index_text))


        index_text += sentslen[index_sent]
        index_sent += 1

        if(index_text > max_len):
            break;

    return data
