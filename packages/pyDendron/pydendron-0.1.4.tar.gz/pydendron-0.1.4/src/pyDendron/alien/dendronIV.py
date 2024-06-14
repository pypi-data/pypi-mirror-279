import glob
import logging
import copy
import re
from lxml import etree as ET
import numpy as np
import pandas as pd
import pickle

from pyDendron.tools.location import reverse_geocode, get_elevation
from pyDendron.dataset import Dataset
from pyDendron.app_logger import logger
from pyDendron.dataname import *
from pathlib import Path

class DendronIV:

    
    def __init__(self, glob_str=None, source=None, laboratories=None, places='reverse_places.p', get_place=True, get_altitude=True):
        self.glob_str = glob_str
        self.uri = None
        self.filename = None
        self.source = source
        self.idx = 0
        self.idxs = {}
        self.sequences = []
        self.components = []
        self.get_place = get_place
        self.get_altitude = get_altitude
        self.places = {}
        self.elevations = {}
        self.laboratories = laboratories
        self.places_fn = places
        self.projects = {}
        
        self._readall()
            
    def _read_places(self):
        if (self.places_fn is not None) and Path(self.places_fn).exists():
            with open(self.places_fn , 'rb') as fic:
                self.places, self.elevations = pickle.load(fic)

    def _write_places(self):
        with open(self.places_fn , 'wb') as fic:
            pickle.dump([self.places, self.elevations], fic)
         
    def _readall(self):
        self._read_places()
        
        lst = [x for x in glob.glob(self.glob_str)]
        card_dict = {}
        seqs = {}
        for i, self.filename in enumerate(lst):
            #print(np.round((i/len(lst))*100, 2), self.filename)
            self.uri = Path(self.filename).resolve().as_uri()
            if (i % 25) == 0:
                logger.debug('_write_places')
                self._write_places()
            with open(self.filename, 'r', encoding='ISO-8859-1') as file:
                    data = file.read()
                    data = data.replace('&', '&amp;')
                    #logging.info('='*5 + self.filename + '='*5)
                    root = ET.fromstring(data)
                    #root = tree.getroot()
                    card_dict.update(self.read_begin_table(root))
                    seqs.update(self._read_cards(root, card_dict))
        
        diff =  set(card_dict.values()) - set(seqs.keys())
        if len(diff) > 0:
            logging.warning(f'\t missing sequences  {diff}')
            
        self.sequences = list(seqs.values())
        self.components = self.get_components(seqs, card_dict)
        self._write_places()
                    
    def get_components(self, seqs, card_dict):
        components = []
        for idx_parent in seqs:
            meta = seqs[idx_parent]
            if CATEGORY not in meta:
                logging.warning(f'\t undefined category for {meta[KEYCODE]}')
            elif (meta[CATEGORY] != TREE) and ('comps' in meta):
                tmp = []
                for comp in meta['comps']:
                    if comp in card_dict:
                        idx_child = card_dict[comp]
                        if idx_child != idx_parent:
                            if idx_child not in seqs:
                                logging.warning(f'\t remove missing sequences {idx_child} in {idx_parent}')
                            else:
                                offset = 0
                                if DATE_BEGIN in seqs[idx_child]:
                                    offset = seqs[idx_child][DATE_BEGIN]
                                    if pd.notna(offset) and (offset > 3000):
                                        ('Offset', offset)
                                        offset -= 3000
                                        seqs[idx_child][DATE_BEGIN] = pd.NA
                                        seqs[idx_child][DATE_END] = pd.NA
                                        
                                tmp.append({IDX_PARENT:idx_parent, IDX_CHILD:idx_child, OFFSET:offset})
                if len(tmp) == 0:
                    logging.warning(f"empty set {idx_parent} {meta[KEYCODE]} ({meta[CATEGORY]})")
                components += tmp
        return components                            

    def read_begin_table(self, root):
        card_dict = {}
        data = root.find('FirstTable/text').text
        for line in data.split('\n'):
            line = line.strip()
            fields = line.split()
            if (len(fields) == 4) and (fields[3] == 'Ok'):
                if fields[0] in card_dict:
                    logging.warning(f'\t duplicate card: {fields[0]}')
                card_dict[fields[0]] = self.idx
                self.idx += 1
        #print('card_dict', card_dict)
        return card_dict
    
    def _add_project(self, seqs, card_dict):
        fn = Path(self.filename)
        project = fn.parent.name
        
        if project in self.projects:
            return project, self.projects[project]['comps']
        else:
            file_idx = self.idx
            meta = {IDX: file_idx, 
                    KEYCODE: project, 
                    PROJECT: project, 
                    #URI: self.filename,
                    CATEGORY: SET,
                    'comps': {} 
                    }
            seqs[file_idx] = meta
            card_dict[file_idx] = file_idx
            self.idx += 1
            self.projects[project] = meta
            return project, meta['comps']
      
    def _read_cards(self, root, card_dict):
        seqs = {}
        project, comps = self._add_project(seqs, card_dict)
        
        for card in root.findall("Card"):
            meta, key = self._read_card(card, card_dict)
            #print('meta', meta)
            if meta is not None:
                if meta[IDX] in seqs:
                    logging.warning(f'\t duplicate sequences: {key} / {meta[KEYCODE]}')
                else:
                    meta[PROJECT] = project
                    meta[URI] = self.filename
                    seqs[meta[IDX]] = meta
                    comps[meta['cardName']] = 'head'
        return seqs

    def _read_card(self, card, card_dict):
            #print("-"*10)
            meta = {}
            card_name = card.find('name').text.strip()
            if card_name == '000_A':
                return None, None
            if card_name not in card_dict:
                logging.warning(f'\t Card not in list {card_name}')
                return None, None
            meta['cardName'] = card_name
            user_name = card.find('userName').text.strip()
            meta[IDX] = card_dict[card_name]
            meta[KEYCODE] = user_name
            for field in card.findall("field"):
                self._read_field(field, meta)
            #yl = yf =''
            #if DATE_END in meta:
            #    yl = meta[DATE_END]
            #if DATE_BEGIN in meta:
            #    yf = meta[DATE_BEGIN]
            #print(card_name, user_name, meta[IDX], meta[CATEGORY], yf, yl)
            return meta, card_name        
    
    def _read_field(self, field, meta):
        def _read_category():
            if text.startswith('indiv'):
                meta[CATEGORY] = TREE
            elif text.startswith('group'):
                meta[CATEGORY] = SET
            else:
                logging.warning(f'\t Unknown card type |{text}| {name}')
                meta[CATEGORY] = TREE

        def _read_values():
            values = []
            for line in text.split('\n'):
                line = line.strip()
                if line != '':
                    try:
                        values.append(float(line))
                    except :
                        logging.warning(f'\t* values error: |{line}|')
                else:
                    values.append(np.nan)

            if len(values) > 0:
                meta[DATA_VALUES] = np.array(values)
                meta[DATA_LENGTH] = len(values)
                meta[DATA_TYPE] = RAW
                if (CATEGORY in meta) and (meta[CATEGORY] == SET):
                    meta[CATEGORY] = CHRONOLOGY

        def _read_location():
            f = text.split()
            meta[SITE_LATITUDE] = float(f[1])
            meta[SITE_LONGITUDE] = float(f[0])
            meta[SITE_ELEVATION] = pd.NA
            meta[SITE_CODE] = ''
            #meta[SITE_COUNTRY] = meta[SITE_STATE] = meta[SITE_DISTRICT] = meta[SITE_TOWN] = meta[SITE_ZIP] = ''
            if self.get_place:
                _, __, ___, ____, _____, meta[SITE_CODE] = reverse_geocode(meta[SITE_LATITUDE], meta[SITE_LONGITUDE], self.places)
            if self.get_altitude: 
                meta[SITE_ELEVATION] = get_elevation(meta[SITE_LATITUDE], meta[SITE_LONGITUDE], self.elevations)
        
        def _read_working_list():
            f = text.split()
            comps = {}
            for line in text.split('\n'):
                line = line.strip()
                f = line.split()
                if len(f) == 5:
                    comps[f[1]] = f
            meta['comps'] = comps
          
        name = field.find('name').text.strip()
        text = field.find('text').text.strip()

        if name == 'card type':
            _read_category()
        elif name == 'i_01':
            _read_values()
        elif name =='sample':
            v = text.split('\n')
            if len(v) > 3:
                if v[0] == '1':
                    meta[PITH] = True
                i = re.search(r'\d+', v[1])
                if i:
                    meta[SAPWOOD] = int(i.group()) - 1
                if v[2] == '1':
                    meta[CAMBIUM] = True
        elif (name == 'material') and (text != ''):
            meta[SUBCATEGORY] = text
        elif (name == 'creation date') and (text != ''):
            try:
                meta[CREATION_DATE] = pd.to_datetime(text, format="%Y%m%d")
            except :
                meta[CREATION_DATE] = ''
        elif (name == 'start date') and (text != ''):
            meta[DATE_BEGIN] = float(text)
        elif (name == 'stop date') and (text != ''):
            meta[DATE_END] = float(text)
        elif (name == 'location') and (text != ''):
            _read_location()
        elif (name == 'tree type') and (text != ''):
            meta[SPECIES] = text
        elif name == 'working list':
            _read_working_list()
        elif name == 'waiting list':
            if text != '':
                meta[DATA_INFO] = text
        elif name == 'comments':
            if text != '':
                meta[COMMENTS] = text
        elif name == 'labs authors':
            if text != '':
                meta[LABORATORY_CODE] = text
        elif name == 'people authors':
            if text != '':
                meta[PERS_ID] = text
        elif name == 'references':
            if text != '':
                meta[BIBLIOGRAPHY_CODE] = text
        elif name == 'source file':
            if text != '':
                meta[URI] = text
                
        #elif name == 'building date':
        #    if text != '':
        #        meta[CREATION_DATE] = text
                    
    def to_dataset(self, root_keycode='Dataset', root_idx=ROOT, trash_keycode='Trash', clipboard_keycode='Clipboard'):

        self.dataset = Dataset(sequences=self.sequences, components=self.components, save_auto=False)

        for k, t in sequences_dtype_dict.items():
            if k not in self.dataset.sequences.columns:
                self.dataset.sequences[k] = ''
            if t == 'string':
                self.dataset.sequences[k] = self.dataset.sequences[k].fillna('')
        
        self.dataset.sequences[SPECIES] = self.dataset.sequences[SPECIES].str.upper()
        mask = self.dataset.sequences[SPECIES].str.startswith('QU')
        self.dataset.sequences.loc[mask, SPECIES] = 'QU'

        
        logger.info(f'to_dataset roots: {self.dataset.get_roots()}')
        self.dataset.new_root(root_keycode, root_idx)
        self.dataset.new_clipboard(clipboard_keycode)
        self.dataset.new_trash(trash_keycode)
        
        return self.dataset
    
    def compact(self, drop=False):
        # remove duplicate samples in the tree. Keep deeper nodes
        # parent categories is set to SET dans RING_* are set empty
        def iterate(node):
            #print('dup:', node.detect_duplicates(category=TREE, raise_error=False))
            dup = [ x for (x, y) in node.detect_duplicates(category=TREE, raise_error=False)]
            for child in node.children:
                if child.category != TREE:
                    iterate(child)
                else:
                    if child.idx in dup:
                        remove_list.append((node.idx, child.idx))
                        chronology_idx_list.append(node.idx)
                
        tree = self.dataset.get_descendants(self.dataset.get_roots())
        remove_list = []
        chronology_idx_list = []
        iterate(tree)
        
        if drop:
            self.dataset.components.drop(remove_list, inplace=True)
            mask = self.dataset.sequences.index.isin(set(chronology_idx_list))
            cols = [CATEGORY, DATA_LENGTH, DATA_INFO, RING_NAN, DATA_TYPE, DATA_WEIGHTS, DATA_VALUES]
            self.dataset.sequences.loc[mask, cols] = SET, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA 

        return self.dataset   
                
