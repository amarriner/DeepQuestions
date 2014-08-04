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
import sys


# List of potential questions to pull from
QUESTIONS = [
               'If <NN> <VBZ>, can <PN> <VB> it?',
               'If you <VBN> <NN>, how would you <VB> it?',
               'When would you <VB> <NN>?',
               'How does one <VB> <NN> with <NN$|NN>?',
               'How does one <VB> <NN> with <NN>?',
               'Why does <PN> <VB>?',
               'When <VBG> <NN>, who <VBZ> it?',
               'Who <VBZ> the <AP> <NNS>?',
               'Who is <VBG> the <NNS>?',
            ]
# Working directory
PWD = '/home/amarriner/python/question/'

# Used to replace parts of speech within a string
TAG_PATTERN = re.compile(r'(<.*?>)')

# Just a list of vowels...
VOWELS = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']


def build_word_lists():
   """Run through the POS tags and get lists of words for each"""

   # Grab a cached version if possible, otherwise load words from the brown corpus with the given tag into the
   # appropriate POS dict entry
   for tag in POS.keys():
      filename = PWD + 'cache/pos_' + tag + '.cache'
      if os.path.isfile(filename):
         POS[tag]['words'] = cache_object.load(filename)
      else:
         POS[tag]['words'] = [w for w in brown.tagged_words() if w[1] == tag]
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

         if t == 'VBG':
            synset = wordnet.synsets(conjugate(word), pos=t)
         else:
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

   return singularize(word).replace('\'', '')


def replace_pos(question):
   """Replaces tags in a question with a random word of the same POS type"""

   done = False
   while not done:

      try:

         # Get a new iterator for the regex pattern. No terribly efficient, but since we're potentially
         # changing the length and indicies of the string on each pass, we have to get a new one every time
         last = None
         replace = ''
         tag = TAG_PATTERN.finditer(question).next()
         (start, end) = tag.span()
         for t in tag.group().replace('<', '').replace('>', '').split('|'):

            # If the POS tag we found exists in the POS tag, strip out the placeholder and replace it with a random word
            if t in POS.keys():

               # ref determines whether to place an article before the word or not
               ref = POS[t]['ref']
               if last:
                  if POS[t]['ref'] and POS[last]['ref']:
                     ref = False

               word = get_random_word(t, ref)

               if replace:
                  replace = replace + ' '

               replace = replace + word

            last = t

         question = question[:start] + replace + question[end:]

      except StopIteration, e:
         done = True

   return question


def main():
   """Main entry point"""

   build_word_lists()

   question = random.choice(QUESTIONS)
   print question
   print replace_pos(question)


if __name__ == "__main__":
   sys.exit(main())

