# Crawl through the recipes we have, and make a tree of all the categories

import os
import json
from IPython import embed
import numpy as np
import matplotlib

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
  # There are probably better ways to do this, but I'm not aware of good ways
  # that generalize to arbitrary numbers of colors
  H = np.linspace(0, 1, len(tree.keys()), endpoint=False)
  S = 0.8
  V = 0.6
  colormap = {}
  for num,name in enumerate(tree):
    rgb = matplotlib.colors.hsv_to_rgb([H[num], S, V])
    colormap[name] = [x for x in rgb] # Convert from numpy array to list for JSON
  # TODO: keep working down the tree
  return colormap

#for inpath in os.listdir(data_dir):
inpath = 'ingredients_10000-20000.json'

infile = open(data_dir + os.sep + inpath)
for line in infile:
  recipe = json.loads(line)
  category = recipe['category'].split('>')[1:] # Drop the "Home"

  subcat = categories
  for c in category:
    if c not in subcat:
      #print "Adding subcategory " + c
      subcat[c] = {}

    # Now we've ensured the category exists, keep digging down
    subcat = subcat[c]

embed()
colorfile = open('colormap.json', 'w')
json.dump(pick_colors(categories['Recipes']), colorfile)

#print_subtree(categories, 0)

