# Read a recipe and attempt to convert it to masses of known ingredients.
# Steven Bell <sebell@stanford.edu>
# 19 November 2016

from csv import DictReader
import re # Regular expressions
from enum import Enum
from IPython import embed
from ingredientmap import ingredient_remap,adjectives

def parse_amount(ing):
  # Assume that the amount is at the beginning of the line

  # Whole number plus a fraction, e.g., 1 1/2 cups flour
  s = re.match('\d+ \d+/\d+', ing)
  if s is not None:
    (whole, fraction, rem) = ing.strip().split(' ', 2)
    coeff = fraction.split('/')
    amount = float(whole) + float(coeff[0]) / float(coeff[1])
    return (amount, rem)

  # Regular fraction, e.g., 3/4 cup sugar
  s = re.match('\d+/\d+', ing)
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

  # Convert volume units to ml
  volumeunits = {'cup':236.6, 'cups':236.6, 'c':236.6,
                 'teaspoon':4.929, 'teaspoons':4.929, 't':4.929,
                 'tablespoon':14.79, 'tablespoons':14.79, 'T':14.79,
                 'pinch':0.308 }

  # Convert mass units to grams
  massunits = {'ounce':28.34, 'ounces':28.34, 'oz':28.34,
               'pound':453.6, 'pounds':453.6, 'lb':453.6,
               'gram':1.0, 'grams':1.0,
               'kilogram':1000.0, 'kilograms':1000.0}

  (unit, rem) = ing.strip().split(' ', 1)
  if unit in volumeunits:
    return (volumeunits[unit], 'volume', rem)
  elif unit in massunits:
    return (massunits[unit], 'mass', rem)
  else:
    return (None, None, ing) 

  # TODO: what about ounces?
  # print "Not cool, imperialists!"


ing_reader = DictReader(open('knowningredients.csv'))
ingredient_details = [row for row in ing_reader]
known_ingredients = [i['ingredient'] for i in ingredient_details]

def parse_ingredient(ing):
  # If there's a comma, strip off the adjectives to the right
  ing = ing.split(',')[0]
  # Convert to lowercase
  ing = ing.lower()

  # Remove other adjectives, e.g., chopped, diced, etc.
  words = ing.split()
  ing = ' '.join([w for w in words if w not in adjectives])

  # TODO: deal with plurals properly (maybe using NLTK?)
  if ing.endswith('es'):
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

  return None

dr = DictReader(open('ingredients_testing.csv'))

for row in dr:

  print row['name']
  ingredients = eval(row['ingredients'])
  for ing in ingredients:
  
    (amount, remainder) = parse_amount(ing)
    if amount is None:
      print ing
      continue
    
    (unit, utype, remainder) = parse_unit(remainder)
    if unit is None:
      print "[%0.1f] %s" % (amount, remainder)
      # TODO: don't just continue
      continue

    ingredient = parse_ingredient(remainder)
    if ingredient is None:
      print "Can't identify %s" % remainder
      continue

    if utype is 'volume':
      print "[%0.2f ml] %s" % (amount*unit, ingredient)
    else:
      print "[%0.2f g] %s" % (amount*unit, ingredient)
  
  print "--------"
    #embed()
    # TODO: logic to convert ingredients to mass (grams)
    # It would be nice to keep the info about volume, because the user will think
    # about liquids in volumes.
  
    # If we can't read it, just give up, print the offending line, and move on
  
    # Assume ingredients are already lowercase; if not: ing = ing.lower();
  
  # TODO: handle plurals of things which are counted, e.g., eggs

