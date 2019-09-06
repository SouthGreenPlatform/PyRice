# -*- coding: utf-8 -*-
from pyrice.multi_query import MultiQuery
import time
import csv
from pyrice.utils import search_text
from multiprocessing import cpu_count
from argparse import ArgumentParser
from pyrice.build_dictionary import update_gene_dictionary, update_rapdb_oryzabase


parser = ArgumentParser("PyRice", conflict_handler='resolve')

parser.add_argument("--number_process", type=int)
parser.add_argument("--case",type=int)
parser.add_argument("--multi_processing",action='store_true', default=False)
parser.add_argument("--multi_threading",action='store_true', default=False)
parser.add_argument("--number_gene",type = float)
args = parser.parse_args()

if __name__ == "__main__":
    # # Search gene and query loc
    test = MultiQuery()
    file_id = test.search_gene(chro="chr01", start_pos="1",
                               end_pos="20000", number_process = 4, dbs="all", save_path="./result/")
    print("Output database:", file_id)


    # # Query with chromosome
    test = MultiQuery()
    db = test.query_iric(chro="chr01", start_pos="1",
                         end_pos="20000", number_process = 4, multi_processing=True, multi_threading=True,
                         dbs="all")
    test.save_file(db, save_path="./result/", format=["csv", "html", "json", "pkl"], hyper_link=False)
    print("Output database:", db)


    # # Query with ids, locs and irics
    test = MultiQuery()
    db = test.query_ids_locs(idents=["Os08g0164400", "Os07g0586200"],
                             locs=["LOC_Os10g01006", "LOC_Os07g39750"],
                             irics=["OsNippo01g010050", "OsNippo01g010300"], number_process = 4,
                             multi_processing=True, multi_threading=True, dbs="all")
    test.save_file(db,save_path = "./result/",format=["csv","html","json","pkl"],hyper_link=False)
    print("Output database:",db)

    # # Query with new database
    test = MultiQuery()
    db = test.new_query(atts=['TRAES3BF001000010CFD'], number_process= 4,
                        multi_processing=True,multi_threading=True,dbs=['urgi'])
    test.save_file(db, save_path="./result/", format=["csv", "html", "json", "pkl"], hyper_link=False)
    print("Output database:",db)


# chro="chr01", start_pos="1", end_pos="43270923"
# chro="chr02", start_pos="1", end_pos="35937250"
# chro="chr03", start_pos="1", end_pos="36413819"
# chro="chr04", start_pos="1", end_pos="35502694"
# chro="chr05", start_pos="1", end_pos="29958434"
# chro="chr06", start_pos="1", end_pos="31248787"
# chro="chr07", start_pos="1", end_pos="29697621"
# chro="chr08", start_pos="1", end_pos="28443022"
# chro="chr09", start_pos="1", end_pos="23012720"
# chro="chr10", start_pos="1", end_pos="23207287"
# chro="chr11", start_pos="1", end_pos="29021106"
# chro="chr12", start_pos="1", end_pos="27531856"
