import pandas as pd
import psycopg2
from seqhash import seqhash
import gzip
from jsonslicer import JsonSlicer
import json
import time
from collections import Counter

start = time.perf_counter()

# Postgres connection string
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

with open('data.json') as f:
    data = json.load(f)

true_organisms = ['Escherichia coli (strain K12)',
                  'Mesoplasma florum (strain ATCC 33453 / NBRC 100688 / NCTC 11704 / L1)',
                 'Bacillus subtilis (strain 168)',
                 'Mycoplasma mycoides subsp. capri',
                 'Mycoplasma pneumoniae (strain ATCC 29342 / M129)',
                 'Mycoplasma genitalium (strain ATCC 33530 / G-37 / NCTC 10195)']
real_dict = {}

for k,v in data.items():
    real_dict[k] = [x for x in v if x['organism'] in true_organisms]

for k,v in real_dict.items():
    if len(v) > 1:
        v0 = v[0].get('description')
        v1 = v[1].get('description')
        
        if v0 == None:
            v0 = []
        if v1 == None:
            v1 = []
        
        if len(v0) > len(v1):
            real_dict[k] = [v[0]]
        else:
            real_dict[k] = [v[1]]
            
single_dict = {}
for k,v in real_dict.items():
    if len(v) > 0:
        single_dict[k] = v[0]
    
for k,v in single_dict.items():
    l = single_dict[k]['possible_names']
    name = l[0]
    for x in l:
        if len(name) < len(x):
            name = x
    single_dict[k]['name'] = name
    single_dict[k]['bbf_gene_id'] = d[k]


for k,v in single_dict.items():
    cursor.execute("UPDATE dna SET notes = %s, long_name = %s WHERE gene_id = %s", (v['description'],v['name'],v['bbf_gene_id']))
conn.commit()


for k,v in single_dict.items():
    if v['organism'] == 'Escherichia coli (strain K12)':
        check_df = pd.read_sql("SELECT * FROM ref JOIN dna_ref ON ref.url = dna_ref.ref_id WHERE dna_ref.dna_id = '{}'".format(v['bbf_gene_id']), p)
        if 'ncbi_gene_id' not in check_df['reftype'].tolist():
            if v['gene_id'] != None:
                cursor.execute("INSERT INTO ref (url, name, date, reftype) VALUES (%s,%s,%s,%s)", ('https://www.ncbi.nlm.nih.gov/gene/{}'.format(v['gene_id']),
                                                                                              '{} gene id'.format(v['bbf_gene_id']),
                                                                                              '2020',
                                                                                              'ncbi_gene_id'))
                cursor.execute('INSERT INTO dna_ref (ref_id,dna_id) VALUES (%s,%s)', ('https://www.ncbi.nlm.nih.gov/gene/{}'.format(v['gene_id']),
                                                                                v['bbf_gene_id']))
        if 'uniprot' not in check_df['reftype'].tolist():
            cursor.execute("INSERT INTO ref (url, name, date, reftype) VALUES (%s,%s,%s,%s)", ('https://www.uniprot.org/uniprot/{}'.format(v['accession']),
                                                                                              '{} uniprot id'.format(v['bbf_gene_id']),
                                                                                              '2020',
                                                                                              'uniprot'))
            cursor.execute('INSERT INTO dna_ref (ref_id,dna_id) VALUES (%s,%s)', ('https://www.uniprot.org/uniprot/{}'.format(v['accession']),
                                                                                v['bbf_gene_id']))
conn.commit()


end = time.perf_counter()

print(end-start)


