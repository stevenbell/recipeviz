# Read a recipe and attempt to convert it to masses of known ingredients.
# Steven Bell <sebell@stanford.edu>
# 19 November 2016

import mysql.connector
import re # Regular expressions
from enum import Enum
from IPython import embed

def parse_amount(ing):
  # Assume that the amount is at the beginning of the line

  # Whole number plus a fraction, e.g., 1 1/2
  s = re.match('\d+ \d+/\d+', ing)
  if s is not None:
    (whole, fraction, rem) = ing.strip().split(' ', 2)
    coeff = fraction.split('/')
    amount = float(whole) + float(coeff[0]) / float(coeff[1])
    return (amount, rem)

  # Regular fraction
  s = re.match('\d+/\d+', ing)
  if s is not None:
    fraction = ing[0:s.end()]
    coeff = fraction.split('/')
    amount = float(coeff[0]) / float(coeff[1])
    return (amount, ing[s.end():])

  # Counted object
  s = re.match('\d+', ing)
  if s is not None:
    amount = float(ing[0:s.end()])
    return (amount, ing[s.end():])

  # All else failed; just return None
  return (None, ing)


def parse_unit(ing):
  # TODO: need to specify whether we're returning volume units or mass units
  # An ingredient line *should* consist of [number/fraction, unit, ingredient],
  # or just of [number, ingredient].  In some cases, there might be
  # [unit, ingredient], as in "dash of salt"

  # Convert volume units to ml
  volumeunits = {'cup':236.6, 'cups':236.6, 'c':236.6,
                 'teaspoon':4.929, 'teaspoons':4.929, 't':4.929,
                 'tablespoon':14.79, 'tablespoons':14.79, 'T':14.79 }

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


config = {
  'user': 'recipes',
  'password': 'cookies',
  'host': 'localhost',
  'database': 'recipedb',
  'raise_on_warnings': True,
}

# Open the database
database = mysql.connector.connect(**config)
cursor = database.cursor()

# Get ingredients
cursor.execute("SELECT ingredients FROM cooking_recipes_reformat LIMIT 10")

for result in cursor:

  ingredients = eval(result[0])
  for ing in ingredients:
  
    (amount, remainder) = parse_amount(ing)
    if amount is None:
      print ing
      continue
    
    (unit, utype, remainder) = parse_unit(remainder)
    if unit is None:
      print "[%0.1f] %s" % (amount, remainder)
      continue

    if utype is 'volume':
      print "[%0.2f ml] %s" % (amount*unit, remainder)
    else:
      print "[%0.2f g] %s" % (amount*unit, remainder)
  
  print "--------"
    #embed()
    # TODO: logic to convert ingredients to mass (grams)
    # It would be nice to keep the info about volume, because the user will think
    # about liquids in volumes.
  
    # If we can't read it, just give up, print the offending line, and move on
  
    # Assume ingredients are already lowercase; if not: ing = ing.lower();
  
  # TODO: handle plurals of things which are counted, e.g., eggs

