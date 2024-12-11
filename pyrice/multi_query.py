# -*- coding: utf-8 -*-
from multiprocessing import cpu_count, Pool
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from pyrice import utils
import json
import regex
import requests
import pickle
import csv
import pandas as pd
import os
import copy
import json2table
import glob

download_dir = os.path.join(os.path.dirname(utils.__file__),"support/download/")

class MultiQuery():
    """
    This class will represent query gene rice for database
    """
    def __init__(self):
        """
        self.loc_dict: dictionary for looking loc of gene
        self.id_dict: dictionary for looking id of gene
        self.oryzabase: dictionary for looking information of gene on oryzabase database
        self.rapdb: dictionary for looking information of gene on rapdb database
        self.gwas_atlas:  dictionary for looking id of gene on gwas_atlas database
        self.database_file:  database wrapper
        """
        dir_path = os.path.dirname(utils.__file__)
        with open(os.path.join(dir_path, 'support/iric_dict.pkl'), 'rb') as f:
            self.iric_dict = pickle.load(f)
        f.close()
        with open(os.path.join(dir_path, 'support/loc_dict.pkl'), 'rb') as f:
            self.loc_dict = pickle.load(f)
        f.close()
        with open(os.path.join(dir_path, 'support/id_dict.pkl'), 'rb') as f:
            self.id_dict = pickle.load(f)
        f.close()
        with open(os.path.join(dir_path, 'support/oryzabase.pkl'), 'rb') as f:
            self.oryzabase = pickle.load(f)
        f.close()
        with open(os.path.join(dir_path, 'support/rapdb.pkl'), 'rb') as f:
            self.rapdb = pickle.load(f)
        f.close()
        with open(os.path.join(dir_path, 'support/gwas_atlas.json'), 'r') as f:
            self.gwas_atlas = json.load(f)
        f.close()
        with open(os.path.join(dir_path, 'database_description.xml'), 'r') as f:
            self.database_file = f.read()
        f.close()

    def query(self, iricname, db, qfields=[], verbose=False):
        """
        Query one gene by id or loc on each database

        :param iricname: (str) iricname or id of gene
        :param db: (str) name database in 8 databases
        :param qfields: (list) list of loc, id
        :param verbose: (bool) if True print for debug

        :return: a list with format: [iricname,name_db,iric_on_db]
        """
        # Fetch database description
        database_description = BeautifulSoup(self.database_file, "xml").find_all("database", dbname=db.lower())
        if not database_description:
            return
        # Get Headers list
        headers = []
        for header in database_description[0].find_all("header"):
            headers.append(header.text)

        res = utils.execute_query(database_description, qfields, verbose)
        if res == None:
            return
        # Handle HTML based query
        if (database_description[0]["type"] == "text/html"):
            # Handling Connection
            ret = BeautifulSoup(res.content, "lxml")
            if verbose:
                print("return value:", ret)
                print(database_description[0].find_all("data_struct")[0]["identifier"])
            if database_description[0].find_all("data_struct")[0]["identifier"] != "":
                data = ret.find_all(database_description[0].find_all("data_struct")[0]["indicator"],
                                    {database_description[0].find_all("data_struct")[0]["identifier"]:
                                    database_description[0].find_all("data_struct")[0]["identification_string"]})
            else:
                data = ret.find_all(database_description[0].find_all("data_struct")[0]["indicator"])
            if data != []:
                replaceBy = database_description[0].find_all(
                    "prettify")[0]['replaceBy']
                for dataLine in data[0].find_all(database_description[0].find_all("data_struct")[0]["line_separator"]):
                    dict_ = {}
                    i = 0
                    for dataCell in dataLine.find_all(
                            database_description[0].find_all("data_struct")[0]["cell_separator"]):
                        dataFormat = regex.sub(replaceBy + '+', ' ', dataCell.text)
                        if (i < len(headers)):
                            dict_[headers[i]] = dataFormat
                        i += 1
                    if dict_ == {}:
                        continue
                    dict_.pop("", None)
                    if verbose:
                        print(dict_)
                    if len(dict_) >0:
                        return [iricname,db,dict_]
        # Handle JSON based query
        elif (database_description[0]["type"] == "text/JSON"):
            # Return as a List of Dictionary
            if len(res.content) > 3:
                if iricname == "snpseek":
                    return [iricname,qfields[-1],json.loads(res.content.decode('utf-8'))]
                elif db == "ic4r":
                    return [iricname,db,json.loads(res.content.decode('utf-8'))[0][1]]
                elif db == "gramene":
                    r_tmp = json.loads(res.content.decode('utf-8'))
                    if len(r_tmp) > 0:
                        return [iricname,db,r_tmp[0]]
                    else:
                        return [iricname,db,{}]
                else:
                    return [iricname,db,json.loads(res.content.decode('utf-8'))]
            if verbose: print(self.result[db])
        # Handle csv based DB
        # Auto detect and support local csv databases
        fields = database_description[0].find_all("field")
        if (database_description[0]["type"] == "text/csv"):
            if db == "funricegene_genekeywords":
                url=database_description[0].find_all("link")[0]["stern"]
                data = pd.read_csv(url, sep='\t', encoding=database_description[0]["encoding"])
                # Convert to list of lists for compatibility
                ret = data.values.tolist()      
            elif type(res) is requests.models.Response:
                ret = csv.reader(res.content.decode(database_description[0]["encoding"]).splitlines(),
                                 delimiter=list(database_description[0]["deli"])[0], quoting=csv.QUOTE_NONE)
            else:
                ret = csv.reader(res, delimiter=list(database_description[0]["deli"])[0], quoting=csv.QUOTE_NONE)
            l_res = set()
            tmp = []
            dict_2 = dict()
            for row in ret:
                tup_row = tuple(row)
                if tup_row not in l_res:
                    l_res.add(tup_row)
                    i = 0
                    dict_ = {}
                    for header in headers:
                        dict_[header] = row[i]
                        #print(row[i])
                        i += 1
                    f = 0
                    for field in fields:
                        match = True
                        if (dict_[field.text] != qfields[f]) & (qfields[f] != ""):
                            match = False
                            break
                        f += 1
                    if match:
                        for k,v in dict_.items():
                            if k not in dict_2.keys():
                                dict_2.setdefault(k,set())
                                dict_2[k].add(v)
                            else:
                                dict_2[k].add(v)
                        tmp.append(dict_)
            if len(tmp)>0:
                for k, v in dict_2.items():
                    dict_2[k] = repr(v);
                return [iricname,db,dict_2]
        elif database_description[0]["type"] == "javascript":
            if db =="embl_ebi":
                list_of_files = glob.glob(download_dir+'*.tsv') # * means all if need specific format then *.tsv
                if len(list_of_files) > 0:
                    latest_file = max(list_of_files, key=os.path.getctime)
                    dict_jvs = dict()
                    with open(latest_file) as file:
                        rd = csv.reader(file, delimiter="\t", quotechar='"')
                        result = []
                        for row in rd:
                            result.append(row)
                        for i in range(5,len(result)):
                            for pos_att in range(1,len(result[4])):
                                dict_jvs.setdefault(result[i][0]+" - "+result[4][pos_att],result[i][pos_att])
                    # print(dict_jvs)
                    file.close()
                    os.remove(latest_file)
                    return [iricname,db,dict_jvs]
            elif db == "gwas_atlas":
                list_of_files = glob.glob(download_dir + '*.csv')  # * means all if need specific format then *.csv
                if len(list_of_files) > 0:
                    latest_file = max(list_of_files, key=os.path.getctime)
                    data = pd.read_csv(latest_file)
                    data2dict = {}
                    for key in data.columns:
                        data2dict.setdefault(key, [])
                        for value in data[key]:
                            if key == "Mapped Gene(s)" or key == "Consequence Type(s)":
                                if type(value) == str:
                                    value = value.replace('\n', ' ')
                            data2dict[key].append(value)
                    os.remove(latest_file)
                    return [iricname, db, data2dict]

    def save(self, result, save_path, format=None, hyper_link=False):
        """
        Save result of query with differents types of files

        :param result: (dictionary) get after query with query functions
        :param save_path: (str) path to save result after call function
        :param format: (list) 4 format: html, csv, json, pkl
        :param hyper_link: (bool) hyper_link in csv file
        """
        if save_path != None:
            data_folder = save_path + "data/"
            gene_folder = save_path + "gene/"
            if not os.path.exists(data_folder):
                os.makedirs(data_folder)
            if not os.path.exists(gene_folder):
                os.makedirs(gene_folder)
            # ouput data/db.csv
            test = copy.deepcopy(result)
            # filter allow attributes
            filter_ = ["db_type", "gene_idx", "location", "xrefs", "gene_structure", "bins", "homology"]
            annotations =["taxonomy", "familyRoot","pathways","domains"]
            go = ["ancestors"]
            entries = ["subset"]
            ic4r_atts = ["Leaf", "Root", "Panicle"]
            for i in test.keys():
                for k, v in test[i].items():
                    if k == "Gramene":
                        for att in filter_:
                            v.pop(att, None)
                        if "annotations" in v.keys():
                            for att in annotations:
                                v["annotations"].pop(att, None)
                            if "GO" in v["annotations"].keys():
                                for att in go:
                                    v["annotations"]["GO"].pop(att, None)
                                if "entries" in v["annotations"]["GO"].keys():
                                    # list entries
                                    for j in range(len(v["annotations"]["GO"]["entries"])):
                                        # print(v["annotations"]["GO"]["entries"][j],type(v["annotations"]["GO"]["entries"][j]))
                                        for att in entries:
                                            v["annotations"]["GO"]["entries"][j].pop(att, None)
                    elif k == "ic4r":
                       #Get all att of ic4r
                       if v != None:
                           for att in list(v):
                               if att not in ic4r_atts:
                                    v.pop(att,None)
            # Convert output db.csv
            html_dict = dict()
            csv_dict = dict()
            path = os.path.abspath(gene_folder)
            for iricname, databases in test.items():
                new_dict = dict()
                for db,data in databases.items():
                    if data != None :
                        new_data = dict()
                        # print(data)
                        for att,value in data.items():
                            if value != "":
                                new_data.setdefault(db + "." + att, value)
                        new_dict.update(new_data)
                    # Rapdb + MSU name
                if iricname in self.iric_dict.keys():
                    all_name = ""
                    if len(self.iric_dict[iricname]["msu7Name"]) > 0 and len(self.iric_dict[iricname]["raprepName"]) > 0:
                        all_name = iricname + "_" + next(iter(self.iric_dict[iricname]["raprepName"])) + "_" + next(iter(self.iric_dict[iricname]["msu7Name"]))
                    elif len(self.iric_dict[iricname]["msu7Name"]) > 0 and len(self.iric_dict[iricname]["raprepName"]) == 0:
                        all_name = iricname + "_" + next(iter(self.iric_dict[iricname]["msu7Name"]))
                    elif len(self.iric_dict[iricname]["msu7Name"]) == 0 and len(self.iric_dict[iricname]["raprepName"]) > 0:
                        all_name = iricname + "_" + next(iter(self.iric_dict[iricname]["raprepName"]))
                    else:
                        all_name = iricname
                else:
                    all_name = iricname
                html_dict.setdefault("<a href= \"../gene/" + all_name + ".html\" target=\"_blank\">" + all_name + "</a>", new_dict)
                if hyper_link == True:
                    csv_dict.setdefault("=HYPERLINK(\"file://"+path+"/"+ all_name + ".html\""+",\""+ all_name+"\")",new_dict)
                else:
                    csv_dict.setdefault(all_name, new_dict)
               #= "\"=HYPERLINK(\"\"file://" + DocumentDataType.strDirectoy + docName + "\"\",\"\"" + DocumentDataType.strDirectoy + docName + "\"\")\"" + ",";
            for form in format:
                if form == "csv" :
                    my_db = data_folder + "db" + '.csv'
                    df = pd.DataFrame.from_dict(csv_dict, orient='index')
                    df.reset_index(level=0, inplace=True)
                    df.rename(columns={'index': 'iric_name'}, inplace=True)
                    with open(my_db, 'w') as f:
                        df.to_csv(f, header=True)
                    f.close()
                elif form == "pkl":
                    my_db = data_folder + "db" + '.pkl'
                    df = pd.DataFrame.from_dict(csv_dict, orient='index')
                    df.reset_index(level=0, inplace=True)
                    df.rename(columns={'index': 'iric_name'}, inplace=True)
                    with open(my_db,"wb") as f:
                        df.to_pickle(f)
                    f.close()
                elif form == "html":
                    my_db = data_folder + "db" + '.html'
                    df = pd.DataFrame.from_dict(html_dict, orient='index')
                    # HTML(df.to_html(my_db,escape=False))
                    df.to_html(my_db, escape=False)
                elif form =="json":
                    my_db = data_folder + "db" + '.json'
                    with open(my_db, 'w') as f:
                        json.dump(test,f)
                    f.close()
            # output gene/iricname.txt
            test = copy.deepcopy(result)
            # filter allow attributes
            filter_ = ["gene_structure", "bins", ]
            annotations = ["taxonomy", "familyRoot"]
            go = ["ancestors"]
            entries = ["subset"]
            homology = ["gene_tree"]
            homologous_genes = ["syntenic_ortholog_one2one", "ortholog_one2many"]
            for i in test.keys():
                for k, v in test[i].items():
                    if k == "Gramene":
                        for att in filter_:
                            v.pop(att, None)
                        if "annotations" in v.keys():
                            for att in annotations:
                                v["annotations"].pop(att, None)
                            if "GO" in v["annotations"].keys():
                                for att in go:
                                    v["annotations"]["GO"].pop(att, None)
                                if "entries" in v["annotations"]["GO"].keys():
                                    # list entries
                                    for j in range(len(v["annotations"]["GO"]["entries"])):
                                        for att in entries:
                                            v["annotations"]["GO"]["entries"][j].pop(att, None)
                        if "homology" in v.keys():
                            for att in homology:
                                v["homology"].pop(att, None)
                            if "homologous_genes" in v["homology"].keys():
                                for att in homologous_genes:
                                    v["homology"]["homologous_genes"].pop(att, None)
            for iricname in test.keys():
                # Rapdb + MSU name
                if iricname in self.iric_dict.keys():
                    all_name = ""
                    if len(self.iric_dict[iricname]["msu7Name"]) > 0 and len(self.iric_dict[iricname]["raprepName"]) > 0:
                        all_name = iricname + "_" + next(iter(self.iric_dict[iricname]["raprepName"])) + "_" + next(iter(self.iric_dict[iricname]["msu7Name"]))
                    elif len(self.iric_dict[iricname]["msu7Name"]) > 0 and len(self.iric_dict[iricname]["raprepName"]) == 0:
                        all_name = iricname + "_" + next(iter(self.iric_dict[iricname]["msu7Name"]))
                    elif len(self.iric_dict[iricname]["msu7Name"]) == 0 and len(self.iric_dict[iricname]["raprepName"]) > 0:
                        all_name = iricname + "_" + next(iter(self.iric_dict[iricname]["raprepName"]))
                    else:
                        all_name = iricname
                else:
                    all_name = iricname
                my_gene = gene_folder + all_name
                build_direction = "LEFT_TO_RIGHT"
                table_attributes = {"style": "width:100%","class" : "table table-striped","border" : 1 }
                html = json2table.convert(test[iricname],
                                          build_direction=build_direction,
                                          table_attributes=table_attributes)
                #Check if have format ->save
                for form in format:
                    if form == "html":
                        # html formart
                        with open(my_gene+'.html', "w") as f:
                            f.write(html)
                        f.close()
                    elif form == "json":
                        #json formart
                        with open(my_gene+'.json', "w") as f:
                            json.dump(test[iricname], f)
                        f.close()


    def query_expansion(self, ids = None, locs = None, irics = None, number_process = cpu_count()-1):
        """
        Query gene using id, loc or iric

        :param ids: (list) list id of gene
        :param locs: (list) list loc of gene
        :param irics: (list) list iric name of gene
        :param number_process: (int) number of process or number of threading

        :return: a dictionary, format: gene:{database: attribute}
        """
        set_iric = set()
        if ids != None:
            for id in ids:
                if id in self.id_dict.keys():
                    set_iric.add(self.id_dict[id])
        if locs != None:
            for loc in locs:
                if loc in self.loc_dict.keys():
                    set_iric.add(self.loc_dict[loc])
        if irics != None:
            for iric in irics:
                if iric in self.iric_dict.keys():
                    set_iric.add(iric)

        self.result = dict()
        # Check support of database
        name_db = ["planttfdb_tf","planttfdb_target_gene"]
        # Query in multi_database
        # i = 1
        number_query = len(set_iric)
        list_ids = []
        list_dbs = []
        list_key = []
        for key in set_iric:
            value = self.iric_dict[key]
            # print("Query iricname: {} --- Gene {}/{}".format(key, i, number_query))
            # i += 1
            self.result.setdefault(key, dict())
            for db in name_db:
                if db == "planttfdb_tf" or db == "planttfdb_target_gene":
                    for loc in value["msu7Name"]:
                        list_ids.append([loc])
                        list_dbs.append(db)
                        list_key.append(key)
        try:
            p = ThreadPoolExecutor(max_workers=number_process)
            tmp = p.map(self.query, list_key, list_dbs, list_ids)
            for t in tmp:
                if t != None:
                    self.result[t[0]].setdefault(t[1], t[2])
        finally:
            p.shutdown()
        return self.result


    def query_by_chromosome(self, chro, start_pos, end_pos, number_process = cpu_count()-1, multi_processing = False,
                   multi_threading = True, dbs='all', query_expansion = False):
        """
        Query gene by chromosome

        :param chro: (str) chromosome (ex: "chr01")
        :param start_pos: (str) start of chromosome
        :param end_pos: (str) end of chromosome
        :param number_process: (int) number of process or number of threading
        :param multi_processing: (bool) if True, use multi_processing
        :param multi_threading: (bool) if True, use multi_threading
        :param dbs: (list) list databases (support 10 available databases)
        :param query_expansion: (bool) if True, find list list of associated genes

        :return: a dictionary, format : gene:{database: attributes}
        """
        #Check support of database
        support_db = ["oryzabase", "rapdb", "gramene", "funricegene_genekeywords",
                   "funricegene_faminfo", "msu",
                   "funricegene_geneinfo","embl_ebi","gwas_atlas","planttfdb_tf","planttfdb_target_gene"]# ic4r,
        if dbs == 'all':
            name_db = support_db
        else:
            name_db= []
            for db in dbs:
                if db not in support_db:
                    print("Don't support databse: ", db)
                else:
                    name_db.append(db)
        #Query in multi_database
        i=1
        file_id = self.search_on_chromosome(chro=chro,start_pos=start_pos,end_pos=end_pos,number_process = number_process)
        self.result = dict()
        if query_expansion:
            list_expansion = self.query_expansion(irics = list(file_id.keys()))
            set_target_gene = set()
            for new_iric in list_expansion.keys():
                if 'planttfdb_tf' in list_expansion[new_iric]:
                    list_tf = list_expansion[new_iric]['planttfdb_tf']['results']['bindings']
                    if len(list_tf) > 0:
                        for value in list_tf:
                            target_gene = value['TF']['value'].split('/')[-1]
                            set_target_gene.add(target_gene)
                if 'planttfdb_target_gene' in list_expansion[new_iric]:
                    list_target_gene = list_expansion[new_iric]['planttfdb_target_gene']['results']['bindings']
                    if len(list_target_gene) > 0:
                        for value in list_tf:
                            target_gene = value['target_gene']['value'].split('/')[-1]
                            set_target_gene.add(target_gene)
            for target_gene in set_target_gene:
                if target_gene in self.loc_dict.keys():
                    file_id.setdefault(self.loc_dict[target_gene],self.iric_dict[self.loc_dict[target_gene]])
            print("Add {} associated genes for query information".format(len(set_target_gene)))
        self.result = dict()
        number_query = len(file_id)
        # No multi-processing and No multi-threading
        if multi_processing == False and multi_threading == False:
            for key, value in file_id.items():
                print("Query iricname: {} --- Gene {}/{}".format(key, i, number_query))
                i += 1
                self.result.setdefault(key, dict())
                for db in name_db:
                    if db == 'oryzabase':
                        if key in self.oryzabase.keys():
                            self.result[key].setdefault("oryzabase", self.oryzabase[key]["oryzabase"])
                    elif db == "rapdb":
                        if key in self.rapdb.keys():
                            self.result[key].setdefault("rapdb", self.rapdb[key]["rapdb"])
                    elif db == "gramene" or db == "ic4r" or db=="embl_ebi":
                        for ident in value["raprepName"]:
                            tmp = self.query(key, db, [ident])
                            if tmp != None:
                                self.result[tmp[0]].setdefault(tmp[1], tmp[2])
                    elif db == "msu" or db == "planttfbd_tf" or db =="planttfdb_target_gene":
                        for loc in value["msu7Name"]:
                            tmp = self.query(key, db, [loc])
                            if tmp != None:
                                self.result[tmp[0]].setdefault(tmp[1], tmp[2])
                    elif db == "funricegene_genekeywords" or db == "funricegene_faminfo" or db == "funricegene_geneinfo":
                        if len(value["raprepName"]) > 0:
                            for ident in value["raprepName"]:
                                if len(value["msu7Name"]) > 0:
                                    for loc in value["msu7Name"]:
                                        tmp = self.query(key, db, [ident,loc])
                                        if tmp != None:
                                            self.result[tmp[0]].setdefault(tmp[1], tmp[2])
                                else:
                                    tmp = self.query(key, db, [ident, ""])
                                    if tmp != None:
                                        self.result[tmp[0]].setdefault(tmp[1], tmp[2])
                        else:
                            for loc in value["msu7Name"]:
                                tmp = self.query(key, db, ["", loc])
                                if tmp != None:
                                    self.result[tmp[0]].setdefault(tmp[1], tmp[2])
                    elif db=="gwas_atlas":
                        for ident in value["raprepName"]:
                            if ident in self.gwas_atlas.keys():
                                tmp = self.query(key, db, [self.gwas_atlas[ident]])
                                if tmp != None:
                                    self.result[tmp[0]].setdefault(tmp[1], tmp[2])
        # Multi-processing and Multi-threading
        elif multi_processing == True and multi_threading== True:
            try:
                list_process = []
                list_dbs = []
                list_ids = []
                list_key = []
                if len(file_id) > number_process:
                    gene_per_process = int(len(file_id)/number_process)
                else:
                    gene_per_process = len(file_id)
                count_gene = 0
                p = Pool(processes=number_process) #number_core*2
                # p = ThreadPoolExecutor(max_workers=number_process)
                for key, value in file_id.items():
                    print("Query iricname: {} --- Gene {}/{}".format(key, i, number_query))
                    i+=1
                    self.result.setdefault(key,dict())
                    # new_save_result= partial(self.save_refult,result=self.result)
                    for db in name_db:
                        if db == 'oryzabase':
                            if key in self.oryzabase.keys():
                                self.result[key].setdefault("oryzabase", self.oryzabase[key]["oryzabase"])
                        elif db == "rapdb":
                            if key in self.rapdb.keys():
                                self.result[key].setdefault("rapdb", self.rapdb[key]["rapdb"])
                        elif db == "gramene" or db == "ic4r" or db=="embl_ebi":
                            for ident in value["raprepName"]:
                                list_ids.append([ident])
                                list_dbs.append(db)
                                list_key.append(key)
                        elif db == "msu" or db == "planttfdb_tf" or db == "planttfdb_target_gene":
                            for loc in value["msu7Name"]:
                                list_ids.append([loc])
                                list_dbs.append(db)
                                list_key.append(key)
                        elif db == "funricegene_genekeywords" or db == "funricegene_faminfo" or db == "funricegene_geneinfo":
                            if len(value["raprepName"]) >0:
                                for ident in value["raprepName"]:
                                    if len(value["msu7Name"]) >0:
                                        for loc in value["msu7Name"]:
                                            list_ids.append([ident,loc])
                                            list_dbs.append(db)
                                            list_key.append(key)
                                    else:
                                        list_ids.append([ident,""])
                                        list_dbs.append(db)
                                        list_key.append(key)
                            else:
                                for loc in value["msu7Name"]:
                                    list_ids.append(["",loc])
                                    list_dbs.append(db)
                                    list_key.append(key)
                        elif db=="gwas_atlas":
                            for ident in value["raprepName"]:
                                if ident in self.gwas_atlas.keys():
                                    list_ids.append([self.gwas_atlas[ident]])
                                    list_dbs.append(db)
                                    list_key.append(key)
                    count_gene += 1
                    if count_gene == gene_per_process or i-1 == len(file_id):
                        list_process.append(p.apply_async(self.query_multi_threading, args=(list_key, list_dbs, list_ids)))
                        list_ids = []
                        list_dbs = []
                        list_key = []
                        count_gene = 0
                for count_process in range(len(list_process)):
                    result_process = list_process[count_process].get()
                    if result_process != None:
                        for iricname,data in result_process.items():
                            self.result[iricname].update(data)

            finally:
                p.close()
                p.join()
        # Multi-processing or Multi-threading
        else:
            list_ids = []
            list_dbs = []
            list_key = []
            for key, value in file_id.items():
                print("Query iricname: {} --- Gene {}/{}".format(key, i, number_query))
                i += 1
                self.result.setdefault(key, dict())
                for db in name_db:
                    if db == 'oryzabase':
                        if key in self.oryzabase.keys():
                            self.result[key].setdefault("oryzabase", self.oryzabase[key]["oryzabase"])
                    elif db == "rapdb":
                        if key in self.rapdb.keys():
                            self.result[key].setdefault("rapdb", self.rapdb[key]["rapdb"])
                    elif db == "gramene" or db == "ic4r" or db=="embl_ebi":
                        for ident in value["raprepName"]:
                            list_ids.append([ident])
                            list_dbs.append(db)
                            list_key.append(key)
                    elif db == "msu" or db == "planttfdb_tf" or db =="planttfdb_target_gene":
                        for loc in value["msu7Name"]:
                            list_ids.append([loc])
                            list_dbs.append(db)
                            list_key.append(key)
                    elif db == "funricegene_genekeywords" or db == "funricegene_faminfo" or db == "funricegene_geneinfo":
                        if len(value["raprepName"]) > 0:
                            for ident in value["raprepName"]:
                                if len(value["msu7Name"]) > 0:
                                    for loc in value["msu7Name"]:
                                        list_ids.append([ident,loc])
                                        list_dbs.append(db)
                                        list_key.append(key)
                                else:
                                    list_ids.append([ident, ""])
                                    list_dbs.append(db)
                                    list_key.append(key)
                        else:
                            for loc in value["msu7Name"]:
                                list_ids.append(["", loc])
                                list_dbs.append(db)
                                list_key.append(key)
                    elif db=="gwas_atlas":
                        for ident in value["raprepName"]:
                            if ident in self.gwas_atlas.keys():
                                list_ids.append([self.gwas_atlas[ident]])
                                list_dbs.append(db)
                                list_key.append(key)
            if multi_processing == True and multi_threading == False:
                try:
                    p = Pool(processes=number_process)
                    tmp = p.starmap(self.query,zip(list_key,list_dbs,list_ids))
                    for t in tmp:
                        if t!= None:
                            self.result[t[0]].setdefault(t[1], t[2])
                finally:
                    p.close()
                    p.join()
            elif multi_processing == False and multi_threading == True:
                try:
                    p = ThreadPoolExecutor(max_workers=number_process)
                    tmp = p.map(self.query, list_key, list_dbs, list_ids)
                    for t in tmp:
                        if t != None:
                            self.result[t[0]].setdefault(t[1], t[2])
                finally:
                    p.shutdown()
        return self.result

    def query_multi_threading(self, list_key, list_dbs, list_ids, number_threading = 2):
        """
        Query function when using both of multi_processing and multi_threading

        :param list_key: (list) list of iricname
        :param list_dbs: (list) list of database
        :param list_ids: (list) list of id or locus
        :param number_threading: (int) number threading per core

        :return: a dictionary, format: gene:{database:attributes}
        """
        result = dict()
        try:
            p = ThreadPoolExecutor(max_workers=number_threading)
            tmp = p.map(self.query,list_key,list_dbs,list_ids)
            for t in tmp:
                if t != None:
                    result.setdefault(t[0],dict())
                    result[t[0]].setdefault(t[1],t[2])
        finally:
            p.shutdown()
        return result

    def query_by_ids(self, ids = None, locs = None, irics = None, number_process = cpu_count()-1, multi_processing = False,
                   multi_threading = True, dbs='all',query_expansion = False):
        """
        Query gene using id, loc or iric

        :param ids: (list) list id of gene
        :param locs: (list) list loc of gene
        :param irics: (list) list iric name of gene
        :param number_process: (int) number of process or number of threading
        :param multi_processing: (bool) if True use multi_processing
        :param multi_threading: (bool) if True use multi_threading
        :param dbs: (list) databases (support 10 available databases)
        :param query_expansion: (bool) if True, find list list of associated genes

        :return: a dictionary, format: gene:{database: attribute}
        """
        set_iric = set()
        if ids != None:
            for id in ids:
                if id in self.id_dict.keys():
                    set_iric.add(self.id_dict[id])
        if locs != None:
            for loc in locs:
                if loc in self.loc_dict.keys():
                    set_iric.add(self.loc_dict[loc])
        if irics != None:
            for iric in irics:
                if iric in self.iric_dict.keys():
                    set_iric.add(iric)
        if query_expansion:
            list_expansion = self.query_expansion(irics = list(set_iric))
            set_target_gene = set()
            for new_iric in list_expansion.keys():
                if 'planttfdb_tf' in list_expansion[new_iric]:
                    list_tf = list_expansion[new_iric]['planttfdb_tf']['results']['bindings']
                    if len(list_tf) > 0:
                        for value in list_tf:
                            target_gene = value['TF']['value'].split('/')[-1]
                            set_target_gene.add(target_gene)
                if 'planttfdb_target_gene' in list_expansion[new_iric]:
                    list_target_gene = list_expansion[new_iric]['planttfdb_target_gene']['results']['bindings']
                    if len(list_target_gene) > 0:
                        for value in list_tf:
                            target_gene = value['target_gene']['value'].split('/')[-1]
                            set_target_gene.add(target_gene)
            for target_gene in set_target_gene:
                if target_gene in self.loc_dict.keys():
                    set_iric.add(self.loc_dict[target_gene])
            print("Add {} associated genes for query information".format(len(set_target_gene)))
        self.result = dict()
        # Check support of database
        support_db = ["oryzabase", "gramene", "funricegene_genekeywords",
                      "funricegene_faminfo", "msu", "rapdb", "ic4r",
                      "funricegene_geneinfo","embl_ebi","gwas_atlas","planttfdb_tf","planttfdb_target_gene"]
        if dbs == 'all':
            name_db = support_db
        else:
            name_db = []
            for db in dbs:
                if db not in support_db:
                    print("Don't support databse: ", db)
                else:
                    name_db.append(db)
        # Query in multi_database
        i = 1
        number_query = len(set_iric)
        if multi_processing == False and multi_threading == False:
            for key in set_iric:
                value = self.iric_dict[key]
                print("Query iricname: {} --- Gene {}/{}".format(key, i, number_query))
                i += 1
                self.result.setdefault(key, dict())
                for db in name_db:
                    if db == 'oryzabase':
                        if key in self.oryzabase.keys():
                            self.result[key].setdefault("oryzabase", self.oryzabase[key]["oryzabase"])
                    elif db == "rapdb":
                        if key in self.rapdb.keys():
                            self.result[key].setdefault("rapdb", self.rapdb[key]["rapdb"])
                    elif db == "gramene" or db == "ic4r" or db == "embl_ebi":
                        for ident in value["raprepName"]:
                            tmp = self.query(key, db, [ident])
                            if tmp != None:
                                self.result[tmp[0]].setdefault(tmp[1], tmp[2])
                    elif db == "msu" or db == "planttfdb_tf" or db =="planttfdb_target_gene":
                        for loc in value["msu7Name"]:
                            tmp = self.query(key, db, [loc])
                            if tmp != None:
                                self.result[tmp[0]].setdefault(tmp[1], tmp[2])
                    elif db == "funricegene_genekeywords" or db == "funricegene_faminfo" or db == "funricegene_geneinfo":
                        if len(value["raprepName"]) > 0:
                            for ident in value["raprepName"]:
                                if len(value["msu7Name"]) > 0:
                                    for loc in value["msu7Name"]:
                                        tmp = self.query(key, db, [ident,loc])
                                        if tmp != None:
                                            self.result[tmp[0]].setdefault(tmp[1], tmp[2])
                                else:
                                    tmp = self.query(key, db, [ident, ""])
                                    if tmp != None:
                                        self.result[tmp[0]].setdefault(tmp[1], tmp[2])
                        else:
                            for loc in value["msu7Name"]:
                                tmp = self.query(key, db, ["", loc])
                                if tmp != None:
                                    self.result[tmp[0]].setdefault(tmp[1], tmp[2])
                    elif db == "gwas_atlas":
                        for ident in value["raprepName"]:
                            if ident in self.gwas_atlas.keys():
                                tmp = self.query(key, db, [self.gwas_atlas[ident]])
                                if tmp != None:
                                    self.result[tmp[0]].setdefault(tmp[1], tmp[2])
        # Multi-processing and Multi-threading
        elif multi_processing == True and multi_threading== True:
            try:
                list_process = []
                list_dbs = []
                list_ids = []
                list_key = []
                if len(set_iric) > number_process:
                    gene_per_process = int(len(set_iric)/number_process)
                else:
                    gene_per_process = len(set_iric)
                count_gene = 0
                p = Pool(processes=number_process) #number_core*2
                # p = ThreadPoolExecutor(max_workers=number_process)
                for key in set_iric:
                    value = self.iric_dict[key]
                    print("Query iricname: {} --- Gene {}/{}".format(key, i, number_query))
                    i+=1
                    self.result.setdefault(key,dict())
                    # new_save_result= partial(self.save_refult,result=self.result)
                    for db in name_db:
                        if db == 'oryzabase':
                            if key in self.oryzabase.keys():
                                self.result[key].setdefault("oryzabase", self.oryzabase[key]["oryzabase"])
                        elif db == "rapdb":
                            if key in self.rapdb.keys():
                                self.result[key].setdefault("rapdb", self.rapdb[key]["rapdb"])
                        elif db == "gramene" or db == "ic4r" or db=="embl_ebi":
                            for ident in value["raprepName"]:
                                list_ids.append([ident])
                                list_dbs.append(db)
                                list_key.append(key)
                        elif db == "msu" or db == "planttfdb_tf" or db =="planttfdb_target_gene":
                            for loc in value["msu7Name"]:
                                list_ids.append([loc])
                                list_dbs.append(db)
                                list_key.append(key)
                        elif db == "funricegene_genekeywords" or db == "funricegene_faminfo" or db == "funricegene_geneinfo":
                            if len(value["raprepName"]) >0:
                                for ident in value["raprepName"]:
                                    if len(value["msu7Name"]) >0:
                                        for loc in value["msu7Name"]:
                                            list_ids.append([ident,loc])
                                            list_dbs.append(db)
                                            list_key.append(key)
                                    else:
                                        list_ids.append([ident,""])
                                        list_dbs.append(db)
                                        list_key.append(key)
                            else:
                                for loc in value["msu7Name"]:
                                    list_ids.append(["",loc])
                                    list_dbs.append(db)
                                    list_key.append(key)
                        elif db == "gwas_atlas":
                            for ident in value["raprepName"]:
                                if ident in self.gwas_atlas.keys():
                                    list_ids.append([self.gwas_atlas[ident]])
                                    list_dbs.append(db)
                                    list_key.append(key)
                    count_gene += 1
                    if count_gene == gene_per_process or i-1 == len(set_iric):
                        list_process.append(p.apply_async(self.query_multi_threading, args=(list_key, list_dbs, list_ids)))
                        list_ids = []
                        list_dbs = []
                        list_key = []
                        count_gene = 0
                for count_process in range(len(list_process)):
                    result_process = list_process[count_process].get()
                    if result_process != None:
                        for iricname,data in result_process.items():
                            self.result[iricname].update(data)
            finally:
                p.close()
                p.join()
        # Multi-processing or Multi-threading
        else:
            list_ids = []
            list_dbs = []
            list_key = []
            for key in set_iric:
                value = self.iric_dict[key]
                print("Query iricname: {} --- Gene {}/{}".format(key, i, number_query))
                i += 1
                self.result.setdefault(key, dict())
                for db in name_db:
                    if db == 'oryzabase':
                        if key in self.oryzabase.keys():
                            self.result[key].setdefault("oryzabase", self.oryzabase[key]["oryzabase"])
                    elif db == "rapdb":
                        if key in self.rapdb.keys():
                            self.result[key].setdefault("rapdb", self.rapdb[key]["rapdb"])
                    elif db == "gramene" or db == "ic4r" or db=="embl_ebi":
                        for ident in value["raprepName"]:
                            list_ids.append([ident])
                            list_dbs.append(db)
                            list_key.append(key)
                    elif db == "msu" or db == "planttfdb_tf" or db =="planttfdb_target_gene":
                        for loc in value["msu7Name"]:
                            list_ids.append([loc])
                            list_dbs.append(db)
                            list_key.append(key)
                    elif db == "funricegene_genekeywords" or db == "funricegene_faminfo" or db == "funricegene_geneinfo":
                        if len(value["raprepName"]) > 0:
                            for ident in value["raprepName"]:
                                if len(value["msu7Name"]) > 0:
                                    for loc in value["msu7Name"]:
                                        list_ids.append([ident,loc])
                                        list_dbs.append(db)
                                        list_key.append(key)
                                else:
                                    list_ids.append([ident, ""])
                                    list_dbs.append(db)
                                    list_key.append(key)
                        else:
                            for loc in value["msu7Name"]:
                                list_ids.append(["", loc])
                                list_dbs.append(db)
                                list_key.append(key)
                    elif db == "gwas_atlas":
                        for ident in value["raprepName"]:
                            if ident in self.gwas_atlas.keys():
                                list_ids.append([self.gwas_atlas[ident]])
                                list_dbs.append(db)
                                list_key.append(key)

            if multi_processing == True and multi_threading == False:
                try:
                    p = Pool(processes=number_process)
                    tmp = p.starmap(self.query,zip(list_key,list_dbs,list_ids))
                    for t in tmp:
                        if t!= None:
                            self.result[t[0]].setdefault(t[1], t[2])
                finally:
                    p.close()
                    p.join()
            elif multi_processing == False and multi_threading == True:
                try:
                    p = ThreadPoolExecutor(max_workers=number_process)
                    tmp = p.map(self.query, list_key, list_dbs, list_ids)
                    for t in tmp:
                        if t != None:
                            self.result[t[0]].setdefault(t[1], t[2])
                finally:
                    p.shutdown()
        return self.result

    def query_new_database(self, atts, number_process = cpu_count()-1, multi_processing = False, multi_threading = True ,dbs = None):
        """
        Query for new attributes on new databases

        :param atts: (list) list of new attributes
        :param number_process: (int) number of process or number of threading
        :param multi_processing: (bool) if True use multi_processing
        :param multi_threading: (bool) if True use multi_threading
        :param dbs: (list) list of new databases

        :return: dictionary, format : attribute:{database: information of attribute}
        """
        self.result = dict()
        name_db = dbs
        # Query in multi_database
        number_query = len(atts)
        list_key = []
        list_dbs = []
        list_ids = []
        for att in atts:
            for db in name_db:
                list_key.append(att)
                list_ids.append(att)
                list_dbs.append(db)
        i = 1
        number_query = len(atts)
        if multi_processing == False and multi_threading == False:
            for key in atts:
                print("Query attribute: {} --- attribute {}/{}".format(key, i, number_query))
                self.result.setdefault(key,dict())
                for db in name_db:
                    tmp = self.query(key, db, [key])
                    if tmp != None:
                        self.result[tmp[0]].setdefault(tmp[1], tmp[2])
                i+=1
        # Multi-processing and Multi-threading
        elif multi_processing == True and multi_threading == True:
            try:
                list_process = []
                list_dbs = []
                list_ids = []
                list_key = []
                if len(atts) > number_process:
                    gene_per_process = int(len(atts) / number_process)
                else:
                    gene_per_process = len(atts)
                count_gene = 0
                p = Pool(processes=number_process)  # number_core*2
                for key in atts:
                    print("Query attribute: {} --- attribute {}/{}".format(key, i, number_query))
                    self.result.setdefault(key, dict())
                    for db in name_db:
                        list_key.append(key)
                        list_dbs.append(db)
                        list_ids.append(key)
                    i += 1
                    count_gene += 1
                    if count_gene == gene_per_process or i - 1 == len(atts):
                        list_process.append(
                            p.apply_async(self.query_multi_threading, args=(list_key, list_dbs, list_ids)))
                        list_ids = []
                        list_dbs = []
                        list_key = []
                        count_gene = 0
                for count_process in range(len(list_process)):
                    result_process = list_process[count_process].get()
                    if result_process != None:
                        for iricname, data in result_process.items():
                            self.result[iricname].update(data)
            finally:
                p.close()
                p.join()
        # Multi-processing or Multi-threading
        else:
            list_ids = []
            list_dbs = []
            list_key = []
            for key in atts:
                print("Query attribute: {} --- attribute {}/{}".format(key, i, number_query))
                self.result.setdefault(key, dict())
                for db in name_db:
                    list_key.append(key)
                    list_dbs.append(db)
                    list_ids.append(key)
                i+=1
            if multi_processing == True and multi_threading == False:
                try:
                    p = Pool(processes=number_process)
                    tmp = p.starmap(self.query, zip(list_key, list_dbs, list_ids))
                    for t in tmp:
                        if t != None:
                            self.result[t[0]].setdefault(t[1], t[2])
                finally:
                    p.close()
                    p.join()
            elif multi_processing == False and multi_threading == True:
                try:
                    p = ThreadPoolExecutor(max_workers=number_process)
                    tmp = p.map(self.query, list_key, list_dbs, list_ids)
                    for t in tmp:
                        if t != None:
                            self.result[t[0]].setdefault(t[1], t[2])
                finally:
                    p.shutdown()
        return self.result

    def search_on_chromosome(self, chro, start_pos, end_pos, number_process = cpu_count()-1, save_path = None, dbs='all'):
        """
        Search gene by potision on chromosome

        :param chro: (str) chromosome (ex: "chr01")
        :param start_pos: (str) start of chromosome
        :param end_pos: (str) end of chromosome
        :param number_process: (int) number of threading
        :param dbs: (list) list databases (support 3 available databases)
        :param save_path: (str) path to save result after call function

        :return: a dictionary, format: iricname:{{msu7Name:LOC_Os..},{raprepName:Os..},{contig:chr0..},{fmin:12..},{fmax:22...}}
        """
        self.result = dict()
        if dbs == 'all':
            name_db = ["rap", "msu7", "iric"]
        else:
            name_db = dbs
        self.result.setdefault('snpseek', dict())
        list_ids = []
        list_dbs = []
        list_key = []
        for i in range(len(dbs)):
            list_dbs.append('snpseek')
            list_ids.append([str(chro), str(start_pos), str(end_pos), name_db[i]])
            list_key.append('snpseek')
        try:
            p = ThreadPoolExecutor(max_workers=number_process)
            tmp = p.map(self.query,list_key,list_dbs,list_ids)
            for t in tmp:
                if t != None:
                    self.result[t[0]].setdefault(t[1], t[2])
        finally:
            p.shutdown()
        item_dict = dict()
        key_att = "iricname"
        id_att = "raprepName"
        id_att_sup = "rappredName"
        loc_att = "msu7Name"
        contig = "contig"
        fmin = "fmin"
        fmax = "fmax"
        #Build dictionary iricname:{{msu7Name:LOC_Os..},{raprepName:Os}}
        for key, value in self.result.items():
            for db, list_gene in value.items():
                for gene in list_gene:
                    if gene[key_att] not in item_dict.keys():
                        item_dict.setdefault(gene[key_att],dict())
                        item_dict[gene[key_att]].setdefault("msu7Name",set())
                        item_dict[gene[key_att]].setdefault("raprepName", set())
                        item_dict[gene[key_att]].setdefault("contig", gene[contig])
                        item_dict[gene[key_att]].setdefault("fmin", gene[fmin])
                        item_dict[gene[key_att]].setdefault("fmax", gene[fmax])
                    if gene[loc_att] != None:
                        for l in gene[loc_att].split(','):
                            item_dict[gene[key_att]]["msu7Name"].add(l)
                    if gene[id_att] != None:
                        for g in gene[id_att].split(','):
                            item_dict[gene[key_att]]["raprepName"].add(g)
                        continue
                    if gene[id_att_sup] != None:
                        for g in gene[id_att_sup].split(','):
                            item_dict[gene[key_att]]["raprepName"].add(g)
        #Save output
        if save_path != None:
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            my_db = save_path + chro +"_items.csv"
            df = pd.DataFrame.from_dict(item_dict, orient='index')
            with open(my_db, 'w') as f:
                df.to_csv(f, header=True)
            f.close()
        return item_dict
