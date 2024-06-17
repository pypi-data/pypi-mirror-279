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
import warnings
from panel.viewable import Viewer

from pyDendron.app_logger import logger

from pyDendron.dataname import *
from pyDendron.gui_panel.tabulator import (_cell_text_align, _cell_editors, _header_filters, _cell_formatters, 
                                           _hidden_columns)

class DatasetPackageBuilder(Viewer):
    selection = param.List(default=[], doc='path')

    def __init__(self, treeview, **params):
        bt_size = 80
        super(DatasetPackageBuilder, self).__init__(**params)   

        self.treeview = treeview
        self.treeview.wcolumn_selector.param.watch(self.sync_columns, ['value'], onlychanged=True)

        self.wpath = pn.Row()
        self.treeview.wpath.param.watch(self.sync_path, ['objects'], onlychanged=True)
        
        self.dataset = self.treeview.dataset
        
        self.wcolumns = pn.widgets.AutocompleteInput(name='Column', min_characters=0, options=list(sequences_dtype_dict.keys()), placeholder='Select a column', width=bt_size*2)
        self.wcolumns.param.watch(self.sync_wvalue, ['value'], onlychanged=True)
        self.woperator = pn.widgets.Select(name='operator', options=['==', '>', '<', '!=', 'contains' ], width=bt_size*2)
        self.wvalue = pn.widgets.AutocompleteInput(name='value', min_characters=0, restrict=False, options=[], placeholder='Enter a value', width=bt_size*2)
        self.bt_and_add = pn.widgets.Button(name='And ...', icon='logic-and', button_type='primary', width=int(1.5*bt_size), align=('start', 'end'))
        self.bt_and_add.on_click(self.on_add_and)
        self.bt_or_add = pn.widgets.Button(name='Or ...', icon='logic-or', button_type='primary', width=int(1.5*bt_size), align=('start', 'end'))
        self.bt_or_add.on_click(self.on_add_or)

        self.wfilter = pn.widgets.TextAreaInput(name='Filter', value=f'(`{CATEGORY}` != "{SET}")', height=60, sizing_mode='stretch_width')

        self.bt_select = pn.widgets.Button(name='Append', icon='table-plus', button_type='primary', width=int(1.5*bt_size), align=('start', 'center'))
        self.bt_select.on_click(self.on_select)
        self.rb_append_mode = pn.widgets.RadioBoxGroup(name='Append mode', options=['empty table', 'current table'], inline=True, align=('start', 'center'))
        self.tg_level = pn.widgets.RadioBoxGroup(name='Level', value='current level', options=['current level', 'all descendants'], inline=True, align=('start', 'center'))

        self.wtabulator = pn.widgets.Tabulator(pd.DataFrame(columns=list(dtype_view.keys())), name='Result',                 
                hidden_columns=_hidden_columns(self.treeview.wcolumn_selector.value), 
                pagination='local',
                selectable='checkbox', 
                sizing_mode='stretch_width',
                text_align=_cell_text_align(dtype_view),
                editors=_cell_editors(dtype_view), 
                header_filters=_header_filters(dtype_view), 
                formatters=_cell_formatters(dtype_view),
                min_height=300,
                page_size=1000,
                max_height=300,
                height_policy='max',
                )
        self.bt_erase = pn.widgets.Button(name='Remove row', icon='eraser', button_type='primary', width=int(1.5*bt_size), align=('start', 'end'))
        self.bt_erase.on_click(self.on_erase)
        
        self.bt_save = pn.widgets.Button(name='Save', icon='file', button_type='primary', width=bt_size, align=('start', 'end'))
        self.bt_save.on_click(self.on_save)
        self.wselection_name = pn.widgets.TextInput(name='', width=bt_size*2)
        
        
        self._layout = pn.Column(
                        self.wpath,
                        pn.Row(self.wcolumns, self.woperator, self.wvalue, self.bt_and_add, self.bt_or_add), 
                                self.wfilter, #title='Select', collapsed=True, sizing_mode='stretch_width'),
                        pn.Row(self.bt_select, 
                               pn.pane.HTML('<b>In:</b>', align=('start', 'center')), self.rb_append_mode, 
                               pn.pane.HTML('<b>From:</b>', align=('start', 'center')), self.tg_level),
                        self.wtabulator, 
                        self.bt_erase,
                        pn.Row(self.bt_save, self.wselection_name),
                        )

    def __panel__(self):
        return self._layout
    
    def sync_path(self, event):
        self.wpath.objects = self.treeview.wpath.objects
        
    def sync_columns(self, event):
        #self.wcolumns.options = self.treeview.wcolumn_selector.value
        self.wtabulator.hidden_columns = _hidden_columns(self.treeview.wcolumn_selector.value)

    def build(self):
        return self.wtabulator, self._layout 

    def sync_wvalue(self, event):
        if event.new != '':
            try:
                self._layout.loading = True
                if event.new not in [DATA_INFO, DATA_VALUES, DATA_WEIGHTS]:
                    lst = self.treeview.data[event.new].dropna().unique().tolist()
                    if dtype_view[event.new] != 'string':
                        #lst = [str(x) for x in lst]
                        self.wvalue.options = []
                    else:
                        self.wvalue.options = lst
            except Exception as inst:
                logger.error(f'sync_wvalue: {inst}', exc_info=True)
                self.wvalue.options = []
            finally:
                self._layout.loading = False

    def on_save(self, event):
        def nan_(df, key):
            mask = df[key].isna()
            return df.index[mask].to_list()
        
        def get_missing_keycodes(df, key):
            mask = df[key].isna()
            return df.loc[mask, KEYCODE].to_list()
        
        if self.wselection_name.value == '':
            logger.warning(f'Selection name is empty')
        else:
            try:
                df = self.wtabulator.value.set_index([IDX_PARENT, IDX_CHILD])
                paires = df.index.tolist()            
                missing_date_begin = nan_(df, DATE_BEGIN)
                if len(missing_date_begin) > 0:       
                    logger.warning(f'{DATE_BEGIN} is missing for {get_missing_keycodes(df, DATE_BEGIN)}')
                missing_offset = nan_(df, OFFSET)
                if len(missing_offset) > 0:       
                    logger.warning(f'{OFFSET} is missing for {get_missing_keycodes(df, OFFSET)}')
                missing_ring_values = nan_(df, DATA_VALUES)
                if len(missing_ring_values) == 0:      
                    self.dataset.set_package(self.wselection_name.value, paires)
                    #self.wselection_name.options = self.dataset.package_keys()
                    self.dataset.dump()
                    logger.info(f'Save selection')
                else:
                    logger.error(f'Selection is not save, missing {DATA_VALUES} for {get_missing_keycodes(df, DATA_VALUES)}')
            except Exception as inst:
                logger.error(f'on_save: {inst}', exc_info=True)
            
    def on_add_filter(self):
        if dtype_view[self.wcolumns.value] == 'string':
            if self.woperator.value == 'contains':
                self.wfilter.value += f'(`{self.wcolumns.value}`.str.contains("{self.wvalue.value}"))'
            else:
                self.wfilter.value += f'(`{self.wcolumns.value}` {self.woperator.value} "{self.wvalue.value}")'
        else:
            if self.woperator.value != 'contains':
                self.wfilter.value += f'(`{self.wcolumns.value}` {self.woperator.value} {self.wvalue.value})'
        
    def on_add_and(self, event):
        self.wfilter.value += ' and '
        self.on_add_filter()
        
    def on_add_or(self, event):
        self.wfilter.value += ' or '
        self.on_add_filter()
    
    def on_erase(self, event):
        try:
            self._layout.loading = True
            self.wtabulator.value = self.wtabulator.value.drop(self.wtabulator.selected_dataframe.index.to_list())
        except Exception as inst:
            logger.error(f'on_erase: {inst}', exc_info=True)
            self.wtabulator.value = pd.DataFrame(columns=list(dtype_view.keys()))
        finally:
            self.wtabulator.selection = []
            self._layout.loading = False

    def get_descendants(self, groups, groups_all, idx_parent):
        lst = []
        if idx_parent in groups.groups:
            for idx_parent, idx_child in groups.get_group(idx_parent).index:
                lst += self.get_descendants(groups, groups_all, idx_child)
        
        if idx_parent in groups_all.groups:
            lst += groups_all.get_group(idx_parent).index.to_list()

        return lst

    def on_select(self, event):
        try:
            self._layout.loading = True
            res = None
            # if self.tg_level.value == 'Roots':
            #     if self.wfilter.value == '':
            #         logger.warning('on_select: empty filter, inconsistent query')
            #     else:
            #         res = self.treeview.data.query(self.wfilter.value)
            #         self.wselection_name.value = 'Roots: '+self.wfilter.value
            # el
            if self.tg_level.value == 'current level':
                res = self.treeview.wtabulator.value.set_index([IDX_PARENT, IDX_CHILD])
                if self.wfilter.value != '':
                    res = res.query(self.wfilter.value)
                self.wselection_name.value = self.wpath.objects[-1].name
            else:
                if len(self.treeview.path) == 0:
                    logger.warning('on_select: path is root')
                else:
                    idx_parent = self.treeview.path[-1]
                    #idxs = list(set(self.dataset.get_descendants(idxs=idx_parent).filter().keys()))
                    res = self.dataset.get_data(idx_parent, include_parent=False)
                    #print(res)
                    #res = self.treeview.data.loc[self.treeview.data.reset_index()[IDX_CHILD].isin(idxs)].query(self.wfilter.value)
                    
                    if self.wfilter.value != '':
                        res = res.query(self.wfilter.value)
                    if self.rb_append_mode.value ==  'empty table':
                        self.wselection_name.value = self.wpath.objects[-1].name
                    else:
                        self.wselection_name.value = f'{self.wselection_name.value} + {self.wpath.objects[-1].name}'
            if res is not None:
                if self.rb_append_mode.value ==  'empty table':
                    self.wtabulator.value = self.treeview.data.loc[res.index.to_list(), :].reset_index()
                else:
                    with warnings.catch_warnings():
                        # TODO: pandas 2.1.0 has a FutureWarning for concatenating DataFrames with Null entries
                        warnings.filterwarnings("ignore", category=FutureWarning)
                        self.wtabulator.value = pd.concat([self.wtabulator.value, self.treeview.data.loc[res.index.to_list(), :].reset_index()])
            else:
                logger.warning('on_select: empty result')
        except Exception as inst:
            logger.error(f'on_select: {inst}', exc_info=True)
            self.wtabulator.value = pd.DataFrame(columns=list(dtype_view.keys()))
            
        finally:
            self._layout.loading = False
