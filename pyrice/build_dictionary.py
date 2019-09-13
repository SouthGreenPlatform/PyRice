# -*- coding: utf-8 -*-

from argparse import ArgumentParser
from pyrice.multi_query import MultiQuery
from pyrice import multi_query
import time
import pickle
import gzip
import shutil
import os
import wget

# parser = ArgumentParser("build_dictionary", conflict_handler='resolve')
# parser.add_argument("--rapdb_url", type=str, default="https://rapdb.dna.affrc.go.jp/download/archive/irgsp1/IRGSP-1.0_representative_annotation_2019-03-22.tsv.gz")
# parser.add_argument("--oryzabase_url",type=str, default="https://shigen.nig.ac.jp/rice/oryzabase/gene/download?classtag=GENE_EN_LIST")
# args = parser.parse_args()

dir_path = os.path.dirname(multi_query.__file__)

def update_gene_dictionary():
    """
    Update function for gene dictionary

    """
    test = MultiQuery()
    chromosome = ["chr01", "chr02", "chr03", "chr04", "chr05", "chr06", "chr07", "chr08", "chr09", "chr10", "chr11",
                  "chr12"]
    start = ["1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1"]
    end = ["43270923", "35937250", "36413819", "35502694", "29958434", "31248787", "29697621", "28443022", "23012720"
        , "23207287", "29021106", "27531856"]
    iric_dict = dict()
    for i in range(len(chromosome)):
        t = time.time()
        file_id = test.search_on_chromosome(chro=chromosome[i], start_pos=start[i],
                                   end_pos=end[i], number_process=4, dbs=["iric"])
        iric_dict.update(file_id)
        print("Time for search gene on chromosome {} : {}".format(chromosome[i],time.time() - t))
    id_dict = dict()
    loc_dict = dict()
    for iric_name in iric_dict.keys():
        if iric_dict[iric_name]["msu7Name"] != None:
            for loc in iric_dict[iric_name]["msu7Name"]:
                if loc not in loc_dict.keys():
                    loc_dict.setdefault(loc, iric_name)
        if iric_dict[iric_name]["raprepName"] != None:
            for ids in iric_dict[iric_name]["raprepName"]:
                if ids not in id_dict.keys():
                    id_dict.setdefault(ids, iric_name)
    with open(os.path.join(dir_path,'support/iric_dict.pkl'), 'wb') as f:
        pickle.dump(iric_dict, f)
        f.close()
    with open(os.path.join(dir_path,'support/loc_dict.pkl'), 'wb') as f:
        pickle.dump(loc_dict, f)
        f.close()
    with open(os.path.join(dir_path,'support/id_dict.pkl'), 'wb') as f:
        pickle.dump(id_dict, f)
        f.close()


source_filepath = "support/rapdb.gz"
dest_filepath = "support/rapdb.tsv"
oryzabase_filepath = 'support/oryzabase.txt'

def gunzip_shutil(source_filepath, dest_filepath, block_size=65536):
    """
    Function to unzip file

    :param source_filepath: (str) source file path file .zip
    :param dest_filepath: (str) destination file path
    :param block_size: (int)

    """
    with gzip.open(source_filepath, 'rb') as s_file, \
            open(dest_filepath, 'wb') as d_file:
        shutil.copyfileobj(s_file, d_file, block_size)

def update_local_database(rapdb_url, oryzabase_url):
    """
    Update function for rapdb database and oryzabase database

    :param rapdb_url: (str) url for download rapdb database
    :param oryzabase_url: (str) url for download oryzabase database

    """
    with open("./support/id_dict.pkl", "rb") as f:
        id_dict = pickle.load(f)
    f.close()
    # Oryzabase
    print('Beginning Oryzabase database download with requests')
    wget.download(oryzabase_url,os.path.join(dir_path,oryzabase_filepath))
    print('Download successfully Oryzabase database')

    with open(os.path.join(dir_path,oryzabase_filepath), "r") as f:
        data = f.readlines()
    f.close()
    filter_data = []
    for d in data:
        filter_data.append(d.split("\t"))
    c = 0
    oryzabase = dict()
    for d in filter_data:
        if len(d) > 10:
            if d[10] in id_dict.keys():
                iric_name = id_dict[d[10]]
                oryzabase.setdefault(iric_name, {"oryzabase": dict()})
                oryzabase[iric_name]["oryzabase"].setdefault("CGSNL Gene Symbol", d[1])
                oryzabase[iric_name]["oryzabase"].setdefault("Gene symbol synonym(s)", d[2])
                oryzabase[iric_name]["oryzabase"].setdefault("CGSNL Gene Name", d[3])
                oryzabase[iric_name]["oryzabase"].setdefault("Gene name synonym(s)", d[4])
                oryzabase[iric_name]["oryzabase"].setdefault("Chr. No.", d[7])
                oryzabase[iric_name]["oryzabase"].setdefault("Trait Class", d[9])
                oryzabase[iric_name]["oryzabase"].setdefault("Gene Ontology", d[14])
                oryzabase[iric_name]["oryzabase"].setdefault("Trait Ontology", d[15])
                oryzabase[iric_name]["oryzabase"].setdefault("Plant Ontology", d[16])
                oryzabase[iric_name]["oryzabase"].setdefault("RAP ID", d[10])
                c += 1
    with open(os.path.join(dir_path,"support/oryzabase.pkl"), "wb") as f:
        pickle.dump(oryzabase, f)
    f.close()
    os.remove(oryzabase_filepath)
    print('Build successfully Oryzabase database')

    # Rapdb
    print('Beginning Rapdb database download with requests')
    wget.download(rapdb_url, source_filepath)
    gunzip_shutil(source_filepath, dest_filepath)
    print('Download successfully Oryzabase database')
    data = []
    with open(os.path.join(dir_path,dest_filepath), "r") as f:
        data = f.readlines()
        f.close()
    filter_data = []
    for d in data:
        filter_data.append(d.split("\t"))
    c = 0
    rapdb = dict()
    for d in filter_data:
        if len(d) > 10:
            if d[1] in id_dict.keys():
                iric_name = id_dict[d[1]]
                rapdb.setdefault(iric_name, {"rapdb": dict()})
                rapdb[iric_name]["rapdb"].setdefault("Locus_ID", d[1])
                rapdb[iric_name]["rapdb"].setdefault("Description", d[2])
                rapdb[iric_name]["rapdb"].setdefault("Position", d[3])
                rapdb[iric_name]["rapdb"].setdefault("RAP-DB Gene Symbol Synonym(s)", d[4])
                rapdb[iric_name]["rapdb"].setdefault("RAP-DB Gene Name Synonym(s)", d[5])
                rapdb[iric_name]["rapdb"].setdefault("CGSNL Gene Symbol", d[6])
                rapdb[iric_name]["rapdb"].setdefault("CGSNL Gene Name", d[7])
                rapdb[iric_name]["rapdb"].setdefault("Oryzabase Gene Symbol Synonym(s)", d[8])
                rapdb[iric_name]["rapdb"].setdefault("Oryzabase Gene Name Synonym(s)", d[9])
            c += 1
    with open(os.path.join(dir_path,"support/rapdb.pkl"), "wb") as f:
        pickle.dump(rapdb, f)
    f.close()
    os.remove(source_filepath)
    os.remove(dest_filepath)
    print('Build successfully Rapdb database')
