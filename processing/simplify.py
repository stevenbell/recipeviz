# Read a recipe and attempt to convert it to masses of known ingredients.
# Steven Bell <sebell@stanford.edu>
# 19 November 2016

import os # Searching directories
from csv import DictReader
import re # Regular expressions
import json
import codecs # For writing unicode in log files
#from IPython import embed
from ingredientmap import ingredient_remap,adjectives

data_dir = 'scraped' # Path to a directory of recipe JSON files
outpath = 'ingredients_simplified.json' # Single output file for recipes
errpath = 'ingredients_missing.txt' # Log file for missing ingredients

def parse_amount(ing):
  # Assume that the amount is at the beginning of the line

  # Whole number plus a fraction, e.g., 1 1/2 cups flour
  s = re.match('\d+ \d+/\d+ ', ing) # require a space between amount and the rest
  if s is not None:
    (whole, fraction, rem) = ing.strip().split(' ', 2)
    coeff = fraction.split('/')
    amount = float(whole) + float(coeff[0]) / float(coeff[1])
    return (amount, rem)

  # Regular fraction, e.g., 3/4 cup sugar
  s = re.match('\d+/\d+ ', ing)
  if s is not None:
    fraction = ing[0:s.end()]
    coeff = fraction.split('/')
    amount = float(coeff[0]) / float(coeff[1])
    return (amount, ing[s.end():])

  # TODO: Number with a size, e.g., "1 (8 ounce) package cream cheese"
  # Pull out the numbers, remove the closing paren, and let the unit parser
  # do its part.

  # Counted object, e.g., 2 eggs
  s = re.match('\d+', ing)
  if s is not None:
    amount = float(ing[0:s.end()])
    return (amount, ing[s.end():])

  # All else failed; just return None
  return (None, ing)


def parse_unit(ing):
  # An ingredient line *should* consist of [number/fraction, unit, ingredient],
  # or just of [number, ingredient].  In some cases, there might be
  # [unit, ingredient], as in "dash of salt"

  # Convert volume units to mlv
  volumeunits = {'gallon':3785.4, 'quart':946.3,
                 'cup':236.6, 'cups':236.6, 'c':236.6,
                 'teaspoon':4.929, 'teaspoons':4.929, 't':4.929,
                 'tablespoon':14.79, 'tablespoons':14.79, 'T':14.79,
                 'pinch':0.308 }

  # Convert mass units to grams
  massunits = {'ounce':28.34, 'ounces':28.34, 'oz':28.34,
               'pound':453.6, 'pounds':453.6, 'lb':453.6,
               'gram':1.0, 'grams':1.0,
               'kilogram':1000.0, 'kilograms':1000.0}

  counters = ['cubes', 'stalks']

  # If there's only one word, it had better be the ingredient
  if not ' ' in ing.strip():
    return (None, None, ing)

  # Split the first word and see if it's a unit
  (unit, rem) = ing.strip().split(' ', 1)
  if unit in volumeunits:
    return (volumeunits[unit], 'volume', rem)
  elif unit in massunits:
    return (massunits[unit], 'mass', rem)
  elif unit in counters:
    return (None, None, rem) # Just drop the counter word
  else:
    return (None, None, ing) 

  # TODO: what about ounces?
  # print "Not cool, imperialists!"


ing_reader = DictReader(open('knowningredients.csv'))
ingredient_details = [row for row in ing_reader]
known_ingredients = [i['ingredient'] for i in ingredient_details]

def parse_ingredient(ing):
  # If there's a comma, strip off the adjectives to the right
  # This is a little dangerous; e.g., "peeled, cored and sliced apples"
  ing = ing.split(',')[0]
  # Convert to lowercase
  ing = ing.lower()

  # Remove other adjectives, e.g., chopped, diced, etc.
  words = ing.split()
  ing = ' '.join([w for w in words if w not in adjectives])

  # TODO: deal with plurals properly (maybe using NLTK?)
  if ing.endswith('ses'):
    ing = ing[:-2]
  elif ing.endswith('s'):
    ing = ing[:-1]

  # Map this to a known ingredient
  while ing in ingredient_remap:
    #print "applying %s -> %s" % (ing, ingredient_remap[ing])
    ing = ingredient_remap[ing]

  # Find the known ingredient that matches this
  if ing in known_ingredients:
    return ing

  # Not an exact match, try searching for a partial match
  else:
    print ing.encode('ascii', 'ignore')
    for k in known_ingredients:
      if k in ing:
        pass
        #print u"Possible match for \"", ing, u"\": ", k

  #print ing
  return None

outfile = open(outpath, 'w')
errfile = codecs.open(errpath, encoding='utf-8', mode='w')

for inpath in os.listdir(data_dir):
  infile = open(data_dir + os.sep + inpath)
  for line in infile:
    row = json.loads(line)
  
    # Ignore the Johnsonville Sausage nonsense
    if row['name'] == u"Johnsonville\xae Three Cheese Italian Style Chicken Sausage Skillet Pizza":
      continue

    #print row['name'].encode('ascii', 'ignore')
    ingredients_simple = []
    for ing in row['ingredients']:
    
      (amount, remainder) = parse_amount(ing)
      if amount is None:
        #print ing
        continue
      
      (unit, utype, remainder) = parse_unit(remainder)
  
      ingredient = parse_ingredient(remainder)
      if ingredient is None:
        errfile.write("Can't identify %s\n" % remainder)
        continue
  
      if unit is None:
        #print "[%0.1f] %s" % (amount, ingredient)
        ingredients_simple.append({'amount':amount, 'type':'counted', 'item':ingredient})
      elif utype is 'volume':
        #print "[%0.2f ml] %s" % (amount*unit, ingredient)
        ingredients_simple.append({'amount':amount*unit, 'type':'volume', 'item':ingredient})
      else:
        #print "[%0.2f g] %s" % (amount*unit, ingredient)
        ingredients_simple.append({'amount':amount*unit, 'type':'mass', 'item':ingredient})
    
    # Normalize to unit mass
    # TODO: need to convert volume/counted units to mass before doing this
    total_mass = sum([i['amount'] for i in ingredients_simple])
    for i in ingredients_simple:
      i['amount'] /= total_mass
    
    row_simple = {'name':row['name'], 'number':row['number'], 'category':row['category'], 'ingredients':ingredients_simple}
  
    json.dump(row_simple, outfile)
    outfile.write('\n')
  
    #print "--------"
 
outfile.close()
errfile.close()

