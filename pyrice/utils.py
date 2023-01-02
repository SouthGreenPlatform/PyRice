# -*- coding: utf-8 -*-
import os
import requests
import urllib3
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException,WebDriverException
from time import sleep
import json

chrome_path = ""
dir_path = os.path.dirname(os.path.realpath(__file__))
download_dir = os.path.join(dir_path,"support/download/")

def connection_error(link, data = "", type = None, db = None, gene_id=None):
    """
     Get result with request post or get; with JavaScript

    :param link: (str) url
    :param data: (str) data to give to the form
    :param type: (str) use with JavaScript format
    :param db: (str) database name - use with JavaScript format
    :param gene_id: (str) gene id - use with JavaScript format

    :return: object of requests
    """
    """
    Get result with request post or request get

    :param link: (str) url
    :param data: (str) data to give to the form

    :return: object of requests
    """
    if type == "javascript":
        options = webdriver.ChromeOptions()

        profile = {"plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}],
                   # Disable Chrome's PDF Viewer
                   "download.default_directory": download_dir, "download.extensions_to_open": "applications/pdf"}
        options.add_experimental_option("prefs", profile)
        try:
            if (os.path.exists(chrome_path)):
                driver = webdriver.Chrome(chrome_path, chrome_options=options)
            else:
                options = webdriver.ChromeOptions()
                options.add_argument('--headless')
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                driver = webdriver.Chrome(options=options)
            driver.get(link)
            wait = WebDriverWait(driver, 5)
            men_menu = wait.until(ec.visibility_of_element_located((By.XPATH, data)))
            button = driver.find_elements_by_xpath(data)[0]
            ActionChains(driver).move_to_element(men_menu).click(button).perform()
            sleep(1)
            if db == "gwas_atlas":
                csv_button = driver.find_elements_by_xpath("//ul[@class='dropdown-menu'and @role='menu']/li[2]/a")[0]
                ActionChains(driver).move_to_element(csv_button).click().perform()
                sleep(2)
            driver.close()
            driver.quit()
            return 1
        except (TimeoutException, WebDriverException) as e:
            print(e)
            return None
        # finally:
        #     driver.close()
        #     driver.quit()
    else:
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
            return res
        except requests.exceptions.RequestException as error:
            print("Can't connect: {} - Eror: {}".format(link,error))
            return None

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
            data = {"format":"json"}
            i = 0
            for field in fields:
                query = field.text.replace("GENE_ID",qfields[i])
                data.setdefault("query",query)
                i+=1
            # i = 0
            # data = {'format':'json'}
            # for field in fields:
            #     data.setdefault(field.text,qfields[i])
            #     i += 1
            return connection_error(link, data)
        elif db[0]["method"] == "GET":
            query_string = ""
            if db[0]["type"] == "javascript":
                div = db[0].find_all("div")
                button = db[0].find_all("button")
                input = db[0].find_all("input")
                if len(div) > 0:
                    download_button = "//div["
                    download_source = div
                elif len(button) > 0:
                    download_button = "//button["
                    download_source = button
                elif len(input) > 0:
                    download_button = "//input["
                    download_source = input
                for key, value in download_source[0].attrs.items():
                    if type(value) is list:
                        download_button += "@" + key + " = '"
                        for v in value:
                            download_button += v +' '
                        download_button = download_button[:-1]
                        download_button += "' and "
                    else:
                        download_button += "@" + key + " = '" + value + "' and "
                download_button = download_button[:-5] + "]"
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
                link += query_string + db[0].find_all("link")[0]["aft"]
                if verbose: print(link)
                return connection_error(link, download_button, type='javascript', db = db[0]["dbname"])
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
