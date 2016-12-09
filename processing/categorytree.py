# Crawl through the recipes we have, and make a tree of all the categories

import os
import json
from IPython import embed

data_dir = 'scraped'
categories = {'Recipes':{}}

def print_subtree(tree, indent):
  for leaf in tree.keys():
    print ' |'*indent, leaf
    print_subtree(tree[leaf], indent + 1)

"""
For any tree or subtree, pick colors to represent the different categories.
This works best when there are a small number of categories.
"""
def pick_colors(tree):
  # At the top level, pick bold colors around the color wheel  
  # There are probably better ways to do this,


#for inpath in os.listdir(data_dir):
inpath = 'ingredients_10000-20000.json'

infile = open(data_dir + os.sep + inpath)
for line in infile:
  recipe = json.loads(line)
  category = recipe['category'].split('>')[1:] # Drop the "Home"

  subcat = categories
  for c in category:
    if c not in subcat:
      print "Adding subcategory " + c
      subcat[c] = {}

    # Now we've ensured the category exists, keep digging down
    subcat = subcat[c]

embed()

print_subtree(categories, 0)

