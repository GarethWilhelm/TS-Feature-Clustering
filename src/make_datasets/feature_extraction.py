import os
import pandas as pd
import matplotlib.pyplot as plt
import logging
import warnings

import tsfresh
from tsfresh import extract_features, select_features
from tsfresh import defaults
from tsfresh.feature_extraction import feature_calculators
from tsfresh.feature_extraction.settings import ComprehensiveFCParameters
from tsfresh.utilities import dataframe_functions, profiling
from tsfresh.utilities.distribution import MapDistributor, MultiprocessingDistributor,DistributorBaseClass
from tsfresh.utilities.string_manipulation import convert_to_output_format
from tsfresh.feature_extraction.settings import EfficientFCParameters
from tsfresh.utilities.dataframe_functions import roll_time_series

%tensorflow_version 2.x
import tensorflow as tf
device_name = tf.test.gpu_device_name()
if device_name != '/device:GPU:0':
  raise SystemError('GPU device not found')
print('Found GPU at: {}'.format(device_name))

def extract_product_features(df,fc_parameter,destination):
  features_product = []
  extraction_method = fc_parameter.__class__.__name__
  for p in df.sitc_id.unique():
    product = df[df.sitc_id==p]
    p_features = extract_features(
      product[["export_val","year","country"]],
      column_id="country",
      column_sort="year",
      column_value=None,column_kind=None,
      chunksize=None,
      default_fc_parameters=fc_parameter
      )
    features_product.append(p_features)
    p_features.to_csv(f"{p}_{extraction_method}_expval.csv")
    print(f'Extracted features for {p}: \n {features_product}')
  product_features = pd.concat(features_product)
  return p_features

%timeit
destination_1 =f'{PATH}/efficient_parameters'
destination_2 = f'{PATH}/comprehensive_parameters'
fc_parameters=[EfficientFCParameters(),ComprehensiveFCParameters()]
extract_product_features(trade_dframe,fc_parameters[0],destination_1)
extract_product_features(trade_dframe,fc_parameters[1],destination_2)