
# PyRice - a Python package for query rice gene information

## Install from source:

- Clone project from Github:
  ```
  git clone https://github.com/SouthGreenPlatform/PyRice.git
  ```
## Install from PyPI

- Use pip to install package PyRice (the newest version)
    ```
    pip install pyrice
    ```
    
- Now there are 2 versions available:
    
    - Version 0.1.6: Addition of crawling JavaScript data with Selenium.
        * If you want to use Selenium, please follow these steps:
            + Please check carefully the current version of Chrome on your computer before downloading
            + Download the [Chrome driver](https://chromedriver.chromium.org/downloads).
            + After downloading, fill the file path lead to Chrome driver before querying:
                ```py
                from pyrice import utils
                utils.chrome_path = "the path of your Chrome driver"
                ```
    - Version 0.1.5: Crawl data without Selenium.
    

 ## Instruction 

### Example of system search_gene

```python
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

```python
from pyrice.multi_query import MultiQuery

query = MultiQuery()
result = query.query_by_chromosome(chro="chr01", start_pos="1", end_pos="20000", 
                                   number_process = 4, multi_processing=True,
                                   multi_threading=True, dbs="all")

query.save(result, save_path="./result/",
           format=["csv", "html", "json", "pkl"], hyper_link=False)
print("Output database:", result)
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
```python
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
```python
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
from pyrice.build_dictionary import update_gene_dictionary, update_rapdb_oryzabase

update_gene_dictionary()
update_rapdb_oryzabase(rapdb_url, oryzabase_url)
```

### Example of Search Module
**You have to save file as .pkl and re-load it again to use search function.**

```python
from pyrice import utils 
import pandas as pd

df1 = pd.read_pickle("./result1/data/db.pkl")
df2 = pd.read_pickle("./result2/data/db.pkl")
df = pd.concat([df1,df2])
result = utils.search(df,"Amino acid ")
```

### Example of SQL Query
You can execute a SQL query over a pandas dataframe.
You have to install package [Pandasql](<https://pypi.org/project/pandasql/>). The variable name is same with the table name in SQL query.
Next, follow the code below to run SQL query:
```python
import pandas as pd
from pandasql import sqldf

data = pd.read_pickle("./result/data/db.pkl")
data = data.astype(str)
sql = "SELECT * FROM data WHERE `oryzabase.CGSNL Gene Symbol` = 'TLP27' or `gramene.system_name` = 'oryza_sativa'"
pysqldf = lambda q: sqldf(q, globals())
print(pysqldf(sql))
```
**The variable name must be same with the table name in SQL query.**

## List of supported database

* Oryzabase
* RapDB
* Gramene
* IC4R
* SNP-Seek
* Funricegene
* MSU
* EMBL-EBI
* GWAS_ATLAS

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
