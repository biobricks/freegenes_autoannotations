SELECT tk.name as toolkit, d.gene_id as gene_id, d.name as name, d.long_name as long_name, d.notes as description, t.url as uniprot_id, u.url as ncbi_gene_id, 
x.url as ncbi_protein_id, y.url as genbank_source

FROM dna as d 
LEFT JOIN (SELECT r.url as url, dr.dna_id as gene_id FROM ref as r JOIN dna_ref as dr ON dr.ref_id=r.url WHERE r.reftype = 'uniprot') as t on t.gene_id = d.gene_id
LEFT JOIN (SELECT r.url as url, dr.dna_id as gene_id FROM ref as r JOIN dna_ref as dr ON dr.ref_id=r.url WHERE r.reftype = 'ncbi_gene_id') as u on u.gene_id = d.gene_id
LEFT JOIN (SELECT r.url as url, dr.dna_id as gene_id FROM ref as r JOIN dna_ref as dr ON dr.ref_id=r.url WHERE r.reftype = 'ncbi_protein_id') as x on x.gene_id = d.gene_id
LEFT JOIN (SELECT r.url as url, dr.dna_id as gene_id FROM ref as r JOIN dna_ref as dr ON dr.ref_id=r.url WHERE r.reftype = 'genbank_source') as y on y.gene_id = d.gene_id

JOIN toolkits_dna as td on td.dna = d.gene_id
JOIN toolkits as tk on tk.id = td.toolkit_id

WHERE tk.name IN ('E. coli essential genes (20 sense codon recoding)','JCVI-Syn3.0 genes (E. coli codon optimized)','Mesoplasma florum genes (E. coli codon optimized)',
                  'Bacillus subtilis genes (E. coli codon optimized)','Mycoplasma pneumoniae genes (E. coli codon optimized)',
                  'Mycoplasma genitalium genes (E. coli codon optimized)')

ORDER BY toolkit
;

