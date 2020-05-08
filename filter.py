#!/usr/bin/python3
import json
sites_to_remove = []
with open("./kaushik_sivashankar.csv") as reference:
    for line in reference:
        sites_to_remove.append(line.rstrip())
with open("./data.json") as allsites:
    sites = json.load(allsites)
print(sites_to_remove)
topop=[]
for element in sites:
    if sites[element]["urlMain"] in sites_to_remove:
        topop.append(element)
for element in topop:
    sites.pop(element)

with open("./new_data.json","w+") as newfile:
    json.dump(sites, newfile, indent = 4)
