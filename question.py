#!/usr/bin/env python

"""Script to ask silly questions?"""

from nltk.corpus import brown
from pattern.en import wordnet
from string import Template

import cache_object
import nltk
import os
import pattern.en
import random
import re
import sys

TAG_PATTERN = re.compile(r'(<.*?>)')

POS = {
         'NN' : {'name'    : 'noun',
                 'lexnames': [
                                'noun.animal',
                                'noun.body',
                                'noun.food',
                                'noun.plant',
                                'noun.shape',
                             ]
                },
         'VB' : {'name'    : 'verb',
                 'lexnames': [
                                'verb.body',
                                'verb.communication',
                                'verb.competition',
                                'verb.contact',
                                'verb.social',
                             ]
                },
         'VBN': {'name'    : 'past-participle',
                 'lexnames': []
                },
      }

VOWELS = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']


def build_word_lists():
   """Run through the POS tags and get lists of words for each"""

   for tag in POS.keys():
      filename = 'pos_' + tag + '.cache'
      if os.path.isfile(filename):
         POS[tag]['words'] = cache_object.load(filename)
      else:
         POS[tag]['words'] = [w for w in brown.tagged_words() if w[1] == tag]
         cache_object.dump(POS[tag]['words'], filename)


def get_random_word(t):
   """Return a random word from a set filtering on lexname category if necessary"""

   word = None
   if len(POS[t]['lexnames']):

      lexname = ''
      while lexname not in POS[t]['lexnames']:
         word = random.choice(POS[t]['words'])[0]
         synset = wordnet.synsets(word, pos=t)

         if synset:
            lexname = synset[0].lexname

   else:
      word = random.choice(POS[t]['words'])[0]

   return word


def replace_articles(question):
   """Replaces [A] placeholder with 'a' or 'an'"""

   if question.split(' ').index('[A]') >= 0:
      if question.split(' ')[question.split(' ').index('[A]') + 1][:1] in VOWELS:
         question = question.replace('[A]', 'an')
      else:
         question = question.replace('[A]', 'a')

   return question


def replace_pos(question):
   """Replaces tags in a question with a random word of the same POS type"""

   done = False
   while not done:

      try:

         tag = TAG_PATTERN.finditer(question).next()
         t = tag.group().replace('<', '').replace('>', '')
         if t in POS.keys():
            word = get_random_word(t)
            (start, end) = tag.span()
            question =  question[:start] + word + question[end:]

      except StopIteration, e:
         done = True

   return question


def main():
   """Main entry point"""

   build_word_lists()
   print replace_articles(replace_pos('If you <VBN> [A] <NN>, how would you <VB> it?'))
      

if __name__ == "__main__":
   sys.exit(main())
