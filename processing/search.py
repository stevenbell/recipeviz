# Search for a particular keyword or category, and generate the information
# for a visualization
# Steven Bell <sebell@stanford.edu>

import json
import csv
import codecs # For writing unicode
#from IPython import embed

inpath = 'ingredients_simplified.json'
outpath = 'ingredients_matrix.csv'
infile = open(inpath)

# Spin through the database and select the matching ones
keyword = 'cookie'

all_ingredients = ['name']
# Sort ingredients by popularity; keep only the top few
# Use 2x the median number of ingredients

all_recipes = []

for line in infile:
  row = json.loads(line)
  # TODO: better filtering - perhaps based on category, multiple keywords,
  # wildcard matching, etc.
  if keyword in row['name'].lower():
    for ing in row['ingredients']:
      if ing['item'] not in all_ingredients:
        all_ingredients.append(ing['item'])

    # Transform from {'item':'cheese', 'amount':30.2} to {'cheese':30.2}
    ingredient_remap = {ing['item']:ing['amount'] for ing in row['ingredients']}
    ingredient_remap['name'] = row['name']
    all_recipes.append(ingredient_remap)

# Write a CSV file for the top ingredients, putting "-1" where it's not used,
# and ignoring any extra ingredients.

outfile = csv.DictWriter(codecs.open(outpath, encoding='utf-8', mode='w'), all_ingredients, restval=0)
outfile.writeheader()
outfile.writerows(all_recipes)

#json.dump(all_recipes, open(outpath, 'w'))

