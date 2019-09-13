"""Helper module
Handle supportive function such as connection handling, path checking and error handling
"""
# -*- coding: utf-8 -*-
import os
import requests
from bs4 import BeautifulSoup
import urllib3

def connection_error(link, data=""):
    """
    Get result with request post or request get

    :param link: (str) url
    :param data: (str) data to give to the form

    :return: object of requests
    """
    try:
        urllib3.disable_warnings()
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}
        #print(link)
        if data!= "":
            res = requests.post(link, data=data, headers=headers,verify=False)
        else:
            res = requests.get(link, allow_redirects=False,stream=True,verify=False)
        if res.status_code != 200:
            print('Server Error: ' + str(res.status_code) + '\n' + 'For url:' + link)
            #raise Exception('Server Error: ' + str(res.status_code) + '\n' + 'For url:' + link)
            # sys.exit(1)
        return res
    except requests.exceptions.RequestException as error:
        print("Can't connect: {} - Eror: {}".format(link,error))
        return
        #raise Exception("Internet Connection error")
        # sys.exit(1)

def execute_query(db, qfields=[], verbose=False):
    """
    Get url and result of api databases

    :param db: (str) name of database
    :param qfields: (list) list of loc,id
    :param verbose: (bool) if True print for debug

    :return: information of gene after send request to url api
    """
    #Get query qfields list
    fields = db[0].find_all("field")
    # Prepare URL
    link = db[0].find_all("link")[0]["stern"]
    # Compile URL
    if link[:4] == 'http':
        if db[0]["method"] == "POST":
            i = 0
            for field in fields:
                data = {field.text: qfields[i]}
                i += 1
            return connection_error(link, data)
        elif db[0]["method"] == "GET":
            query_string = ""
            if db[0]["type"] != "text/csv":
                i = 0
                for field in fields:
                    # Detect controller field (always first field)
                    if "lowercase" in field:
                        print(qfields[i].lower())
                    if field.text == "":
                        query_string += qfields[i] + "?"
                    # All other fields are query fields
                    else:
                        query_string += field.text + field["op"] + qfields[i] + "&"
                    i += 1
                query_string = query_string[:-1]
                link += query_string + \
                        db[0].find_all("link")[0]["aft"]
                if verbose: print(link)
            return connection_error(link)
    else:
        return open(link)

def search(df, text):
    """
    Search function on result (file .pkl)

    :param df: (dataframe) dataframe of pandas
    :param text: (str) text

    :return: a dataframe of pandas that include text
    """
    df = df.astype(str)
    result_set = set()
    for column in df.columns:
        # print(column)
        result = df[column].str.contains(text)
        for i in range(len(result.values)):
            if result.values[i] == True:
                result_set.add(result.index[i])
                # print(column,df[column].str.contains(text))
    return df.loc[result_set]