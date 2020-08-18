import pandas as pd
import psycopg2
from seqhash import seqhash
import gzip
from jsonslicer import JsonSlicer
import json

# Postgres connection string:
p = ""
conn = psycopg2.connect(p)
cursor= conn.cursor()
df = pd.read_sql("SELECT gene_id, translation FROM dna WHERE translation IS NOT NULL", p)

d = {}
for i,row in df.iterrows():
    translation = row['translation']
    if translation[-1] == "*":
        translation = translation[:-1]
    d[seqhash(translation)] = row['gene_id'] 

entries = []
for organization in ["sprot", "trembl"]:
    with gzip.open("uniprot_{}.json.gz".format(organization), "rt") as data:
        for entry in JsonSlicer(data, ('items', None)):
            for item in entry['items']:
                if type(item) == dict:
                    if item["name"] == "sequence":
                        seq = item["items"][0]
            if d.get(seqhash(seq)) != None:
                entries.append(entry)

new_dict = {}
for entry in entries:
    accession = None
    possible_names = []
    access = None
    organism = None
    gene_id = None
    description = None
    seq = None
    for item in entry['items']:
        if item['name'] == 'name':
            name = item['items'][0]
        if item['name'] == 'accession':
            accession = item['items'][0]
        if item['name'] == 'protein':
            for i in item['items'][0]['items']:
                possible_names.append(i['items'][0])
        if item['name'] == 'organism':
            for i in item['items']:
                if i.get('attrs') != None:
                    if i['attrs'].get('type') == 'scientific':
                        organism = i['items'][0]
        if item['name'] == 'dbReference':
            if item.get('attrs') != None:
                if item['attrs'].get('type') == 'GeneID':
                    gene_id = item['attrs']['id']
        if item['name'] == 'comment':
            if item.get('attrs') != None:
                if item['attrs'].get('type') == 'function':
                    for i in item['items']:
                        if i['name'] == 'text':
                            description = i['items'][0]
        if item["name"] == "sequence":
            seq = item["items"][0]
    # Get uniprot, short name, full_name
    if new_dict.get(seqhash(seq)) == None:
        new_dict[seqhash(seq)] = []
    new_dict[seqhash(seq)].append({
        "accession": accession,
        "possible_names": possible_names,
        "organism": organism,
        "gene_id": gene_id,
        "description": description
    })

with open('data.json', 'w') as outfile:
    json.dump(new_dict, outfile)

