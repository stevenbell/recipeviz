# Make a plot of all the IDs, and whether they were a real recipe, a 404, or the
# infamous Johnsonville Italian Style Three Cheese Chicken Sausage Skillet Pizza
# Steven Bell <sebell@stanford.edu>

import os
import json
import numpy as np
import matplotlib.pyplot as plt
from IPython import embed

min_id = 0
max_id = 180000
plot_width = 300

rows = int(np.ceil(float(max_id - min_id) / plot_width))
img = np.zeros([rows, plot_width, 3], dtype=np.float32)

for inpath in os.listdir('scraped'):
  infile = open(inpath)
  for line in infile:
    recipe = json.loads(line)
    x = (recipe['number'] - min_id) % plot_width
    y = (recipe['number'] - min_id) / plot_width
  
    if recipe['name'] == u"Johnsonville\xae Three Cheese Italian Style Chicken Sausage Skillet Pizza":
      img[y, x, :] = [0.7, 0.0, 0.0]
    else:
      img[y, x, :] = [0.1, 0.3, 0.9]
    
plt.imshow(img)
plt.show()

plt.imsave('matrix.png', img)

