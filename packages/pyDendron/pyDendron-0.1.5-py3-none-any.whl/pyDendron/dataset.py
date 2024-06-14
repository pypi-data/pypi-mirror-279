"""
Dataset class
"""
__author__ = "Sylvain Meignier"
__copyright__ = "Copyright 2023 Sylvain Meignier, Le Mans Université, LIUM (https://lium.univ-lemans.fr/)"
__license__ = "GPL"

from typing import List, Tuple, Union
import warnings
import copy
import pickle
import json
from pathlib import Path
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor


import pandas as pd
import numpy as np
import panel as pn
import param

from collections import Counter
from scipy.stats import  kurtosis, skew, entropy

from pyDendron.app_logger import logger
from pyDendron.dataname import *
from pyDendron.components_tree import ComponentsNode, ComponentsTree
from pyDendron.chronology import chronology, chronologies
from pyDendron.crossdating import CrossDating
from pyDendron.detrend import detrend

class Dataset(param.Parameterized):
    """
    Data storage of sequences and components. Includes also selections of pairs.
    """
    VERSION = 3
    
    notify_message = param.String(default='', doc='log change in the dataset') 
    notify_reload = param.Event()
    notify_synchronize = param.Event()
    notify_packages = param.Event()
    counter = param.Integer(3, doc='Node added in tree')
    save_auto =  param.Boolean(False, doc='show all components / sequences')
            
    version_control = True
    
    def __init__(self, sequences=None, components=None, username='None', **params):
        super(Dataset, self).__init__(**params)   
        self.username = username        
        self.filename = None
        
        if (components is not None) and (sequences is not None):
            self.sequences = pd.DataFrame(sequences)
            self.components = pd.DataFrame(components)
            self.update()
        else:
            self.clean()   
        self._packages = {}
        self._freeze_components = None
        self._freeze_sequences = None
        self._log = []
        self._crossdating = pd.DataFrame()
    
    
    def get_log(self):
        return pd.DataFrame(self._log, columns=log_dtype_dict.keys())
    
    def get_sequences_copy(self, idxs):
        data = self.sequences.loc[idxs].copy()
        return data

    def get_components_copy(self, idx_pairs):
        data = self.components.loc[idx_pairs].copy()
        return data
        
    def freeze_sequences(self, idxs):
        self._freeze_sequences = self.get_sequences_copy(idxs)

    def freeze_components(self, idx_pairs):
        """
        Freezes the components specified by the given index pairs.

        Args:
            idx_pairs (list): A list of index pairs specifying the components to freeze.

        Returns:
            None
        """
        self._freeze_components = self.get_components_copy(idx_pairs)

    def log_components(self, idx_pairs, comments=''):
        """
        Compare the components specified by the given index pairs.

        Args:
            idx_pairs (list): A list of index pairs specifying the components to compare.

        Returns:
            None

        Raises:
            None
        """
        new_df = self.get_components_copy(idx_pairs)
        old_df = self._freeze_components
        log = []
        
        merge = old_df.join(new_df, lsuffix='_old', rsuffix='_new')
        #print('merge', merge)
        for idxs, row in merge.iterrows():
            (idx_child, idx_parent) = idxs
            old, new = row[OFFSET+'_old'], row[OFFSET+'_new']
            #print(idx_child, idx_parent)
            #print('old', old, 'new', new)
            if old != new:
                log.append([datetime.now(), idx_child, idx_parent ,OFFSET, old, new, self.username, comments])
        
        self._freeze_components = None
        if len(log) > 0:
            self._log += log
            self.notify_changes(comments)
            return True
        #print('no change in components')
        return False
        
    def log_sequences(self, idxs, comments=''):
        """
        Compare sequences between the old and new dataframes.

        Args:
            idxs (list): List of indices to compare.
            comments (str, optional): Additional comments for the comparison. Defaults to ''.

        Returns:
            dict: A dictionary containing the history of changes made in the sequences.
                The dictionary keys are tuples of (index, column, date), and the values are lists
                containing the old value, new value, user, and comments.

        Raises:
            KeyError: If the two dataframes are not aligned.

        """
        def compare(idx, old_row, new_row):
            log = []
            d = new_row[DATE_SAMPLING]
            for col in new_row.index:
                cmp = False 
                old, new = old_row[col], new_row[col]
                if col in [DATA_INFO, DATA_VALUES, DATA_WEIGHTS]:
                    cmp = not np.array_equal(np.nan_to_num(old), np.nan_to_num(new))
                elif (pd.isna(old) or pd.isna(new)) or (col == DATE_SAMPLING):
                    cmp = False
                else:
                    cmp = old != new
                if cmp:
                    log.append([d, idx, pd.NA ,col, old, new, self.username, comments])
            return log
        
        old_df = self._freeze_sequences
        new_df = self.get_sequences_copy(idxs)
        log = []
        if isinstance(new_df, pd.Series):
            log = compare(idxs, old_df, new_df)
        else:
            for (idx1, row1), (idx2, row2) in zip(old_df.iterrows(), new_df.iterrows()):
                if idx1 == idx2:
                    log = compare(idx1, row1, row2)
                else:
                    raise KeyError('The 2 dataframes are not aligned.')
        self._freeze_sequences = None
        #print('Log', log)
        if len(log) > 0:
            self._log += log
            self.notify_changes(comments)
            return True
        return False
    
    def get_crossdating_log(self):
        return self._crossdating
    
    def log_crossdating(self, crossdating = {}):
        crossdating[CROSSDATING_DATE] = datetime.now()
        if len(self._crossdating) > 0:
            self._crossdating.loc[self._crossdating.index.max()+1] = crossdating
        else:
            self._crossdating = pd.DataFrame([crossdating])
    
    def is_empty(self):
        """
        Returns True if dataset is empty.
        """
        return len(self.sequences) == 0
        
    def notify_changes(self, message):
        """
        Set `msg` into `self.change`.
        """
        self.notify_message = message
        if self.save_auto:
            print('*** Save auto ***')
            self.dump()
            
        if message in ['load', 'reindex']:
            self.param.trigger('notify_reload')
        else:
            self.param.trigger('notify_synchronize')
        logger.debug(f'dataset notify_changes: {message}')
        
    def update(self, update_tree=False):
        """
        Update index and dtype of `self.sequences` and `self.component`.
        """
        self.sequences.reset_index(inplace=True)
        self.sequences = pd.DataFrame(self.sequences, columns=sequences_index+sequences_cols)
        self.sequences.set_index(sequences_index, inplace=True, verify_integrity=True)  
        #for key, value in sequences_dtype_dict.items():
            #print(key, value)
        #    self.sequences[key] = self.sequences[key].astype(value, copy=True)
            
        self.sequences = self.sequences.astype(sequences_dtype_dict, copy=True)

        self.components.reset_index(inplace=True)
        self.components = pd.DataFrame(self.components, columns=components_index+components_cols)
        self.components.set_index(components_index, inplace=True, verify_integrity=True)  
    
    def clone(self):
        """
        Copy the dataset and returns it.
        """
        tmp = Dataset()
        tmp.sequences = self.sequences.copy()
        tmp.components = self.components.copy()
        tmp._packages = copy.deepcopy(self._packages)
        
        return tmp
    
    def _get_filename(self, filename: str = None) -> str:
        if filename is None:
            if self.filename is None:
                raise ValueError('DataSet._get_filename: empty filename')
            else:
                filename = self.filename
        else:
            self.filename = filename
        return filename
 
    def dump(self, filename: str = None):
        """
        Dump/save a dataset into `filename`.
        """
        filename = self._get_filename(filename)
        suffix = Path(filename).suffix
        if suffix == '.json':
            self._dump_json(filename)
        elif suffix == '.p':
            self._dump_pickle(filename)
        elif suffix == '.xlsx':
            self._dump_excel(filename)
        else:
            raise TypeError(f'DataSet.dump: unknown suffix {suffix} from {filename}')

    def _dump_pickle(self, filename: str):
        dataset_path = Path(filename) 
        with dataset_path.open('wb') as fic:
            pickle.dump((self.VERSION, self.sequences, self.components, self._packages, self._log, self._crossdating), fic)

    def _dump_json(self, filename: str):
        dataset_path = Path(filename) 
        with dataset_path.open('w') as fic:
            dfs_json = {
                VERSION: self.VERSION,
                SEQUENCES: json.loads(self.sequences.to_json(orient='table', index=True, force_ascii=False, indent=2)),
                COMPONENTS: json.loads(self.components.to_json(orient='table', index=True, force_ascii=False, indent=2)),
                SELECTIONS: self._packages,
                LOG: self._log,
                CROSSDATING: json.loads(self._crossdating.to_json(orient='table', index=True, force_ascii=False, indent=2))
            }
            json.dump(dfs_json, fic, indent=2)            

    def _dump_excel(self, filename: str):
        filename = Path(filename) 
        with pd.ExcelWriter(filename) as writer:
            self.sequences.to_excel(writer, sheet_name=SEQUENCES, merge_cells=False, float_format="%.6f")
            self.components.to_excel(writer, sheet_name=COMPONENTS, merge_cells=False, float_format="%.6f")

    def _dump_csv(self, path: str):
        base_path = Path(path)
        self.sequences.to_csv(base_path / 'sequences.csv', sep='\t', float_format="%.6f")
        self.components.to_csv(base_path / 'components.csv', sep='\t', float_format="%.6f")

    def update_version(self, version):
        self._log = []
        if version == self.VERSION:
            return
        if version <= 0:
            self.sequences = self.sequences.rename(columns={'uri': URI})
            self.sequences = self.sequences.rename(columns={'dated': DATED})
            self.sequences[DATED] = self.sequences[DATED].astype('string', copy=True)
            #print(self.sequences.info())
            self.sequences[DATED] = self.sequences[DATED].fillna('unknown')
            self.sequences[DATED].replace('0', 'unconfirmed', inplace=True)
            self.sequences[DATED].replace('1', 'confirmed', inplace=True)
        if version <= 1:
            self.sequences = self.sequences.rename(columns={'LabotaryCode': LABORATORY_CODE})
        if version <= 2:
            self.sequences[INCONSISTENT] = False
        logger.info(f'update dataset version {version} to {self.VERSION}')

    def load(self, filename: str=None):
        """
        Load a dataset from `filename`.
        """
        filename = self._get_filename(filename)
        suffix = Path(filename).suffix
        version = self.VERSION
        if suffix == '.json':
            version = self._load_json(filename)
        elif suffix == '.p':
            version = self._load_pickle(filename)
        elif suffix == '.xlsx':
            self._load_excel(filename)
        else:
            raise TypeError(f'DataSet.load: unknown suffix {suffix} from {filename}')
        self.update_version(version)
        self.notify_changes(f'load')

    def _load_pickle(self, filename: str):
        dataset_path = Path(filename) 
        with dataset_path.open('rb') as fic:
            data = pickle.load(fic)
            #if len(data) == 4:
            #    version, self.sequences, self.components, self._packages = data
            #elif len(data) == 5:
            #    version, self.sequences, self.components, self._packages, self._vc_history = data
            #else:
            version, self.sequences, self.components, self._packages, self._log, self._crossdating = data
        return version

    def _load_json(self, filename):
        dataset_path = Path(filename) 
        with dataset_path.open('r') as fic:
            dfs_json = json.load(fic)
        version = dfs_json[VERSION]
        self.sequences = pd.DataFrame(dfs_json[SEQUENCES])
        self.components = pd.DataFrame(dfs_json[COMPONENTS])    
        self._packages = dfs_json[SELECTIONS]
        self._log = dfs_json[LOG]
        self._crossdating = pd.DataFrame(dfs_json[CROSSDATING])
        self.update()
        return version
    
    def _load_excel(self, filename: str):
        filename = Path(filename) 
        seqs = pd.read_excel(filename, sheet_name=SEQUENCES)
        comps = pd.read_excel(filename, sheet_name=COMPONENTS)
        self.sequences = pd.DataFrame(seqs)
        self.components = pd.DataFrame(comps)        
        self.update()

    def _load_csv(self, path: str):
        base_path = Path(path)
        seqs = pd.read_csv(base_path / 'sequences.csv', sep='\t')
        comps = pd.read_csv(base_path / 'components.csv', sep='\t')
        self.sequences = pd.DataFrame(seqs)
        self.components = pd.DataFrame(comps)        
        self.update()
        
    def new_dataset(cls):
        dataset = cls.Dataset()
        dataset.new_root()
        dataset.new_trash()
        return dataset

    def new_root(self, keycode: str = 'Dataset', idx = ROOT):
        
        self.new(keycode, SET, idx_parent=None, idx=idx)
        data = []
        for idx_child in set(self.get_roots()):
            if idx != idx_child:
                data.append({IDX_PARENT: idx, IDX_CHILD: idx_child, OFFSET: pd.NA})
        df = pd.DataFrame(data).set_index(components_index, verify_integrity=True)
        with warnings.catch_warnings():
            # TODO: pandas 2.1.0 has a FutureWarning for concatenating DataFrames with Null entries
            warnings.filterwarnings("ignore", category=FutureWarning)
            self.components = pd.concat([self.components, df])
        return idx
            
    def new_trash(self, keycode: str = 'Trash' ):
        return self.new(idx=TRASH, idx_parent=None, keycode=keycode, category=SET)

    def new_clipboard(self, keycode: str = 'Clipboard' ):
        return self.new(idx=CLIPBOARD, idx_parent=None, keycode=keycode, category=SET)

    def new(self, keycode: str, category: str, idx_parent: int | None, 
            idx: int | None = None, others = {}, offset : int = pd.NA) -> int:
        """
        Creat a new Sequence and component if idx_parent is not None.
        
        Arguments
        ---------
        keycode: KEYCODE of the new Sequence.
        category: CATEGORY of the new Sequence.
        idx_parent: IDX_PARENT of the new Conponent.
        idx: IDX of the Sequence.
        others: dictionary of field, value pairs to set in new Sequence.
        offset: offset to set in new Component.
        make_root : !!!! error !!! make_root and idx_parent
        
        
        Returns
        -------
        The IDX of the new Sequence.
        """
        idx = self.sequences.index.max() + 1 if idx is None else idx
        others.update({KEYCODE: keycode, CATEGORY: category})
        if CREATION_DATE not in others:
            others[CREATION_DATE] = datetime.now()
        self.sequences.loc[idx, list(others.keys())] = others
        if idx_parent is not None:
            self.components.loc[(idx_parent, idx), OFFSET] = offset
        self.notify_changes(f'new')
        return idx                

    def _idx_list(self, idxs):
        """
        Returns a list of int created form a List[int] of from int.
        """
        if not isinstance(idxs, list):
            idxs = [idxs]
        return idxs
 
    def copy(self, triplets: List[Tuple[int, int, int]], dest_path:  List[int], notify=True) -> str:
        """
        Copy `triplets` in dest_path.
        
        Arguments
        ---------
        triplets: list of tuples (IDX_PARENT, IDX_CHILD, OFFSET)
        dest_path: a path
        
        Returns
        -------
        A dictonary of destination data : {(IDX_PARENT, IDX_CHILD): OFFSET}
        """
        # detect circular referencies
        couples_ = [(p, c) for p, c, o in triplets if dest_path[-1] != p]
        if len(couples_) != len(triplets):
            logger.warning('Destination and source are equal. Copy aborded.')
            return None

        couples_ = [(p, c) for p, c, o in triplets if c not in dest_path] 
        if len(couples_) != len(triplets):
            logger.warning('circular reference. Copy aborded.')
            return None

        dest_map = {(dest_path[-1], c) : o for p, c, o in triplets}
        msg = ''
        for keys, offset in dest_map.items():
            if keys in self.components.index:
                msg= str(keys[1])+', '
            else :
                self.components.loc[keys, OFFSET] = offset
        if msg != '':
            msg = 'Duplicates not copied: ' + msg 
            logger.warning(msg)

        if notify:
            self.notify_changes(f'copy')
                            
        return dest_map
    
    def cut(self, triplets: List[Tuple[int, int, int]], dest_path:  List[int]) -> str:
        """
        Cut `triplets` in dest_path.
        
        Arguments
        ---------
        triplets: list of tuples (IDX_PARENT, IDX_CHILD, OFFSET)
        dest_path: a path
        
        Returns
        -------
        A dictonary of destination data : {(IDX_PARENT, IDX_CHILD): OFFSET}
        """
        dest_map = self.copy(triplets, dest_path, notify=False)
        if dest_map is not None:
            keys = [(p, c) for p, c, o in triplets]
            #logger.info(f'dataset cut keys: {keys}')
            self.components.drop(index=keys, inplace=True)
            self.notify_changes(f'cut')
        return dest_map
        
    def drop(self, triplets: List[Tuple[int, int, int]])-> str:
        """
        drop `triplets`.
        
        Arguments
        ---------
        triplets: list of tuples (IDX_PARENT, IDX_CHILD, OFFSET)
        
        Returns
        -------
        List of sequences droped
        """
        def recursif_drop(node, idx_data, drop_seq):
            if node.idx not in idx_data: #drop seq
                drop_seq.append(node.idx)
                for child_node in node.children:
                    recursif_drop(child_node, idx_data, drop_seq)
                
        idx_roots = list(set(self.get_roots()) - set([TRASH]))
        tree_roots = self.get_descendants(idx_roots)
        idx_data = [x.idx for k, l in tree_roots.descendants.items() for x in list(l.keys())]
            
        idxs = list(set([c for p, c, o in triplets]))
        idxs_pairs = {c: (p, c) for p, c, o in triplets}
        tree = self.get_descendants(idxs)    
        drop_seq = []
        for node in tree.children:
            recursif_drop(node, idx_data, drop_seq)
        self.components.drop(index=set(idxs_pairs.values()), inplace=True)
        if len(drop_seq) > 0:
            self.components = self.components[~self.components.index.get_level_values(IDX_CHILD).isin(drop_seq)]
            self.sequences.drop(index=drop_seq, inplace=True)
        self.notify_changes(f'drop')
        return drop_seq

    def soft_drop(self, pairs: List[Tuple[int, int]]) -> str:
        """
        soft drop of `triplets` in trash set.
        
        Arguments
        ---------
        triplets: list of tuples (IDX_PARENT, IDX_CHILD, OFFSET)

        Returns
        -------
        A string with duplicate sequences erased in trash.
        """
        return self.cut(pairs, dest_path=[TRASH])
        
    def clean(self):
        """
        Remove data in `self.sequences` and `self.components` 
        """
        self.sequences = pd.DataFrame()
        self.components = pd.DataFrame()
        #self.notify_changes(f'clean')

    def append(self, dataset, verify_integrity=True, reindex=True):
        """
        Append a dataset to `self`. Warning use pd.concat with NA values.
        """
        if len(self.sequences) > 0:
            tmp = dataset.clone()
            if reindex:
                start = self.sequences.index.max() + 1
                tmp.reindex(start=start)
            with warnings.catch_warnings():
                # TODO: pandas 2.1.0 has a FutureWarning for concatenating DataFrames with Null entries
                warnings.filterwarnings("ignore", category=FutureWarning)
                keep = list(set(tmp.sequences.index[tmp.sequences.index < 0].to_list()) -
                             set(self.sequences.index[self.sequences.index < 0].to_list()))
                #print(keep)
                self.sequences = pd.concat([self.sequences, tmp.sequences.loc[tmp.sequences.index >= 0], tmp.sequences.loc[keep]], verify_integrity=verify_integrity)
                self.components = pd.concat([self.components, tmp.components], verify_integrity=verify_integrity)
        else:
            self.sequences = dataset.sequences.copy()
            self.components = dataset.components.copy()
        self.notify_changes(f'append')
              
    def reindex(self, start=0) -> int:
        """
        Reindex sequences from `start` to `start` + number of sequences. 
        Modifies IDX_CHILD and IXD_PARENT values in components.

        Returns
        -------
        the last IDX        
        """
        # Reindexing with contiguous index
        last = start + len(self.sequences.loc[self.sequences.index >= 0])
        new_index = list(range(start, last))
        # Create a mapping dictionary between old and new index
        index_mapping = dict(zip(self.sequences.index[self.sequences.index >= 0], new_index))
        # Use the dictionary to reindex
        tmp = self.components.rename(index=index_mapping, level=IDX_PARENT)
        self.components = tmp.rename(index=index_mapping, level=IDX_CHILD)
        self.sequences = self.sequences.rename(index=index_mapping, level=IDX)
        self.notify_changes(f'reindex')
        return last

    def get_roots(self):
        """
        Get IDX_CHILD roots of components and orphan IDX sequences

        Returns
        -------
        List of IDX        
        """
        root = ~self.sequences.index.isin(self.components.index.get_level_values(IDX_CHILD))
        idxs = self.sequences.index[root].unique().tolist() 
        return idxs

    def get_leafs(self) -> List[int]:
        """
        Get IDX_CHILD leafs of components 

        Returns
        -------
        List of IDX_CHILD        
        """
        leaf = ~self.components.index.get_level_values(IDX_CHILD).isin(self.components.index.get_level_values(IDX_PARENT))
        return self.components[leaf].index.get_level_values(IDX_CHILD).unique().tolist()

    def get_sequences(self, idxs: int | List[int]) -> pd.DataFrame:
        """
        Get sequences of `idxs`

        Returns
        -------
        A pandas DataFrame.        
        """
        return self.sequences.loc[self._idx_list(idxs), :]
    
    def get_components(self, pairs : Tuple[int, int] | List[Tuple[int, int]]) -> pd.DataFrame:
        """
        Get the  joint view of components and sequences of `pairs` (IDX_PARENT, IDX_CHILD)
        
        Returns
        -------
        A pandas DataFrame.        
        """
        comps = self.components.loc[pairs, :]
        return comps.join(self.sequences, on=IDX_CHILD, how='left')    

    def package_keys(self):
        return list(self._packages.keys())
    
    def set_package(self, key: str, value: List[Tuple[int, int]]):
        self._packages[key] = value
        self.param.trigger('notify_packages')

    def get_package(self, key: str) -> List[Tuple[int, int]]:
        if key not in self._packages:
            raise KeyError(f'DataSet.get_selections: {key} not in selections')
        return self._packages[key]

    def delete_package(self, key: str):
        if key not in self._packages:
            raise KeyError(f'DataSet.get_selections: {key} not in selections')
        del self._packages[key]
        self.param.trigger('notify_packages')
    
    def get_package_components(self, key: str) -> pd.DataFrame:
        """
        Return the selection (a joint view of components and sequences) stored in dictonary `self.selection`.        
        
        Arguments
        ---------
        key: name of the selection.
        
        Returns
        -------
        A pandas DataFrame.
        """        
        return self.get_components(self.get_package(key))

    def get_data(self, idxs: Union[int, List[int], None] = None, category: Union[str, None] = None, 
                 include_parent = True, max_depth: Union[int, None] = None) -> pd.DataFrame:
        """
        Create a joint view of components and sequences of `idxs` descendants.        
        
        Arguments
        ---------
        idxs: an `idx` or a list of `idx`.
        max_depth: if not `pd.NA`, limits the recursive loop to max_deep level.
        
        Returns
        -------
        A pandas DataFrame.
        """
        d = []
        if idxs is None:
            idxs = self.get_roots()
        idxs = self._idx_list(idxs)
        pairs = set()
        tree = self.get_descendants(idxs, max_depth=max_depth)        
        for node, offset in tree.filter(categories=category, max_depth=max_depth).items():
            idx_parent = node.parent.idx if  node.parent is not None else -1
            if (node.idx not in idxs) or include_parent:
                if (node.idx, idx_parent) not in pairs:
                    d.append({IDX_CHILD: node.idx, IDX_PARENT: idx_parent, OFFSET: offset})
                    pairs.add((node.idx, idx_parent))
            
        components = pd.DataFrame(d, columns=components_index+components_cols)
        components.set_index(components_index, inplace=True, verify_integrity=True)  
        return components.join(self.sequences, on=IDX_CHILD, how='left')

    def get_ascendants(self, idx: int, recursive=False, categories=[CHRONOLOGY, SET]):
        idx_parents = self.components.xs(idx, level=IDX_CHILD).index.to_list()
        #print('dataset get_ascendants', idx_parents)
        l = self.sequences.loc[idx_parents, CATEGORY].isin(categories).index.tolist() if len(idx_parents) > 0 else []
        #print('dataset get_ascendants parents', l)

        if recursive:
            for i in l:
                l += self.get_ascendants(i, recursive, categories)
        return l

    def get_descendants(self, idxs: int | List[int], max_depth=None) -> ComponentsTree():
        """
        Get descendants of `idxs`.
        
        Arguments
        ---------
        idxs: an `idx` or a list of `idx`.
        max_depth: if not `pd.NA`, limits the recursive loop to max_deep level.

        Returns
        -------
            A tree.
        """
        categories_keycodes = self.sequences.loc[:, [CATEGORY, KEYCODE]]
        data = self.components.join(categories_keycodes, on=IDX_CHILD, how='left')
        group_parents = data.groupby(IDX_PARENT)
        idx_depth = []

        def iterate(parent, idx, keycode, category, offset, depth, max_depth):
            if idx in idx_depth:
                raise KeyError(f'DataSet.get_descendants: circular reference: {idx} in {idx_depth}')
            idx_depth.append(idx)
            node = ComponentsNode(parent, idx, keycode, category, offset, depth=depth)
            if (idx in group_parents.groups) and (category != TREE) and ((max_depth is None) or (depth+1 <= max_depth)):
                for (_, idx_child), row in group_parents.get_group(idx).iterrows():
                    #offset = row[OFFSET] if pd.notna(row[OFFSET]) else 0
                    child = iterate(node, idx_child, row[KEYCODE], row[CATEGORY], row[OFFSET], depth+1, max_depth)
                    node.append(child)
            idx_depth.pop()
            return node
        tree = ComponentsTree()
        for idx in self._idx_list(idxs):
            child = iterate(tree, idx, categories_keycodes.at[idx, KEYCODE], categories_keycodes.at[idx, CATEGORY], 0, 0, max_depth)
            tree.append(child)
        return tree

    def edit_component(self, idx_parent, idx_child, value):
        idxs = [(idx_parent, idx_child)]
        self.freeze_components(idxs)
        self.components.at[(idx_parent, idx_child), OFFSET] = np.round(value)

        self.log_components(idxs, 'edit_component')
        if self.save_auto:
            print('*** Save auto ***')
            self.dump()


    def edit_sequence(self, idxs, data):
        for column, value in data.items():
            print(column, value)
            if dtype_view[column].lower().startswith('int'):
                value = np.round(value) if pd.notna(value) else pd.NA
            elif dtype_view[column].lower().startswith('float'):
                if pd.isna(value):
                    value = pd.NA   
            elif dtype_view[column].lower().startswith('boolean'):
                if isinstance(value, str):
                    if value.lower() == 'true':
                        value = True
                    elif value.lower() == 'false':
                        value = False
                    else:
                        value = pd.NA
            print(column, value)
            
            idxs = self._idx_list(idxs)        
            self.freeze_sequences(idxs)
            if isinstance(value, object):
                for idx in idxs:
                    self.sequences.at[idx, column] = value        
            else:
                self.sequences.loc[idxs, column] = value        
           
            self.log_sequences(idxs, 'edit_sequence')
        if self.save_auto:
            print('*** Save auto ***')
            self.dump()
    
    # def edit_sequence(self, idxs, column, value):
    #     if dtype_view[column].lower().startswith('int'):
    #         value = np.round(value) if pd.notna(new) else pd.NA
    #     elif dtype_view[column].lower().startswith('float'):
    #         if pd.isna(value):
    #             value = pd.NA   
    #     elif dtype_view[column].lower().startswith('boolean'):
    #         if isinstance(value, str):
    #             if value.lower() == 'true':
    #                 value = True
    #             elif value.lower() == 'false':
    #                 value = False
    #             else:
    #                 value = pd.NA
        
    #     idxs = self._idx_list(idxs)        
        
    #     self.freeze_sequences(idxs)
    #     self.sequences.loc[idxs, column] = value        
    #     self.log_sequences(idxs, 'edit_sequence')
    #     if self.save_auto:
    #         print('*** Save auto ***')
    #         self.dump()

    def shift_offsets(self, parent_idx):
        """
        Get children of `parent_idx` and shift the children offsets to 0.
        """
        data = self.get_data(parent_idx, max_depth=1, include_parent=False)
        if data[OFFSET].isna().any():
            raise ValueError(f'DataSet.shift_offsets: one or more ({IDX_PARENT}, {IDX_CHILD}) contain NA values in {OFFSET} field.')
        self.freeze_components(data.index.to_list())
        self.components.loc[data.index.to_list(), OFFSET] -= data[OFFSET].min()
        self.log_components(data.index.to_list(), 'shift_offsets')

    def copy_dates_to_offsets(self, parent_idx):
        """
        Get children of `parent_idx`, copy dates to offsets and shift to 0 (if `shift` is True).
        """
        data = self.get_data(parent_idx, max_depth=1, include_parent=False)
        if data[DATE_BEGIN].isna().any():
            logger.warning(f'one or more ({IDX_PARENT}, {IDX_CHILD}) contain NA values in {DATE_BEGIN} field.')
        idxs = data.index.to_list()
        self.freeze_components(idxs)
        self.components.loc[idxs, OFFSET] = data.loc[idxs, DATE_BEGIN]
        self.log_components(idxs, 'copy_dates_to_offsets')

    def set_offsets_to_dates(self, parent_idx):
        """
        Get children of `parent_idx`, copy dates to offsets and shift to 0 (if `shift` is True).
        """
        data = self.get_data(parent_idx, max_depth=1, include_parent=False)
        if data[OFFSET].isna().any():
            raise ValueError(f'DataSet.set_offsets_to_dates: one or more ({IDX_PARENT}, {IDX_CHILD}) contain NA values in {OFFSET} field.')
        min_offset = data[OFFSET].min()
        min_date = data.at[(data[OFFSET] == min_offset).idxmax(), DATE_BEGIN]
        if pd.isna(min_date):
            raise ValueError(f'DataSet.set_offsets_to_dates: {DATE_BEGIN} corresponding to min {OFFSET} contains NA value.')
        data[OFFSET] -= min_offset
        idxs = data.index.get_level_values(IDX_CHILD).to_list()
        self.freeze_sequences(idxs)
        self.sequences.loc[idxs, DATE_BEGIN] =  data.reset_index().set_index(IDX_CHILD)[OFFSET] + min_date
        self.sequences.loc[idxs, DATE_END] = self.sequences.loc[idxs, DATE_BEGIN] + self.sequences.loc[idxs, DATA_LENGTH]         
        self.log_sequences(idxs, 'set_offsets_to_dates')

    def check_ring_count(self, parent_idx):
        def length_(values):
            l = len(values) if values is not None else 0
            logger.debug(f'{l}, {values}')
            return l
        data = self.get_data(parent_idx, max_depth=1, include_parent=False)
        ring_count = data[DATA_VALUES].apply(lambda x: length_(x))
        if ring_count != data[DATA_LENGTH]:
            raise ValueError(f'{DATA_LENGTH} not match length of {DATA_VALUES}.')

    def check_date_ring_count(self, parent_idx):
        self.check_ring_count(parent_idx)
        data = self.get_data(parent_idx, max_depth=1, include_parent=False)
        min_date = data[DATE_BEGIN].min()
        data[DATE_BEGIN] -= min_date        
        data[DATE_END] -= min_date
        if (data[DATE_END] - data[DATE_BEGIN]) != + data[DATA_LENGTH]:
            raise ValueError(f'DataSet.check_date_ring_count: {DATE_BEGIN} - {DATE_BEGIN} and {DATA_LENGTH} are not consistent.')
    
    def check_offset_begin_date(self, parent_idx):        
        data = self.get_data(parent_idx, max_depth=1, include_parent=False)
        data[OFFSET] -= data[OFFSET].min()
        min_date = data[DATE_BEGIN].min()
        data[DATE_BEGIN] -= min_date        
        if data[OFFSET] != data[DATE_BEGIN]:
            raise ValueError(f'DataSet.check_offset_begin_date: {DATE_BEGIN} and {OFFSET} are not consistent.')
        
    def check_date_offset_count(self, parent_idx):
        self.check_date_ring_count(parent_idx)
        self.check_offset_begin_date(parent_idx)

    def set_dates(self, idx, date_begin, data_lenght=None, sequences=None, warning=True):
        """
        Set DATE_END and DATE_BEGIN (if not NA) of `idx` serie given a `date_begin` 
        and a `ring_count`.
        """    
        if sequences is None:
            sequences = self.sequences
        if pd.notna(date_begin):
            keycode = sequences.at[idx, KEYCODE]
            date_first = sequences.at[idx, DATE_BEGIN]
            if pd.notna(date_first) and (date_begin != date_first) and (warning):
                logger.warning(f'potentiel inconsistent chronology, {keycode} {DATE_BEGIN} changed: {date_begin} ')
            if data_lenght is None:
                data_lenght = sequences.at[idx, DATA_LENGTH]
            else:
                sequences.at[idx, DATA_LENGTH] = data_lenght
            sequences.at[idx, DATE_BEGIN] = date_begin                
            sequences.at[idx, DATE_END] = date_begin + data_lenght         
    
    def set_chononology_info(self, idx, means, weights, offsets, data_type, data_samples, sequences=None):
        if sequences is None:
            sequences = self.sequences
        self.freeze_sequences(idx)
        sequences.at[idx, DATA_VALUES] = means
        sequences.at[idx, DATA_TYPE] = data_type
        sequences.at[idx, DATA_LENGTH] = len(means)
        sequences.at[idx, DATA_WEIGHTS] = weights
        sequences.at[idx, DATA_INFO] = offsets
        sequences.at[idx, DATE_SAMPLING] = datetime.now()
        sequences.at[idx, INCONSISTENT] = False
        
        sequences.at[idx, CATEGORY] = CHRONOLOGY
        for key in [SITE_ELEVATION, SITE_CODE, SITE_LATITUDE, SITE_LONGITUDE, SPECIES, LABORATORY_CODE, PROJECT, URI]: 
            l = data_samples[key].unique()
            if len(l) == 1:
                sequences.at[idx, key] = l[0]
        date_min = data_samples[DATE_BEGIN].min()
        self.set_dates(idx, date_min, len(means))
        
        self.log_sequences(idx, 'Chronology update')
    
    def chronologies(self, idxs, date_as_offset=False, biweight=False, num_threads=1):
        #print('1 chronologies tree', num_threads)
        tree = self.get_descendants(idxs)
        #print('2 chronologies filter')
        node_chronologies = tree.filter(categories=[CHRONOLOGY, SET], max_depth=1) 
        idx_chronologies = []
        data_dict = {}
        #print('3 chronologies data')
        for node in node_chronologies:
            idx = node.idx
            if idx in idxs: # Need in the return
                if (idx not in idx_chronologies):  # Never computed 
                    idx_chronologies.append(idx)
                    samples = {node.idx: offset for node, offset in node.descendants[TREE].items()}
                    dt_data = self.get_sequences(list(samples.keys())).copy()
                    dt_data[OFFSET] = list(samples.values())
                    data_dict[idx] = dt_data
        #print('4 chronologies chronologies')
        results = chronologies(data_dict, ring_type=RAW, date_as_offset=date_as_offset, biweight=biweight, num_threads=num_threads)
        #print('5 chronologies results')
        for idx, values in results.items():
            means, weights, offsets = values
            #seq = self.get_sequences(idx).copy()
            self.set_chononology_info(idx, means, weights, offsets, RAW, data_dict[idx], sequences=None)
        
        if self.save_auto:
            print('*** Save auto ***')
            self.dump()


    def detrend(self, idxs, ring_type, window_size=5, do_log=False, date_as_offset=False, biweight=False, num_threads=1):
        tree = self.get_descendants(idxs)
        if TREE in tree.descendants:
            idxs_samples = list(set([node.idx for node in tree.descendants[TREE].keys()]))
            data_samples = self.get_sequences(idxs_samples)
            dt_samples = detrend(data_samples, ring_type, window_size=window_size, do_log=do_log, num_threads=num_threads)
        dt_chonology = []
        if CHRONOLOGY in tree.descendants:
            node_chronologies = tree.filter(categories=[CHRONOLOGY], max_depth=1)
            idx_chronologies = []
            data_dict = {}
            for node in node_chronologies:
                idx = node.idx
                if idx in idxs: # Need in the return
                    if (idx not in idx_chronologies):  # Never computed 
                        idx_chronologies.append(idx)
                        samples = {node.idx: offset for node, offset in node.descendants[TREE].items()}
                        dt_data = dt_samples.loc[list(samples.keys()), :]
                        dt_data[OFFSET] = list(samples.values())
                        data_dict[idx] = dt_data
            results = chronologies(data_dict, ring_type=ring_type, date_as_offset=date_as_offset, biweight=biweight, num_threads=num_threads)
            for idx, values in results.items():
                means, weights, offsets = values
                seq = self.get_sequences(idx).copy()
                self.set_chononology_info(idx, means, weights, offsets, ring_type, data_dict[idx], sequences=seq)
                dt_chonology.append(seq)
        with warnings.catch_warnings():
            # TODO: pandas 2.1.0 has a FutureWarning for concatenating DataFrames with Null entries
            warnings.filterwarnings("ignore", category=FutureWarning)
            data_dt = pd.concat([dt_samples]+dt_chonology)
        return data_dt.loc[idxs, :]

    def check(self, idx):
        def check_children(node):
            children = node.get_children()
            idx_children = [node.idx for node in children.keys()]
            category_children = [node.category for node in children.keys()]
            offsets = pd.Series([offset for offset in children.values()], index=idx_children)
            offset_nonan = offsets.notna()
            noffset = offset_nonan.sum()
            offsets_norm = offsets - offsets.min()
            keycodes = self.sequences.loc[idx_children, KEYCODE]
            dates = self.sequences.loc[idx_children, DATE_BEGIN]
            date_nonan = dates.notna()
            dates_norm = dates - dates.min()
            ndate = date_nonan.sum()
            norm = dates_norm.max()+offsets_norm.max()
            diff =  dates_norm.fillna(norm) != offsets_norm.fillna(norm) 
            equal =  dates_norm.fillna(norm) == offsets_norm.fillna(norm) 
            ndiff = diff.sum()
            if node.category == CHRONOLOGY:
                if (ndiff == 0) and (ndate == len(dates)) and (noffset == len(offsets)): 
                    if SET not in category_children:
                        msg = '1: dates and offsets are consistent.'
                    else:
                        msg = '-1: dates and offsets are consistent. But some children are "set".'
                elif (ndate == len(dates)) and (noffset == 0):
                    # all dates, no offset
                    if SET not in category_children:
                        msg = '2: dates are available, no offsets. Offsets update required.'
                    else:
                        msg = '-2: dates are available, no offsets. Offsets update required. But some children are "set".'
                elif (noffset == len(offsets)) and (ndate == 0):
                    # all offsets, no date
                    msg = '3: offsets are available, no dates. Undated serie.'
                elif (noffset == len(offsets)) and (equal[dates != pd.NA].sum() == ndate):
                    # all offsets, subset of dates and offsets consistent
                    if SET not in category_children:
                        msg = '4: offsets are available, some empty dates. subset of dates and offsets are consistent. Years update required.'
                    else:
                        msg = '-4: offsets are available, some empty dates. But some children are "set".'
                elif (ndate == len(dates)) and (equal[offsets != pd.NA].sum() == noffset):
                    # all offsets, subset of dates and offsets consistent
                    if SET not in category_children:
                        msg = '5: Years are available, some empty offsets. subset of dates and offsets are consistent. Offsets update required.'
                    else:
                        msg = '-5: Years are available, some empty offset. But some children are "set".'
                else:
                    if SET not in category_children:
                        msg = '-6: Years and offsets are unconsistent. Undated serie. '
                    else:
                        msg = f'-7: Contain {SET}, dates and offsets are unconsistent. Undated serie.'
            else:
                msg = f'-7: Years and offsets are unconsistent. Parent is not a {CHRONOLOGY}. Correction required'
            
            info = [(node.idx, self.sequences.at[node.idx, KEYCODE], self.sequences.at[node.idx, CATEGORY],
                          self.sequences.at[node.idx, DATE_BEGIN],  pd.NA,  pd.NA , pd.NA, pd.NA)]
            info += zip(idx_children, keycodes.to_list(), category_children, dates.tolist(), offsets.tolist(), 
                        dates_norm.tolist(), offsets_norm.tolist(), equal)            
            df = pd.DataFrame(info, columns=[IDX, KEYCODE, CATEGORY, DATE_BEGIN, OFFSET, DATE_BEGIN_NORM, OFFSET_NORM, 'date ~ offset'])          
            return (msg, df)
        
        def get(node):
            out[node.idx] = check_children(node)
            for child_node in node.children:
                if child_node.category != TREE:
                    get(child_node)
        out = {}
        tree = self.get_descendants(idx)
        for child_node in tree.children:
            get(child_node)        
        return out

    def statistics(self, data=None):
        stats_lst = []
        if data is None:
            data = self.sequences
        for idx, row in data.iterrows():
            stats = {
                IDX: idx,
                KEYCODE: row[KEYCODE],
                DATE_BEGIN: row[DATE_BEGIN],
                DATE_END: row[DATE_END],
                DATA_LENGTH: row[DATA_LENGTH],
            }
            stat2 = {}
            if pd.notna(row[DATA_LENGTH]) and (row[DATA_LENGTH] > 0):
                values = row[DATA_VALUES]
                ring_NAN = np.sum(np.isnan(values))
                values = values[~np.isnan(values)]
                stats2 = {
                    RING_NAN: ring_NAN,
                    STAT_MEAN: np.mean(values),
                    STAT_MEDIAN: np.median(values),
                    #STAT_MODE: mode(values).mode[0],
                    STAT_STD: np.std(values),
                    #STAT_VAR: np.var(values),
                    STAT_MIN: np.min(values),
                    STAT_MAX: np.max(values),
                    STAT_PERC35: np.percentile(values, 25),
                    STAT_PERC50: np.percentile(values, 50),
                    STAT_PERC75: np.percentile(values, 75),
                    STAT_SUM: np.sum(values),
                    STAT_KURTOSIS: kurtosis(values),
                    STAT_SKEWNESS: skew(values),
                    STAT_ENTROPY: entropy(values)
                }
            stats_lst.append(stats | stats2)
        return pd.DataFrame(stats_lst)

    def get_keycodes(self, idxs, fields=None):
        """
        Generate unique keycodes for each element stored in attributes of the Sequences DataFrame.

        Returns:
            A dictionary containing the keycodes as keys and their corresponding values.
        """
        cols = [KEYCODE, PROJECT]
        if fields is not None:
            cols += fields
        data = self.sequences.loc[idxs, cols]
        if fields == None:
            if len(data) == len(data[KEYCODE].unique()):
                return {x:y for x, y in zip(data.index, data[KEYCODE])}
            if len(data) == len(data[[PROJECT, KEYCODE]].drop_duplicates()):
                return {x:f'{x}/{y}/{z}' for x, y, z in zip(data.index, data[PROJECT], data[KEYCODE])}
            return {x:f'{x}/{y}' for x, y in zip(data.index, data[KEYCODE])}
        else:
            return {x:f'{x}/{y}' for x, y in zip(data.index, data[fields])}

