
# PyRice - a Python package for query rice gene information

* [PrePrint version of our paper](https://www.biorxiv.org/content/10.1101/2020.04.20.049742v3)
* [Online documentation](https://pyrice.readthedocs.io/en/latest/pyrice_instruction.html)
* How to cite : [Bioinformatics Application notes](https://doi.org/10.1093/bioinformatics/btaa694)

## Install from source:

- Clone project from Github:
  ```
  git clone https://github.com/SouthGreenPlatform/PyRice.git
  ```
## Install from PyPI


- If you install PyRice on your local machine:
    ```
    pip install pyrice
    ```
    
- Now there is only version available (should use the latest version):
     - Verrsion 0.2.0: Update reference for gene from Oryzabase. Add 2 new databases PlantTFDB for PyRice
        * If you install PyRice on your local machine, please follow these steps:
            + Please check carefully the current version of Chrome on your computer before downloading
            + Download the [Chrome driver](https://chromedriver.chromium.org/downloads).
            + After downloading, fill the file path lead to Chrome driver before querying:
                ```py
                from pyrice import utils
                utils.chrome_path = "the path of your Chrome driver"
                ``` 
  
     - Version 0.1.9: PyRice on Google Colab or other cloud platform. Updating the change output format.
 
     - Version 0.1.8: Addition of crawling JavaScript data with Selenium.
    
**IN PROCESS**: If you want to install the newest demo of PyRice: 
```
!pip install -i https://test.pypi.org/simple/ pyrice
```
         
- To see demo of package: [Demo_PyRice.ipynb](https://github.com/SouthGreenPlatform/PyRice/blob/master/Demo_PyRice.ipynb)
    

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
result = query.query_new_database(atts=['AT4G32150'], number_process= 4,
                                  multi_processing=True,multi_threading=True,dbs=['planteome'])
query.save(result, save_path="./result/",
           format=["csv", "html", "json", "pkl"], hyper_link=False) 
print("Output database:",result)                          
```
```bash
Output database:
{'AT4G32150':
    {'planteome':{
        'service': '/api/search/annotation', 
        'status': 'success',
        'arguments': {},
        'comments': ['Results found for: annotation; queries: ; filters: '],
        'data': [{...}]
        ...
   }
   ...
}
```
### Example of Build Dictinary Module
```py
from pyrice.build_dictionary import update_gene_dictionary, update_rapdb_oryzabase

update_gene_dictionary()
update_local_database(rapdb_url, oryzabase_url)
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

## List of supported databases

Database_name: keywords

* [Oryzabase](https://shigen.nig.ac.jp/rice/oryzabase/) : oryzabase
* [RapDB](https://rapdb.dna.affrc.go.jp) : rapdb
* [Gramene](http://www.gramene.org) : gramene
* [IC4R](http://expression.ic4r.org) : ic4r
* [SNP-Seek](https://snp-seek.irri.org) : snpseek
* [Funricegene](https://funricegenes.github.io) : funricegene_genekeywords, funricegene_faminfo, funricegene_geneinfo
* [MSU](http://rice.plantbiology.msu.edu) : msu
* [EMBL-EBI Expression Atlas](https://www.ebi.ac.uk/gxa/home) : embl_ebi
* [GWAS-ATLAS](https://bigd.big.ac.cn/gwas/#) : gwas_atlas
* [Planteome](http://planteome.org) : planteome
* [AgroLD](http://www.agrold.org) : planttfdb_tf, planttfdb_target_gene

**Keywords are value of arguments in query module.**

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
