# FreeGenes Auto-annotation scripts

Steps:
1. Fill Postgresql database with translation data [Note: this can also be subsituted with a list of IDs and translations. Modify json_db.py accordingly]
2. Download [xml-to-json-fast](https://github.com/sinelaw/xml-to-json-fast). This program is necessary for conversion of XML files to JSON files.
3. Run `get_uniprot.sh` (this should take a while). This will download and covert full dumps of uniprot to JSON.
4. Run json_db.py (this should take a while). This script will iterate through the uniprot data dumps and save potentially relevant annotations.
5. Run update_db.py (this should take a little while). This script will choose the proper annotations from the relevant annotations, and if there is nothing there, apply the annotations to the postgres database. This can also be replaced with scripts that convert to different data types, like CSV files. The important part is the sorting of potentially relevant annotations.

An example postgres dump is provided for schema. 

