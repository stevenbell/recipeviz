# Scrape allrecipes.com and extract recipes
# Steven Bell <sebell@stanford.edu>
# 18 November 2016

from IPython import embed
from lxml import html
import requests
import time

# Individual recipes are at
# http://allrecipes.com/recipe/[NUMBER]/[...]

# A quick perusal of the website shows numbers between ~1000 and 250000.
# Not all numbers are valid; there is probably some kind of numbering scheme
# based on the category.

outfile = open('ingredients.csv', 'w')
outfile.write('id,name,ingredients\n')

for number in range(9500, 10500):
  url = "http://allrecipes.com/recipe/%d" % number

  try:
    page = requests.get(url)

    # tmp = open('%d.html' % number, 'w')
    # tmp.write(page.content)
    # tmp.close()

    document = html.fromstring(page.content)
  
    name = document.xpath('//h1[@class="recipe-summary__h1"]/text()')[0]
  
    inglines = document.xpath('//span[@class="recipe-ingred_txt added"]')
    ingredients = [i.xpath('text()')[0] for i in inglines]
  
    outfile.write('%d,"%s","%s"\n' % (number, name, str(ingredients)))
    print name
  
  except Exception as e:
    print e
    print url

  time.sleep(1) # Rate limit, to be nice

