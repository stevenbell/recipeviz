# Make a plot of all the IDs, and whether they were a real recipe, a 404, or the
# infamous Johnsonville Italian Style Three Cheese Chicken Sausage Skillet Pizza
# Steven Bell <sebell@stanford.edu>

import os
import json
import numpy as np
import matplotlib.pyplot as plt
from IPython import embed

min_id = 0
max_id = 260000
plot_width = 350
data_dir = 'scraped'

colormap = json.load(open('colormap.json'))

rows = int(np.ceil(float(max_id - min_id) / plot_width))
img = np.zeros([rows, plot_width, 3], dtype=np.float32)

for inpath in os.listdir(data_dir):
  infile = open(data_dir + os.sep + inpath)
  for line in infile:
    recipe = json.loads(line)
    x = (recipe['number'] - min_id) % plot_width
    y = (recipe['number'] - min_id) / plot_width
  
    if recipe['name'] == u"Johnsonville\xae Three Cheese Italian Style Chicken Sausage Skillet Pizza":
      img[y, x, :] = [0.3, 0.3, 0.3]
    else:
      # Color based on the category
      # TODO: handle subcategories?
      cat_tree = recipe['category'].split('>')
      if len(cat_tree) > 2 and cat_tree[2] in colormap:
        img[y, x, :] = colormap[cat_tree[2]]
      else:
        # print recipe['name']
        # print cat_tree
        img[y, x, :] = [0.8, 0.8, 0.8]

plt.imshow(img)

ticks = np.arange(min_id, max_id, 20000)
ticks_loc = ticks / plot_width
plt.yticks(ticks_loc, ticks)
plt.xticks([])

# Plot a lengend
# from matplotlib.patches import Rectangle
# plt.figure()
# ax = plt.gca()
# for i,c in enumerate(colormap.keys()):
#   ax.add_patch(Rectangle([0.3,i], 0.7, 0.7, color=colormap[c]))
#   plt.text(1.2, i, c)
# 
# plt.ylim([0, len(colormap.keys())])
# plt.xlim([0, 3])
# plt.show()

plt.imsave('matrix.png', img)

