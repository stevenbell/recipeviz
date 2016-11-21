# Scrape allrecipes.com and extract recipes
# Steven Bell <sebell@stanford.edu>
# 18 November 2016

from IPython import embed
from lxml import html
import requests
import time
import codecs # Write unicode files

# Individual recipes are at
# http://allrecipes.com/recipe/[NUMBER]/[...]

# A quick perusal of the website shows numbers between ~1000 and 250000.
# Not all numbers are valid; there is probably some kind of numbering scheme
# based on the category.

# Don't overwrite, just append, which we can fix manually later
outfile = codecs.open('ingredients.csv', encoding='utf-8', mode='w+')
outfile.write('id,name,category,ingredients\n')

for number in range(12500, 15500):
  url = "http://allrecipes.com/recipe/%d" % number

  try:
    page = requests.get(url)
    if page.status_code == 404:
      print "404: %s" % url
      continue

    document = html.fromstring(page.content)
  
    name = document.xpath('//h1[@class="recipe-summary__h1"]/text()')[0]

    categorybits = document.xpath('//ul[@class="breadcrumbs breadcrumbs"]/li/a/span[@itemprop="title"]/text()')
    category = '>'.join([c.strip() for c in categorybits])

    inglines = document.xpath('//span[@class="recipe-ingred_txt added"]')
    ingredients = [i.xpath('text()')[0] for i in inglines]
  
    outfile.write('%d,"%s","%s","%s"\n' % (number, name, category, str(ingredients)))
    print name
  
  except Exception as e:
    print e
    print url

  time.sleep(1) # Rate limit, to be nice

