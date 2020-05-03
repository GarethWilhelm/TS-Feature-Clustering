!pip install oec
import oec
import pandas as pd
import numpy as np
import os, os.path, csv, requests, pathlib
import math
from datetime import datetime

def build_call(*args):
    call_url = 'http://atlas.media.mit.edu/'
    for val in args:
        call_url += str(val) + '/'
    return call_url


def request_data(call_url):
    r = requests.get(call_url)
    response_dict = r.json()
    json_list = response_dict['data']  # list of dicts containing data
    return json_list


def get_countries(filename=None):
    call = build_call('attr', 'country')
    json_list = request_data(call)
    if filename is not None:
        data_to_csv(json_list, filename)
    return json_list


def get_products(classification, filename=None):
    call = build_call('attr', classification)
    json_list = request_data(call)
    if filename is not None:
        data_to_csv(json_list, filename)
    return json_list


def get_trade(classification, trade_flow, year, origin, destination,product, filename=None):
    call = build_call(classification, trade_flow, year, origin, destination,
                      product)
    json_list = request_data(call)
    if filename is not None:
        data_to_csv(json_list, filename)
    return json_list


def trade_params(classification, trade_flow, year, origin, destination,product):
    parameters = {'classification': classification,
                  'trade_flow': trade_flow,
                  'year': year,
                  'origin': origin,
                  'destination': destination,
                  'product': product}
    return parameters


def get_header(json_list):
    header = set()
    for dict in json_list:
        header.update(dict.keys())
    header = list(header)
    header.sort()
    return header


def create_csv(json_list, filename):
    with open(filename, 'w') as csvfile:
        header = get_header(json_list)
        cw = csv.writer(csvfile)
        cw.writerow(header)
        for dict in json_list:
            row = dict_to_list(dict, header)
            cw.writerow(row)


def dict_to_list(dict, header):
    row = []
    for field in header:
        if field in dict:
            row.append(str(dict[field]))
        else:
            row.append(None)
    return row

### Dataset
trade_codes = ['6519',
               '6531',
               '8471','6571','7849','7810','7842','7764','7723','7522','2924','5419','5417','7763','7711','7188']
PATH = '/data'
os.chdir(PATH)
trade_classification = 'sitc'
def countries_and_products():
  countries = oec.get_countries()
  products = oec.get_products(trade_classification)
  create_csv(countries,f'{PATH}/list_countries.csv')
  create_csv(products,f'{PATH}/list_products.csv')

import os.path
from os import path
def download_data(list_of_codes):
  for i in trade_codes:
    csv_name = f"{trade_classification}-{i}"
    # Set parameters to extract top exporters from the API documentation
    params = {'classification': trade_classification,
          'trade_flow': 'export',
          'year': 'all',
          'origin': 'show', #Set origin to all for comparison
          'destination': 'all',
          'product': i} #Set code for product of interest
    print(f'Data for {i} processed.....')
    oec_data = get_trade(**params)
    # Save the results in CSV file
    if path.exists(PATH):
      create_csv(oec_data,f'{csv_name}.csv')#,locals(),globals())
    else:
      print('Choose destination directory')

def create_df():
  trade_data = [i for i in os.listdir() if i.endswith('.csv') and 'sitc' in i]
  trade_history = []
  for file in trade_data:
    file_name = pd.read_csv(file)
    trade_history.append(file_name)
  products_dataframe = pd.concat(trade_history)
  return products_dataframe
# cols = ('export_rca','export_val','origin_id','sitc_id','year'
trade_dframe = create_df()
countries = pd.read_csv(f'{PATH}/list_countries.csv',usecols=['id','name'],index_col='id',squeeze = True)
products = pd.read_csv(f'{PATH}/list_products.csv',usecols=['id','name'],index_col='id',squeeze = True)

countries_and_products()
