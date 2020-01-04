import os
import sys
import numpy as np
import pandas as pd
from datetime import datetime
from pprint import pprint

def get_array(given_field):
    given_field = str(given_field)
    arr = []
    if not given_field:
        return arr
    if given_field == 'nan':
        return arr
    # print("Processing:", given_field)
    if ',' in given_field:
        arr = [x.strip() for x in given_field.split(',')]
    else:
        arr.append(given_field)
    return arr


date = datetime.now()
print("Before reading the data:", date)
filter = ['region', 'country', 'state', 'commod1', 'prod_size', 'ore', 'gangue']
print("My filtered columns are:", filter)
df = pd.read_csv("mrds.csv", low_memory=False, usecols=filter)
date = datetime.now()
print("After  reading the data:", date)
print(df.head())

print("Just checking for the LARGE production size:")
ndf = df[df['prod_size']== 'L'] # new datafrom
test_df = ndf.head()

hash            = {}
hash['country'] = {}
hash['state']   = {}

# replace ndf with test_df for all your debug. else it will be a mess!
for tup in ndf.itertuples(): # tup is a tuple
    # print("Handling:", tup)
    state     = str(tup[3])+" in "+ str(tup[2])
    country   = str(tup[2])
    elements  = str(tup[4])
    ores      = str(tup[6])
    gangues   = str(tup[7])

    name_match             = {}
    name_match['elements'] = elements
    name_match['ores']     = ores
    name_match['gangues']  = gangues

    region_match            = {}
    region_match['country'] = country
    region_match['state']   = state

    for key, value in name_match.items():
        for x in get_array(value):
            for k, v in region_match.items():
                if v not in hash[k]:
                    hash[k][v] = {}
                if not key in hash[k][v]:
                    hash[k][v][key] = []
                # print("Debug", x, k, v, key, value)
                if x not in hash[k][v][key]:
                    hash[k][v][key].append(x)
# pprint(hash)

for r in ['country', 'state']:
    for i in ['elements', 'ores', 'gangues']:
        filename = 'gen__'+r+'__'+i+'.csv'
        filename = filename.replace(" ", "")
        with open(filename, 'w+') as fd:
            fd.write(r+','+i+'\n')
            for region in hash[r].keys():
                # print("Debug1:", r, i, region)
                if i in hash[r][region]:
                    st = ','.join(hash[r][region][i])
                    # print("Debug2:", st)
                    fd.write(region+',"'+st+'"\n')

date = datetime.now()
print("Completed execution at:", date)
