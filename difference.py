# -*- coding: utf-8 -*-
"""
Name: difference.py
Description:

Author: Bryan Tutt
Created: 26Nov2018
"""

# from difflib import SequenceMatcher
import difflib
import string


# gets percentage difference between 2 strings
def similar(a, b):
    return str(difflib.SequenceMatcher(None, a, b).ratio()*100) + '%'


# def thediff(a, b):
#     return difflib.unified_diff(a, b)


# removes punctuation
def remove_punctuation(sentence):
    nopunct = sentence.translate(None, string.punctuation)
    return nopunct.upper()


# sorts sentence
def sorted_sentence(sentence):
    words = sentence.split(' ')
    words.sort()
    newSentence = ' '.join(words)
    print('Sorted: ', newSentence.strip())
    return newSentence.strip()


def run(field_a, field_b):
    cleaned_a = remove_punctuation(field_a)
    cleaned_b = remove_punctuation(field_b)
    sorted_A = sorted_sentence(cleaned_a)
    sorted_B = sorted_sentence(cleaned_b)
    percentdifference = similar(sorted_A, sorted_B)

    return percentdifference



a = 'Ziggy Stardust David Bowie'
b = 'Bowie, David Stardust yggiz '

# a = "bob obrien"
# b = "bob o'brien"

bob = run(a, b)
print(bob)


