"""
File Name: crossdating.py
Author: Sylvain Meignier
Organization: Le Mans Université, LIUM (https://lium.univ-lemans.fr/)
Creation Date: 2023-12-03
Description: cross-dating class
This file is governed by the terms of the GNU General Public License v3.0.
Please see the LICENSE file for more details.
"""

#from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
import time
import warnings
import os
import copy

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import networkx as nx

#from sklearn.metrics import det_curve, DetCurveDisplay
import seaborn as sns

from scipy import stats, spatial
#from scipy.cluster import hierarchy
from scipy.stats import gaussian_kde

import param
import panel as pn
from bokeh.plotting import figure
from bokeh.models import (PrintfTickFormatter, RangeTool, ColumnDataSource, Range1d,
                            Legend, LegendItem) 
from bokeh.transform import factor_mark 
from bokeh.palettes import brewer 
from bokeh.layouts import gridplot

from pyDendron.detrend import slope
from pyDendron.app_logger import logger
from pyDendron.dataname import *

COLS = {IDX_MASTER: 'Int32', IDX: 'Int32', 
        KEYCODE_MASTER: 'string', KEYCODE: 'string', 
        DATA_TYPE: 'string', 
        OFFSET: 'Int32', DATE_BEGIN_ESTIMATED: 'Int32', DATE_END_ESTIMATED: 'Int32', DATED: 'boolean', OVERLAP: 'Int32', OVERLAP_NAN: 'Int32', 
        CORR: 'float32', T_SCORE: 'float32', TP_VALUE: 'float32', T_RANK: 'Int32',
        GLK: 'float32', Z_SCORE: 'float32', ZP_VALUE: 'float32', Z_RANK: 'Int32',
        DIST: 'float32', D_RANK: 'Int32',
        }

DEFAULTS = {IDX_MASTER: pd.NA, IDX: pd.NA, 
        KEYCODE_MASTER: '', KEYCODE: '', 
        DATA_TYPE: '', 
        OFFSET: pd.NA, DATE_BEGIN_ESTIMATED: pd.NA, DATE_END_ESTIMATED: pd.NA, DATED: False, OVERLAP: pd.NA, OVERLAP_NAN: pd.NA, 
        CORR: pd.NA, T_SCORE: pd.NA, TP_VALUE: pd.NA, T_RANK: pd.NA,
        GLK: pd.NA, Z_SCORE: pd.NA, ZP_VALUE: pd.NA, Z_RANK: pd.NA,
        DIST: pd.NA, D_RANK: pd.NA,
        }

#def worker(instance, i, self_crossdating, data, master_data):
#    print('worker', i)
#    return instance.run_one(i, self_crossdating, data, master_data)

def worker(instance, i):
    #print('worker', i)
    return instance.run_one(i, self_crossdating, data, master_data)

# def worker(args):
#     instance, i = args
#     print('worker', i)
#     return instance.run_one(i, self_crossdating, data, master_data)

def set_worker(arg1, arg2, arg3):
    print('set_worker ')
    global self_crossdating 
    self_crossdating = arg1
    global data 
    data = arg2
    global master_data 
    master_data = arg3

class CrossDatingWorker:
    
    def __init__(self, num_threads, min_overlap, method, distance='cosine'):
        self.offsets = None
        self.results = {}
        self.dcg = {}
        self.self_crossdating = False
        self.ring_type = None
        self.num_threads = num_threads
        self.min_overlap = min_overlap
        self.method = method
        self.distance = distance
        self.COLS = COLS
    
    def run_one(self, i, self_crossdating, data, master_data=None):
        results = {}
        
        idx = data.index[i]
        row = data.iloc[i]
        first_j = i + 1 if self_crossdating else 0
        for j, (idx_master, row_master) in  enumerate(master_data.iloc[first_j:].iterrows()):
            res = self.run_series(row, row_master)
            results[(idx, idx_master)] = res

        return results #, sdcg, ndcg, n

    def run_series(self, series, master_series):
        """
        Perform dating analysis between two data series.

        :param series: A dictionary representing the first data series.
        :param seriesMaster: A dictionary representing the second data series.
        :return: A Pandas DataFrame containing the dating results.
        """
        
        def add_rank(results_lst, key_score, key_rank, reverse=False):
            #print(key_score, results_lst)
            results_lst = sorted(results_lst, key=lambda x: x[key_score], reverse=reverse)
            for i, res in enumerate(results_lst):
                res[key_rank] = i+1
            return results_lst

        results_lst = []
        # Extract data from the 2 series
        master_idx, series_idx = master_series[IDX_CHILD], series[IDX_CHILD]
        master_keycode, series_keycode = master_series[KEYCODE], series[KEYCODE]
        master_values, values = master_series[DATA_VALUES], series[DATA_VALUES]
        master_values_slope, values_slope = slope(master_values), slope(values)
        master_begin, series_begin = master_series[DATE_BEGIN], series[DATE_BEGIN]
        ring_count = series[DATA_LENGTH]
        
        # Generate offsets and windows for the 2 series
        offsets, windows, master_windows = self._generate_dating_index(values, master_values, self.min_overlap)
        for pos, window, master_window in zip(offsets, windows, master_windows):
            # Calculate the estimated first date
            if pd.notna(master_begin):
                date_begin_estimated = master_begin + pos
                date_end_estimated = date_begin_estimated + ring_count
            else:
                date_begin_estimated = pd.NA
                date_end_estimated = pd.NA

            res = copy.copy(DEFAULTS)
            res[IDX_MASTER], res[IDX], res[KEYCODE_MASTER], res[KEYCODE] =  master_idx, series_idx,  master_keycode, series_keycode
            res[DATA_TYPE], res[OFFSET], res[DATE_BEGIN_ESTIMATED], res[DATE_END_ESTIMATED] = self.ring_type, pos, date_begin_estimated, date_end_estimated
            res[DATED] = (series_begin == date_begin_estimated) if pd.notna(master_begin) else pd.NA
            if CORRELATION in self.method:
                overlap, nnan, r, p_value, score = self._correlation(values[window[0]:window[1]], master_values[master_window[0]:master_window[1]], min_overlap=self.min_overlap)
                if overlap < self.min_overlap:
                    continue
                res[OVERLAP], res[OVERLAP_NAN], res[CORR], res[TP_VALUE], res[T_SCORE] = overlap, nnan, r, p_value, score
            if GLK in self.method:
                overlap, nnan, agc, ssgc, sgc, score, p_value = self._glk(values_slope[window[0]:window[1]], master_values_slope[master_window[0]:master_window[1]], min_overlap=self.min_overlap)
                if overlap < self.min_overlap:
                    continue
                res[OVERLAP], res[OVERLAP_NAN], res[GLK], res[ZP_VALUE], res[Z_SCORE] = overlap, nnan, sgc, p_value, score
            if DISTANCE in self.method:
                if self.distance == COSINE:
                    overlap, nnan, score = self._distance(values[window[0]:window[1]], master_values[master_window[0]:master_window[1]], min_overlap=self.min_overlap, distance=COSINE)
                    if overlap < self.min_overlap:
                        continue
                    res[OVERLAP], res[OVERLAP_NAN], res[DIST] = overlap, nnan, score
                if self.distance == EUCLIDEAN:
                    overlap, nnan, score = self._distance(values[window[0]:window[1]], master_values[master_window[0]:master_window[1]], min_overlap=self.min_overlap, distance=EUCLIDEAN)
                    if overlap < self.min_overlap:
                        continue
                    res[OVERLAP], res[OVERLAP_NAN], res[DIST] = overlap, nnan, score
                if self.distance == CITYBLOCK:
                    overlap, nnan, score = self._distance(values[window[0]:window[1]], master_values[master_window[0]:master_window[1]], min_overlap=self.min_overlap, distance=CITYBLOCK)
                    if overlap < self.min_overlap:
                        continue
                    res[OVERLAP], res[OVERLAP_NAN], res[DIST] = overlap, nnan, score
            results_lst.append(res)
            
        if DISTANCE in self.method:
            results_lst = add_rank(results_lst, DIST, D_RANK, reverse=False)
        if GLK in self.method:
            results_lst = add_rank(results_lst, Z_SCORE, Z_RANK, reverse=True)
        if CORRELATION in self.method:
            results_lst = add_rank(results_lst, T_SCORE, T_RANK, reverse=True)
            
        return pd.DataFrame(results_lst, columns=list(self.COLS.keys()))

    def _offset(self, offsets, windows, master_windows):
        # Check if a specific offset is provided for analysis
        if self.offsets is not None:
            lst = list(offsets)
            # If the specified offset exists in the list, narrow down the analysis to that offset
            if self.offsets in lst:
                i = lst.index(self.offsets)
                offsets = offsets[i:i+1]
                windows = windows[i:i+1]
                master_windows = master_windows[i:i+1]
            else:
                # If the specified offset does not exist, dating will be empty
                self.offsets = windows = master_windows = np.array([])
        return offsets, windows, master_windows

    def _generate_dating_index(self, series: np.ndarray, master: np.ndarray, min_overlap: int = 1):
        def generate_windows_offset(series_length: int, window_size: int, min_overlap: int = 1, flip: bool = False):
            if min_overlap < 1:
                raise ValueError('cross dating._generate_dating_index: min_periods must be > 0')
            # Calculate the ending offsets of the sliding window
            end = np.arange(1, series_length + window_size)
            start = end - window_size
            # Clip the end and start offsets to ensure they stay within the valid range
            end = np.clip(end, 0, series_length)
            start = np.clip(start, 0, series_length)
            if flip:
                # Optionally, flip the offsets
                end = np.flip(end)
                start = np.flip(start)
            # Identify offsets where the window size meets the minimum period requirement
            keep = np.where((end - start) >= min_overlap)
            return list(zip(start[keep], end[keep])), keep

        # Get the lengths of the 'master' and 'series' numpy.array
        length_master = len(master)
        length_series = len(series)
        # Calculate windows and offsets for 'series'
        series_windows, keep1 = generate_windows_offset(length_series, length_master, min_overlap)
        # Calculate windows and offsets for 'master' while optionally flipping them
        master_windows, _ = generate_windows_offset(length_master, length_series, min_overlap, True)
        # Generate offsets that correspond to the 'master' and 'series' windows
        offsets = -1*np.arange(-length_master + 1, length_series + 1)[keep1]

        return self._offset(offsets, series_windows, master_windows)

    def _glk(self, segments: np.ndarray, master_segments: np.ndarray, min_overlap: int = 30):
        # Visser, R. M. (2021) On the similarity of tree-ring patterns: Assessing the influence of 
        # semi-synchronous growth changes on the Gleichläufigkeitskoeffizient for big tree-ring data 
        # sets. Archaeometry, 63: 204–215. https://doi.org/10.1111/arcm.12600.
        
        diff = np.abs(segments + master_segments)
        # Count the number of valid data points
        nan_mask = np.isnan(diff)
        nnan = np.sum(nan_mask) # number of nan
        n = len(diff) - nnan # number of not nan values
        agc = ssgc = sgc = z_score = p_value = np.nan
        if n >= min_overlap:
            # agc (asynchonous growth change): number of 0 -> (-1, 1), (1, -1)
            # ssgc (semi-synchonous growth change): number of 1 -> (0, 1), (0, -1) (1, 0), (-1, 0)
            # sgc (synchonous growth change): number of 2 -> (1, 1), (-1, -1)
            agc = np.sum((diff[~nan_mask] == 0.0)) 
            ssgc = np.sum((diff[~nan_mask] == 1.0)) 
            sgc = np.sum((diff[~nan_mask] == 2.0))  # score glk
            agc /= n
            ssgc /= n
            sgc /= n
            # z_score and p_score
            s = 1.0 / (2.0 * np.sqrt(n))
            # parallel values folow a binomial distribution of parameter n, p=0.5
            z_score = (sgc - 0.5) / s
            p_value = 0
            #p_value =  stats.norm.cdf(z_score) # normal cumulative distribution fonction
            #print(f'n {n} nnan {nnan} sgc {sgc}')
        return n, nnan, agc * 100, ssgc * 100, sgc * 100, z_score, p_value

    def _correlation(self, segment: np.ndarray, master_segment: np.ndarray, method: str = 'pearson', min_overlap: int = 30):
        # Find valid data points
        valid_data_points = (~np.isnan(segment)) & (~np.isnan(master_segment))
        n = np.count_nonzero(valid_data_points)

        if n < min_overlap:
            return np.nan, np.nan, np.nan, np.nan, n

        nnan =  len(valid_data_points) - n # number of nan
        r = np.corrcoef(segment[valid_data_points], master_segment[valid_data_points])[0, 1]

        if abs(r) == 1:
            r -= np.finfo(float).eps
            
        # Wikipedia : https://en.wikipedia.org/wiki/Pearson_correlation_coefficient
        # For pairs from an uncorrelated bivariate normal distribution, the sampling distribution of the studentized 
        # Pearson's correlation coefficient follows Student's t-distribution with degrees of freedom n − 2. 
        t_score = r * np.sqrt((n - 2) / (1.0 - r ** 2))  # Calculate t-score
        
        #ab = n/2 - 1
        #dist = stats.beta(ab, ab, loc=-1, scale=2)
        #pvalue = self.beta_dist.sf(r)
        
        p_value = 0 #reject of null hypothese = no relation
        return n, nnan, r, p_value, t_score
    
    def _distance(self, segment: np.ndarray, master_segment: np.ndarray, distance: str = COSINE, min_overlap: int = 30):
        # Find valid data points
        valid_data_points = (~np.isnan(segment)) & (~np.isnan(master_segment))
        length = np.count_nonzero(valid_data_points)
        nnan =  len(valid_data_points) - length # number of nan

        if length < min_overlap:
            return length, nnan, np.nan 

        if EUCLIDEAN == distance:
            d = spatial.distance.euclidean(segment[valid_data_points], master_segment[valid_data_points])
        elif CITYBLOCK == distance:
            d = spatial.distance.cityblock(segment[valid_data_points], master_segment[valid_data_points])
        elif COSINE == distance:
            d = spatial.distance.cosine(segment[valid_data_points], master_segment[valid_data_points])
        else:
            raise ValueError('cross dating._distance: Unavailable distance method: ' + distance)

        return length, nnan, d

class CrossDating(param.Parameterized):
    num_threads = param.Integer(default=1, bounds=(1, 10), step=1, doc='number of threads')
    min_overlap = param.Integer(default=50, bounds=(10, 100), step=5, doc='Minimal number of overlap ring')
    method = param.ListSelector([CORRELATION, GLK] , objects=crossdating_method, doc='Crossdating method')
    distance = param.Selector(objects=crossdating_distance, doc='Crossdating distance')

    class ParamProgress(param.Parameterized):
        start_time = param.Number(default=0, doc='start time of the run')
        current_time = param.Number(default=0, doc='current time of the run')
        max_count = param.Integer(default=0, doc='number of computed results to count')
        count = param.Integer(default=0, doc='number of computed results')
        
        def reset(self, max_count=0):
            self.max_count = max_count
            self.current_time = self.start_time = time.time()
            self.count = 0 
        
        def inc(self):
            self.current_time = time.time()
            self.count += 1 
            self.ring_type = None
        
        def info(self):
            if self.max_count <= 0:
                return 0, ''
            t = self.current_time - self.start_time
            st = time.strftime("%M:%S", time.gmtime(t))
            #itt = time.strftime("%M:%S", time.gmtime(t/self.count)) if self.count > 0 else 0
            r = round(self.count/self.max_count*100, 2)
            return int(r), f'{r}%, {self.count}/{self.max_count}' #[{st}s, {itt}it/s ]'
    progress = ParamProgress()
    
    class ParamMatrix(param.Parameterized):
        metric = param.Selector(default='euclidean', objects=['cityblock', 'correlation', 'cosine', 'euclidean', 'mahalanobis',  
                                                'seuclidean',  'sqeuclidean'], doc='Dendrogram metric')
        method = param.Selector(default='ward', objects=['single', 'complete', 'average', 'weighted', 'centroid', 
                                                'median', 'ward', ], doc='Dendrogram method to merge two clusters')
        sorted = param.Boolean(default=True, doc='Sort the matrix')
        size_scale = param.Number(default=0.5, bounds=(0.1, 1), step=0.1, doc='figure h/w scale')
        font_scale = param.Number(default=0.5, bounds=(0.1, 2), step=0.1, doc='figure font scale')
    
    param_matrix = ParamMatrix(name='Matrix')

    class ParamStem(param.Parameterized):
        height = param.Integer(default=500, bounds=(50, 1000), step=25)
        keycode_nrows = param.Integer(default=3, bounds=(1, 10), step=1)
        win = param.Integer(default=25, bounds=(5, 50), step=5)

    param_stem = ParamStem(name='Stem')

    class ParamHist(param.Parameterized):
        height = param.Integer(default=200, bounds=(50, 500), step=10)
        aspect = param.Number(default=2, bounds=(0.1, 5), step=0.1)
        font_size = param.Integer(default=5, bounds=(1, 20), step=1)
        bullet_size = param.Integer(default=5, bounds=(1, 20), step=1)

    param_hist = ParamHist(name='Hist')

    class ParamMap(param.Parameterized):
        height_width = param.Integer(default=1000, bounds=(1000, 2000), step=10)
        font_size = param.Integer(default=5, bounds=(1, 20), step=1)
        line_ratio = param.Number(default=1, bounds=(0.1, 10), step=0.1)
        bullet_ratio = param.Number(default=1, bounds=(0.1, 10), step=0.1)
            
    param_map = ParamMap(name='Map')

    class ParamGraph(param.Parameterized):
        height_width = param.Integer(default=1000, bounds=(1000, 2000), step=10)
        font_size = param.Integer(default=5, bounds=(1, 20), step=1)
        line_ratio = param.Number(default=0.5, bounds=(0.1, 2), step=0.1)
        bullet_ratio = param.Number(default=0.5, bounds=(0.1, 2), step=0.1)
        layout = param.Selector(default='spring', objects=['circular', 'spring', 'spectral'], doc='algorithm for node positions')
            
    param_graph = ParamGraph(name='Graph')


    results = None
    #matrix_dendrogram = param.Boolean(default=False, doc='If matrix is sorted, plot the matrix dendrogram')
    
    COLS = COLS

    def __init__(self, **params):

        super(CrossDating, self).__init__(**params)   
        self.offsets = None
        self.results = {}
        self.dcg = {}
        self.self_crossdating = False
        self.param_data = {}
        self.ring_type = ''
        
    def run(self, data, master_data=None, param_data={DETREND: RAW}):
        self.param_data = param_data
        self.ring_type = param_data[DETREND]
        self.results = {}
        if self.num_threads > 1:
            return self._run_thread(data, master_data)
        return self._run(data, master_data)
            
    def _run_thread(self, data, master_data):
        worker_class = CrossDatingWorker(self.num_threads, self.min_overlap, self.method)
        self.self_crossdating = False
        last_data = len(data)
        
        if master_data is None:
            self.self_crossdating = True
            master_data = data
            last_data -= 1
        self.progress.reset(last_data)

        print('---> _run_thread with map', self.num_threads)
        with ProcessPoolExecutor(max_workers=self.num_threads, initializer=set_worker, initargs=(self.self_crossdating, data, master_data)) as executor:
            futures = []
            res_lst = []
            # Start an asynchronous task (future) for each index
            for i, idx in enumerate(data.index[:last_data]):
                future = executor.submit(worker, worker_class, i)
                futures.append(future)

            # Wait for all tasks to be completed
            for future in futures:
                res = future.result()
                res_lst.append(res)
                self.progress.inc()
        for res in res_lst:
            self.results.update(res)
            
        executor.shutdown()
        self.progress.count = self.progress.max_count
        return self.results

    def _run(self, data, master_data=None):
        #import cProfile, pstats, io
        #from pstats import SortKey
        #cp = cProfile.Profile()
        #cp.enable()

        worker_class = CrossDatingWorker(self.num_threads, self.min_overlap, self.method)
        # sdcg = ndcg = n = 0
        self.self_crossdating = False
        end_data = len(data)
        
        if master_data is None: # crossdating over data
            self.self_crossdating = True
            master_data = data
            end_data -= 1        

        self.progress.reset(end_data)
            
        for i, idx in  enumerate(data.index[:end_data]):
            res = worker_class.run_one(i, self.self_crossdating, data, master_data)
            self.results.update(res)
            self.progress.inc()

        #cp.disable()
        #s = io.StringIO()
        #sortby = SortKey.CUMULATIVE
        #ps = pstats.Stats(cp, stream=s).sort_stats(sortby)
        #ps.print_stats()
        #logger.info(s.getvalue())

        return self.results

    def discounted_cumulative_gain (self, results: pd.DataFrame, rank_key):
    # Discounted Cumulative Gain 
    # https://en.wikipedia.org/wiki/Discounted_cumulative_gain

        #dating_result_sorted = sorted(dating_result, key=lambda x: x[key], reverse=True)
        sdcg = 0
        srank = 0
        n = 0
        res = []
        
        dated = results.loc[results[DATED] == True, :]
        for i, row in dated.iterrows():
            n += 1
            rank = row[rank_key]
            idx_master = row[IDX_MASTER]
            idx_samples = row[IDX]
            dcg = 1 / np.log2(rank + 1)
            res.append({IDX_MASTER: idx_master, IDX: idx_samples, rank_key: rank, DCG: dcg})
            sdcg += dcg
            srank += rank
            
        return res, sdcg/n, srank/n
    
    """def det_curve(self, key_score=SCORE):
        df = self.concat_results()[[key_score, DATED]]
        fpr, fnr, thresholds = det_curve(y_score=df[key_score].to_numpy(), y_true=df[DATED].to_numpy(dtype='Int32') )
        det = DetCurveDisplay(fpr=fpr, fnr=fnr, estimator_name=key_score+' / '+self.ring_type)
        return fpr, fnr, thresholds, det"""
    
    def matrix(self, data, score, col_keys=[KEYCODE_MASTER, KEYCODE]):#, score=None, threshold=None):
        #data = self.get_dated()
        if (data is None) or (len(self.results) == 0):
            raise ValueError('no dated results')
        if score not in data.columns:
            raise KeyError(f'cross dating.matrix: {score} not in results')

        columns = data[col_keys[1]].unique().tolist()
        index = data[col_keys[0]].unique().tolist()
        df = data.loc[:, col_keys + [score]]
        #if threshold is None:
        #    threshold = np.finfo(np.float64).min
        if self.self_crossdating:
            idxs = list(set(columns + index))    
            mat = pd.DataFrame(columns=idxs, index=idxs, dtype='float')
            for _, (idx1, idx2, value) in df.iterrows():
                #if (value > threshold):
                mat.at[idx1, idx2] = mat.at[idx2, idx1] = float(value)
        else:
            mat = pd.DataFrame(columns=columns, index=index, dtype='float')
            for _, (idx1, idx2, value) in df.iterrows():
                #if (value > threshold):
                mat.at[idx1, idx2] = float(value)
        return mat

    # def get_dated(self):
    #     lst = []
    #     for df in self.results.values():
    #         df_dated = df[df[DATED] == True]
    #         if len(df_dated) > 0:
    #             lst.append(df_dated)
    #     df = pd.concat(lst) if len(lst) > 0 else None
    #     return df
    
    def get_rank_key(self, score):
        if score in [DIST, COSINE, EUCLIDEAN, CITYBLOCK]:
            return D_RANK
        elif score == Z_SCORE:
            return Z_RANK
        else:
            return T_RANK
                 
    def concat_results(self, score, threshold=None, max_rank=None, dated=None):
        rank_key = self.get_rank_key(score)
        if len(self.results) == 0:
            raise ValueError('cross dating.concat_results: no results')
        if (threshold is None) and (max_rank is None) and (dated is not None):
            #print('concat_results no filter')
            with warnings.catch_warnings():
                # TODO: pandas 2.1.0 has a FutureWarning for concatenating DataFrames with Null entries
                warnings.filterwarnings("ignore", category=FutureWarning)
                return pd.concat(list(self.results.values()), ignore_index=True)
        lst = []
        #print('concat_results filter')
        for df in self.results.values():
            mask = np.array([True] * len(df))
            if (max_rank is not None):
                mask = (df[rank_key] <= max_rank) & mask
                #df = df[df[rank_key] <= max_rank]
            if threshold is not None:
                mask = (df[score] > threshold) & mask
                #df = df[df[score] > threshold]
            if dated is not None:
                mask = (df[DATED] == dated) & mask
                #df = df[df[DATED] == dated]
            lst.append(df[mask])
        #print('concat_results concat')
        with warnings.catch_warnings():
            # TODO: pandas 2.1.0 has a FutureWarning for concatenating DataFrames with Null entries
            warnings.filterwarnings("ignore", category=FutureWarning)
            df = pd.concat(lst, ignore_index=True)
            #print('concat_results concat done', len(df))
            return df
    
    def fillmat(self, mat):
        mat = mat.copy()
        center = mat.mean(axis=None)
        max_ = mat.max(axis=None) + np.finfo(float).eps
        mask = mat.isna()
        if self.self_crossdating:
            for i in range(len(mat)):
                mat.iat[i, i] = max_
        return mat.fillna(mat.min(axis=None) - np.finfo(float).eps)
    
    def heat_matrix(self, score, threshold=None, col_keys=[KEYCODE_MASTER, KEYCODE], 
                    metric=None, method=None):
        sns.set_theme(font_scale=0.5, palette='colorblind')

        if metric is None: metric = self.param_matrix.metric
        if method is None: method = self.param_matrix.method
        
        data = self.concat_results(score=score, threshold=threshold, max_rank=None, dated=True)
        data = self.matrix(data, score, col_keys)        
        
        #data = self.matrix(col_keys, score=score, threshold=threshold)        
        size_h = np.ceil(data.shape[0]) * self.param_matrix.size_scale
        size_w = np.ceil(data.shape[1]) * self.param_matrix.size_scale
        #print('size', size_h, size_w)
        sns.set_context("notebook", font_scale=self.param_matrix.font_scale)
        mat = self.fillmat(data)
        mask = data.isna()
        cm = sns.light_palette("#79C", n_colors=mat.stack().nunique(), reverse=True, as_cmap=True)
        if self.param_matrix.sorted:
            fig = sns.clustermap(mat, metric=metric ,method=method, cmap=cm, linewidths=.5, 
                                 figsize=(size_h, size_w), mask=mask, annot=data)._figure
        else: 
            fig, ax = plt.subplots(figsize=(size_h, size_w))
            ax = sns.heatmap(mat, cmap=cm, linewidths=.5, ax=ax, mask=mask, annot=data)
        plt.close(fig)
        return fig
    
    def stem(self, score, threshold=None, max_rank=None, keycode=''):    
        rank_key = self.get_rank_key(score)
        #print(rank_key)
            
        data = self.concat_results(score=score, threshold=threshold, max_rank=max_rank)
        #print(data.info())
        if max_rank is None:
            max_rank = data[rank_key].max()
            
        if len(data) == 0:
            raise ValueError(f'cross dating.stem: The results matrix is empty after applying the threshold and max_rank.')
        if data[DATE_END_ESTIMATED].isna().all():
            raise ValueError(f'cross dating.stem: no {DATE_END_ESTIMATED}')

        keycodes = sorted(data[KEYCODE].unique().tolist())
        ranks = [f'rank {x}' for x in range(max_rank)]
        MARKERS = ['circle', 'square', 'diamond', 'hex', 'star', 'triangle', 'inverted_triangle', 'asterisk',
                   'circle_cross', 'square_cross', 'diamond_cross', 
                   'circle_dot', 'square_dot', 'diamond_dot', 'hex_dot', 'star_dot', 'triangle_dot',
                   'circle_x', 'circle_y', 'dash', 'plus', 'square_pin', 'square_x', 'triangle_pin', 'x', 'y', 'dot', 'cross', ]
        #w = self.param_stem.width
        h = self.param_stem.height
        win = self.param_stem.win//2
        date_max = data.loc[data[rank_key] == 1, DATE_END_ESTIMATED].value_counts().idxmax()
        nranks = len(ranks) if len(ranks) < 11 else 11
        colors = brewer['RdYlBu'][nranks]
        fig = figure(title=keycode, background_fill_color="#fafafa", 
                   x_range=(date_max-win, date_max+win), height=h, sizing_mode='stretch_width',
                   tools="pan,wheel_zoom,box_zoom,reset,hover,save",
                   tooltips=[(KEYCODE, f'@{KEYCODE}'), ('keycode master', '@MASTER'), (f'{score}', '@score'), (f'{rank_key}', '@rank')])
        fig.output_backend = "svg"

        fig.xaxis.axis_label = DATE_END_ESTIMATED
        fig.yaxis.axis_label = score
        
        for rank, df in data.groupby(rank_key):
            df2 = df.rename(columns={KEYCODE_MASTER: 'MASTER', score:'score', rank_key: 'rank'})
            c = colors[rank-1] if rank < nranks else colors[nranks-1]
            fig.scatter(DATE_END_ESTIMATED, 'score', source=ColumnDataSource(df2), 
                    fill_alpha=0.8, size=12, marker=factor_mark(KEYCODE, MARKERS, keycodes), color=c) #legend_group=KEYCODE,
        
        # Add keycodes legend
        # create an invisible renderer to drive shape legend
        rs = fig.scatter(x=0, y=0, color="grey", size=6, marker=MARKERS[:len(keycodes)])
        rs.visible = False

        # add a shape legend with explicit index, set labels to fit your needs
        legend = Legend(
            items=[LegendItem(label=s, renderers=[rs], index=i) for i, s in enumerate(keycodes)],
            location='center_left', orientation='horizontal', nrows=self.param_stem.keycode_nrows, title=KEYCODE)
        fig.add_layout(legend, 'above')
        
        # Add rank legend
        # create an invisible renderer to drive color legend
        rc = fig.rect(x=0, y=0, height=1, width=1, color=colors[:nranks])
        rc.visible = False

        # add a color legend with explicit index, set labels to fit your need
        labels = [f'rank {i}' if i < nranks -1 else f'rank \u2265 {i}' for i, c in enumerate(colors[:nranks])]
        legend = Legend(items=[LegendItem(label=labels[i], renderers=[rc], index=i) for i, c in enumerate(colors[:nranks])], 
                location='center_left', orientation='horizontal', nrows=1, title=rank_key)
        fig.add_layout(legend, 'above')
        
        # Add ZOOM
        zoom_fig = figure(sizing_mode='stretch_width', height=round(h / 4), y_range=fig.y_range,
            toolbar_location=None, background_fill_color="#fafafa",)

        for rank, df in data.groupby(rank_key):
            c = colors[rank-1] if rank < nranks else colors[nranks-1]
            zoom_fig.scatter(DATE_END_ESTIMATED, score, source=ColumnDataSource(df), fill_alpha=0.8, 
                                size=3, marker=factor_mark(KEYCODE, MARKERS, keycodes), color=c)

        zoom_fig.x_range.range_padding = 0
        zoom_fig.ygrid.grid_line_color = None

        range_tool = RangeTool(x_range=fig.x_range)
        range_tool.overlay.fill_color = "navy"
        range_tool.overlay.fill_alpha = 0.2
        zoom_fig.add_tools(range_tool)
        
        return fig, zoom_fig
                
    def hist(self, score=None) :
        data = self.concat_results(score=score)
        if len(data) == 0:
            raise ValueError(f'cross dating.hist: The results matrix is empty after applying the threshold and max_rank.')
        
        aspect = self.param_hist.aspect
        height = self.param_hist.height
        width = round(height*aspect)
        font_size = f'{self.param_hist.font_size}pt'
        bullet_size = self.param_hist.bullet_size
        idxs = data[IDX].unique().tolist()
        master_idxs = data[IDX_MASTER].unique().tolist()

        gdata = data.groupby([IDX, IDX_MASTER])

        smin, smax = data[score].min() , data[score].max() 
        d = (smax - smin) * 0.01
        smin, smax = smin - d, smax + d
        n = round((smax - smin) * 100)
        x = np.linspace(smin, smax, n)
        pdf = gaussian_kde(data[score])
        y_max = 0
        rows = []
        for j, master_idx in enumerate(master_idxs):
            row = []
            for i, idx in enumerate(idxs):
                if (idx, master_idx) in gdata.groups:
                    grp = gdata.get_group((idx, master_idx))
                    
                    keycode = f'(Master) {grp.loc[grp[IDX_MASTER] == master_idx, KEYCODE_MASTER].iloc[0]} / {grp.loc[grp[IDX] == idx, KEYCODE].iloc[0]}'
                    if grp[DATED].isna().any():
                        keycode += '(no date set)'
                    p = figure(title=keycode, width=width, height=height, tools='save')
                    p.output_backend = "svg"
                    p.toolbar_location = None

                    p.xaxis.ticker = [0]
                    p.xaxis[0].formatter = PrintfTickFormatter(format="%5.2f")
                    pdf = gaussian_kde(grp[score])
                    y = pdf(x)
                    y[0] = y[-1] = 0
                    ly_max = np.nanmax(y)
                    y_max = max(ly_max, y_max) 
                    if grp[DATED].isna().any():
                        p.patch(x, y, alpha=0.3, line_color="black", color='red')
#                        p.xaxis.ticker = [dx]
                    else:
                        p.patch(x, y, alpha=0.3, line_color="black")
                        ey = grp.loc[grp[DATED], DATE_END_ESTIMATED].max()
                        dx = grp.loc[grp[DATED], score].max()
#                        p.xaxis.ticker = [dx]
                        if not np.isnan(dx):
                            s = p.scatter([dx], [pdf(dx)[0]], color='red', size=bullet_size, legend_label=f'date: {ey}')
                            p.patch([dx, dx], [0, pdf(dx)[0]], color='red')
                            p.legend.label_text_font_size = font_size
                            p.legend.label_height = round(y_max*0.05)
                            p.legend.location = "top_right"
                            p.legend.padding = 1
                            p.legend.margin = 1
                            p.legend.glyph_width = round(4*aspect)
                            p.legend.glyph_height = round(4*aspect)
                            p.legend.background_fill_alpha = 0.5
                    
                    p.xaxis.visible = True
                    p.yaxis.visible = False
                    p.title.text_font_size = font_size
                    p.xaxis.major_label_text_font_size = font_size
                    p.yaxis.major_label_text_font_size = font_size
                    p.ygrid.grid_line_color = None
                    row.append(p)
            rows.append(row)

        y_max *= 1.01
        cols = pn.Column()
        for i, ri in enumerate(rows):
            cols.append(pn.Row(*ri))
            for j, rj in enumerate(ri):
                rj.y_range = Range1d(0, y_max)
        #return cols
        gp = gridplot(rows, merge_tools=True, toolbar_location='above') 
        return cols, gp

    def chord(self, score, threshold=0, max_rank=None):
        data = self.concat_results(score=score, threshold=threshold, max_rank=max_rank)
        #links = data[[IDX_CHILD, IDX_MASTER, score]]
        #nodes = hv.Dataset(pd.DataFrame(data['nodes'])

    def map(self, score, data_dt=None, threshold=0, max_rank=None):
        
        def lnglat_to_meters(longitude: float, latitude: float) -> tuple[float, float]:
            """ Projects the given (longitude, latitude) values into Web Mercator
            coordinates (meters East of Greenwich and meters North of the Equator)."""
            origin_shift = np.pi * 6378137
            easting = longitude * origin_shift / 180.0
            northing = np.log(np.tan((90 + latitude) * np.pi / 360.0)) * origin_shift / np.pi
            return (easting, northing)
        
        rank_key = self.get_rank_key(score)
        data = self.concat_results(score=score, threshold=threshold, max_rank=max_rank, dated=True)
        
        if len(data) == 0:
            raise ValueError(f'cross dating.stem: The results matrix is empty after applying the threshold and max_rank.')
        if data_dt[SITE_LONGITUDE].isna().all():
            raise ValueError(f'map no {SITE_LONGITUDE}')
        if data_dt[SITE_LATITUDE].isna().all():
            raise ValueError(f'map no {SITE_LATITUDE}')

        nodes = data.groupby(IDX)[score].sum().to_dict()
        nodes.update(data.groupby(IDX_MASTER)[score].sum().to_dict())
        keycodes = data[[IDX, KEYCODE]].drop_duplicates().set_index(IDX).to_dict()[KEYCODE]
        keycodes.update(data[[IDX_MASTER, KEYCODE_MASTER]].drop_duplicates().set_index(IDX_MASTER).to_dict()[KEYCODE_MASTER])
        geo = {}
        for _, row in data_dt.iterrows():
            geo[row[IDX_CHILD]] = lnglat_to_meters(row[SITE_LONGITUDE], row[SITE_LATITUDE])
        
        map_center = lnglat_to_meters(3.0, 46.0) # Map center
        delta = 1000000 # (m)  plus-and-minus from map center

        fig = figure(x_range=(map_center[0] - delta, map_center[0] + delta), 
                    y_range=(map_center[1] - delta, map_center[1] + delta) , 
                    x_axis_type="mercator", y_axis_type="mercator",
                    height=self.param_map.height_width, width=self.param_map.height_width, 
                    tools="pan,wheel_zoom,box_zoom,reset,hover,save",)
                    #tooltips=[(KEYCODE, f'@{KEYCODE}'), ('keycode master', '@MASTER'), (f'{score}', '@score'), ('rank', f'@{rank_key}')])
        fig.add_tile("CartoDB Positron", retina=True)
        
        for _, row in data.iterrows():
            idx_master = row[IDX_MASTER]
            idx = row[IDX]
            value = row[score]
            #fig.line([geo[idx][0], geo[idx_master][0]], [geo[idx][1], geo[idx_master][1]], color='black', line_width=int((value+1)*self.param_map.line_ratio), line_cap='round')

        for idx, value in nodes.items():
            v = int((value+1)*self.param_map.bullet_ratio)
            if (geo[idx][0] is not None) and (geo[idx][1] is not None):
                #print(keycodes[idx], geo[idx])
                fig.scatter([geo[idx][0]], [geo[idx][1]], alpha=0.3, size=v, legend_label=f'{keycodes[idx]}')
                fig.text(x=geo[idx][0], y=geo[idx][1], text=str(value), x_offset=5, y_offset=5, anchor="bottom_left")
        
        fig.legend.location = "top_left"
        fig.legend.padding = 1
        fig.legend.margin = 1
        
        return fig
    
    def graph(self, score, data_dt=None, threshold=0, max_rank=None):
        def get_graph(G, scale=1.8):
            if self.param_graph.layout == 'cirular':
                graph = from_networkx(G, nx.circular_layout, scale=scale, center=(0,0))
            elif self.param_graph.layout == 'spectral':
                graph = from_networkx(G, nx.spectral_layout, scale=scale, center=(0,0))
            else:
                graph = from_networkx(G, nx.spring_layout, scale=scale, center=(0,0))
            return graph
        
        #print('*** score:', score)
        
        rank_key = self.get_rank_key(score)
        data = self.concat_results(score=score, threshold=threshold, max_rank=max_rank, dated=True)
        
        if len(data) == 0:
            raise ValueError(f'cross dating.stem: The results matrix is empty after applying the threshold and max_rank.')
        if data_dt[SITE_LONGITUDE].isna().all():
            raise ValueError(f'map no {SITE_LONGITUDE}')
        if data_dt[SITE_LATITUDE].isna().all():
            raise ValueError(f'map no {SITE_LATITUDE}')
        
        #nodes = data.groupby(IDX)[score].sum().to_dict()
        #nodes.update(data.groupby(IDX_MASTER)[score].sum().to_dict())
        keycodes = data[[IDX, KEYCODE]].drop_duplicates().set_index(IDX).to_dict()[KEYCODE]
        keycodes.update(data[[IDX_MASTER, KEYCODE_MASTER]].drop_duplicates().set_index(IDX_MASTER).to_dict()[KEYCODE_MASTER])
        nodes = data.groupby(IDX)[score].sum().to_dict()
        nodes.update(data.groupby(IDX_MASTER)[score].sum().to_dict())

        from bokeh.palettes import Turbo256
        from bokeh.plotting import figure, from_networkx

        G = nx.Graph()
        elist = [(row[IDX_MASTER], row[IDX], row[score]) for _, row in data.iterrows()]
        G.add_weighted_edges_from(elist)
        
        fig = figure(x_range=(-2, 2), y_range=(-2, 2),
           x_axis_location=None, y_axis_location=None,
           height=self.param_graph.height_width, width=self.param_graph.height_width, 
           tools="hover", tooltips=f"{KEYCODE}: @{KEYCODE}")
        fig.grid.grid_line_color = None

        graph = get_graph(G)

        fig.renderers.append(graph)

        # Add some new columns to the renderers 
        color = []
        size = []
        value = []
        name = []
        d = max(256 // len(graph.node_renderer.data_source.data['index']), 1)
        for i, idx in enumerate(graph.node_renderer.data_source.data['index']):
            color.append(Turbo256[min(i*d, 255)])
            size.append(int(max(nodes[idx], 1) * self.param_graph.bullet_ratio))
            value.append(nodes[idx])
            name.append(keycodes[idx])
        graph.node_renderer.data_source.data['color'] = color
        graph.node_renderer.data_source.data['size'] = size
        graph.node_renderer.data_source.data['value'] = value
        graph.node_renderer.data_source.data['name'] = name
        
        width = []
        tmp = graph.edge_renderer.data_source.data
        for start, end, weight in zip(tmp['start'], tmp['end'], tmp['weight']):
            width.append(int((weight+1)*self.param_graph.line_ratio))

        graph.edge_renderer.data_source.data['width'] = width
        
        #print('-'*10)
        text_ds = ColumnDataSource()
        xs, ys, idxs, keys = [], [], [], []
        for key, (x, y) in graph.layout_provider.graph_layout.items():
            xs.append(x)           
            ys.append(y) 
            idxs.append(key) 
            keys.append(keycodes[key]) 
        
        text_ds.data['x'], text_ds.data['y'] = xs, ys
        text_ds.data[IDX], text_ds.data[KEYCODE] = idxs, keys
        fig.text(x='x', y='y', text=KEYCODE, source=text_ds,  anchor="bottom_left") #x_offset=5, y_offset=5,
            

        #print('-'*10)
        #print(graph.node_renderer.data_source.data)
        #print(graph.layout_provider.graph_layout)
        #print('-'*10)
        #print(graph.edge_renderer.data_source.data)
        
        graph.node_renderer.glyph.update(size="size", fill_color="color")
        graph.edge_renderer.glyph.update(line_width="width")
        
        return fig


