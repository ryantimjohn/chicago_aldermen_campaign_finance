import os
from pdf2image import convert_from_path

directory = os.fsencode("C:/gd/Projects/chicago_aldermen_campaign_finance/infographics")

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith('.pdf'):
        print('Working on: ' + filename)
        images = convert_from_path(filename)
        images[0].save(filename.split('.')[0] + '.png')

