""" I/O Heidelberg file format. """

__author__ = "Sylvain Meignier"
__copyright__ = "Copyright 2023 Sylvain Meignier, Le Mans Université, LIUM (https://lium.univ-lemans.fr/)"
__license__ = "GPL"

from pathlib import Path
import pandas as pd
import numpy as np
import re
import io

from pyDendron.dataname import *
from pyDendron.dataset import Dataset
from pyDendron.alien.io import IO

"""
From TRICYCLE: A UNIVERSAL CONVERSION TOOL FOR DIGITAL TREE-RING DATA – SUMMARY OF DENDRO DATA FORMATS
The header block begins with a line HEADER:. This is followed by lines of metadata, with one field on each line, in the format keywords=value much like a standard Windows INI file. As mentioned previously there are a number of predefined keywords, all of which are outlined here:

• KeyCode, KeyNo
• LabotaryCode
• Project, ProtectionCode

• BHD
• Bibliography, Bibliography[n], BibliographyCount
• Bundle
• ChronologyType, ChronoMemberCount, ChronoMemberKeycodes 

• Age
• Bark, Pith, JuvenileWood, SapWoodRings
• Circumference

• PersId
• Client, ClientNo
• Collector
• CreationDate
• Comment, • Comment[n], CommentCount

• Continent, Country, Town, TownZipCode, Street, District, State, Province
• CardinalPoint, Latitude, Longitude, Elevation, Exoffset

• CoreNo

• DataFormat, DataType

• AcceptDate
• DateBegin
• Dated
• DateEnd, DateEndRel, DateOfSampling
• DateRelBegin[n], DateRelEnd[n], DateRelReferenceKey[n], DateRelCount
• LastRevisionDate, LastRevisionPersID
• Location, LocationCharacteristics

• DeltaMissingRingsAfter, DeltaMissingRingsBefore, DeltaRingsFromSeedToPith 
• Disk
• 
• EdgeInformation
• EffectiveAutoCorrelation, EffectiveMean, EffectiveMeanSensitivity, EffectiveNORFAC, AutoCorrelation 
• StandardDeviation

• Key
• EffectiveNORFM, EffectiveStandardDeviation • Eigenvalue
• 
• EstimatedTimePeriod

• FieldNo
• FilmNo
• FirstMeasurementDate, FirstMeasurementPersID
• FromSeedToDateBegin
• GlobalMathComment[n], GlobalMathCommentCount 
• GraphParam
• Group
• HouseName, HouseNo
• ImageCellRow, ImageComment[n], ImageFile[n], ImageCount, ImageFile

• Interpretation
• InvalidRingsAfter • InvalidRingsBefore 
• 
• 
• LeaveLoss
• Length
• 
• MajorDimension
• MathComment, MathComment[n], MathCommentCount
• MeanSensitivity
• MinorDimension
• MissingRingsAfter, MissingRingsBefore

• NumberOfSamplesInChrono • NumberOfTreesInChrono

• 
• QualityCode
• Radius, RadiusNo
• RelGroundWaterLevel
• RingsFromSeedToPith
• SampleType, SamplingHeight, SamplingPoint
• Sequence
• SeriesEnd, SeriesStart, SeriesType
• ShapeOfSample
• Site, SiteCode
• SocialStand
• SoilType
• Species, SpeciesName
• StemDiskNo 
• Tree, TreeHeight
• Timber, TimberHeight, TimberType, TimberWidth
• TotalAutoCorrelation, TotalMean, TotalMeanSensitivity, TotalNORFAC, TotalNORFM, TotalStandardDeviation
• TreeNo
• Unit
• UnmeasuredInnerRings, UnmeasuredOuterRings 
• WaldKante
• WoodMaterialType
• WorkTraces

The header section is followed by a data section denoted by a line containing the keyword DATA: followed by the type of data present which can be one of Tree; HalfChrono; Chrono; Single; Double; Quad. Tree, HalfChrono and Chrono are the original keywords supported by early versions of TSAP but these are now deprecated in preferences of the more generic Single, Double and Quad terms. The terms Single, Double and Quad are largely interchangeable with Tree, HalfChrono and Chrono respectively, but not completely. Double can refer to both Tree and HalfChrono format data. When the newer terms are used, the header keyword DataFormat is used to record whether the data is equivalent to Tree, HalfChrono or Chrono.
Single format - data is typically used for storing raw measurement series. Each data line contains 10 data values each being a left space padded integer taking up 6 characters. Any spare data values in the final data line are filled with zeros. Alternatively it appears that TSAP-Win also accepts this data section as single integer values one per line.
Double format - data is for storing data with sample depth information - typically chronologies. Like the single format section, data is stored as 10 integer values, each taking up 6 characters and left padded with spaces. The values are in pairs of ring-widths and sample depths, therefore five rings are stored per line.
Quad format - data is for storing chronologies with sample depth as well as data on how many of the constituent series increase and decrease. This format therefore requires four numbers for each data point: ring-width; sample depth; increasing series; decreasing series. Numbers are stored as integers, left space padded as before, but this time only using 5 characters not 6. Four data points are included on each line, therefore this means there are 16 numbers per row and each row is 80 characters long.
"""

class IOHeidelberg(IO):
    # Define regex patterns as class variables to compile them only once
    LONGITUDE_PATTERN = re.compile(r'(\d+). (\d+)\' (\d+)\'\' ([NS])')
    LATITUDE_PATTERN = re.compile(r'(\d+). (\d+)\' (\d+)\'\' ([WE])')

    def read_header(self, buffer, meta):
        @staticmethod
        def location(value):
            return value
        
        @staticmethod
        def boolean_(value):
            return value.upper() in ['TRUE', '+', '1', 'P', 'B']
        
        @staticmethod
        def integer_(value):
            return int(value) if value != '' else pd.NA

        @staticmethod
        def date(value):
            return pd.to_datetime(value) if value != '' else pd.NA

        @staticmethod
        def longitude(value):
            if not value:
                return pd.NA
            match = IOHeidelberg.LONGITUDE_PATTERN.match(value)
            if match:
                lon = match.group(1) + match.group(2) / 60 + match.group(3) / 3600        
                return -lon if match.group(4) == 'S' else lon
            return float(value)

        @staticmethod
        def latitude(value):
            if value == '':
                return pd.NA
            match = IOHeidelberg.LATITUDE_PATTERN.match(value)
            if match:
                lat = match.group(1) + match.group(2) / 60 + match.group(3) / 3600        
                return -lat if match.group(4) == 'W' else lat
            return float(value)

        @staticmethod
        def string_(value):
            return value

        @staticmethod
        def float_(value):
            return float(value)
        
        @staticmethod
        def list_(value):
            return [x for x in re.split(r',|\s', value) if x != '']

        keys ={
            'Project': (PROJECT, string_),
            'Keycode': (KEYCODE, string_),
            'Bark': (BARK, boolean_), 
            'Pith': (PITH, boolean_),
            'Species': (SPECIES, string_),
            'MissingRingsAfter': (CAMBIUM_MAXIMUM, integer_), 
            'MissingRingsBefore': (PITH_MAXIMUM, integer_),
            #'Location': (SITE_COUNTRY, location),
            'Country': (SITE_COUNTRY, string_),
            'Town': (SITE_TOWN, string_),
            'TownZipCode': (SITE_ZIP, string_),
            'State': (SITE_STATE, string_),
            'Province': (SITE_DISTRICT, string_),
            'Latitude': (SITE_LATITUDE, latitude),
            'Longitude': (SITE_LONGITUDE, longitude),
            'Elevation': (SITE_ELEVATION, float_),
            'CreationDate': (CREATION_DATE, date),
            'SapWoodRings': (SAPWOOD, integer_),
            'DateEnd': (DATE_END, integer_),
            'DateBegin': (DATE_BEGIN, integer_),
            'Length': (DATA_LENGTH, integer_),
            'ChronoMemberKeycodes': (None, list_),
            }
        chrono_member_keycodes = None
        lines = buffer.split('\n')
        for line in lines:
            s = line.split('=')
            #print('read_header:', line, s)
            key = s[0] 
            value = s[1] if len(s) > 1 else ''
            if key in keys:
                (k, fct) = keys[key]
                if k is None:
                    chrono_member_keycodes = fct(value)
                else:
                    x = fct(value)
                    if pd.notna(x):
                        meta[k] = x
            elif key != '':
                logger.warning(f'key "{key}" with value "{value}" is not imported')
        
        if (DATE_BEGIN in meta ) and (meta[DATE_BEGIN] < 0): meta[DATE_BEGIN] += 1
        if (DATE_END in meta ) and (meta[DATE_END] > 0): meta[DATE_END] += 1
        if SAPWOOD in meta: meta[SAPWOOD] = meta[DATA_LENGTH] - meta[SAPWOOD]
        if PITH_MAXIMUM in meta: meta[PITH_MAXIMUM] *= -1
        if (SITE_ELEVATION in meta) and (SITE_LONGITUDE in meta): self._get_location(meta)
        
        return chrono_member_keycodes
         
    def read_data(self, buffer, meta, kind):
        kind = kind.upper()
        dec = 1
        meta[CATEGORY] = TREE
        #print(meta)
        if kind in ['DOUBLE', 'HALFCHRONO']:
            kind = 2
            meta[CATEGORY] = CHRONOLOGY
        elif kind in ['QUAD', 'CHRONO']:
            kind = 4
            meta[CATEGORY] = CHRONOLOGY
        words = buffer.upper().split()   
        values = [] 
        for i, word in enumerate(words):
            if i * dec >= meta[DATA_LENGTH]:
                break
            if i % dec == 0:
                v = int(word)
                if v == 0:
                    values.append(pd.NA)
                else:
                    values.append(v)

        meta[DATA_VALUES] = np.array(values, dtype='float')
        meta[DATA_TYPE] = RAW
    
    def read_sequences(self, idx_parent, lines):
        meta = {}
        state = 'start'
        buffer = ''
        idx_comps = {}
        kind = 'single'
        chrono_member_keycodes = None
        
        for line in lines:
            #print(state, line)
            if line.upper().startswith('HEADER:'): # new sequences
                if state == 'data':
                    #print(meta)
                    self.read_data(buffer, meta, kind)
                if state != 'start':
                    self.components.append({IDX_PARENT: idx_parent, IDX_CHILD: meta[IDX], OFFSET: pd.NA})
                    self.sequences.append(meta)
                    idx_comps[meta[KEYCODE]] = meta[IDX]
                    if chrono_member_keycodes is not None:
                        for keycode in chrono_member_keycodes:
                            if keycode not in idx_comps:
                                raise ValueError(f'"{keycode}" is missing')
                        for keycode in chrono_member_keycodes:
                            self.components.append({IDX_PARENT: meta[IDX], IDX_CHILD: idx_comps[keycode], OFFSET: pd.NA})

                meta = {IDX: self.next_idx()}
                state = 'header'                
                buffer = ''
            elif line.upper().startswith('DATA:'): # new values
                if state != 'header':
                    raise ValueError('inconsistent state: {state}')
                kind = line.split(':')[1]
                chrono_member_keycodes = self.read_header(buffer, meta)
                state = 'data'          
                meta[DATA_TYPE] = RAW
                buffer = ''
            else:
                buffer += line
                
        if state == 'header':
            raise ValueError('inconsistent state: {state}')
        elif state != 'data':
            self.read_data(buffer, meta, kind)
            self.components.append({IDX_PARENT: idx_parent, IDX_CHILD: meta[IDX], OFFSET:pd.NA})
            self.sequences.append(meta)

    def write_file(self, data: pd.DataFrame, chronologies, filename: str):
        with open(Path(filename), mode='w', encoding=self.encoding, errors='ignore') as fd:
            for _, row in data.iterrows():
                if row[CATEGORY] in [TREE, CHRONOLOGY]:
                    fd.write('HEADER:\n')
                    for col in data.columns:
                        if (not col.startswith('Data')):
                            v = row[col]
                            if pd.notna(v):
                                fd.write(f'{col}={v}\n')
                    if row[DATA_TYPE] != RAW:
                        fd.write(f'{DATA_TYPE}={row[DATA_TYPE]}\n')
                    fd.write(f'Lenght={row[DATA_LENGTH]}\n')
                    fd.write(f'DATA:Tree\n')
                    tmp = np.nan_to_num(row[DATA_VALUES], nan=0).astype(int).tolist()
                    for i, v in enumerate(tmp):
                        fd.write(f'{v} ')
                        if (i + 1) % 10 == 0:
                            fd.write('\n')
                    while (i + 1) % 10 != 0:
                        fd.write('0 ')
                        i += 1
                    fd.write('\n')
                            
                        
                    
