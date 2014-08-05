#!/usr/bin/env python

"""Script to ask silly questions?"""
from nltk.corpus import brown
from pattern.en import conjugate, referenced, singularize, wordnet
from pos import POS

import cache_object
import nltk
import os
import pattern.en
import random
import re
import string
import sys


# List of potential questions to pull from
QUESTIONS = [
               'If <NN> <VBZ>, can <PN> <VB> it?',
               'If you <VBN> <NN>, how would you <VB> it?',
               'How does one <VB> <NN> with <NNX> <NN>?',
               'How does one <VB> <NN> with <JJ?25> <NN>?',
               'Why does <PN> <JJ?10> <VB>?',
               'When <VBG> <NN>, who <VBZ> it?',
               'When would you <VB> <JJ?50> <NN>?',
               'Who <VBZ> the <AP> <NNS>?',
               'Who is <RB?25> <VBG> the <NNS>?',
               'Is <JJ?50> <NN> <RBR> than <JJ?50> <NN>?',
               'Does <NNX?75> <NN> <VB> <NN>?',
               'What if <NN> <VBZ> <IN> <NN>?',
               'What does <NNX?50> <NN> <VB> with <NN>?',
            ]

# Working directory
PWD = '/home/amarriner/python/question/'

# Used to replace parts of speech within a string
TAG_PATTERN = re.compile(r'<(?P<tag>.*?)>')

# Just a list of vowels...
VOWELS = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']


def build_word_lists():
   """Run through the POS tags and get lists of words for each"""

   # Grab a cached version if possible, otherwise load words from the brown corpus with the given tag into the
   # appropriate POS dict entry
   for tag in POS.keys():

      nltk_tag = tag
      if 'tag' in POS[tag].keys():
         nltk_tag = POS[tag]['tag']

      filename = PWD + 'cache/pos_' + nltk_tag + '.cache'
      if os.path.isfile(filename):
         POS[tag]['words'] = cache_object.load(filename)
      else:
         POS[tag]['words'] = [w for w in brown.tagged_words() if w[1] == nltk_tag]
         cache_object.dump(POS[tag]['words'], filename)


def get_random_word(t, ref=False):
   """Return a random word from a set filtering on lexname category if necessary"""

   # If there are entries in the lexnames list for the given POS tag, limit results to that,
   # otherwise just return a random word for that POS
   word = None
   if len(POS[t]['lexnames']):

      lexname = ''
      while lexname not in POS[t]['lexnames']:
         word = random.choice(POS[t]['words'])[0]

         synset = wordnet.synsets(get_singular(word), pos=t)

         if synset:
            lexname = synset[0].lexname

   else:
      word = random.choice(POS[t]['words'])[0]

   if ref:
      word = referenced(word)

   return word.lower()


def get_singular(word):
   """Further refinement of the pattern.en.singularize function"""

   return conjugate(singularize(word).replace('\'', ''))


def replace_pos(question):
   """Replaces tags in a question with a random word of the same POS type"""

   tokens = nltk.word_tokenize(re.sub(TAG_PATTERN, strip_tag, question))
   question = []

   last = None
   for t in tokens:

      if t in POS.keys():

         ref = POS[t]['ref']

         if last:
            if POS[t]['ref'] and POS[last]['ref']:
               ref = False

         question.append(get_random_word(t, ref))
         last = t

      else:

         if t in string.punctuation:
            question[-1] = question[-1] + t
         else:
            question.append(t)

         last = None

   return ' '.join(question)


def strip_tag(match):
   """Returns the stripped version of a tag for tokenization, sometimes erases it entirely"""

   str = match.group('tag')
   split = str.split('?')
   if len(split) == 2:
      rnd = random.choice(range(1,100))
      if rnd < int(split[1]):
         str = split[0]
      else:
         str = ''
   
   return str


def main():
   """Main entry point"""

   build_word_lists()

   question = random.choice(QUESTIONS)
   print question
   question = replace_pos(question)
   print question


if __name__ == "__main__":
   sys.exit(main())

