"""Small script to cache and load python objects"""

import cPickle

def dump(obj, filename):

   f = open(filename, 'wb')
   cPickle.dump (obj, f, -1)
   f.close()

def load(filename):
   f = open(filename, 'rb')
   obj = cPickle.load(f)
   f.close()

   return obj

