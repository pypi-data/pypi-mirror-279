"""
    Import RWL file with text metadata
"""
__license__ = "GPL"
__author__ = "Sylvain Meignier"
__copyright__ = "Copyright 2023 Sylvain Meignier, Le Mans Université, LIUM (https://lium.univ-lemans.fr/)"
__maintainer__ = "Sylvain Meignier"
__email__ = "pyDendron@univ-lemans.fr"
__status__ = "Production"
"""
From TRICYCLE: A UNIVERSAL CONVERSION TOOL FOR DIGITAL TREE-RING DATA – SUMMARY OF DENDRO DATA FORMATS

Tucson RWL files begin with three lines of metadata. Strictly these lines should contain structured metadata, but with no software to assist in this, users either only partially stick to these rules, or reject them entirely instead using the three lines as free-text comment lines. The metadata should be set out as follows:
• Line1-Chars1-6SiteID
• Line 1 - Chars 10-61 Site Name
• Line 1 - Chars 62-65 Species Code followed by optional ID number
• Line2-Chars1-6SiteID
• Line 2 - Chars 10-22 State/Country
• Line 2 - Chars 23-30 Species
• Line 2 - Chars 41-45 Elevation
• Line 2 - Chars 48-57 Lat-Long in degrees and minutes, ddmm or dddmm • Line 2 - Chars 68-76 1st and last Year
• Line3-Chars1-6SiteID
• Line 3 - Chars 10-72 Lead Investigator
• Line 3 - Chars 73-80 comp. date
Then follows the data lines which are set out as follows:
• Chars 1-8 - Series ID - the series ID should be unique in the file so that it is clear where one series ends and another begins when multiple series are present in the same file.
• Next 4 chars - Year of first value in this row.
• Ten data values consisting of a space character and 5 integers. The file and last data line for a series may have
less than 10 data values so that the majority of lines begin at the start of a decade.
The final data value should be followed by a a stop marker which is either 999 or -9999. When a stop marker of 999 is used this indicates that the integer values in the file are measured in 0.01mm (1/100th mm) units, whereas if a -9999 stop marker is used the units are 0.001mm (microns). The stop marker is therefore used to indicate the end of the data series and the units the data are stored in.
There appears to be no official specification as to how missing rings should be encoded, but the standard notation seems to be to use -999 or 0.
"""
from pathlib import Path
import numpy as np
import re
import pickle

from pyDendron.app_logger import logger
from pyDendron.dataname import *
from pyDendron.dataset import Dataset
from pyDendron.tools.location import reverse_geocode, get_elevation

meta_key = {
    #'Dataset_DOI':'doi',
    'Collection_Name' : PROJECT,
    'Study_Name' : 'creation.comment',
    #'Investigators' : LABs,
    #'Description' : 'description',
    'First_Year' : DATE_BEGIN,
    'Last_Year' : DATE_END,
    #'Time_Unit' : 'timeUnit',
    'Tree_Species_Code' : SPECIES,
    #'Funding_Agency_Name' : 'fundingAgencyName',
    #'Grant' : 'grant',
     #'NOAA_Landing_Page': URI,
     'state': 'state',
     'Northernmost_Latitude': SITE_LATITUDE,
     'Easternmost_Longitude': SITE_LONGITUDE,
     'Elevation_m': SITE_ELEVATION,
}

class RWL:
    def __init__(self, path, source='irtdb', places='reverse_places.p', get_place=True, get_altitude=True):
        self.path = Path(path)
        self.sequences = []
        self.components = []
        self.idx_irtdb = 0
        self.idx = 1
        self.source = source
        self.places = {}
        self.elevations = {}
        
        self.get_place = get_place
        self.get_altitude = get_altitude
        self.places_fn = places
    
    def _read_places(self):
        if (self.places_fn is not None) and Path(self.places_fn).exists():
            with open(self.places_fn , 'rb') as fic:
                self.places, self.elevations = pickle.load(fic)

    def _write_places(self):
        with open(self.places_fn , 'wb') as fic:
            pickle.dump([self.places, self.elevations], fic)
                
    def _read_rwl_metadata(self, filename, meta):
        pattern = re.compile(r'#\s*(\w+):\s*(.*)')
        if Path(filename).exists():
            with open(Path(filename), 'r') as fd:
                for ligne in fd:
                    match = pattern.match(ligne)
                    if match:
                        key, value = match.groups()
                        if key in meta_key:
                            meta[meta_key[key]] = value   
                        
    def _readline(self, fd):
        line = fd.readline().strip()
        while line == '':
            line = fd.readline().strip()
        return line
        
    def _read_rwl(self, filename, meta_filename=None):
        def get_header(fd):
            # Header, line 1
            line = self._readline(fd)
            if line.startswith('#'):
                return
            site_id = line[0:6]
            # Header, line 2
            line = self._readline(fd)
            # Header, line 3
            line = self._readline(fd)
    
        meta = {}
        series = {}
        with open(Path(filename), encoding='utf-8', errors='ignore') as fd:
            get_header(fd)
            serie_id = ''
            
            for line in fd:
                line = line.strip()
                if len(line) < 12 or line.startswith('#'):
                    continue
                if len(line) > 72:
                    line = line[:72]
                tab = line[8:].split()
                if tab[0].startswith('#'):
                    continue
                if line[0:8] != serie_id:
                    serie_id = line[0:8]
                    begin_date = float(tab[0])
                    values = []
                values += [float(x) for x in tab[1:]]
                if (values[-1] == 999) or (values[-1] == -9999): # end serie
                    d = 1
                    if values[-1] == -9999: 
                        d = 10
                    values = [np.nan if (x == 999) or (x <= 0) else x/d for x in values[:-1]]
                    end_date = begin_date + len(values) - 1
                    series[serie_id] = (begin_date, end_date, len(values), np.array(values))

        if meta_filename is not None:
            self._read_rwl_metadata(meta_filename, meta)

        return meta, series

    def _meta_to_row(self, idx , cols, meta):
        d = idx
        for col in cols:
            if col in meta:
                d[col] = meta[col]
            else:
                d[col] = None
        return d
        #vect = [None] * len(cols)
        #for i, col in enumerate(cols):
        #    if col in meta:
        #        vect[i] = meta[col]
        #return idx + vect

    def _set_meta(self, meta, begin_date, end_date, count, values, keycode, project):
        meta[DATE_BEGIN] = begin_date
        meta[DATE_END] = end_date
        meta[DATA_LENGTH] = count
        meta[DATA_VALUES] = values
        meta[KEYCODE] = keycode
        meta['keycode.child'] = meta[KEYCODE]
        meta[OFFSET] = np.nan
        meta[CATEGORY] = TREE
        meta[PROJECT] = project
        #meta[SOURCE] = self.source
        meta[DATA_TYPE] = RAW

        meta[SITE_ELEVATION] = np.nan
        meta[SITE_COUNTRY] = meta[SITE_STATE] = meta[SITE_DISTRICT] = meta[SITE_TOWN] = ''
        if (SITE_LATITUDE in meta) and  (SITE_LONGITUDE in meta):
            if self.get_place:
                _, __, ___, ____, _____, meta[SITE_CODE] = reverse_geocode(meta[SITE_LATITUDE], meta[SITE_LONGITUDE], self.places)
                #meta[SITE_COUNTRY], meta[SITE_STATE], meta[SITE_DISTRICT], meta[SITE_TOWN], meta[SITE_ZIP] = reverse_geocode(meta[SITE_LATITUDE], meta[SITE_LONGITUDE], self.places)
            alt = meta[SITE_ELEVATION]
            if self.get_altitude: 
                meta[SITE_ELEVATION] = get_elevation(meta[SITE_LATITUDE], meta[SITE_LONGITUDE], self.elevations)
        else:
            meta[SITE_LATITUDE] = np.nan
            meta[SITE_LONGITUDE] = np.nan
     
    def _add(self, meta, series, project):
        idx_project = self.idx
        self.idx += 1
        
        def add_project():
            meta_project = {}
            meta_project[KEYCODE] = meta['keycode.child'] = meta_project[PROJECT] = project
            meta_project[CATEGORY] = SET
            self.sequences.append(self._meta_to_row({IDX: idx_project}, sequences_cols, meta_project))
            self.components.append(self._meta_to_row({IDX_PARENT: self.idx_irtdb, IDX_CHILD:idx_project}, components_cols, meta_project))
            return False

        add_project()
        for keycode in series:
            (begin_date, end_date, count, values) = series[keycode]
            self._set_meta(meta, begin_date, end_date, count, values, keycode, project)
            self.sequences.append(self._meta_to_row({IDX: self.idx}, sequences_cols, meta))
            self.components.append(self._meta_to_row({IDX_PARENT: idx_project, IDX_CHILD: self.idx}, components_cols, meta))
            self.idx += 1
    
    def to_dataset(self, root_keycode='Dataset', root_idx=ROOT, trash_keycode='Trash', clipboard_keycode='Clipboard'):
        self._read_places()
        
        meta = {}
        #meta[SOURCE] = self.source
        meta[KEYCODE] = self.source
        meta[CATEGORY] = SET
        self.sequences.append(self._meta_to_row({IDX:self.idx_irtdb}, sequences_cols, meta))
        lst = [fn for fn in self.path.glob('*.rwl')]
        for i, filename in enumerate(lst):
            logger.debug(f'{np.round((i/len(lst))*100, 2)}, {filename}')
            filename_meta = Path(filename.parent) / Path(filename.stem + '-rwl-noaa.txt')
            meta, series = self._read_rwl(filename, filename_meta)
            self._add(meta, series, filename.stem)
            if i % 100 == 0:
                self._write_places()

        self._write_places()
        
        dataset = Dataset(sequences=self.sequences, components=self.components, save_auto=False)
        #idx_trash = data.new(idx=TRASH, idx_parent=None, no_comps=True, keycode='trash', category=SET)
        
        dataset.new_root(root_keycode, root_idx)
        dataset.new_clipboard(clipboard_keycode)
        dataset.new_trash(trash_keycode)
        
        return dataset

    
                