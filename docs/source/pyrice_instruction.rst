Instruction
===========

Before start using package
--------------------------
If you want to use Selenium with a Chrome to crawl JavaScript data, please fill the path lead to Chrome driver before querying::

	>>> from pyrice import utils

	>>> utils.chrome_path = "the path of your Chrome driver"

Using the multi_query module
----------------------------

The core of PyRice package based on the :py:mod:`~pyrice.multi_query` module.
Class :py:class:`~pyrice.multi_query.MultiQuery` in :py:mod:`~pyrice.multi_query` module is the main object for query informations of gene in many databases.
Users can create instances of this class in several ways.

Search gene on chromosome
^^^^^^^^^^^^^^^^^^^^^^^^^

To search gene on chromosome, use the :py:func:`~pyrice.multi_query.MultiQuery.search_gene` function
in the :py:class:`~pyrice.multi_query.MultiQuery` class::

	>>> from pyrice.multi_query import MultiQuery

	>>> query = MultiQuery()
	>>> result = query.search_on_chromosome(chro="chr01", start_pos="1", end_pos="20000",
	                                        number_process = 4, dbs="all", save_path="./result/")

The function returns output in form of a :py:class:`dictionary`.
In addition, to save data on file (in term of .csv), you can set a destination through `save_path` argument ::

	>>> print("Output database:", result)
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

Search informations gene using chromosome
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

PyRice package supports users to search following the start and end position of genes on a chromosome. Use the :py:func:`~pyrice.MultiQuery.query_by_chromosome` function in the :py:class:`~pyrice.multi_query.MultiQuery` class::

	>>> from pyrice.multi_query import MultiQuery

	>>> query = MultiQuery()
	>>> result = query.query_by_chromosome(chro="chr01", start_pos="1", end_pos="20000",
	                                       number_process = 4, multi_processing=True,
	                                       multi_threading=True, dbs="all")

This function returns an :py:class:`dictionary`. ::

	>>> print("Output database:", result)
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

To save the result, package uses the :py:func:`~pyrice.multi_query.MultiQuery.save` function in the :py:class:`~pyrice.multi_query.MultiQuery` with different types of file html, pkl, json, csv::

	>>> query.save(result, save_path="./result/",
	               format=["csv", "html", "json", "pkl"], hyper_link=False)

Search informations gene by IDs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

PyRice package supports searching gene information follow three identifications of gene: IDs on Oryzabase, locus on MSU and iric_name on SNP-SEEK.
The :py:func:`~pyrice.multi_query.MultiQuery.query_by_ids` function in the :py:class:`~pyrice.multi_query.MultiQuery` class is used following::

	>>> from pyrice.multi_query import MultiQuery

	>>> query = MultiQuery()
	>>> result = query.query_by_ids(ids=["Os08g0164400", "Os07g0586200"],
	                                locs=["LOC_Os10g01006", "LOC_Os07g39750"],
	                                irics=["OsNippo01g010050", "OsNippo01g010300"],
	                                number_process = 4, multi_processing=True, multi_threading=True, dbs="all")

This function returns a :py:class:`dictionary` where the key is iric_name::

	>>> print("Output database:",result)
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


To save the result, package uses the :py:func:`~pyrice.multi_query.MultiQuery.save` function in the :py:class:`~pyrice.multi_query.MultiQuery` with different types of file html, pkl, json, csv.::

	>>> query.save(result, save_path = "./result/",
	               format=["csv", "html", "json", "pkl"], hyper_link=False)

Using the build_dictionary module
---------------------------------

PyRice package saves 2 databases: Oryzabase and RapDB as local; three dictionaries of identifications of gene.
Therefore, it also has  functions to update regularly gene use the :py:func:`~pyrice.build_dictionary.update_gene_dictionary` function
and :py:func:`~pyrice.build_dictionary.update_rapdb_oryzabase` function in the :py:mod:`~pyrice.build_dictionary` module::

	>>> from pyrice.build_dictionary import update_gene_dictionary, update_rapdb_oryzabase

	>>> update_gene_dictionary()
	>>> update_local_database(rapdb_url, oryzabase_url)

Using the search function and query SQL
---------------------------------------

PyRice package has a function to support searching text on result file after using query functions.
Use the :py:func:`~pyrice.utils.search` function in the :py:mod:`~pyrice.utils` module::

	>>> from pyrice import utils
	>>> import pandas as pd

	>>> df1 = pd.read_pickle("./result1/data/db.pkl")
	>>> df2 = pd.read_pickle("./result2/data/db.pkl")
	>>> df = pd.concat([df1,df2])
	>>> result = utils.search(df,"Amino acid ")

You can execute a SQL query over a pandas dataframe.
You have to install package `pandasql <https://pypi.org/project/pandasql/>`_.
Next, follow the code below to run SQL query::

	>>> import pandas as pd
	>>> from pandasql import sqldf

	>>> data = pd.read_pickle("./result/data/db.pkl")
	>>> data = data.astype(str)
	>>> sql = "SELECT * FROM data WHERE `oryzabase.CGSNL Gene Symbol` = 'TLP27' or `gramene.system_name` = 'oryza_sativa'"
	>>> pysqldf = lambda q: sqldf(q, globals())
	>>> print(pysqldf(sql))

.. note::   You have to save file as .pkl and re-load it again to use :py:func:`~pyrice.utils.search` function.

			The variable name is same with the table name in SQL query.

Structure of file database wrapper
----------------------------------

PyRice package contains a file which includes all database wrapper (database_description.xml) to manage all information of databases::

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

Example: here is a Oryzabase database::

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

Search new attributes on new databases
--------------------------------------

Add new database
^^^^^^^^^^^^^^^^^^^
PyRice package supports queries on new databases by adding its description manually on `database_description.xml`.
With JSON format, here is SNP-SEEK database with API: https://snp-seek.irri.org/ws/genomics/gene/osnippo/chr01?start=1&end=15000&model=iric::

    <database dbname="snpseek" type="text/JSON" method="GET" normalize="false">
        <link stern="https://snp-seek.irri.org/ws/genomics/gene/osnippo/" aft=""/>
        <fields>
            <field></field>
            <field op="=">start</field>
            <field op="=">end</field>
            <field op="=">model</field>
        </fields>
    </database>

For more details:
    - dbname : database name
    - type : the result return by API
    - method : GET/POST (usually GET)
    - normalize : normalize name of database true/false (usually false)
    - stern : URL of API
    - op : paramaters (see on API above)

For example, with an API from Planteome: http://browser.planteome.org/api/search/annotation?bioentity=AT4G32150::

    <database dbname="planteome" type="text/JSON" method="GET" normalize="false">
        <link stern="http://browser.planteome.org/api/search/annotation?" aft=""></link>
        <fields>
            <field op="=">bioentity</field>
        </fields>
    </database>

Use new query funtion
^^^^^^^^^^^^^^^^^^^^^
Use the :py:func:`~pyrice.multi_query.MultiQuery.query_new_databse` function in the :py:class:`~pyrice.multi_query.MultiQuery` class::

	>>> from pyrice.multi_query import MultiQuery

	>>> query = MultiQuery()
	>>> result = query.query_new_database(atts=['AT4G32150'], number_process= 4,
	                                      multi_processing=True,multi_threading=True,dbs=['planteome'])


This function returns a :py:class:`dictionary`.::

	>>> print("Output database:",result)
	Output database:
	{'AT4G32150': {
		'planteome': {
			'service': '/api/search/annotation',
			'status': 'success.',
			'arguments': '{}',
			'comments': ['Results found for: annotation; queries: ; filters: '],
			'data': [{...}]
			...},
	    ...}
	}

To save the result, package uses the :py:func:`~pyrice.multi_query.MultiQuery.save` function in the :py:class:`~pyrice.multi_query.MultiQuery` with different types of file html, pkl, json, csv.::

	>>> query.save(result, save_path="./result/",
	               format=["csv", "html", "json", "pkl"], hyper_link=False)

.. note::   With APIs return results with HTML and Javascript format, it might have some problems due to the difference of GUI (Javascript) or tag (HTML).
            So, we are working to simplize the package on those two formats to make it easier for updating new databases.