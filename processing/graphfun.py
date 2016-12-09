# Read in a JSON ingredient file and build a matrix
# Steven Bell <sebell@stanford.edu>

import json
import numpy as np
import matplotlib.pyplot as plt
from IPython import embed

inpath = 'ingredients_simplified.json'

# Do this in two passes; one to get all the ingredients and count the recipes,
# and a second to populate the matrix.

all_ingredients = []
all_recipes = []

infile = open(inpath)
for line in infile:
  row = json.loads(line)
  all_recipes.append(row['name'])

  for ing in row['ingredients']:
    if ing['item'] not in all_ingredients:
      all_ingredients.append(ing['item'])

# Now we've got the number of recipes and ingredients; create an empty matrix
# and fill it with the values
ing_matrix = np.zeros([len(all_recipes), len(all_ingredients)])

infile = open(inpath)
recipe_num = 0 # Used as a counter to index rows
for line in infile:
  row = json.loads(line)
  for ing in row['ingredients']:
    ing_matrix[recipe_num, all_ingredients.index(ing['item'])] = ing['amount']
  recipe_num += 1

# Normalize the ingredient lists

# We have all the ingredients in a matrix, run PCA
# The first two columns of V are the principal components
#(U, S, V) = np.linalg.svd(ing_matrix, full_matrices=False)
#pca = np.dot(U, np.dot(np.diag(S), V[:, 0:2]))

x_ing = 'all-purpose flour'
y_ing = 'baking soda'

x = ing_matrix[:, all_ingredients.index(x_ing)]
y = ing_matrix[:, all_ingredients.index(y_ing)]

plt.scatter(x, y);
# for ii in range(len(x)):
#   plt.text(x[ii], y[ii], all_recipes[ii])

plt.xlabel(x_ing)
plt.ylabel(y_ing)

plt.show()

