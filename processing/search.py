# Search for a particular keyword or category, and generate the information
# for a visualization
# Steven Bell <sebell@stanford.edu>

import json
import csv
import codecs # For writing unicode
#from IPython import embed

inpath = 'ingredients_simplified.json'
outpath = 'ingredients_matrix.json'
infile = open(inpath)

# Spin through the database and select the matching ones
keyword = 'cookie'

# Sort ingredients by popularity; keep only the top few
# Use 2x the median number of ingredients

all_recipes = []

# Reads file to find the most popular ingredients
ingredient_counter = {}

for line in infile:
  row = json.loads(line)
  if keyword in row['name'].lower():
    for ing in row['ingredients']:
      if ing['item'] not in ingredient_counter:
        ingredient_counter[ing['item']] = 0
      else:
        ingredient_counter[ing['item']] += 1

#print ingredient_counter

popular = sorted(ingredient_counter, key=ingredient_counter.get, reverse = True)
all_ingredients = popular[:4]
all_ingredients.append('name')

#print all_ingredients

infile = open(inpath)

for line in infile:
  row = json.loads(line)
  # TODO: better filtering - perhaps based on category, multiple keywords,
  # wildcard matching, etc.
  if keyword in row['name'].lower():
    #for ing in row['ingredients']:
      #if ing['item'] not in all_ingredients: #commented out for controlled ingredient list
        #all_ingredients.append(ing['item'])

    # Transform from {'item':'cheese', 'amount':30.2} to {'cheese':30.2}
    #ingredient_remap = {ing['item']:ing['amount'] for ing in row['ingredients']}

    # Only add ingredients fron all_ingredients list into the matrix
    ingredient_remap = {'name':row['name']}
    ingredient_remap['link'] = 'allrecipes.com/recipe/' + str(row['number']);
    for ing in row['ingredients']:
      if ing['item'] in all_ingredients:
        ingredient_remap[ing['item']] = ing['amount']

    # Add keys for all remaining, unused ingredients, with -1 for value -- change this?
    for i in all_ingredients:
      if i not in ingredient_remap:
        ingredient_remap[i] = 0 

    #ingredient_remap['name'] = row['name']

    all_recipes.append(ingredient_remap)

# Write a CSV file for the top ingredients, putting "-1" where it's not used,
# and ignoring any extra ingredients.

#outfile = csv.DictWriter(codecs.open(outpath, encoding='utf-8', mode='w'), all_ingredients, restval=0)
#outfile.writeheader()
#outfile.writerows(all_recipes)

json.dump(all_recipes, open(outpath, 'w'))

