"""Holds the POS object, just to get it out of the main script"""

# Parts of speech dict with various information about each, used in processing questions
POS = {
         'AP' : {'name'    : 'determiner/pronoun, post-determiner',
                 'lexnames': [],
                 'ref'     : False,
                },
         'IN' : {'name'    : 'preposition',
                 'lexnames': [],
                 'ref'     : False,
                },
         'JJ' : {'name'    : 'adjective',
                 'lexnames': [],
                 'ref'     : True,
                },
         'NN' : {'name'    : 'noun',
                 'lexnames': [
                                'noun.animal',
                                'noun.artifact',
                                'noun.body',
                                'noun.food',
                                'noun.motive',
                                'noun.plant',
                                'noun.shape',
                             ],
                 'ref'     : True,
                },
         # At the moment, I'm using nltk.word_tokenizer to split the question up which breaks on 
         # special characters, so I don't want to use special characters in the tag name. 
         # However, in order to look up the words associated with a tag, I need to have the
         # actual tag name available as well otherwise things break
         'NNX': {'name'    : 'noun, singular, common, genitive',
                 'tag'     : 'NN$',
                 'lexnames': [
                                'noun.animal',
                                'noun.artifact',
                                'noun.body',
                                'noun.food',
                                'noun.motive',
                                'noun.plant',
                                'noun.shape',
                             ],
                 'ref'     : True,
                },
         'NNS': {'name'    : 'noun, plural, common',
                 'lexnames': [
                                'noun.animal',
                                'noun.artifact',
                                'noun.body',
                                'noun.food',
                                'noun.motive',
                                'noun.plant',
                                'noun.shape',
                             ],
                 'ref'     : False,
                },
         'PN' : {'name'    : 'pronoun',
                 'lexnames': [],
                 'ref'     : False,
                },
         'RB' : {'name'    : 'adverb',
                 'lexnames': [],
                 'ref'     : False,
                },
         'RBR': {'name'    : 'adverb, comparative',
                 'lexnames': [],
                 'ref'     : False,
                },
         'VB' : {'name'    : 'verb',
                 'lexnames': [
                                'verb.body',
                                'verb.competition',
                                'verb.contact',
                                'verb.perception',
                                'verb.possession',
                                'verb.social',
                             ],
                 'ref'     : False,
                },
         'VBG': {'name'    : 'verb, present participle or gerund',
                 'lexnames': [
                                'verb.body',
                                'verb.competition',
                                'verb.contact',
                                'verb.perception',
                                'verb.possession',
                                'verb.social',
                             ],
                 'ref'     : False,
                },
         'VBN': {'name'    : 'past-participle',
                 'lexnames': [],
                 'ref'     : False,
                },
         'VBZ': {'name'    : 'verb, present tense, 3rd person singular',
                 'lexnames': [
                                'verb.body',
                                'verb.competition',
                                'verb.contact',
                                'verb.perception',
                                'verb.possession',
                                'verb.social',
                             ],
                 'ref'     : False,
                },
      }
