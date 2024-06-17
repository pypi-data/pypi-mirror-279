"""
File Name: tabulator.py
Author: Sylvain Meignier
Organization: Le Mans Université, LIUM (https://lium.univ-lemans.fr/)
Creation Date: 2023-12-03
Description: panel to select path
This file is governed by the terms of the GNU General Public License v3.0.
Please see the LICENSE file for more details.
"""
import numpy as np
import pandas as pd
import panel as pn
from bokeh.models.widgets.tables import (NumberFormatter, DateFormatter, 
                                         SelectEditor, NumberEditor)

from pyDendron.dataname import *

def _cell_transform(data):
    if data is None:
        return data
    data_out = pd.DataFrame()
    for col, dtype in data.dtypes.to_dict().items():
        if col not in [ICON, IDX, IDX_CHILD, IDX_PARENT]:                    
            if str(dtype).lower().startswith('int'):
                data_out[col] = data[col].fillna(np.nan).astype('float')
            elif str(dtype).lower().startswith('float'):
                data_out[col] = data[col].fillna(np.nan).astype('float')
            elif str(dtype).lower().startswith('bool'):
                data_out[col] = data[col].astype('string').fillna('unk').str.lower()
            elif str(dtype).lower().startswith('string'):
                data_out[col] = data[col].fillna('')
            else:            
                data_out[col] = data[col]
        else:            
            data_out[col] = data[col]
    return data_out
            
def _cell_text_align(dtype_dict):
    aligns = {} 
    for key, dtype in dtype_dict.items():
        aligns[key] = 'left' if (dtype == 'string') or (dtype == 'object') else 'center' 
    if ICON in aligns:
        aligns[ICON] = 'center'
    return aligns

def _cell_formatters(dtype_dict):
    formatters = {} 
    for key, dtype in dtype_dict.items():
        if dtype == 'int': formatters[key] = NumberFormatter(format='0')
        if dtype == 'Int32': formatters[key] = NumberFormatter(format='0')
        if dtype == 'float32': formatters[key] = NumberFormatter(format='0.000')
        #if dtype == 'boolean': formatters[key] = StringFormatter(nan_format = '-') #BooleanFormatter() #{'type': 'tickCross', 'allowEmpty': True, 'tickElement': "<i class='fa fa-check'></i>",'crossElement':"<i class='fa fa-times'></i>"} #BooleanFormatter(icon='check-square')
        if dtype == 'datetime64[ns]': formatters[key] = DateFormatter()
    if ICON in dtype_dict:
        formatters[ICON] = {'type': 'html'}
    return formatters

def _header_filters(dtype_dict):
    filters = {}
    for key, dtype in dtype_dict.items():
        if key != ICON:                
            if dtype == 'string': filters[key] =  {'type': 'input', 'func': 'like', 'placeholder': 'Like..'}
            if dtype == 'boolean': filters[key] = {'type': 'list', 'valuesLookup': True}
            if dtype == 'Int32': filters[key] = {'type': 'number', 'func': '=='}
            if dtype == 'float32': filters[key] = {'type': 'number', 'func': '=='}
    return filters

def _header_filters_lookup(dtype_dict):
    filters = {}
    for key, dtype in dtype_dict.items():
        if dtype == 'string': filters[key] =  {'type': 'list', 'func': 'in', 'valuesLookup': True, 'sort': 'asc', 'multiselect': True}
        if dtype == 'boolean': filters[key] = {'type': 'list', 'valuesLookup': True}
        if dtype == 'Int32': filters[key] = {'type': 'number', 'func': '=='}
        if dtype == 'float32': filters[key] = {'type': 'number', 'func': '>='}
    return filters


def _cell_editors(dtype_dict, edit=False):
    if edit == False:
        editors = {x:None for x in dtype_dict.keys()}
    else:
        editors = {}
        for key, dtype in dtype_dict.items():
            editors[key] = None
            if dtype == 'string': editors[key] =  {'type': 'list', 'valuesLookup': True, 'autocomplete':True, 'freetext':True, 'allowEmpty':True, }
            if dtype == 'Int32': editors[key] = NumberEditor(step=1) 
            if dtype == 'Float32': editors[key] = NumberEditor() 
            if dtype == 'boolean': editors[key] = SelectEditor(options=['true', 'false', 'unk'])
            if dtype == 'datetime64[ns]': editors[key] = 'date'
        if CATEGORY in dtype_dict:
            editors[CATEGORY] = SelectEditor(options=[SET, CHRONOLOGY, TREE])
        for col in [ICON, IDX, IDX_CHILD, IDX_MASTER]:
            if col in dtype_dict:
                editors[col] = None            

    return editors

def tabulator(data):    
    return pn.widgets.Tabulator(data.reset_index(),
        pagination='local',
        header_filters=True, 
        sizing_mode='stretch_width',
        ) 

def _hidden_columns( columnList=[ICON, KEYCODE, DATE_BEGIN, DATE_END, OFFSET], dtype_view=dtype_view):
    return list(set(dtype_view.keys()) - set(columnList)) 
        
# def _tabulator_columns(columnList=[ICON, KEYCODE, DATE_BEGIN, DATE_END, OFFSET], title='Dataview options'):
#     wchoice = pn.widgets.MultiChoice(name='Columns', value=columnList, options=list(dtype_view.keys())+['Index'], sizing_mode='stretch_width')

#     card = pn.Card(wchoice, 
#                     title=title, 
#                     sizing_mode='stretch_width', margin=(5, 0),
#                     collapsed=True)  
    
#     return wchoice, card
