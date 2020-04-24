import pandas as pd
import numpy as np

product = 'engine_parts' # Create a dictionary to store product code and sitc code
code = 7132
experiment = 'rca_values'

def load_data(csv_name,trade_form,target_value, code_system,sitc_code,ts_type):
    '''
    Ingests SITC multi-time series trade data in csv format, filters for one product code, removes zero values for 
    target value, screens target values and renames target columns & creates dataframe for the target columns
    
    Parameters:
    -----------
    csv:
    trade_form:
    target_value:
    code_system:
    sitc_code:
    ts_type:
    '''
    data = pd.read_csv(csv_name)#,header=None
    # TO DO: Create for loop to read sitc code from dictionary
    dframe = data.loc[data[code_system]==sitc_code]
    dframe.rename(columns={'location_name_short_en': 'exporter','export_rca': 'rca'}, inplace=True)
    dframe = dframe[[ts_type,trade_form,target_value]]
    dframe = dframe[dframe[trade_form] != 'Undeclared Countries']
    dframe[target_value].replace('',0, inplace=True)
    dframe = dframe[dframe[target_value] != 0]
    dframe = dframe[dframe[target_value] >= 0.09]
    dframe = dframe[dframe[target_value] <= 20]
    return dframe