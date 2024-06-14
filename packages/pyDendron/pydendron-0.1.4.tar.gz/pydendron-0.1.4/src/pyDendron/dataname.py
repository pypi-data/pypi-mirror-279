"""
Data Name
"""
__license__ = "GPL"
__author__ = "Sylvain Meignier"
__copyright__ = "Copyright 2023 Sylvain Meignier, Le Mans Université, LIUM (https://lium.univ-lemans.fr/)"
__license__ = "GPL"
__maintainer__ = "Sylvain Meignier"
__email__ = "pyDendron@univ-lemans.fr"
__status__ = "Production"

import pandas as pd
import numpy as np
from pyDendron.app_logger import logger

ROOT = -30
CLIPBOARD = -10
TRASH = -20

ICON = 'Open'

CHRONOLOGY = 'Chronology'
TREE = 'Tree'
SET = 'Set'

CATEGORIES = [CHRONOLOGY, TREE, SET]

SEQUENCES = 'sequences'
COMPONENTS = 'components'
SELECTIONS = 'selections'
VERSION = 'version'
LOG = 'log'
CROSSDATING = 'crossdating'

HIDDEN = 'hidden'

# DataSet
IDX = 'Idx'
IDX_MASTER = 'IdxMaster'
IDX_PARENT = 'IdxParent'
IDX_CHILD = 'IdxChild'
OFFSET = 'Offset'
OFFSET_NORM = 'OffsetNorm'
#SOURCE = 'source'
#LABORATORY_CODE = 'LabotaryCode'
LABORATORY_CODE = 'LaboratoryCode'
PERS_ID = 'PersId'
PROJECT = 'Project'
KEYCODE = 'Keycode'
KEYCODE_MASTER = 'KeycodeMaster'
SPECIES = 'Species'
SITE_LATITUDE = 'Latitude'
SITE_LONGITUDE = 'Longitude'
SITE_ELEVATION = 'Elevation'
SITE_CODE = 'SiteCode'
BIBLIOGRAPHY_CODE = 'BibliographyCode'
DATE_BEGIN = 'DateBegin'
DATE_BEGIN_MASTER = 'DateBeginMaster'
DATE_END = 'DateEnd'
#DATE_END_OPTIMUM = 'DateEndOptimum'
#DATE_END_MAXIMUM = 'DateEndMaximum'
DATED = 'Dated'
DATE_BEGIN_NORM = 'BateBeginNorm'
DATE_BEGIN_ESTIMATED = 'DateBeginEstimated'
DATE_END_ESTIMATED = 'DateEndEstimated'
CREATION_DATE = 'CreationDate'
DATE_SAMPLING = 'DateOfSampling'
CATEGORY = 'Category'
SUBCATEGORY = 'Subcategory'
SAPWOOD = 'Sapwood' # not in data
#SAPWOOD_OFFSET = 'Sapwood'
PITH = 'Pith'
CAMBIUM = 'Cambium'
#CAMBIUM_METHOD = 'CambiumMethod'
CAMBIUM_SEASON = 'CambiumSeason'
BARK = 'Bark'
COMMENTS = 'Comments'
URI = 'URI'
DATA_LENGTH = 'DataLength'
DATA_TYPE = 'DataType' 
DATA_VALUES = 'DataValues'
DATA_WEIGHTS = 'DataWeights'
DATA_INFO = 'DataInfo'
INCONSISTENT = 'Inconsistent'

DEPTH='depth'

# Detrend
HANNING = 'Hanning'
HAMMING = 'Hamming'
BARTLETT = 'Bartlett'
BLACKMAN = 'Blackman'
RECTANGULAR = 'Rectangular'
BESANCON = 'Besancon (classic)'
BESANCON1 = 'besancon (log at the end)'
BP73 = 'BP73'
SPLINE = 'Spline'
SLOPE = 'Slope'
RAW = 'Raw'
CORRIDOR = 'Corridor (polynome)'
CORRIDOR_SPLINE = 'Corridor (spline)'
DELTA = 'Delta (first derivative)'
DELTADELTA = 'DeltaDelta (second derivative)'
LOG = 'log'
DETREND = 'Detrend'
DETREND_WSIZE = 'Detrend Window Size'
DETREND_LOG = 'Detrend Log'
CHRONOLOGY_DATE_AS_OFFSET = 'Chronology Date as Offset'
CHRONOLOGY_BIWEIGHT_MEAN = 'Chronology Biweight Mean'
CROSSDATING_DATE = 'Crossdating Date'

ring_types = [RAW, HANNING, HAMMING, BARTLETT, BLACKMAN, RECTANGULAR, BESANCON, BESANCON1, 
             BP73, SPLINE, SLOPE, CORRIDOR, CORRIDOR_SPLINE, DELTA, DELTADELTA, LOG]

# CrossDating
OVERLAP = 'overlap'
CORRELATION = 'correlation'

CORR = 'r'
GLK = 'glk'
DIST = 'distance' 

T_SCORE = 't-score' 
Z_SCORE = 'z-score'

T_RANK= 't-rank'
Z_RANK= 'z-rank'
D_RANK= 'd-rank'

ZP_VALUE = 'zp-value'
TP_VALUE = 'tp-value'

OVERLAP_NAN = 'Nnan'
#PV = 'PV'
DCG = 'DCG'
AGC = 'agc'
SSGC = 'ssgc'
SGC = 'sgc'

COSINE = 'cosine'
EUCLIDEAN = 'euclidean'
CITYBLOCK = 'cityblock'
DISTANCE = 'distance'

crossdating_method = [CORRELATION, GLK, DISTANCE]
crossdating_distance = [COSINE, CITYBLOCK, EUCLIDEAN]

# Location
SITE_COUNTRY = 'SiteCountry'
SITE_STATE = 'SiteState'
SITE_DISTRICT = 'SiteDistrict'
SITE_TOWN = 'SiteTown'
SITE_ZIP = 'SiteZipcode'


#Drawing
HEARTWOOD = 'Heartwood'
CAMBIUM_MAXIMUM = 'CambiumMaximum'
CAMBIUM_OPTIMUM = 'CambiumOptimum'
PITH_OPTIMUM = 'PithOptimum'
PITH_MAXIMUM = 'PithMaximum'

# Statistics
RING_NAN = 'ring.NAN'
STAT_MEAN = 'Mean'
STAT_MEDIAN= 'Median'
STAT_MODE= 'Mode'
STAT_STD= 'STD'
STAT_VAR= 'Variance'
STAT_MIN= 'Minimum'
STAT_MAX= 'Maximum'
STAT_PERC35= 'Percentil 25'
STAT_PERC50= 'Percentil 50'
STAT_PERC75= 'Percentil 75'
STAT_SUM= 'Sum'
STAT_KURTOSIS= 'Kurtosis'
STAT_SKEWNESS= 'Skewness'
STAT_ENTROPY= 'Entropy'

components_index = [IDX_PARENT, IDX_CHILD]
components_dtype_dict = {
    OFFSET: 'Int32'
}
components_cols = list(components_dtype_dict.keys())
components_dtype = list(components_dtype_dict.values())

sequences_index = [IDX]
sequences_dtype_dict = {
    #SOURCE: 'string', LABs: 'string', 
    KEYCODE: 'string', PROJECT: 'string', 
    SPECIES: 'string', 
    CATEGORY: 'string', SUBCATEGORY: 'string', 
    DATE_BEGIN: 'Int32', DATE_END: 'Int32', 
    DATED: 'string', 
    SITE_LATITUDE: 'Float32', SITE_LONGITUDE: 'Float32', SITE_ELEVATION: 'Float32',
    SITE_CODE: 'string',
    PITH: 'boolean', 
    SAPWOOD: 'Int32', 
    CAMBIUM: 'boolean', 
    CAMBIUM_SEASON: 'string', 
    BARK: 'boolean', 
    CREATION_DATE: 'datetime64[ns]',
    DATE_SAMPLING : 'datetime64[ns]',
    LABORATORY_CODE : 'string',
    PERS_ID : 'string',
    BIBLIOGRAPHY_CODE : 'string',
    COMMENTS: 'string',
    URI: 'string',
    DATA_LENGTH : 'Int32', DATA_TYPE : 'string', DATA_VALUES : 'object',
    DATA_WEIGHTS : 'object', DATA_INFO : 'object',
    INCONSISTENT : 'boolean'
}

sequences_cols = list(sequences_dtype_dict.keys())
sequences_dtype = list(sequences_dtype_dict.values())

dtype_view = sequences_dtype_dict.copy()
dtype_view.update(components_dtype_dict)
dtype_view[ICON] = 'string'
dtype_view[IDX_CHILD] = 'Int32'
dtype_view[IDX_PARENT] = 'Int32'

COLUMN = 'ColumnName'
DATE = 'UpdateDate'
NEWVALUE = 'NewValue'
OLDVALUE = 'OldValue'
USERNAME = 'UserName'

log_dtype_dict = {
    DATE: 'datetime64[ns]',
    IDX_CHILD: 'Int32',
    IDX_PARENT: 'Int32',
    COLUMN : 'String',
    OLDVALUE : 'object',
    NEWVALUE : 'object',
    USERNAME : 'String',
    COMMENTS: 'string',
}

def category_utf8(category):
    if category == SET:
        return '\U0001F4C1' # file folder
    elif category == TREE:
        return '\U0001F33F' # mapple leaf, seedling, 1F331, herbe : 1F33F, 219F, 100C9
    elif category == CHRONOLOGY:
        return '\U0001F332' # Evergreen Tree 1F332, U0001F333 tree, 21C8

def category_html(row):
    if pd.notna(row[CATEGORY]):
        if row[CATEGORY] == TREE:
            #return '<img src="data:image/png;base64,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">'
            #return '<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAAsTAAALEwEAmpwYAAADAElEQVR4nO2VTUwTQRiGS0zUqwfj0RjjybsHPRCkM112ZqvpzhQlgASjiEYbqUGCoF4AiVECGiI/gYKlFbVEDYmI/AttQYQWCBoKB+NB48HEAxdtO2YWWqyFmtYljQlv8l5m0u995tuZrxrNlv5Hpaae2glEch4g0gf1xiWIjVNaRO6mCZn7Nz1ciwwHgJ76ACIs83RhoLD8Bss3FzNBnxkAiPwEIinYtHCEsnZBiX6UjDn+ey+fs64lb9gdHic7W1LKACLB9AyDvCkAAJFbENNgw1BPRHjITxemWfYFU1CH6RdBEHaoDgAx/VxQWr5ueMi13V28CyxdpIKq4UelE3t44ZvNDTEBOt+/VQC0iJhVC9eKNAdK9BsvXPPCERPAPuNWFwCIpIwXzLl4OVj/ujsizDbjZh1eZ8TanWedCgDAMlTj5Ijfav7UHD5P1Glb3QOsxTkQsXat/v5KBzAdTRMNe/8lP0WHqU/OO+Pnt1u55YsexbEAuhY9rMLaxpCc7YcS/SQIdHdC6SDDcISfpMreHi5uGR9ijSOvmHVqVOnIugCrbhzuYcLxLD/E1JEQgFaUr3CA9smRcNEnC1PMMjHE+BxoGullTW96NwTgLqmr5Z8jACS6L/4OILkKSjTo+K3lIT/+8I5ZJoYVkFgALa7BlZmASG4CAKSY/7hzfjJGwNoncCivwsXsc+Nrk9E3zSCmDCC5PH4ALMO/vftWDuDqZ7ZZN2se7VM60jb5Jrxv9ThXZwI1xQ1AKd0OMP2aazL7YwHwUO7msX5mn3VH7Fc8tCgAENFDcQNw8b9WXqDsQf2GAPwiPpqbiNqzeV3s2Mm8ANQbvfxJaxJUCkByB4cwVVYy26wrIsQ6Pab4z3AOZcw/FwCY/Ej49CFRSrcBRG7z5yTojYF889VgUXU1K66piTJfz71UFOTTE2DyXYsMOo1a0knyQYDkOojpPEB0WZn3UabLEBtngEgqEp6A8QiK8mFuTbIERNLHnUyAQe4tAE2ypBXpde6kAWxJo4J+AXBAUAopdYbCAAAAAElFTkSuQmCC">'
            #return '<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAACXBIWXMAAAsTAAALEwEAmpwYAAACTUlEQVR4nGNgGDHA3T1U3c0nuM07MGqlq29Yu4tXuCbVDHfzDk119Q79k1xa8ati0sT/KeWVv119Qv+4+4XnU2y4s0+gqZtv2O+JW9b9X3f3IhxP3bnpv7tf2G9XryA7iizw9Atflt/S+gfZcBgu6en55x0UvY1sw+39/QXc/cMfd65cimE4CPdtWP3fOzjqEVmGu/iE2nsEhL+PzSn4tuT8UbCBa26dB2OYBW3LFv33CY05TbLhbj5BGu5+4V9blyz4h+zixecO/1905jCcn9fa9tfDL+yRu2+wNkkWeARGrM1rbfsJMmT1zXP/V10/C7Hg7BEUC1ZeO/O/tL/vr7tf2Bc331AVogwPDQ1ldvMJ/T3v2F6wIcsvn/w/6+DO/wtOHgBjZAtgGJQIPAMitxNlgbt7uIKrd8i/tbcvwA1Ye/s82PUgi7BZMO/4/v+uPqF/Q0ND2QgHj0eoqKt3yP8VV05hGLToDCQO1t658H/J+WNg30GC8ex/V5+Q/27+4bJE+cIjIOIeKIVgWHD28P+5R/b8n3Vo1/+5x/f9X3XjDFh81sEd/0GZ0d4+noMoC1y9QhN8QmO+LT53BMOCOUf3/F9xFdV3KWUVv72CozYRZTiSL+b7hMd961q97P+qG5BUtPLKKTBGBNmh/2mV1X88/MLfEx08SIDR1Ssk3cM//AUo0j0DI3+i4ICIX1Dxfa6+oYqkGo5ikZtvqIqbd6ixs2dQMAiD2CBs7xMpwkBN4OId0gfCDLQCrl7B/SA8dC1w8Q5yB2GaWTAoAQAlbuaQkJCWkQAAAABJRU5ErkJggg==">'
            return '<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsTAAALEwEAmpwYAAABoElEQVR4nGNgQAKhqwo5Y2ZXqERNqxBMWlhuWLmxZ2rF+q65xauaFRkIgaxlTdodu2dcXXBm1ZdpRxa8WHR+5ddd9/f+B+HWHVNuFa1oLYtdWC6HVXN9fT1Txfruxbse7P2PFd/f+3/b3V3/px5d8LByfdeS0tXtSSiaazb17Vp2cd0PnAag4e49M26FrgplBhuQMK9UdeG5lV+J1QzCG29s+1u3pXcvKMwY4hZUSU8/tuAlKQaA8NY7O/+XrmutY6ja0D1px709JGmG4fpNfXMYqtZ3T9l5nzwDyjd0TWYoXNVUvPba5r+kal5/Y+vv8nWdNQyV6zr7N9/e/o9UAxadW/09fmalBkPazDTWxq0T96MrIOStvgOzb8TPr+cAR2XBqhbvKYfnP9l6Z9f/hWdXvu/dP+tGxcbuffOOL/oNSkCzTy1907dv1rWefbMugeiO3dNPlK7vDEBJjTmrqhULV7UX561oNIWJteb7n2toT72XtrxamWBewAb64x0OgTBZmlsCbY0mJjjdAGEQm2QDGkMtVnTH2C0GYRAbl0IAsZMayBZxUF0AAAAASUVORK5CYII=">'
        elif row[CATEGORY] == CHRONOLOGY:
            #return '<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsTAAALEwEAmpwYAAACT0lEQVR4nK2SX0hTYRjGB3ozmluLLMiCLrrIyyCpu3XWcbMxNJC12o0QEREVGEE6l2eU0ZjYH4OuyjBI8RCsnS2bJTubsoabK6MuCt1q1aanhu4PLqfpE+eMtmQZBr3wwve98Py+932+VyT639FqV241Mgca2xhC1UzvF+OFSAy3VA23rBG+DVv+KjYxysPUE3W6L3gJ3d7jMDHE+9T9qjgCNcBLEvDIU3BLGv4opmyKjWZnbfIdN4pkNo7Udw7Ot92g3foI0uPAQhTgaMArn8NzuawE0OY8SD4Ya8F0alIQ88llIjA5idzKrCcP4DO4D2BlZCmAISy211ZwmXABkMhE0fG0Hul4/xIWwnnAhAZgKyyr239Mbrvq0uYiiRD8bjuS2Rl8TXxAyP8MYx/tuOcxxJAK5gHpAOCtzIHdtL1onoOofzRxDZ+4N7jefAIDdyy4ffE0+m51YDYbA+VUYTHhWimM8UoFsNKjxfbtxLH+EIWZ9BTi3CSsZ5rQ29mOuflpYYx2J4mlxFDRh5AC8Er1RYBNtePKoOZHJDEuzN7bSWFkcEA4+8I07rKGONJjeXFyFBjZvIRhcdXqHXAQXT3+85j6FhBe5wHBKIMOl3Y5+eXhomDi7DAQ2At4pNaSX9DRurI2RnnZ5FBmzS0NONVFwmgnYp97dkaWh3YB/t28+/NgK8ygRWVrbiNFKyTGpjr3hbO1NxWsohysqNxk2HPjnLbGB7ZSsqbw92jVHaKNurqTv+78ma+tSyyYekRNmvSa6oI/ek01X1s34F/iJyxenjAzd/EKAAAAAElFTkSuQmCC">'
            #return '<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAAsTAAALEwEAmpwYAAAEvUlEQVR4nO2Wa0xTZxjHj3PZvtASdC67JO7DksVsS6aLyz64yXqQcZmRLROUiM7MkQyN4uLChB5AM3QQlDkzEcGFDDATNpCdgwwKelqg3ORioW4KpZSrYEsLFAaTwH85bznF0hWKsmRZfJInTduT5/97n9t5Keqx/dftYLH/08yv9F45R+fKOVk1w9GlcpY+Gc16rxOfAe+xDkrJN+AlCvBSNXjJZagkn0BLPfVI4rGsz1sMJ9MzHI35LmfpKYaVJU1kPl99P3fNDJRSODkv6QAv3fhQ4kyhzwaGlY0JYqfLQ6HW56GxuxjKtiykqw/aQSqyX2/7M2UtZqreAwyJQG8q0HYYqHppFkRiBe+5fkniwXnBK+UcrRUEfroRiw5TPYxjBoxMDNq9UpeLWM6HQBjVB6ywKIHJrjkf0wAN74qZ0ADUE+6fnpMFCoFPKj6CzlSHQavOQVz0X24mEoCC2og+GDlgQucIYW0EKp+bhZD6LwXgtBC47HY6AfgnccF1xgYCEFe0ZYoAjGsdAQTX7hJ7ItltADlHXxIC1xkK0TnU5BJgaLzX3gvTAoC12RlAd1QsQ84S6i+rt2UgA3pTvUsAvanJDjDenzcFcxkwaXAEuLVHBKhHHrXSnfTHCgETSrbizmAV+of/cAlgGutBhvoQAThVus1EyiDU/UGAwctAxbNiGeQLih8t8FnNcPSoEPBmbwm6LBqYrf2wjPU7p3+4h3warQYkKbYTiM7274YxVOKcha4kMQsjqJauWqD2snAh0PmKz9FurMG9EQMyE2PwY3KcA8QtTSVOfLYDrU0q8l3VnkMAzl0LHoCRBcbvzOuFTqDmVRuEymPfos2n1ueh09yIlkYezM4PEBMSgKxT8QRC26xC/O4PyW8XE74iAAOjunnN2OTcjG2Rizcjw9IqIUhLfzm6La0keM31QjvEheNf2sXPM4dhsnTZs3KiZBsBmLxbMI3ROmeA7hSxD5QLAMh4IUhrfzl6ZgEEr1NxYEK3EmHBU+WHYDTPidsAgmwAAwXTGKl3Buj5VszA9YUAcuwlmDf/pfmZRDxxf5jDycUSiGt50RIopVmuATjZp0KQC1UH0G6sxdB4t0MWBICzUfudJkJswrRrO+7amvC2o/iEHqh9TczAXrfGUNOrQLdFsyjAvVH93Bh2nB2xjWHXw42hYHJWxpBF9JttEfUN/+4SwGTtQkZ1JBFPUQSZYCxysYieEV9I0ZRbq5ilrwpBj18NQE1nPgzmZlTzVxwANL1lOMPvIeLHOPr+xED+NMzlc0toTAu0HwFUq8TTK8BTT1LuWHyet4ecpfPF2f66OBDnsiMIgPyLIISdoRFdaPsvoXDzsDlt7ehk+stASyig3Q000YBq9YM3o3zwazyoJRmoFUwRHcawtI5cwb73JQBHIt9HSLI3oq/I/mI42UXLDy/UTKS+OD1T6uV8JVNK2qGS7gKoFdSjWAxLvxkT75cuAETt8+sLz/BOjLj0jpedtczLE7zn9rjQNzRRH6/v+Jl5JQ1Kzw3Uclp0cGCIABAd7H/D1TNhm982hWzaiHDfTceWVdxdgJgQ/wbSJzv8g6n/IUCA76xAtmuAgGzhGXmI35ZlB3hs1L9kfwO2SghL5hSargAAAABJRU5ErkJggg==">'
            #return '<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAYAAAByDd+UAAAACXBIWXMAAAsTAAALEwEAmpwYAAAEQ0lEQVR4nO3VbUxbVRgH8O4l0Q3byQejM5EYp6jRRRe/uGVZ1xbCKpgQHYaoWUbiHJsz7kUN0MIdCQZwH5xGtxGcbpPNAXHgvYUBHX2hvHWW0A0GuLJBYS2wvgEW6AD3N+e0pbalo06/LPEkT9Le0/v87vPcc3p4vP8HeMsYNiEumxO+zNRuE4Q2BMrYNdDErIcuNg7gLbvvhqVVpK2QsZKDck40JOfEICFjxXNyVqyQ1ySsnzu7NhWqNfXQCOahEYCGmj8ENX8/Kngr/hHGqIUrZaz4V4IwNUn42cCgvCMfxcrtXpgTTdlK4hx3Tq0Fmp8GjFLAsAXQxnphjaAaat7KqEEZJzpMEpe2fAyTrR12txkTM2NwTVtR13MCuZwEBdXCiZlLO+bxRyfgMXvD0QDoX/FVK5BHW93DMlY0UVCXgn5bO2w+7O9R2fkFrdR0/eg4xrUB0GMGXGqg6TFAwx9HLe+hpatjEzaTZLXXvsOAsyMMI2F2XqVgZetuKxx1waDHDHRt91ap5W9aEpSz4lSSrMlUhiHXlUVBh3uYgsdV6SOwccDMQDDYl+lr6yOpUVQo+okku9hzDIPOzkXBYWc3chUSMIqEWc/ohT8x0RYMdqf7V235PbEcVvwmfXLdHtyw/wbnlGVRkEST6Syt8qTmXQvspMr+AOg2Au0v+dGUe1WnIkl6x3QYnTRBxZah71rbAjI+PQqu7BhuWXro95LmfRR1j5yfw6QhuMrRMj/YuCh2qD4xRs6KZ79W74TJ3o6e7hbkvCNF/s63KUqw898W0mvH8w5QsPVmJQWv9hba4dKELJ4BoPU5sj1mUf94TBiYzQpfIDdfMBZjwGGgCS+Wly6gp4pk9HNh5nswm7vpvOm2noL1hoMWOBvCV2vnNm+Vjfznw8CsGkk8ubnK+CVu+kAS9b/8SKEA1rUw5wcvdRyywqmMDKoFz0Zs6TeaDLrhSQv9ib8v+JyC3Z3aoIXT4mtpV1+RHS5teEtb1nlb2spbteh7lHPiRpKgb6wZI5PXFxKfPsJQ8PdefRB4QrfXu2isFfNhi2bkjO9/la+MuErlnOgNui2aMnHDfhmOqeGI4MK2UL9vhV0Rsi2uAG0v+kFpRNBX5TmaqG0/TDY9bO7BINA5bUFDbwnyFAk4zCV67oyRjd8ewJxKQL/BvyXKeEuNAxWvrwocTYmoMhbjaP6HFGTOZCCvKpVWVlAtnLr9Q7xrXpcBDBYB/TLvMaV5NHBERXp3oYNhmOUyTrRHxoksJHnOZ0kU3PHVVnxybutd8kD2k091eUqfvAuV7/ANxC1oBbsB3vKosFA4l5VszPkg6TIB9x6RlH50WhLvn4d69RNV+es+3Ze8YSg3/VUdNPyN9wWFjuw0aQUBs9KSXwud2yXdIs0Qb8KuxM36fw1FA5JrZI785sEFs95KfoYkZlJSVofOkWtkjvzmPwMf6PEXHiK4cyqCqI4AAAAASUVORK5CYII=">'
            # 24 : return '<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAACXBIWXMAAAsTAAALEwEAmpwYAAADaElEQVR4nN2US0xTQRSGr4obta3GhejChXFnXPhYgvTeQkONcWFCEwOJLhSNaGI0Pugt1mrSJiAYXxEDIUaNIkos95Z0AXIBNaKSChUVFIUCWmqhD5ReIshvZnhIbQEfG+NJzmJmkv+b858zwzD/bRy3JyzhBW6PUeDOG0XOmiOoNWQfYOZAUiWjVmGFpDyHWlUmJNXi3xLn7ZpUXmD7jSKHiBTYqs9FK3q+ORYDtcqp2Yc6pfaXxI2VyWuNIhc+J+1Ei6cGH4OtcPtdsDWfQY5dg3s317UPV28HQo+ALy3AhyLg0WpAUoZxf+Ga2QECV2Z2pKLd1wD/YA9CsncybU15tJJBz50RDL4Ehtxj6a8C6pYCkqJ0doDI9t19bkGX3xUhHpK9cPc3U0BbW34AA89+AEg6k4lVvhnFMxs3zDeK7Ijj5UX0BFuiAJ8G3lPAE9cJL4L1kYAXegIYQSMzf4bbc1Yi8LijHJ6BtpiAgvvpOFWplYe9ttEIm9qPjDdcYYkpbnAkLjcK7NDdJiu6As3o6GhGMNw7Kd7d/Qp9oR688zlhqkxBjfPoRwTqplTRCTxPIRAZ0oL4KECOnc2k/nof4u27pzi5YxtuXbBQSGenC9a96SixZlPYtSfZtAr47GPCExDvrbEqJNXuGNPDniUAMj2BcC9KL1hg0Otw7YyJipsytsLVWEMBVa3FtBfDnypGIbf/AAy+Ggco82NNT/4EgNyaZFlhLoVMFSdZ3VZCASPTAWqVeTNa5PvSSYUIhABuX7JGNJtYZK7UhqMtKh2vYNGuKIDJnhTPC5x822lGV6BpUsyg16Hscu7kmjbZrkWd85gnqsljb0FG9cJlMSeJFzgLqaL+7Q18CL5GSO6NAHT7W1BQk0FvP+ytGKWWEHH5PdC6b2JMT0/7DkxSUhwvsvcI5GrDETR2iRRwseAgiiQDzI7NMFeohzy2FP+ouwTw2QB3HvBs47g1inKUMfOmBVCIyTSXFzSHeJHzERAB7DdrsKdYDaPIPugrXvnm6/V4MilTf1MfJMVBgJnL/GqQbyNH5BIJ4HCWtn5vyabEiTM8UK06nraualfy+l5IixIgMXHMn4ZBr4MhTVf48/6BLeryrM1q/LHwbIBsve4KOftrQLZed4XXp6ZH7aelZpCzvwb88/EdVLJ0za1avWQAAAAASUVORK5CYII=">'
            if not row[INCONSISTENT]:
                return '<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsTAAALEwEAmpwYAAACQElEQVR4nGNgQAKhqwo5Y2dVqJWsaAxu3dQ6v3JNfRnDfwZGmHzCvHJdBlwgd3Gl1qRdnVc3nJ/2dful6V/PPVj4f/e1Wb/KVzcsL1lVlxs/v16gaHXbnYzFNepYDWja1DILpAkdH7s9D4yr17Xe33hj29/azb2LMDQ3bmpumrK36zo2A2C4eWvP35339/xv2j7xbtKcUl645vj55QqrTk9+j08zCLdu7/u868He/917Z1zMnZjLDjcgbUGJ8oqTE9/h07zt0sz/i86u+gsyYOOtbf/K1nXUww1o2NA8+cy9BXhtn7q///+6a5v/gwzYdnfn/9K1nYfhBtSvb5py9j5+A2Yfnvx/651dYANAuGHrhN1wA0pX1RXvvTb7Ly7Nu67M+r/wzDK4ZhBec23zz7K1bXlgA2rWN0wHRRMuAybv6/+/8vJ6FAPWXd/yu3Rt+xFwIoufX89RsKxu/qEbc/5hM2DrpZn/l5xfhWLAppvb/pat76hFpMKJueztW1sOHLwx+9+BG7P/Td7c/H3/9dn/91+f87d1x8RPyJphuHf/7JtpM8v5EdE5M421eGVdPAj3Jjkdaa6PupGzvLaqbefUBxtvbUfRDIqJyYfnvcxZ3piDNVn3xzscAmGIweX8ecub0mqXNq7snln6v25W+dni1e3l6QuqpLFqbgm0NZqY4HQDhEFsqDBjY6hl24Icr/+t4dZb6+3tObBqBueLUIsV3TF2i0EYxAaJ1QZZWLdEWK8HibVF2axpCLVIhmkAAPbPI+veSxwUAAAAAElFTkSuQmCC">'
            else:
                return '<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsTAAALEwEAmpwYAAACPElEQVR4nGNgQAKhqwo5Y2dVqNUuSgqevCJsfvOyxDKG/wyMMPm0mYW6DLhA8dxcrWXrvK9e3mn49fYe7a9/jkj+f7RX7VfjkoTlDYuTcuPn1wuUz429kz8nQx2rARNXhM8CaULHHw/Kg3Hroqj7h+eJ/W2ZHbgIQ3P/iqimVes9rmMzAIb7FgX8PTeP53/XHJ+7SXNKeeGa4+eXK5zabvoen2YQnrDQ5/P5edz/p8xxvpg7MZcdbkDaglzlY9st3uHTfHOXzv9N89T/ggw4Olf4X9WciHq4AX0roib/PCyN1/aVa1z+H5gv9R9kwMl5Av+r5kQdhhvQuyJyyq8jUngN2LjWDqwRZAAIt8/x3w03oGFJcvHTfWp/cWm+v0fj/6aFOnDNILxvrtTPqrlReWADOpZHT/9wUAGn7ctWuf7fM18BxYBD8yR+V82JPgJOZPHz6zkqFqbNf71f6R82A67v0vm/fb4qigFH5on+rZobWQv3Ru7EXPbpq4MPvNqv9O/lfuV/K5a5f3++T+X/i/2qfycu8PqErBmGZ8y1u5k2s5wfEZ0z01irF6fFg3BvktOR9lr/G0UL0qr657o/ODJPFEUzKEDnzzV7WTg7OQdrsu6PdzgEwhCDy/mLZyemNU7yWzmhy/t/c4fX2Yo5ceXpCwqlsWpuCbQ1mpjgdAOEQWyoMGNjqGXbghyv/63h1lvr7e05sGoGgcZQixXdMXaLQRjEBonVBllYt0RYrweJtUXZrGkItUiGaQAAqI/Yr37DSpMAAAAASUVORK5CYII=">'
        elif row[CATEGORY] == SET: 
            return '<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAb0lEQVR4nO2SMQqAMAxFi7uLnf6jt1U8iCfxWLpYKThYOtgogoMfMmTIyyf5zn1CwChpBSKwAbP3vq0GSFpDCN3RNsCUoBYH0VJpoaQhAziDkltJy21AMcMPcI9voDxIlyremEJxinJtkHqr63e0AxiSQjEOWJW+AAAAAElFTkSuQmCC">'
    return ''

