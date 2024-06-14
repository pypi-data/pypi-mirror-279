"""
File Name: dataset_tabulator_filter.py
Author: Sylvain Meignier
Organization: Le Mans Université, LIUM (https://lium.univ-lemans.fr/)
Creation Date: 2023-12-03
Description: fontend application based on sidecar
This file is governed by the terms of the GNU General Public License v3.0.
Please see the LICENSE file for more details.
"""

import pandas as pd
import param
import panel as pn
from panel.viewable import Viewer

from pyDendron.app_logger import logger
from pyDendron.gui_panel.dataset_package import DatasetPackage
from pyDendron.dataname import *
#from pyDendron.gui_panel.tabulator import (_cell_text_align, _cell_editors, _header_filters, _cell_formatters, 
#                                           _hidden_columns)

class DatasetPackageEditor(Viewer):
    selection = param.List(default=[], doc='path')

    def __init__(self, dataset, param_column, param_package, **params):
        bt_size = 150
        super(DatasetPackageEditor, self).__init__(**params) 
        
        self.dataset = dataset
        
        self.package = DatasetPackage(dataset, param_column, param_package)
        self.panel_tabulator = self.package.panel_tabulator
        self.wselection_name = self.package.wselection_name
        self.wtabulator = self.package  .wtabulator
        
        self.bt_remove = pn.widgets.Button(name='Delete package', icon='file-off', button_type='primary', width=bt_size, align=('start', 'end'))
        self.bt_remove.on_click(self.on_remove)
        self.bt_erase = pn.widgets.Button(name='Remove row', icon='eraser', button_type='primary', width=bt_size, align=('start', 'end'))
        self.bt_erase.on_click(self.on_erase)
        
        #self.bt_save = pn.widgets.Button(name='Save', icon='file', button_type='primary', width=bt_size, align=('start', 'end'))
        #self.bt_save.on_click(self.on_save)

        self._layout = pn.Column(self.package, 
                                 pn.Row(self.bt_erase, self.bt_remove))#, self.bt_save))
        #self.dt_info.visible = True
        self.panel_tabulator.collapsed = False
        
    def __panel__(self):
        return self._layout

    def on_remove(self, event):
        if self.wselection_name.value != '':
            self.dataset.delete_package(self.wselection_name.value)
            #self.sync_dataset(event)
            #self.wtabulator.value = pd.DataFrame(columns=list(dtype_view.keys()))
    
    # def on_save(self, event):
    #     def nan_(df, key):
    #         mask = df[key].isna()
    #         return df.index[mask].to_list()
        
    #     def get_missing_keycodes(df, key):
    #         mask = df[key].isna()
    #         return df.loc[mask, key].to_list()
        
    #     if self.wselection_name.value == '':
    #         logger.warning(f'on_save : selection name is empty')
    #     else:
    #         try:
    #             df = self.wtabulator.value.set_index([IDX_PARENT, IDX_CHILD])
    #             paires = df.index.tolist()            
    #             missing_date_begin = nan_(df, DATE_BEGIN)
    #             if len(missing_date_begin) > 0:       
    #                 logger.warning(f'on_save : {DATE_BEGIN} is missing for {get_missing_keycodes(df, DATE_BEGIN)}')
    #             missing_offset = nan_(df, OFFSET)
    #             if len(missing_offset) > 0:       
    #                 logger.warning(f'on_save : {OFFSET} is missing for {get_missing_keycodes(df, OFFSET)}')
    #             missing_ring_values = nan_(df, DATA_VALUES)
    #             if len(missing_ring_values) == 0:     
                     
    #                 self.dataset.set_package(self.wselection_name.value, paires)
    #                 #self.wselection_name.options = list(self.dataset.selections.keys())
    #                 self.dataset.dump()
    #                 logger.info(f'Save selection')
    #             else:
    #                 logger.warning(f'on_save : Selection is not save, missing ring values for {get_missing_keycodes(df, DATA_VALUES)}')
    #         except Exception as inst:
    #             logger.error(f'on_save: {inst}', exc_info=True)
            

    def on_erase(self, event):
        try:
            self._layout.loading = True
            self.wtabulator.value = self.wtabulator.value.drop(self.wtabulator.selection)
        except Exception as inst:
            logger.error(f'on_erase: {inst}', exc_info=True)
            self.wtabulator.value = pd.DataFrame(columns=list(dtype_view.keys()))
        finally:
            self.wtabulator.selection = []
            self._layout.loading = False
