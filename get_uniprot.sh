wget ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.xml.gz
wget ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_trembl.xml.gz

gzip -d -c uniprot_sprot.xml.gz | xml-to-json-fast | gzip > uniprot_sprot.json.gz
gzip -d -c uniprot_trembl.xml.gz | xml-to-json-fast | gzip > uniprot_trembl.json.gz
