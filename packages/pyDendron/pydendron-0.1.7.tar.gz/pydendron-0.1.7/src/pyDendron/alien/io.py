
from pathlib import Path
import pickle
import io
import re

from pyDendron.dataname import *
from pyDendron.tools.location import reverse_geocode, get_elevation
from pyDendron.dataset import Dataset


class IO:
    def __init__(self, encoding='utf-8', source='unk', places='reverse_places.p', get_place=False, get_altitude=False):
        self.sequences = []
        self.components = []
        self.idx = 1
        self.source = source
        self.places = {}
        self.elevations = {}
        self.encoding = encoding
        self.get_place = get_place
        self.get_altitude = get_altitude
        self.places_fn = places
        
        if get_place:
            self._read_places()

    def _read_places(self):
        if (self.places_fn is not None) and Path(self.places_fn).exists():
            with open(self.places_fn , 'rb') as fic:
                self.places, self.elevations = pickle.load(fic)

    def _write_places(self):
        with open(self.places_fn , 'wb') as fic:
            pickle.dump([self.places, self.elevations], fic)

    def _get_location(self, meta):
        meta[SITE_COUNTRY] = meta[SITE_STATE] = meta[SITE_DISTRICT] = meta[SITE_TOWN] = meta[SITE_ZIP] = ''
        if self.get_place:
            meta[SITE_COUNTRY], meta[SITE_STATE], meta[SITE_DISTRICT], meta[SITE_TOWN], meta[SITE_ZIP] = reverse_geocode(meta[SITE_LATITUDE], meta[SITE_LONGITUDE], self.places)
        if self.get_altitude:
            meta[SITE_ELEVATION] = get_elevation(meta[SITE_LATITUDE], meta[SITE_LONGITUDE], self.elevations)

    def init(self, keycode_parent):
        parent_idx = self.next_idx()
        self.sequences.append({IDX: TRASH, KEYCODE: 'Trash', CATEGORY: SET})
        self.sequences.append({IDX: CLIPBOARD, KEYCODE: 'Clipboard', CATEGORY: SET})
        self.sequences.append({IDX: ROOT, KEYCODE: 'Dataset', CATEGORY: SET})
        self.sequences.append({IDX: parent_idx, KEYCODE: keycode_parent, CATEGORY: SET})
        self.components.append({IDX_PARENT: ROOT, IDX_CHILD:parent_idx, OFFSET: pd.NA})

        return parent_idx

    def _readline(self, fd):
        line = fd.readline().strip()
        while line == '':
            line = fd.readline().strip()
        return line
    
    def next_idx(self):
        self.idx += 1
        return self.idx

    def read_sequences(self, idx_parent, lines):
        pass

    def read_buffer(self, keycode_parent, buffer):
        parent_idx = self.init(keycode_parent)
        iobuffer = io.BytesIO(buffer)
        text = iobuffer.getvalue().decode(self.encoding)
        text = re.sub(r'\r\n?|\n', '\n', text)
        lines = text.split('\n')
        #lines = iobuffer.readlines()
        lines = [line+'\n' for line in lines]
        print(lines)
        self.read_sequences(parent_idx, lines)
        self._write_places()
        
        return Dataset(sequences=self.sequences, components=self.components)
    
    def read_file(self, filename):
        with open(Path(filename), 'rt', encoding=self.encoding, errors='ignore', newline=None) as fd:
            keycode_parent = Path(filename).stem
            parent_idx = self.init(keycode_parent)
            lines = fd.readlines()
            print('lines:',lines)
            self.read_sequences(parent_idx, lines)

        self._write_places()

        return Dataset(sequences=self.sequences, components=self.components)

    def write_file(self, data, chronologies, filename):
        pass

    def write_package(self, dataset, data, filename):
        idx_samples = data.loc[data[CATEGORY] == TREE, IDX_CHILD].to_list()
        chronologies = {}
        for _, row in data[data[CATEGORY] == CHRONOLOGY].iterrows():
            tree = dataset.get_descendants(row[IDX_CHILD])
            samples = {dataset.sequences.at[node.idx, KEYCODE]: offset for node, offset in tree.descendants[TREE].items() if node.idx not in idx_samples}
            chronologies[row[IDX_CHILD]] = samples
            
        self.write_file(data, chronologies, filename)
            
    
    
    
