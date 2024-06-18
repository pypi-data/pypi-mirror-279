
import glob
#import xml.etree.ElementTree as ET
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

class Tridas:
    def __init__(self, glob_str=None, places='reverse_places.p', source=None, get_place=True, get_altitude=True):
        self.glob_str = glob_str
        self.uri = None
        self.source = source
        self.laboratories = 'empty'
        self.idx = 0
        self.sequences = []
        self.components = []
        self.tree = None
        self.idx_chronologies = None
        self.meta_chronologies = None
        self.idx_projects = None
        self.meta_projects = None
        self.get_place = get_place
        self.get_altitude = get_altitude
        self.namespaces = {}
        self.identifier = {}
        self.places = {}
        self.elevations = {}
        self.places_fn = places
        self.dataset = None
            
    def _read_places(self):
        if (self.places_fn is not None) and Path(self.places_fn).exists():
            #print('read places')
            with open(self.places_fn , 'rb') as fic:
                self.places, self.elevations = pickle.load(fic)

    def _write_places(self):
        with open(self.places_fn , 'wb') as fic:
            pickle.dump([self.places, self.elevations], fic)
        
    def add_component(self, idx_parent, idx_child, offset=np.nan):
        self.components.append({IDX_PARENT: idx_parent, IDX_CHILD: idx_child, OFFSET: offset})
    
    #def add_raw_indices(self, idx, values):
    #    self.indices.append({IDX: idx, 'key': Indices.RAW, 'values': values, 'count': len(values)})

    def _init_metadata(self, category, category_tridas, parent_meta=None):
        meta = {}
        if parent_meta is not None:
            meta = copy.deepcopy(parent_meta)
        #meta[SOURCE] = self.source
        #meta[LABs] = self.laboratories
        #meta[URI] = self.uri
        meta[IDX] = self.idx
        meta[CATEGORY] = category
        meta[SUBCATEGORY] = category_tridas
        #meta[SAPWOOD] = pd.NA
        #meta[PITH] = pd.NA
        #meta[CAMBIUM] = pd.NA
        #meta[BARK] = pd.NA
        
        self.idx += 1
        return meta, self.idx -1

    def _new_metadata(self, node, parent_meta, category=SET, category_tridas='unk'):
            idx_parent = parent_meta[IDX]
            meta, idx = self._init_metadata(category, category_tridas, parent_meta)
            self._add_keycode(meta, node)
            self.sequences.append(meta)
            self.add_component(idx_parent, idx)
            return meta, idx
    
    def _set_laboratories(self, project):
        self.laboratories = '' 
        for lab in project.findall('tridas:laboratory/tridas:name', self.namespaces):
            if 'acronym' in lab.attrib:
                self.laboratories += lab.attrib['acronym'] + ', '
            else:
                self.laboratories += lab.text + ', '
        self.laboratories = re.sub(', $', '', self.laboratories)

    def _add_keycode(self, meta, node):
        meta[KEYCODE] = node.find('tridas:title', self.namespaces).text
        self._set_identifier(meta, node)

    def _set_identifier(self, meta, node):
        key = self._get_identifier(node)
        self.identifier[key] = meta

    def _get_identifier(self, node):
        _id = node.find('tridas:identifier', self.namespaces)
        if _id is not None:
            domain = self.laboratories
            if 'domain' in _id.attrib:
                domain = _id.attrib['domain']
            if _id.text is None:
                return domain + '// warning empty text'
            return domain + '//' + _id.text
        return None

    def _add_taxon(self, meta, node):
        if node.find('tridas:taxon', self.namespaces) is not None:
            meta[SPECIES] = node.find('tridas:taxon', self.namespaces).text
        
    def _add_location(self, meta, node):
        d = {}
        if node.find('tridas:location/tridas:locationGeometry/gml:Point/gml:pos', self.namespaces) is not None:
            (longitude, latitude) = node.find('tridas:location/tridas:locationGeometry/gml:Point/gml:pos', self.namespaces).text.split(' ')
            latitude, longitude = float(latitude), float(longitude)
            meta[SITE_LATITUDE] = latitude
            meta[SITE_LONGITUDE] = longitude
            if not((latitude < 72) and (latitude > 36) and (longitude > -9.5) and (longitude < 28)):
                 if (longitude < 72) and (longitude > 36) and (latitude > -9.5) and (latitude < 28):
                     latitude, longitude = longitude, latitude
                     #logger.warning(f'location not in europe, invert longitude and lattitude: {latitude}, {longitude}')
                 else:
                     logger.warning(f'location not in europe: {latitude}, {longitude}')
            meta[SITE_COUNTRY] = meta[SITE_STATE] = meta[SITE_DISTRICT] = meta[SITE_TOWN] = meta[SITE_ZIP] = ''
            meta[SITE_ELEVATION] = np.nan
            if self.get_place:
                _, __, ___, ____, _____, meta[SITE_CODE] = reverse_geocode(meta[SITE_LATITUDE], meta[SITE_LONGITUDE], self.places)
#                meta[SITE_COUNTRY], meta[SITE_STATE], meta[SITE_DISTRICT], meta[SITE_TOWN], meta[SITE_ZIP] = reverse_geocode(latitude, longitude, self.places)
            if self.get_altitude:
                meta[SITE_ELEVATION] = get_elevation(meta[SITE_LATITUDE], meta[SITE_LONGITUDE], self.elevations)
#               meta[SITE_ELEVATION] = get_elevation(latitude, longitude, self.elevations)
        
    def presence_of(self, node, key, warning=True):
        keycode = node.find('tridas:title', self.namespaces).text

        if node.find(key, self.namespaces) is not None:
            if warning:
                logger.warning(f'{key} id present but not read in {keycode}')
            return True
        return False
    
    def _presence_of_wood_attribut(self, node):
        if 'presence' in node.attrib:
            if node.attrib['presence'] in ['incomplete', 'complete', 'present']:
                return True
        return False
       
    def _read_wood_completeness(self, meta, node):
        
        info_wood = node.find('tridas:woodCompleteness', self.namespaces)
        if info_wood is not None:
            if info_wood.find('tridas:ringCount', self.namespaces) is not None:
                meta[DATA_LENGTH] = int(info_wood.find('tridas:ringCount', self.namespaces).text)
            if info_wood.find('tridas:pith', self.namespaces) is not None:
                meta[PITH] = self._presence_of_wood_attribut(info_wood.find('tridas:pith', self.namespaces))
            if info_wood.find('tridas:nrOfUnmeasuredInnerRings', self.namespaces) is not None:
                meta[PITH_OPTIMUM] = int(info_wood.find('tridas:nrOfUnmeasuredInnerRings', self.namespaces).text)
                #heartwood = self._presence_of_wood_attribut(info_wood.find('tridas:heartwood', ns))
            #if info_wood.find('tridas:sapwood', self.namespaces) is not None:
            #    meta[SAPWOOD] = self._presence_of_wood_attribut(info_wood.find('tridas:sapwood', self.namespaces))
            if info_wood.find('tridas:sapwood/tridas:nrOfSapwoodRings', self.namespaces) is not None:
                meta[SAPWOOD] = meta[DATA_LENGTH] - int(info_wood.find('tridas:sapwood/tridas:nrOfSapwoodRings', self.namespaces).text)
            if info_wood.find('tridas:sapwood/tridas:lastRingUnderBark', self.namespaces) is not None:
                meta[CAMBIUM_SEASON] = self._presence_of_wood_attribut(info_wood.find('tridas:sapwood/tridas:lastRingUnderBark', self.namespaces))
            if info_wood.find('tridas:sapwood/tridas:missingSapwoodRingsToBark', self.namespaces) is not None:
                meta[CAMBIUM_OPTIMUM] = meta[DATA_LENGTH] + int(info_wood.find('tridas:sapwood/tridas:missingSapwoodRingsToBark', self.namespaces).text)
            #if info_wood.find('tridas:sapwood/tridas:missingSapwoodRingsToBarkFoundation', self.namespaces) is not None:
            #    meta[CAMBIUM_METHOD] = info_wood.find('tridas:sapwood/tridas:missingSapwoodRingsToBarkFoundation', self.namespaces).text
            if info_wood.find('tridas:bark', self.namespaces) is not None:
                meta[BARK] = self._presence_of_wood_attribut(info_wood.find('tridas:bark', self.namespaces))
    
    def _interpretation(self, meta, node):
        def date(node):
            c = 1.0
            d = 0
            if node.attrib['suffix'] in ['BC', 'BCE']:
                c = -1
                d = 1
            elif node.attrib['suffix'] == 'BP':
                logger.debug('date BP !')
                c = -1
                d = 1950
            date = int(node.text) * c + d
            if 'certainty' in node.attrib:
                return date, node.attrib['certainty']
            return date, 'unknown'
        
        if node.find('tridas:interpretation/tridas:firstYear', self.namespaces) is not None:
            y = node.find('tridas:interpretation/tridas:firstYear', self.namespaces)
            meta[DATE_BEGIN], meta[DATED] = date(y)
        if node.find('tridas:interpretation/tridas:lastYear', self.namespaces) is not None:
            y = node.find('tridas:interpretation/tridas:lastYear', self.namespaces)   
            meta[DATE_END], meta[DATED] = date(y)
    
    # ------------------------------------
    def _readall(self):
        self._read_places()

        self.meta_projects, self.idx_projects = self._init_metadata(SET, 'projects')
        self.meta_projects[KEYCODE] = 'projects'
        self.sequences.append(self.meta_projects)
        
        self.meta_chronologies, self.idx_chronologies = self._init_metadata(SET, 'chronologies')
        self.meta_chronologies[KEYCODE] = 'chronologies'
        self.sequences.append(self.meta_chronologies)
        
        self._read(is_projetcs=True) # read all project without derivedSeries
        self._read(is_projetcs=False) # read all derivedSeries

        self._write_places()
       
    def _read(self, is_projetcs=True):
        self.namespaces = {}
        lst = [x for x in glob.glob(self.glob_str)]
        for i, self.filename in enumerate(lst):
            if i % 100 == 0:
                logger.info(f'{np.round((i/len(lst))*100, 2)}, {self.filename}, {is_projetcs}')
                logger.debug('_write_places')
                self._write_places()
            
            self.uri = Path(self.filename).resolve().as_uri()
            tree = ET.parse(self.filename)
            root = tree.getroot()

            for key, value in root.nsmap.items():
                if key is None:
                    key = 'default'
                self.namespaces[key] = value
            
            if root.tag == '{'+self.namespaces["tridas"]+'}project':
                if is_projetcs:
                    self._read_project(root, self.meta_projects.copy())
                else:
                    self._read_chronology(root)
            
    def _read_project(self, project, parent_meta):
        #identifier, createdTimestamp, lastModifiedTimestamp, comments, type_[], description, laboratory[], 
        # category, investigator,period, requestDate, commissioner, reference[], research[], genericField[]
        #self.presence_of(project, 'tridas:file')
        meta, _ = self._new_metadata(project, parent_meta, SET, PROJECT)
        self._set_laboratories(project)
        meta[PROJECT] = meta[KEYCODE]
        #print('_read_project')
        for object in project.findall('tridas:object', self.namespaces):
            self._read_object(object, meta)
        
    def _read_chronology(self, project):
        self._set_laboratories(project)

        for derived_series in project.findall('tridas:derivedSeries', self.namespaces):
            self._read_derived_series(derived_series, project)
            
    def _read_object(self, object, parent_meta):
        #identifier, createdTimestamp, lastModifiedTimestamp, comments, type_, description,
        #, creator, owner, coverage, genericField
        
        #self.presence_of(object, 'tridas:file')
        self.presence_of(object, 'tridas:linkSeries')
        
        meta, idx = self._new_metadata(object, parent_meta, SET, 'object')
        self._add_location(meta, object)
        
        for object_ in object.findall('tridas:object', self.namespaces):
            self._read_object(object_, meta)
        
        elements = object.findall('tridas:element', self.namespaces)
        if elements:
            for element in elements:
                self._read_element(element, meta, len(elements))
        
    def _read_element(self, element, parent_meta, nb):
        #identifier, createdTimestamp, lastModifiedTimestamp, comments, type_, description,
        #shape, dimensions, authenticity, processing, marks, altitude,  slope, soil, bedrock, genericField,
        
        self.presence_of(element, 'tridas:linkSeries')

        if nb == -1 and (element.find('tridas:keycode', self.namespaces).text == parent_meta[KEYCODE]):
            meta = parent_meta
            meta[SUBCATEGORY] += ', element'
        else:
            meta, idx = self._new_metadata(element, parent_meta, SET, category_tridas='element')

        self._add_location(meta, element)
        self._add_taxon(meta, element)

        samples = element.findall('tridas:sample', self.namespaces)
        if samples is not None:
            for sample in samples:
                self._read_sample(sample, meta, len(samples)) 
    
    def _read_sample(self, sample, parent_meta, nb):
        #identifier, createdTimestamp, lastModifiedTimestamp, comments, type_, description,
        #samplingDate, offset, state, knots, genericField,

        #self.presence_of(sample, 'tridas:file')

        if nb == -1 and (sample.find('tridas:keycode', self.namespaces).text == parent_meta[KEYCODE]):
            meta = parent_meta
            meta[SUBCATEGORY] += ', sample'
        else:
            meta, idx = self._new_metadata(sample, parent_meta, SET, category_tridas=TREE)

        radius = sample.findall('tridas:radius', self.namespaces)
        if radius is not None:
            for radius_ in radius:
                self._read_radius(radius_, meta, len(radius) ) 
    
    def _read_radius(self, radius, parent_meta, nb):
        #identifier, createdTimestamp, lastModifiedTimestamp, comments, azimuth, genericField

        if nb == -1 and (radius.find('tridas:keycode', self.namespaces).text == parent_meta[KEYCODE]):
            meta = parent_meta
            meta[SUBCATEGORY] += ', radius'
        else:
            meta, idx = self._new_metadata(radius, parent_meta, SET, category_tridas='radius')

        self._read_wood_completeness(meta, radius)

        measurement_series = radius.findall('tridas:measurementSeries', self.namespaces)
        if measurement_series is not None:
            for ms in measurement_series:
                self._read_measurement_series(ms, meta, len(measurement_series)) 

    def _read_measurement_series(self, measurement_series, parent_meta, nb):
        # keycode, identifier, createdTimestamp, lastModifiedTimestamp, comments, id, measuringDate, derivationDat,  
        # analyst, dendrochronologist, measuringMethod, type_, objective, standardizingMethod, author, version, 
        # interpretationUnsolved,  genericField
        
        self.presence_of(measurement_series, 'tridas:linkSeries')
  
        if nb == -1 and (measurement_series.find('tridas:keycode', self.namespaces).text == parent_meta[KEYCODE]):
            meta = parent_meta
            meta[CATEGORY] = TREE
            meta[SUBCATEGORY] += ', mSeries'
        else:
            meta, idx = self._new_metadata(measurement_series, parent_meta, TREE, category_tridas='mSeries')

        self._read_wood_completeness(meta, measurement_series)
        self._add_location(meta, measurement_series)
        self._interpretation(meta, measurement_series)
      
        for v in measurement_series.findall('tridas:values', self.namespaces):
            vect, _ = self._read_values(v, meta[IDX]) 
            meta[DATA_VALUES] = vect
            meta[DATA_LENGTH] = len(vect)
            meta[DATA_TYPE] = 'raw'

    def _read_derived_series(self, derived_series, project):
        #identifier, createdTimestamp, lastModifiedTimestamp, comments, id, measuringDate, derivationDate,  
        #analyst, dendrochronologist, measuringMethod, type_, objective, standardizingMethod, author, version, 
        #  interpretationUnsolved,  genericField=None, 
        if derived_series.find('tridas:keycode', self.namespaces) is None:
            #logger.warning(f'keycode is missing in derived_series')
            return
        
        keycode = derived_series.find('tridas:keycode', self.namespaces).text
        
        links = derived_series.findall('tridas:linkSeries/tridas:series', self.namespaces)     
        on_set = False   
        if len(links) == 1 :
            id_domain = self._get_identifier(links[0])
            if (id_domain in self.identifier) and (self.identifier[id_domain][CATEGORY] == SET):
                meta = self.identifier[id_domain]
                meta[CATEGORY] = SET
                idx = meta[IDX]
                on_set = True
        if not on_set :   
            for link in links:
                id_domain = self._get_identifier(link)
                if id_domain not in self.identifier:
                    logger.warning(f'Remove derived_series: {id_domain} is missing in {keycode}')
                    return
            
            meta, idx = self._init_metadata(CHRONOLOGY, 'dSeries')
            self._add_keycode(meta, derived_series)
            self.sequences.append(meta)
            meta[PROJECT] = project.find('tridas:keycode', self.namespaces).text
            self.add_component(self.idx_chronologies, idx)
            for link in links:
                self.add_component(idx, self.identifier[self._get_identifier(link)][IDX])

        self._read_wood_completeness(meta, derived_series)
        self._add_location(meta, derived_series)
        self._interpretation(meta, derived_series)

        for v in derived_series.findall('tridas:values', self.namespaces):
            vect, weigths = self._read_values(v, idx)
            meta[DATA_VALUES] = vect
            meta[DATA_WEIGHTS] = weigths
            meta[DATA_LENGTH] = len(vect)
            meta[DATA_TYPE] = 'raw'

    def _read_values(self, values, idx):
        vect = []
        weigths = []
        for value in values.findall('tridas:value', self.namespaces):
            v = float(value.attrib['value'])
            if (v == 9999) or (v == 0):
                v = np.nan
            vect.append(v)
            if 'count' in value.attrib:
                weigths.append(float(value.attrib['count']))
        
        vect = [np.nan if (x == 999) or (x <= 0) else x for x in vect[:-1]]

        return np.array(vect), np.array(weigths)
    
    def to_dataset(self, root_keycode='Dataset', root_idx=ROOT, trash_keycode='Trash', clipboard_keycode='Clipboard'):
        self._readall()
        self.dataset = Dataset(sequences=self.sequences, components=self.components, save_auto=False)

        self.dataset.new_root(root_keycode, root_idx)
        self.dataset.new_clipboard(clipboard_keycode)
        self.dataset.new_trash(trash_keycode)

        return self.dataset
    
    def merge_level(self):
        merge = {}
        
        # merge level with only one son
        def iterate(node):
            sep = '\\'
            for child in node.children:
                if child.category != TREE:
                    iterate(child)
            if  (len(node.children) == 1) and (node.parent is not None) : 
                node.parent.children = node.children
                idx_parent = node.parent.idx
                idx = node.idx
                idx_child = node.children[0].idx
                s = self.dataset.sequences
                if s.at[idx_child, KEYCODE] != s.at[idx, KEYCODE]:
                    s.at[idx_child, KEYCODE] = s.at[idx, KEYCODE] + sep + s.at[idx_child, KEYCODE]
                cols = list(set(s.columns) - set([SUBCATEGORY, KEYCODE, CATEGORY, DATA_LENGTH, DATA_VALUES, DATA_WEIGHTS]))
                for col in cols:
                    if pd.isna(s.at[idx_child, col]):
                        s.at[idx_child, KEYCODE] = s.at[idx, KEYCODE]
                    elif pd.notna(s.at[idx, col]):
                        if s.at[idx_child, col] != s.at[idx, col]:
                            logger.info(f'\t copy [{idx_child} <-- {idx}, {col}] {s.at[idx_child, col]} <-- {s.at[idx, col]}')
                                             
                p = self.dataset.components.at[(idx, idx_child), OFFSET]
                self.dataset.soft_drop(idx)
                self.dataset.components.at[(idx_parent, idx_child), OFFSET] = p
                                
        tree = self.dataset.get_descendants(self.dataset.get_roots())
        iterate(tree)
        return self.dataset

        
