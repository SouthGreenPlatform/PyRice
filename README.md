
# Python query engine for PyRice package

## Instruction for install package on git (on products branch only)

- Clone project on PyRice `master` branch
  ```
  git clone https://github.com/SouthGreenPlatform/PyRice.git
  ```
## Instruction for install package on pypi

- Use pip to install package PyRice
    ```
    pip install pyrice
    ```
 
 ## Instruction 

### Example of system search_gene

```py
from pyrice.multi_query import MultiQuery

query = MultiQuery()
result = query.search_on_chromosome(chro="chr01", start_pos="1", end_pos="20000",
                                    number_process = 4, dbs="all", save_path="./result/")
print("Output database:", result)
```
```bash
Output database:
{'OsNippo01g010050': {
    'msu7Name': {'LOC_Os01g01010'},
    'raprepName': {'Os01g0100100'},
    'contig': 'chr01', 'fmin': 2982,
    'fmax': 10815},
'OsNippo01g010150': {
    'msu7Name': {'LOC_Os01g01019'},
    'raprepName': {'Os01g0100200'},
    'contig': 'chr01',
    'fmin': 11217,
    'fmax': 12435},
...
'OsNippo01g010300': {
    'msu7Name': {'LOC_Os01g01040'},
    'raprepName': {'Os01g0100500'},
    'contig': 'chr01',
    'fmin': 16398,
    'fmax': 20144}
}
```

### Example of system query_by_chromosome

```py
from pyrice.multi_query import MultiQuery

query = MultiQuery()
result = query.query_by_chromosome(chro="chr01", start_pos="1", end_pos="20000", 
                                   number_process = 4, multi_processing=True,
                                   multi_threading=True, dbs="all")

query.save(result, save_path="./result/",
           format=["csv", "html", "json", "pkl"], hyper_link=False)
print("Output database:", db)
```
```bash
Output database:
{'OsNippo01g010050': {
    'rapdb': {
        'Locus_ID': 'Os01g0100100',
        'Description': 'RabGAP/TBC domain containing protein.',
            'Oryzabase Gene Name Synonym(s)': 'Molecular Function: Rab GTPase activator activity (GO:0005097)',
            ...},
        'gramene': {
            '_id': 'Os01g0100100',
            'name': 'Os01g0100100',
            'biotype': 'protein_coding',
            ...},
        ...},
    'OsNippo01g010150': {
        'rapdb': {...},
        'gramene': {...},
        ...},
    ...
}
```

### Example of system query_by_ids
```py
from pyrice.multi_query import MultiQuery
		
query = MultiQuery()
result = query.query_by_ids(ids=["Os08g0164400", "Os07g0586200"],
                            locs=["LOC_Os10g01006", "LOC_Os07g39750"],
                            irics=["OsNippo01g010050", "OsNippo01g010300"],
                            number_process = 4, multi_processing=True, multi_threading=True, dbs="all")
query.save(result, save_path = "./result/",
	       format=["csv", "html", "json", "pkl"], hyper_link=False)   
print("Output database:",result)   
```
```bash
Output database:
{'OsNippo01g010050': {
        'rapdb': {
            'Locus_ID': 'Os01g0100100',
            'Description': 'RabGAP/TBC domain containing protein.',
            'Position': '',
            ...},
        'ic4r': {
            'Anther_Normal': {'expression_value': '0.699962'},
            'Anther_WT': {'expression_value': '13.9268'},
            ...},
        ...},
    'OsNippo01g010300': {
        'rapdb': {...},
        'ic4r': {...},
        ...},
    ...
}            
```
### Example of system query_new_database
```py
from pyrice.multi_query import MultiQuery
    
query = MultiQuery()
result = query.query_new_database(atts=['TRAES3BF001000010CFD'], number_process= 4,
                                  multi_processing=True,multi_threading=True,dbs=['urgi'])
query.save(result, save_path="./result/",
           format=["csv", "html", "json", "pkl"], hyper_link=False) 
print("Output database:",result)                          
```
```bash
Output database:
{'TRAES3BF001000010CFD':
    {'urgi':{
        'recordsTotal': 1177800,
        'recordsFiltered': 1177800,
        'draw': None,
        ...}
    }
}
```
### Example of Build Dictinary Module
```py
from pyrice.build_dictionary import update_gene_dictionary,update_rapdb_oryzabase

update_gene_dictionary()
update_rapdb_oryzabase(rapdb_url, oryzabase_url)
```

### Example of Search Module
You have to save file as .pkl and re-load it again to use search function.

```py
from pyrice.utils import search
import pandas as pd

df1 = pd.read_pickle("./result1/data/db.pkl")
df2 = pd.read_pickle("./result2/data/db.pkl")
df = pd.concat([df1,df2])
result = search(df,"Amino acid ")
```

## List of supported database

* Oryzabase
* RapDB
* Gramene
* IC4R
* SNP-Seek
* Funricegene
* MSU

## List of exception

* Server Exception

    Throw when server response code is not 200.

    Throw with the corresponding server response code.
* Internet Connection Exceptioin

    Throw requests.exceptions.RequestException

    *requests* module exception.
* Timeout Exception

    Throw requests.exceptions.Timeout

    *requests* module exception.
* Database Exception

    Throw when database description is not found.
