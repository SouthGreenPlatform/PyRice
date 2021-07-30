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
# parser.add_argument("--rapdb_url", type=str, default="https://rapdb.dna.affrc.go.jp/download/archive/irgsp1/IRGSP-1.0_representative_annotation_2019-12-17.tsv.gz")
# parser.add_argument("--oryzabase_url",type=str, default="https://shigen.nig.ac.jp/rice/oryzabase/gene/download?classtag=GENE_EN_LIST")
# # args = parser.parse_args()

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
oryzabase_filepaths = ['support/oryzabase.txt','support/oryzabase_ref.txt']

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
    :param oryzabase_url: (list) url for download oryzabase database (1st: url of genes, 2nd: url of refs)

    """
    with open(os.path.join(dir_path,"support/id_dict.pkl"), "rb") as f:
        id_dict = pickle.load(f)
    f.close()
    ## Oryzabase
    print('Beginning Oryzabase database download with requests')
    for url,oryzabase_filepath in zip(oryzabase_url,oryzabase_filepaths):
        wget.download(url,os.path.join(dir_path,oryzabase_filepath))
    print('Download successfully Oryzabase database')

    # Oryzabase refs
    with open(os.path.join(dir_path,oryzabase_filepaths[1]), 'rb') as f:
        data = f.readlines()
    f.close()
    filter_data = []
    count = 0
    for d in data:
        try:
            filter_data.append(d.decode('utf-8').split("\t"))
        except:
            count += 1

    count = 0
    id_2_pubmed = dict()
    for d in filter_data[1:]:
        # Check length pubmed id
        if len(d[1]) > 3:
            # Check case '_,_,_'
            tmp_d = d[8].replace(',', '')
            if len(d[8]) > 0 and d[8] != '\r\n' and d[8] != '-' and d[8] != '_' and not tmp_d == len(tmp_d) * tmp_d[0]:
                use_name = d[8]
            # Check if Gene Name Synonym
            elif len(d[9]) > 0 and d[9] != '\r\n' and d[9] != '-' and d[9] != '_':
                use_name = d[9]
                print(use_name)
            else:
                continue
            use_name = " ".join(use_name.split())
            name = use_name.split(',')
            for n in name:
                # Remove space
                n = " ".join(n.split())
                if len(n) > 0 and n != '_' and n != '-':
                    article = {"PubMedId": d[1],
                               "Author": d[2],
                               "Title": d[3],
                               "Journal": d[4],
                               "Year": d[7]}
                    if n not in id_2_pubmed.keys():
                        id_2_pubmed.setdefault(n, [])
                        id_2_pubmed[n].append(article)
                    else:
                        id_2_pubmed[n].append(article)
        else:
            count += 1
    # Oryzabase genes
    with open(os.path.join(dir_path,oryzabase_filepaths[0]), "r") as f:
        data = f.readlines()
    f.close()
    filter_data = []
    for d in data:
        filter_data.append(d.split("\t"))
    oryzabase = dict()
    filter_data[0][-1] = filter_data[0][-1][:-1]
    for d in filter_data:
        if len(d) > 10:
            if d[10] in id_dict.keys():
                iric_name = id_dict[d[10]]
                oryzabase.setdefault(iric_name, {"oryzabase": dict()})
                for i in range(len(filter_data[0])):
                    if d[i] != '\n' and len(d[i]) > 1:
                        oryzabase[iric_name]["oryzabase"].setdefault(filter_data[0][i], d[i])

                # Match CGSNL Gene Symbol with id
                if len(d[1]) > 0 and d[1] != '\r\n' and d[1] != '-' and d[1] != '_':
                    use_name = d[1]
                    # Match Gene symbol synonym(s) with id
                elif len(d[2]) > 0 and d[2] != '\r\n' and d[2] != '-' and d[2] != '_':
                    use_name = d[2]
                else:
                    continue
                # Remove space
                use_name = " ".join(use_name.split())
                name = use_name.split(',')
                pubmed_exist = set()
                pubmed_final = []
                for n in name:
                    # Remove space
                    n = " ".join(n.split())
                    # Check exist pubmed id
                    if len(n) > 0 and n != '_' and n != '-' and n in id_2_pubmed.keys():
                        for pubmed_art in id_2_pubmed[n]:
                            if pubmed_art['PubMedId'] not in pubmed_exist:
                                pubmed_final.append(pubmed_art)
                oryzabase[iric_name]["oryzabase"].setdefault("Reference", pubmed_final)
    with open(os.path.join(dir_path,"support/oryzabase.pkl"), "wb") as f:
        pickle.dump(oryzabase, f)
    f.close()
    for oryzabase_filepath in oryzabase_filepaths:
        if (os.path.exists(oryzabase_filepath)):
            os.remove(oryzabase_filepath)
    print('Build successfully Oryzabase database')

    # Rapdb
    print('Beginning Rapdb database download with requests')
    wget.download(rapdb_url, os.path.join(dir_path,source_filepath))
    gunzip_shutil(os.path.join(dir_path,source_filepath), os.path.join(dir_path,dest_filepath))
    print('Download successfully Rapdb database')
    data = []
    with open(os.path.join(dir_path,dest_filepath), "r") as f:
        data = f.readlines()
        f.close()
    filter_data = []
    for d in data:
        filter_data.append(d.split("\t"))
    rapdb = dict()
    filter_data[0][-1] = filter_data[0][-1][:-1]
    for d in filter_data:
        if len(d) > 16:
            if d[1] in id_dict.keys():
                iric_name = id_dict[d[1]]
                rapdb.setdefault(iric_name, {"rapdb": dict()})
                for i in range(len(filter_data[0])):
                    if d[i] != '\n' and len(d[i]) > 1:
                        rapdb[iric_name]["rapdb"].setdefault(filter_data[0][i], d[i])
    with open(os.path.join(dir_path,"support/rapdb.pkl"), "wb") as f:
        pickle.dump(rapdb, f)
    f.close()
    if (os.path.exists(source_filepath)):
        os.remove(source_filepath)
    if (os.path.exists(dest_filepath)):
        os.remove(dest_filepath)
    print('Build successfully Rapdb database')

if __name__ == '__main__':
    #update_gene_dictionary()
    update_local_database("https://rapdb.dna.affrc.go.jp/download/archive/irgsp1/IRGSP-1.0_representative_annotation_2021-05-10.tsv.gz",
                          ["https://shigen.nig.ac.jp/rice/oryzabase/gene/download?classtag=GENE_EN_LIST","https://shigen.nig.ac.jp/rice/oryzabase/reference/download"])

