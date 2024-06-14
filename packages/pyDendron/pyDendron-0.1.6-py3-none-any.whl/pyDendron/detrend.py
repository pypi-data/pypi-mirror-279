"""
Detrend / Indices
"""
__license__ = "GPL"
__author__ = "Sylvain Meignier"
__copyright__ = "Copyright 2023 Sylvain Meignier, Le Mans Université, LIUM (https://lium.univ-lemans.fr/)"
__license__ = "GPL"
__maintainer__ = "Sylvain Meignier"
__email__ = "pyDendron@univ-lemans.fr"
__status__ = "Production"

import numpy as np
import pandas as pd
from csaps import csaps
from concurrent.futures import ProcessPoolExecutor

from pyDendron.app_logger import logger
from pyDendron.dataname import *

def worker(detrend_fct, idx, vec, ring_type, window_size, do_log):
    #print(f'thread {idx}')
    return detrend_fct(idx, vec, ring_type, window_size, do_log)

def detrend(data, ring_type, window_size=5, do_log=False, num_threads=1):
    if not (data[CATEGORY] == TREE).all():
        logger.warning('Detrend : data does not contain only samples')
    #print(f'detrend {num_threads}')
    if num_threads > 1:
        return detrend_thread(data, ring_type, window_size, do_log, num_threads)
        
    data_out = data.copy()
    for idx, row in data.iterrows():
        _, vector =  detrend_vector(idx, row[DATA_VALUES], ring_type=ring_type, window_size=window_size, do_log=do_log)
        data_out.at[idx, DATA_VALUES] = vector
        data_out.at[idx, DATA_LENGTH] = len(vector)
        data_out.at[idx, DATA_TYPE] = ring_type
    
    return data_out

def detrend_thread(data, ring_type, window_size=5, do_log=False, num_threads=1):
    with ProcessPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        # Start an asynchronous task (future) for each index
        for idx, row in data.iterrows():
            _window_size = window_size
            if len(row[DATA_VALUES]) < window_size:
                logger.warning(f'detrend_vector: in {row[idx, KEYCODE],} data length < window size ({len(row[DATA_VALUES])} < {window_size})')
                _window_size = len(row[DATA_VALUES])
            future = executor.submit(worker, detrend, idx, row[DATA_VALUES], ring_type, _window_size, do_log)
            futures.append(future)

        # Wait for all tasks to be completed
        data_out = data.copy()
        for future in futures:
            idx, vector = future.result()
            data_out.at[idx, DATA_VALUES] = vector
            data_out.at[idx, DATA_LENGTH] = len(vector)
            data_out.at[idx, DATA_TYPE] = ring_type
        return data_out

def detrend_vector(idx, vec, ring_type, window_size=5, do_log=False):
    #if len(vec) < window_size:

    if ring_type == BESANCON:
        return idx, besancon(vec, window_size=window_size, do_log=do_log, after=False)
    if ring_type == BESANCON1:
        return idx, besancon(vec, window_size=window_size, do_log=do_log, after=True)
    elif ring_type == HANNING:
        return idx, sliding_window(vec, window_type=HANNING, window_size=window_size, do_log=do_log)
    elif ring_type == HAMMING:
        return idx, sliding_window(vec, window_type=HAMMING, window_size=window_size, do_log=do_log)
    elif ring_type == BARTLETT:
        return idx, sliding_window(vec, window_type=BARTLETT, window_size=window_size, do_log=do_log)
    elif ring_type == BLACKMAN:
        return idx, sliding_window(vec, window_type=BLACKMAN, window_size=window_size, do_log=do_log)
    elif ring_type == RECTANGULAR:
        return idx, sliding_window(vec, window_type=RECTANGULAR, window_size=window_size, do_log=do_log)
    elif ring_type == BP73:
        return idx, sliding_window(vec, window_type=RECTANGULAR, window_size=window_size, do_log=True)
    elif ring_type == SPLINE:
        return idx, spline(vec, do_log=do_log)
    elif ring_type == SLOPE:
        return idx, slope(vec)
    elif ring_type == CORRIDOR:
        return idx, corridor(vec, do_log=do_log)
    elif ring_type == CORRIDOR_SPLINE:
        return idx, corridor_spline(vec, do_log=do_log)
    elif ring_type == DELTA:
        return idx, delta(vec, 1)
    elif ring_type == DELTADELTA:
        return idx, delta(vec, 2)
    elif ring_type == LOG:
        return idx, np.log(vec)
    elif ring_type == RAW:
        return idx, vec
    else:
        raise ValueError(f'detrend_vector: unknown method: {ring_type}')

def _spline(x, raw_vector):
    amp = 0.5
    period = len(raw_vector) * 0.67 #[p114 Cook, 1990]
    freq = 1/period
    # ~ eq 3.13 [Cook, 1990]
    param = 1/(((np.cos(2 * np.pi * freq) + 2) * (1 - amp)/(12 * amp * (np.cos(2 * np.pi * freq) - 1) ** 2))+ 1)
    mask = ~np.isnan(raw_vector)
    return csaps(np.array(x)[mask], raw_vector[mask], x, smooth=param)

def spline(raw_vector, do_log=False):
    x = [x for x in range(len(raw_vector))]
    vector = raw_vector / _spline(x, raw_vector)
    if do_log:
        vector[vector == 0] += np.finfo(float).eps
        vector = np.log(vector)
    return np.round(100*vector, 3)

# def spline_dpl(raw_vector):
#     import dplPy
    
#     df = pd.DataFrame(raw_vector, columns=['data'])    
#     return np.round(dplPy.detrend(df, fit="spline", plot=False)['data'].to_numpy()*100, 3)

def vector_log(vector):
    #vector[vector == 0] += np.finfo(float).eps
    vector[vector == 0] += np.nan
    mask = ~np.isnan(vector)
    vector[mask] = np.log(vector[mask])
    return vector
    

def _sliding_window(raw_vector, window):
    vector = np.copy(raw_vector)
    n = len(window)
    view = np.lib.stride_tricks.sliding_window_view(vector, window_shape=n).copy()
    
    view *= window
    conv = np.sum(view, axis=1)
    tmp = np.full(n // 2, np.nan)
    conv = np.concatenate((tmp, conv, tmp))
    vector /= conv
    vector *= 100 # Scale vector
    
    return vector

def sliding_window(raw_vector, window_type=HANNING, window_size: int = 5, do_log=False):    
    if window_type == HANNING:
        window = np.hanning(window_size)
    elif window_type == HAMMING:
        window = np.hamming(window_size)
    elif window_type == BARTLETT:
        window = np.bartlett(window_size)
    elif window_type == BLACKMAN:
        window = np.blackman(window_size)
    elif window_type == RECTANGULAR:
        window = np.ones(window_size)
    else:
        raise ValueError('sliding_window: unknown window_type: {window_type}')
    window /= window.sum()
    
    vector = _sliding_window(raw_vector, window)
    if do_log:
        vector = vector_log(vector)
    
    #print('VERIFIER LA DIMENSSION DES VECTORS IN OUT !!!' , len(raw_vector), len(vector))

    return np.round(vector, 3)

def besancon(raw_vector, window_size, do_log=True, after=False):
    """
    Calculate the Besancon indice for the given DataFrame.

    :param window_size: The size of the sliding window for indice calculation. Default is 7.
    :type window_size: int
    
    :param log_before: Compute the log transformation befor any transformation. 
    :type log_before: bool
    """
    n = window_size // 2
    # Create a view using as_strided to obtain the sliding window
    if do_log and (not after):
        vector = raw_vector.copy()
        vector = vector_log(vector)
    else:
        vector = raw_vector
    view = np.lib.stride_tricks.sliding_window_view(vector, window_shape=window_size).copy()
    vector = view[:, n+1].copy()
    # Set the central value to nan
    view[:, n+1] = np.nan
    vector *= (np.sum(~np.isnan(view), axis=1) - 2) * 100
    denominator = (np.nansum(view, axis=1) - np.nanmax(view, axis=1) - np.nanmin(view, axis=1))
    denominator[denominator == 0] = np.nan
    mask = np.isnan(vector) | np.isnan(denominator)
    vector[mask] = np.nan
    vector[~mask] /= denominator[~mask]
    if do_log and after:
        vector = vector_log(vector)
    tmp = np.full(n, np.nan)
    vector = np.concatenate((tmp, np.round(vector, 3), tmp))
    return vector

def slope(raw_vector):
    """
    Calculate the slope indice ('gleichlaufigkeit') .
    """
    vector = np.copy(raw_vector)
    # Calculate the first-order discrete difference
    diff_series = np.diff(vector)
    # Compute the sign (positive, negative, or zero) of each element 
    sign_series = np.sign(diff_series)
    # Append a NaN value to the end of 'sign_series' to match the original series size
    vector = np.append(sign_series, np.nan)
    return vector

def delta(raw_vector, order=1):
    """
    Calculate the slope indice ('gleichlaufigkeit') .
    """
    vector = np.copy(raw_vector)
    # Calculate the first-order discrete difference
    for i in range(order):
        diff_series = np.diff(vector)
        vector = np.append(diff_series, np.nan)

    return vector

def corridor(raw_vector, do_log=False):
    # 
    vec = np.copy(raw_vector)
    mu = np.nanmean(vec) # mean without NaN value
    std = np.nanstd(vec) # std without NaN value
    thr = mu + 2 * std # Threshold 

    mask_thr = vec > thr # binary mask, True if value > threshold

    windows = np.lib.stride_tricks.sliding_window_view(mask_thr, window_shape=3)
    mask_filters = np.concatenate(( [False], np.sum(windows == [False, True, False], axis=1) == 3, [False]))
    value_filters = np.concatenate(( [np.nan], np.convolve(vec, [1,0,1], mode='valid')/2, [np.nan]))
    vec[mask_filters] = value_filters[mask_filters]

    mask_thr[mask_filters] = False
    vec[mask_thr] = np.nan

    nan_mask = ~np.isnan(vec)

    x = np.array([x for x in range(len(vec))])
    x_masked = x[nan_mask]
    vec_masked = vec[nan_mask]

    # Polynomial regression based on corrected values
    coef_middle = np.polyfit(x_masked, vec_masked, 3)
    fct_middle = np.poly1d(coef_middle)
    #vec_middle = fct_middle(x)
    vec_middle_masked = fct_middle(x_masked)

    # Polynomial regression based on roof values
    mask = (vec_masked - vec_middle_masked) >= 0
    coef_roof = np.polyfit(x_masked[mask], vec_masked[mask], 3)
    fct_roof = np.poly1d(coef_roof)
    vec_roof = fct_roof(x)

    # Polynomial regression based on floor values
    mask = (vec_masked - vec_middle_masked) < 0
    coef_floor = np.polyfit(x_masked[mask], vec_masked[mask], 3)
    fct_floor = np.poly1d(coef_floor)
    vec_floor= fct_floor(x)

    # detrended values
    vector = (vec - vec_floor) / (vec_roof - vec_floor)
    min_ = np.nanmin(vector)
    max_ = np.nanmax(vector)
    min_raw = np.nanmin(raw_vector)
    max_raw = np.nanmax(raw_vector)

    vector = np.round((vector - min_ ) * (max_raw - min_raw) / (max_ - min_) + min_raw, 2)
    
    if do_log:
        vector = vector_log(vector)
   
    return vector

def corridor_spline(raw_vector, do_log):
    # 
    vec = np.copy(raw_vector)
    mu = np.nanmean(vec) # mean without NaN value
    std = np.nanstd(vec) # std without NaN value
    thr = mu + 2 * std # Threshold 

    mask_thr = vec > thr # binary mask, True if value > threshold
    vec[mask_thr] = np.nan
    #raw_vector[mask_thr] = np.nan

    nan_mask = ~np.isnan(vec)

    x = np.array([x for x in range(len(vec))])

    # Spline based on corrected values
    vec_middle = _spline(vec)
    
    mask = (vec - vec_middle) > 0
    vec_roof = _spline(vec[mask])
    
    mask = (vec - vec_middle) < 0
    vec_floor = _spline(vec[mask])

    # detrended values
    vector = np.copy(raw_vector)
    vector = (vector - vec_floor) / (vec_roof - vec_floor) 
    
    min_ = np.nanmin(vector)
    max_ = np.nanmax(vector)
    min_raw = np.nanmin(raw_vector)
    max_raw = np.nanmax(raw_vector)

    vector = np.round((vector - min_ ) * (max_raw - min_raw) / (max_ - min_) + min_raw, 2)

    if do_log:
        vector = vector_log(vector)
    
    return vector

