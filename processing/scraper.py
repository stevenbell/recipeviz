# Scrape allrecipes.com and extract recipes
# Steven Bell <sebell@stanford.edu>
# 18 November 2016

from IPython import embed
from lxml import html
import requests

# Individual recipes are at
# http://allrecipes.com/recipe/[NUMBER]/[...]

# Not clear what numbers are valid

number = 23750

url = "http://allrecipes.com/recipe/%d" % number

try:
  page = requests.get(url)
  document = html.fromstring(page.content)

  name = document.xpath('//h1[@class="recipe-summary__h1"]/text()')[0]

  inglines = document.xpath('//span[@class="recipe-ingred_txt added"]')
  ingredients = [i.xpath('text()')[0] for i in inglines]

  print "-----"
  print name
  print ingredients

except:
  print url
  exit()

