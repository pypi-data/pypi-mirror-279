
"""
Chronology
"""
__license__ = "GPL"
__author__ = "Sylvain Meignier"
__copyright__ = "Copyright 2023 Sylvain Meignier, Le Mans Université, LIUM (https://lium.univ-lemans.fr/)"
__license__ = "GPL"
__maintainer__ = "Sylvain Meignier"
__email__ = "pyDendron@univ-lemans.fr"
__status__ = "Production"

import logging
import numpy as np
import pandas as pd
from concurrent.futures import ProcessPoolExecutor

from pyDendron.app_logger import logger
from pyDendron.dataname import *

epsilon = np.finfo(np.float64).tiny
biweight_factor = 9
#biweight_factor = 5

def data2col(data, key=IDX, use_offset=True, key_offset=OFFSET):
    
    def length_(values):
        l = len(values) if values is not None else 0
        logger.debug(f'{l}, {values}')
        return l
    
    data = data.copy()
    data[DATA_LENGTH] = data[DATA_VALUES].apply(lambda x: length_(x))
    #print('data2col : use_offset', use_offset)
    if use_offset:
        if data[key_offset].isna().any():
            raise ValueError(f'data2col: NA value(s) in {key_offset} column')
        data[key_offset] -= data[key_offset].min()
        end = (data[key_offset]+data[DATA_LENGTH]).max()
    else:
        end = data[DATA_LENGTH].max()

    d = {}
    for idx, row in data.iterrows():
        offset = row[key_offset] if use_offset else 0
        values = row[DATA_VALUES]
        if (values is not None) and (len(values) > 0):
            vec = np.full(end, np.nan)
            vec[offset:offset+len(values)] = values
            k = idx if key == IDX else row[key]
            d[k] = vec
        else:
            raise ValueError(f'data2col: {idx} / {row[KEYCODE]}, ring values is missing')
        
    return pd.DataFrame(d)


def chronology(data, date_as_offset=False, ring_type='raw', biweight=False, idx_chronology=None):
    """
        sequences: DataFrame of samples. `offset` column is need if offset_type is `offset`
    """

    #print('chronology', idx_chronology)
    if OFFSET not in data.columns:
        raise ValueError('chronology: no offset in sequences')
    
    if date_as_offset:
        data[OFFSET] = data[DATE_BEGIN]

    if data[OFFSET].isna().any():
        key = DATE_BEGIN if date_as_offset else OFFSET
        raise ValueError(f'chronology: one or more {key} contain NA values')
            
    if not (data[CATEGORY] == TREE).all():
        raise ValueError('chronology : data need to contain sample only')
        #data = data[data[CATEGORY] == TREE]
    
    if not (data[DATA_TYPE] == ring_type).all():
        raise ValueError("chronology: ring type don't match data")
        
    data_col = data2col(data)
    if biweight:
        #logger.info('chronology : biweight mean')
        median = data_col.median(skipna=True, axis=1)
        data_center = data_col.sub(median, axis=0)
        kind_std = data_center.abs().median(skipna=True, axis=1)
        data_center_reduce = data_center.div((biweight_factor * kind_std) + epsilon, axis=0)
        data_weights = (1 - (data_center_reduce ** 2)) ** 2
        data_weights[np.abs(data_center_reduce) >= 1] = 0
        #print(data_weights)
        weights = np.sum(data_weights, axis=1)
        means = np.sum(data_weights*data_col, axis=1) / weights
    else:
        means = data_col.mean(axis=1)
        weights = data_col.count(axis=1)
    
    offsets = [(idx, row[OFFSET]) for idx, row in data.iterrows()]
    return np.round(means, 3).to_numpy(), weights.to_numpy(), offsets, idx_chronology

def chronologies(data_dict, date_as_offset=False, ring_type='raw', biweight=False, num_threads=1):
    res = dict()
    if num_threads == 1:
        for idx, data in data_dict.items():
            means, weights, offsets, idx = chronology(data, date_as_offset=date_as_offset, ring_type=ring_type, biweight=biweight, idx_chronology=idx)
            res[idx] = (means, weights, offsets)
    else:
        with ProcessPoolExecutor(max_workers=num_threads) as executor:
            futures = []
            # Start an asynchronous task (future) for each index
            for idx, data in data_dict.items():
                future = executor.submit(chronology, data, date_as_offset=date_as_offset, ring_type=ring_type, biweight=biweight, idx_chronology=idx)
                futures.append(future)

            # Wait for all tasks to be completed
            for future in futures:
                means, weights, offsets, idx = future.result()
                res[idx] = (means, weights, offsets)
    return res

