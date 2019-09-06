
# Python query engine for PyRice package

## Instruction for install package on git (on products branch only)

- Clone project on PyRice `products` branch
  ```
  git clone --branch products https://github.com/pierrelarmande/PyRice 
  ```
## Instruction for install package on pypi

- Use pip to install package PyRice
    ```
    pip install pyrice
    ```
    
## Function

### Query Module

```py
def search_gene(self, chro, start_pos, end_pos, number_process = cpu_count()-1, save_path = None, dbs='all'):
    """
    Search gene in snpseek database

    :param chro: (str) chromosome (ex: "chr01")
    :param start_pos: (str) start of chromosome
    :param end_pos: (str) end of chromosome
    :param number_process: (int) number of threading
    :param dbs: (list) list databases (support 3 available databases)
    :param save_path: (str) path to save result after call function

    :return: a dictionary, format: iricname:{{msu7Name:LOC_Os..},{raprepName:Os..},{contig:chr0..},{fmin:12..},{fmax:22...}}
    """
```

```py
def query_iric(self, chro, start_pos, end_pos, number_process = cpu_count()-1, multi_processing = False,
               multi_threading = True, dbs='all'):
    """
    Query gene with chromosome

    :param chro: (str) chromosome (ex: "chr01")
    :param start_pos: (str) start of chromosome
    :param end_pos: (str) end of chromosome
    :param number_process: (int) number of process or number of threading
    :param multi_processing: (bool) if True use multi_processing
    :param multi_threading: (bool) if True use multi_threading
    :param dbs: list databases (support 7 available databases)

    :return: a dictionary, format : gene:{database: attributes}
    """
```
```py
def query_ids_locs(self, idents, locs, irics, number_process = cpu_count()-1, multi_processing = False,
               multi_threading = True, dbs='all'):
    """
    Query gene with id and loc

    :param idents: (list) list id of gene
    :param locs: (list) list loc of gene
    :param irics: (list) list iric name of gene
    :param number_process: (int) number of process or number of threading
    :param multi_processing: (bool) if True use multi_processing
    :param multi_threading: (bool) if True use multi_threading
    :param dbs: list databases (support 7 available databases)

    :return: a dictionary, format: gene:{database: attribute}
    """
```
```py
def new_query(self, atts, number_process = cpu_count() -1, multi_processing = False, multi_threading = True ,dbs = None):
    """
    Query with new attributes and new databases

    :param atts: (list) list of new attributes
    :param number_process: (int) number of process or number of threading
    :param multi_processing: (bool) if True use multi_processing
    :param multi_threading: (bool) if True use multi_threading
    :param dbs: (list) list of new databases

    :return: dictionary, format : attribute:{database: information of attribute}
    """
```
Note: the computation time depend on the length of position you decide.
### Search Module
```py
def search_text(df, text):
    """
    Search function on result (file pkl)

    :param df: (dataframe) dataframe of pandas
    :param text: (str) text

    :return: a dataframe of pandas that include text
    """
```
### Build Dictionary Module
```py
def update_gene_dictionary():
    """
    Update function for gene dictionary
    """
```
```py
def update_rapdb_oryzabase(rapdb_url, oryzabase_url):
    """
    Update function for rapdb database and oryzabase database
    :param rapdb_url: (str) url for download rapdb database
    :param oryzabase_url: (str) url for download oryzabase database
    """
```
## Structure of Database description

```xml
<database dbname="name of the database" type="Type of the response" method="GET or POST">
    <link stern="the link section before the query" aft="section behind the query"/>
    <headers>
        <header type="">Column number 1</header>
        <header type="">Column number 2</header>
        etc.
    </headers>
    <fields>
        <field>Query argument number 1</field>
    </fields>
    <data_struct indicator="indicator of return data segment" identifier="the attribute to identify data section" identification_string="value of said identifier" line_separator="indicator of a line of data" cell_separator="indicator of a cell of data"/>
    <prettify>Regular expression of unwanted character</prettify>
</database>
```

## Example run in Pycharm

### Example of system search_gene

```bash
from pyrice.multi_query import MultiQuery

test = MultiQuery()
file_id = test.search_gene(chro="chr01", start_pos="1",
                           end_pos="20000", number_process = 4, dbs="all", save_path="./result/")
print("Output database:", file_id)
```
```bash
Output database: {'OsNippo01g010050': {'msu7Name': {'LOC_Os01g01010'}, 'raprepName': {'Os01g0100100'}, 'contig': 'chr01', 'fmin': 2982, 'fmax': 10815}, 'OsNippo01g010150': {'msu7Name': {'LOC_Os01g01019'}, 'raprepName': {'Os01g0100200'}, 'contig': 'chr01', 'fmin': 11217, 'fmax': 12435}, 'OsNippo01g010100': {'msu7Name': set(), 'raprepName': {'Os01g0100300'}, 'contig': 'chr01', 'fmin': 11371, 'fmax': 12284}, 'OsNippo01g010200': {'msu7Name': {'LOC_Os01g01030'}, 'raprepName': {'Os01g0100400'}, 'contig': 'chr01', 'fmin': 12720, 'fmax': 15685}, 'OsNippo01g010250': {'msu7Name': set(), 'raprepName': {'Os01g0100466'}, 'contig': 'chr01', 'fmin': 12807, 'fmax': 13978}, 'OsNippo01g010300': {'msu7Name': {'LOC_Os01g01040'}, 'raprepName': {'Os01g0100500'}, 'contig': 'chr01', 'fmin': 16398, 'fmax': 20144}}
```

### Example of system query_iric

```bash
from pyrice.multi_query import MultiQuery

test = MultiQuery()
db = test.query_iric(chro="chr01", start_pos="1",
                     end_pos="20000", number_process = 4, multi_processing=True, multi_threading=True,
                     dbs="all")
test.save_file(db, save_path="./result/", format=["csv", "html", "json", "pkl"], hyper_link=False)
print("Output database:", db)
```
```bash
Output database {'OsNippo01g010050': {'rapdb': {'Locus_ID': 'Os01g0100100', 'Description': 'RabGAP/TBC domain containing protein.', 'Position': '', 'RAP-DB Gene Symbol Synonym(s)': '', 'RAP-DB Gene Name Synonym(s)': '', 'CGSNL Gene Symbol': '', 'CGSNL Gene Name': '', 'Oryzabase Gene Symbol Synonym(s)': '', 'Oryzabase Gene Name Synonym(s)': 'Molecular Function: Rab GTPase activator activity (GO:0005097), Cellular Component: intracellular (GO:0005622), Biological Process: regulation of Rab GTPase activity (GO:0032313)'}, 'gramene': {'_id': 'Os01g0100100', 'name': 'Os01g0100100', 'description': 'RabGAP/TBC domain containing protein. (Os01t0100100-01)', 'biotype': 'protein_coding', 'taxon_id': 39947, 'system_name': 'oryza_sativa', 'db_type': 'core', 'gene_idx': 0, 'location': {'region': '1', 'start': 2983, 'end': 10815, 'strand': 1, 'map': 'GCA_001433935.1'}, 'xrefs': [{'db': 'UniParc', 'ids': ['UPI0001C7F089']}, {'db': 'Uniprot/SPTREMBL', 'ids': ['A0A0P0UX28']}, {'db': 'STRING', 'ids': ['39947.LOC_Os01g01010.1']}, {'db': 'RefSeq_peptide', 'ids': ['XP_015622096.1']}, {'db': 'protein_id', 'ids': ['BAS69908.1']}, {'db': 'RefSeq_dna', 'ids': ['XM_015766610.1', 'XM_015766610.2']}, {'db': 'EntrezGene', 'ids': ['4326813']}], 'gene_structure': {'exons': [{'id': 'Os01t0100100-01.exon1', 'start': 1, 'end': 286}, {'id': 'Os01t0100100-01.exon2', 'start': 372, 'end': 634}, {'id': 'Os01t0100100-01.exon3', 'start': 1375, 'end': 1473}, {'id': 'Os01t0100100-01.exon4', 'start': 2475, 'end': 2578}, {'id': 'Os01t0100100-01.exon5', 'start': 4154, 'end': 4962}, {'id': 'Os01t0100100-01.exon6', 'start': 5046, 'end': 5168}, {'id': 'Os01t0100100-01.exon7', 'start': 5250, 'end': 5338}, {'id': 'Os01t0100100-01.exon8', 'start': 5426, 'end': 5626}, {'id': 'Os01t0100100-01.exon9', 'start': 6228, 'end': 6633}, {'id': 'Os01t0100100-01.exon10', 'start': 7120, 'end': 7205}, {'id': 'Os01t0100100-01.exon11', 'start': 7292, 'end': 7448}, {'id': 'Os01t0100100-01.exon12', 'start': 7522, 'end': 7833}], 'transcripts': .....}
```
### Example of system query_ids_locs
```py
from pyrice.multi_query import MultiQuery

test = MultiQuery()
db = test.query_ids_locs(idents=["Os08g0164400", "Os07g0586200"],
                         locs=["LOC_Os10g01006", "LOC_Os07g39750"],
                         irics=["OsNippo01g010050", "OsNippo01g010300"], number_process = 4,
                         multi_processing=True, multi_threading=True, dbs="all")
test.save_file(db,save_path = "./result/",format=["csv","html","json","pkl"],hyper_link=False)
print("Output database:",db)
```
```bash
Output database {'OsNippo01g010300': {'rapdb': {'Locus_ID': 'Os01g0100500', 'Description': 'Immunoglobulin-like domain containing protein.', 'Position': '', 'RAP-DB Gene Symbol Synonym(s)': '', 'RAP-DB Gene Name Synonym(s)': '', 'CGSNL Gene Symbol': '', 'CGSNL Gene Name': '', 'Oryzabase Gene Symbol Synonym(s)': '', 'Oryzabase Gene Name Synonym(s)': ''}, 'gramene': {'_id': 'Os01g0100500', 'name': 'Os01g0100500', 'description': 'Immunoglobulin-like domain containing protein. (Os01t0100500-01)', 'biotype': 'protein_coding', 'taxon_id': 39947, 'system_name': 'oryza_sativa', 'db_type': 'core', 'gene_idx': 5, 'location': {'region': '1', 'start': 16399, 'end': 20144, 'strand': 1, 'map': 'GCA_001433935.1'}, 'xrefs': [{'db': 'UniParc', 'ids': ['UPI000009FFD9']}, {'db': 'Uniprot/SPTREMBL', 'ids': ['Q93VG6']}, {'db': 'protein_id', 'ids': ['BAF03650.1', 'BAE79749.1', 'EAZ10179.1', 'BAB64233.1', 'BAS69913.1', 'BAB62620.1']}, {'db': 'RefSeq_dna', 'ids': ['XM_026027108.1', 'XM_026027132.1', 'XM_026027147.1', 'NM_001361326.1', 'XM_026027124.1']}], 'gene_structure': {'exons': [{'id': 'Os01t0100500-01.exon1', 'start': 1, 'end': 578}, {'id': 'Os01t0100500-01.exon2', 'start': 985, 'end': 1076}, {'id': 'Os01t0100500-01.exon3', 'start': 1160, 'end': 1860}, {'id': 'Os01t0100500-01.exon4', 'start': 2103, 'end': 2173}, {'id': 'Os01t0100500-01.exon5', 'start': 2570, 'end': 2659}, {'id': 'Os01t0100500-01.exon6', 'start': 2744, 'end': 2923}, {'id': 'Os01t0100500-01.exon7', 'start': 3133, 'end': 3231}, {'id': 'Os01t0100500-01.exon8', 'start': 3336, 'end': 3746}], 'transcripts': [{'exons': ['Os01t0100500-01.exon1', 'Os01t0100500-01.exon2', 'Os01t0100500-01.exon3', 'Os01t0100500-01.exon4', 'Os01t0100500-01.exon5', 'Os01t0100500-01.exon6', 'Os01t0100500-01.exon7', 'Os01t0100500-01.exon8'], 'length': 2222, 'exon_junctions': [578, 670, 1371, 1442, 1532, 1712, 1811],...} ```
```
### Example of system new_query
```py
from pyrice.multi_query import MultiQuery

test = MultiQuery()
db = test.new_query(atts=['TRAES3BF001000010CFD'], number_process= 4,
                    multi_processing=True,multi_threading=True,dbs=['urgi'])
test.save_file(db, save_path="./result/", format=["csv", "html", "json", "pkl"], hyper_link=False)
print("Output database:",db)
```
```bash
Output database: {'TRAES3BF001000010CFD': {'urgi': {'recordsTotal': 1177800, 'recordsFiltered': 1177800, 'draw': None, 'data': [{'id': '622021ba641dc7e1', 'entry_type': 'GO process', 'database_name': 'Gramene', 'db_id': 'GO:0050789', 'db_version': None, 'description': ['GO process', 'Gramene', 'GO:0050789', 'regulation of biological process', 'Any process that modulates the frequency, rate or extent of a biological process. Biological processes are regulated by many means; examples include the control of gene expression, protein modification or interaction with a protein or substrate molecule.', 'regulation of physiological process', 'Triticum aestivum', 'Triticum urartu', 'Brachypodium distachyon', 'Aegilops tauschii', 'Hordeum vulgare subsp. vulgare'], 'url': 'http://search.gramene.org/#%7B%22filters%22:%7B%22GO__ancestors:50789%22:%7B%22category%22:%22GO%20process%22,%22display_name%22:%22regulation%20of%20biological%20process%22,%22fq%22:%22GO__ancestors:50789%22,%22exclude%22:false%7D,%22taxonomy__ancestors:147368%22:%7B%22category%22:%22Taxonomy%22,%22display_name%22:%22Pooideae%22,%22fq%22:%22taxonomy__ancestors:147368%22,%22exclude%22:false%7D%7D,%22taxa%22:%7B%7D%7D', 'species': ['Triticum aestivum', 'Triticum urartu', 'Brachypodium distachyon', 'Aegilops tauschii', 'Hordeum vulgare subsp. vulgare'], 'xref': None, 'feature_type': None, 'sequence_id': None, 'sequence_version': None, 'start_position': None, 'end_position': None, 'map': None, 'map_position': None, 'authority': None, 'trait': None, 'trait_id': None, 'environment': None, 'environment_id': None, 'statistic': None, 'unit': None, 'genotype': None, 'experiment_type': None}, {'id': '1fff80eb16dfbef4', 'entry_type': 'GO process', 'database_name': 'Gramene', 'db_id': 'GO:1902806', 'db_version': None, 'description': ['GO process', 'Gramene', 'GO:1902806', 'regulation of cell cycle G1/S phase transition', 'Any process that modulates the frequency, rate or extent of cell cycle G1/S phase transition.', 'Triticum urartu', 'Brachypodium distachyon', 'Aegilops tauschii', 'Hordeum vulgare subsp. vulgare'], 'url': 'http://search.gramene.org/#%7B%22filters%22:%7B%22GO__ancestors:1902806%22:%7B%22category%22:%22GO%20process%22,%22display_name%22:%22regulation%20of%20cell%20cycle%20G1/S%20phase%20transition%22,%22fq%22:%22GO__ancestors:1902806%22,%22exclude%22:false%7D,%22taxonomy__ancestors:147368%22:%7B%22category%22:%22Taxonomy%22,%22display_name%22:%22Pooideae%22,%22fq%22:%22taxonomy__ancestors:147368%22,%22exclude%22:false%7D%7D,%22taxa%22:%7B%7D%7D', 'species': ['Triticum urartu', 'Brachypodium distachyon', 'Aegilops tauschii', 'Hordeum vulgare subsp. vulgare'], 'xref': None, 'feature_type': None, 'sequence_id': None, 'sequence_version': None, 'start_position': None, 'end_position': None, 'map': None, 'map_position': None, 'authority': None, 'trait': None, 'trait_id': None, 'environment': None, 'environment_id': None, 'statistic': None, 'unit': None, 'genotype': None, 'experiment_type': None}, {'id': '74a4692d47d1ac97', 'entry_type': 'GO component', 'database_name': 'Gramene', 'db_id': 'GO:0022625', 'db_version': None, 'description': ['GO component', 'Gramene', 'GO:0022625', 'cytosolic large ribosomal subunit', 'The large subunit of a ribosome located in the cytosol.', '50S ribosomal subunit', '60S ribosomal subunit', 'eukaryotic ribosomal LSU', 'prokaryotic large ribosomal subunit', 'Triticum aestivum', 'Triticum urartu', 'Brachypodium distachyon', 'Aegilops tauschii', 'Hordeum vulgare subsp. vulgare'], 'url': 'http://search.gramene.org/#%7B%22filters%22:%7B%22GO__ancestors:22625%22:%7B%22category%22:%22GO%20component%22,%22display_name%22:%22cytosolic%20large%20ribosomal%20subunit%22,%22fq%22:%22GO__ancestors:22625%22,%22exclude%22:false%7D,%22taxonomy__ancestors:147368%22:%7B%22category%22:%22Taxonomy%22,%22display_name%22:%22Pooideae%22,%22fq%22:%22taxonomy__ancestors:147368%22,%22exclude%22:false%7D%7D,%22taxa%22:%7B%7D%7D', 'species': ['Triticum aestivum', 'Triticum urartu', 'Brachypodium distachyon', 'Aegilops tauschii', 'Hordeum vulgare subsp. vulgare'], 'xref': None, 'feature_type': None, 'sequence_id': None, 'sequence_version': None, 'start_position': None, 'end_position': None, 'map': None, 'map_position': None, 'authority': None, 'trait': None, 'trait_id': None, 'environment': None, 'environment_id': None, 'statistic': None, 'unit': None, 'genotype': None, 'experiment_type': None}, {'id': 'e2255733d4ff79fd', 'entry_type': 'GO component', 'database_name': 'Gramene', 'db_id': 'GO:0031977', 'db_version': None, 'description': ['GO component', 'Gramene', 'GO:0031977', 'thylakoid lumen', 'The volume enclosed by a thylakoid membrane.', 'Triticum aestivum', 'Triticum urartu', 'Brachypodium distachyon', 'Aegilops tauschii', 'Hordeum vulgare subsp. vulgare'], 'url': 'http://search.gramene.org/#%7B%22filters%22:%7B%22GO__ancestors:31977%22:%7B%22category%22:%22GO%20component%22,%22display_name%22:%22thylakoid%20lumen%22,%22fq%22:%22GO__ancestors:31977%22,%22exclude%22:false%7D,%22taxonomy__ancestors:147368%22:%7B%22category%22:%22Taxonomy%22,%22display_name%22:%22Pooideae%22,%22fq%22:%22taxonomy__ancestors:147368%22,%22exclude%22:false%7D%7D,%22taxa%22:%7B%7D%7D', 'species': ['Triticum aestivum', 'Triticum urartu', 'Brachypodium distachyon', 'Aegilops tauschii', 'Hordeum vulgare subsp. vulgare'], 'xref': None, 'feature_type': None, 'sequence_id': None, 'sequence_version': None, 'start_position': None, 'end_position': None, 'map': None, 'map_position': None, 'authority': None, 'trait': None, 'trait_id': None, 'environment': None, 'environment_id': None, 'statistic': None, 'unit': None, 'genotype': None, 'experiment_type': None}, {'id': '56ae8c1ff68833be', 'entry_type': 'GO process', 'database_name': 'Gramene', 'db_id': 'GO:0060359', 'db_version': None, 'description': ['GO process', 'Gramene', 'GO:0060359', 'response to ammonium ion', 'Any process that results in a change in state or activity of a cell or an organism (in terms of movement, secretion, enzyme production, gene expression, etc.) as a result of an ammonium ion stimulus.', 'Triticum urartu', 'Brachypodium distachyon', 'Aegilops tauschii', 'Hordeum vulgare subsp. vulgare'], 'url': 'http://search.gramene.org/#%7B%22filters%22:%7B%22GO__ancestors:60359%22:%7B%22category%22:%22GO%20process%22,%22display_name%22:%22response%20to%20ammonium%20ion%22,%22fq%22:%22GO__ancestors:60359%22,%22exclude%22:false%7D,%22taxonomy__ancestors:147368%22:%7B%22category%22:%22Taxonomy%22,%22display_name%22:%22Pooideae%22,%22fq%22:%22taxonomy__ancestors:147368%22,%22exclude%22:false%7D%7D,%22taxa%22:%7B%7D%7D', 'species': ['Triticum urartu', 'Brachypodium distachyon', 'Aegilops tauschii', 'Hordeum vulgare subsp. vulgare'], 'xref': None, 'feature_type': None, 'sequence_id': None, 'sequence_version': None, 'start_position': None, 'end_position': None, 'map': None, 'map_position': None, 'authority': None, 'trait': None, 'trait_id': None, 'environment': None, 'environment_id': None, 'statistic': None, 'unit': None, 'genotype': None, 'experiment_type': None}, {'id': '1cea3e085776a6bd', 'entry_type': 'GO process', 'database_name': 'Gramene', 'db_id': 'GO:0032101', 'db_version': None, 'description': ['GO process', 'Gramene', 'GO:0032101', 'regulation of response to external stimulus', 'Any process that modulates the frequency, rate or extent of a response to an external stimulus.', 'Note that this term is in the subset of terms that should not be used for direct gene product annotation. Instead, select a child term or, if no appropriate child term exists, please request a new term. Direct annotations to this term may be amended during annotation QC.', 'Triticum aestivum', 'Triticum urartu', 'Brachypodium distachyon', 'Aegilops tauschii', 'Hordeum vulgare subsp. vulgare'], 'url': 'http://search.gramene.org/#%7B%22filters%22:%7B%22GO__ancestors:32101%22:%7B%22category%22:%22GO%20process%22,%22display_name%22:%22regulation%20of%20response%20to%20external%20stimulus%22,%22fq%22:%22GO__ancestors:32101%22,%22exclude%22:false%7D,%22taxonomy__ancestors:147368%22:%7B%22category%22:%22Taxonomy%22,%22display_name%22:%22Pooideae%22,%22fq%22:%22taxonomy__ancestors:147368%22,%22exclude%22:false%7D%7D,%22taxa%22:%7B%7D%7D', 'species': ['Triticum aestivum', 'Triticum urartu', 'Brachypodium distachyon', 'Aegilops tauschii', 'Hordeum vulgare subsp. vulgare'], 'xref': None, 'feature_type': None, 'sequence_id': None, 'sequence_version': None, 'start_position': None, 'end_position': None, 'map': None, 'map_position': None, 'authority': None, 'trait': None, 'trait_id': None, 'environment': None, 'environment_id': None, 'statistic': None, 'unit': None, 'genotype': None, 'experiment_type': None}, {'id': 'f69e6900e17acf29', 'entry_type': 'GO function', 'database_name': 'Gramene', 'db_id': 'GO:0004527', 'db_version': None, 'description': ['GO function', 'Gramene', 'GO:0004527', 'exonuclease activity', "Catalysis of the hydrolysis of ester linkages within nucleic acids by removing nucleotide residues from the 3' or 5' end.", 'exonuclease IX activity', 'Triticum aestivum', 'Triticum urartu', 'Brachypodium distachyon', 'Aegilops tauschii', 'Hordeum vulgare subsp. vulgare'], 'url': 'http://search.gramene.org/#%7B%22filters%22:%7B%22GO__ancestors:4527%22:%7B%22category%22:%22GO%20function%22,%22display_name%22:%22exonuclease%20activity%22,%22fq%22:%22GO__ancestors:4527%22,%22exclude%22:false%7D,%22taxonomy__ancestors:147368%22:%7B%22category%22:%22Taxonomy%22,%22display_name%22:%22Pooideae%22,%22fq%22:%22taxonomy__ancestors:147368%22,%22exclude%22:false%7D%7D,%22taxa%22:%7B%7D%7D', 'species': ['Triticum aestivum', 'Triticum urartu', 'Brachypodium distachyon', 'Aegilops tauschii', 'Hordeum vulgare subsp. vulgare'], 'xref': None, 'feature_type': None, 'sequence_id': None, 'sequence_version': None, 'start_position': None, 'end_position': None, 'map': None, 'map_position': None, 'authority': None, 'trait': None, 'trait_id': None, 'environment': None, 'environment_id': None, 'statistic': None, 'unit': None, 'genotype': None, 'experiment_type': None}, {'id': '3bd824bc81abcf75', 'entry_type': 'GO component', 'database_name': 'Gramene', 'db_id': 'GO:0005801', 'db_version': None, 'description': ['GO component', 'Gramene', 'GO:0005801', 'cis-Golgi network', 'The network of interconnected tubular and cisternal structures located at the convex side of the Golgi apparatus, which abuts the endoplasmic reticulum.', 'The CGN is not considered part of the Golgi apparatus but is a separate organelle.', 'NIF_Subcellular:sao632188024', 'cis face', 'cis Golgi network', 'forming face', 'Golgi cis face', 'Golgi cis-face', 'Triticum aestivum', 'Triticum urartu', 'Brachypodium distachyon', 'Aegilops tauschii', 'Hordeum vulgare subsp. vulgare'], 'url': 'http://search.gramene.org/#%7B%22filters%22:%7B%22GO__ancestors:5801%22:%7B%22category%22:%22GO%20component%22,%22display_name%22:%22cis-Golgi%20network%22,%22fq%22:%22GO__ancestors:5801%22,%22exclude%22:false%7D,%22taxonomy__ancestors:147368%22:%7B%22category%22:%22Taxonomy%22,%22display_name%22:%22Pooideae%22,%22fq%22:%22taxonomy__ancestors:147368%22,%22exclude%22:false%7D%7D,%22taxa%22:%7B%7D%7D', 'species': ['Triticum aestivum', 'Triticum urartu', 'Brachypodium distachyon', 'Aegilops tauschii', 'Hordeum vulgare subsp. vulgare'], 'xref': None, 'feature_type': None, 'sequence_id': None, 'sequence_version': None, 'start_position': None, 'end_position': None, 'map': None, 'map_position': None, 'authority': None, 'trait': None, 'trait_id': None, 'environment': None, 'environment_id': None, 'statistic': None, 'unit': None, 'genotype': None, 'experiment_type': None}, {'id': 'ee382f03316d64c1', 'entry_type': 'GO process', 'database_name': 'Gramene', 'db_id': 'GO:0015801', 'db_version': None, 'description': ['GO process', 'Gramene', 'GO:0015801', 'aromatic amino acid transport', 'The directed movement of aromatic amino acids, amino acids with aromatic ring, into, out of or within a cell, or between cells, by means of some agent such as a transporter or pore.', 'Triticum aestivum', 'Triticum urartu', 'Brachypodium distachyon', 'Aegilops tauschii', 'Hordeum vulgare subsp. vulgare'], 'url': 'http://search.gramene.org/#%7B%22filters%22:%7B%22GO__ancestors:15801%22:%7B%22category%22:%22GO%20process%22,%22display_name%22:%22aromatic%20amino%20acid%20transport%22,%22fq%22:%22GO__ancestors:15801%22,%22exclude%22:false%7D,%22taxonomy__ancestors:147368%22:%7B%22category%22:%22Taxonomy%22,%22display_name%22:%22Pooideae%22,%22fq%22:%22taxonomy__ancestors:147368%22,%22exclude%22:false%7D%7D,%22taxa%22:%7B%7D%7D', 'species': ['Triticum aestivum', 'Triticum urartu', 'Brachypodium distachyon', 'Aegilops tauschii', 'Hordeum vulgare subsp. vulgare'], 'xref': None, 'feature_type': None, 'sequence_id': None, 'sequence_version': None, 'start_position': None, 'end_position': None, 'map': None, 'map_position': None, 'authority': None, 'trait': None, 'trait_id': None, 'environment': None, 'environment_id': None, 'statistic': None, 'unit': None, 'genotype': None, 'experiment_type': None}, {'id': 'cb20af2fb9322a19', 'entry_type': 'GO process', 'database_name': 'Gramene', 'db_id': 'GO:0002684', 'db_version': None, 'description': ['GO process', 'Gramene', 'GO:0002684', 'positive regulation of immune system process', 'Any process that activates or increases the frequency, rate, or extent of an immune system process.', 'activation of immune system process', 'stimulation of immune system process', 'up regulation of immune system process', 'up-regulation of immune system process', 'upregulation of immune system process', 'Triticum aestivum', 'Triticum urartu', 'Brachypodium distachyon', 'Aegilops tauschii', 'Hordeum vulgare subsp. vulgare'], 'url': 'http://search.gramene.org/#%7B%22filters%22:%7B%22GO__ancestors:2684%22:%7B%22category%22:%22GO%20process%22,%22display_name%22:%22positive%20regulation%20of%20immune%20system%20process%22,%22fq%22:%22GO__ancestors:2684%22,%22exclude%22:false%7D,%22taxonomy__ancestors:147368%22:%7B%22category%22:%22Taxonomy%22,%22display_name%22:%22Pooideae%22,%22fq%22:%22taxonomy__ancestors:147368%22,%22exclude%22:false%7D%7D,%22taxa%22:%7B%7D%7D', 'species': ['Triticum aestivum', 'Triticum urartu', 'Brachypodium distachyon', 'Aegilops tauschii', 'Hordeum vulgare subsp. vulgare'], 'xref': None, 'feature_type': None, 'sequence_id': None, 'sequence_version': None, 'start_position': None, 'end_position': None, 'map': None, 'map_position': None, 'authority': None, 'trait': None, 'trait_id': None, 'environment': None, 'environment_id': None, 'statistic': None, 'unit': None, 'genotype': None, 'experiment_type': None}], 'facets': [{'field': 'entry_type', 'value': 'Genome annotation', 'count': 720072}, {'field': 'entry_type', 'value': 'Gene', 'count': 210254}, {'field': 'entry_type', 'value': 'Genetic Marker', 'count': 139689}, {'field': 'entry_type', 'value': 'Physical Marker', 'count': 34745}, {'field': 'entry_type', 'value': 'Accession', 'count': 21884}, {'field': 'entry_type', 'value': 'Protein', 'count': 16379}, {'field': 'entry_type', 'value': 'Germplasm', 'count': 16106}, {'field': 'entry_type', 'value': 'GO process', 'count': 4286}, {'field': 'entry_type', 'value': 'InterPro Family', 'count': 3280}, {'field': 'entry_type', 'value': 'InterPro Domain', 'count': 3035}, {'field': 'species', 'value': 'Triticum aestivum', 'count': 833218}, {'field': 'species', 'value': 'Triticum dicoccoides', 'count': 111368}, {'field': 'species', 'value': 'Triticum urartu', 'count': 87656}, {'field': 'species', 'value': 'Aegilops tauschii subsp. strangulata', 'count': 86854}, {'field': 'species', 'value': 'Aegilops tauschii', 'count': 50233}, {'field': 'species', 'value': 'Hordeum vulgare subsp. vulgare', 'count': 37940}, {'field': 'species', 'value': 'Brachypodium distachyon', 'count': 14032}, {'field': 'species', 'value': 'Triticum turgidum ssp. durum', 'count': 2891}, {'field': 'species', 'value': 'Triticum aestivum ssp. aestivum', 'count': 1974}, {'field': 'species', 'value': 'Triticum durum', 'count': 989}, {'field': 'database_name', 'value': 'Ensembl Plants', 'count': 720072}, {'field': 'database_name', 'value': 'Gramene', 'count': 221875}, {'field': 'database_name', 'value': 'Triticeae Toolbox', 'count': 199139}, {'field': 'database_name', 'value': 'GrainGenes', 'count': 16755}, {'field': 'database_name', 'value': 'UniProt 2019_07', 'count': 16379}, {'field': 'database_name', 'value': 'Wheat Gene Catalog at Komugi', 'count': 3075}, {'field': 'database_name', 'value': 'CIMMYT Dspace', 'count': 469}, {'field': 'database_name', 'value': 'CIMMYT dataverse', 'count': 36}]}}}
```

### Example of Search Module
```py
from pyrice.utils import search_text
import pandas as pd

df1 = pd.read_pickle("./result1/data/db.pkl")
df2 = pd.read_pickle("./result2/data/db.pkl")
df = pd.concat([df1,df2])
result = search_text(df,"Amino acid ")
```

### Example of Build Dictinary Module
```py
from pyrice.build_dictionary import update_gene_dictionary,update_rapdb_oryzabase

update_gene_dictionary()
update_rapdb_oryzabase(rapdb_url, oryzabase_url)
```

### Example of database description

```xml
<database dbname="oryzabase" type="text/html" method="POST">
    <link stern="https://shigen.nig.ac.jp/rice/oryzabase/gene/advanced/list"/>
    <headers>
        <header type="">CGSNL Gene Symbol</header>
        <header type="">Gene symbol synonym(s)</header>
        <header type="">CGSNL Gene Name</header>
        <header type="">Gene name synonym(s)</header>
        <header type="">Chr. No.</header>
        <header type="">Trait Class</header>
        <header type="">Gene Ontology</header>
        <header type="">Trait Ontology</header>
        <header type="">Plant Ontology</header>
        <header type="">RAP ID</header>
        <header type="">Mutant Image</header>
    </headers>
    <fields>
        <field>rapId</field>
    </fields>
    <data_struct indicator="table" identifier="class" identification_string="table_summery_list table_nowrapTh max_width_element" line_separator="tr" cell_separator="td"/>
    <prettify>\n>LOC_.*\n|\n|\r|\t</prettify>
</database>
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
