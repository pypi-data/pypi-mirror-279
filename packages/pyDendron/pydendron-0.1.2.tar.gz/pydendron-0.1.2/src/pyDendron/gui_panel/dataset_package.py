"""
File Name: dataset_tabulator.py
Author: Sylvain Meignier
Organization: Le Mans Université, LIUM (https://lium.univ-lemans.fr/)
Creation Date: 2023-12-03
Description: fontend application based on sidecar
This file is governed by the terms of the GNU General Public License v3.0.
Please see the LICENSE file for more details.
"""
import pandas as pd
import param
import numpy as np
import panel as pn
from panel.viewable import Viewer

from pyDendron.app_logger import logger
from pyDendron.dataname import *
from pyDendron.gui_panel.tabulator import (_cell_text_align, _cell_editors, _header_filters,
                                           _cell_formatters, _hidden_columns)


class DatasetPackage(Viewer): 
    dt_data = param.DataFrame()
    dt_param = {}
    VALUES_PER_LINE = 20
          
    def __init__(self, dataset, param_column, param_package, param_detrend=None, param_chronology=None, title='', **params):
        super(DatasetPackage, self).__init__(**params)   

        self.param_package = param_package
        self.param_package.param.watch(self._sync_dt_data,  ['show_data'])

        self.param_detrend = param_detrend
        if self.param_detrend is not None:
            self.param_detrend.param.watch(self._sync_dt_data,  ['detrend', 'window_size', 'log'])
        
        self.param_chronology = param_chronology
        if self.param_chronology is not None:
            self.param_chronology.param.watch(self._sync_dt_data,  ['biweight_mean', 'date_as_offset'])

        self.param_column = param_column
        self.wcolumn_selector = self.param_column.columns
        self.wcolumn_selector.param.watch(self.sync_columns, ['value'], onlychanged=True)

        self.dataset = dataset
        self.dataset.param.watch(self.sync_dataset,  ['notify_reload', 'notify_synchronize', 'notify_packages'])

        self.title = title
                
        self.wselection_name = pn.widgets.Select(name='Name: '+self.title, options=[])
        self.wselection_name.param.watch(self.sync_data,  ['value'])

        self.wtabulator = pn.widgets.Tabulator(pd.DataFrame(columns=list(dtype_view.keys())),
                                    hidden_columns=_hidden_columns(), 
                                    text_align=_cell_text_align(dtype_view),
                                    editors=_cell_editors(dtype_view), 
                                    header_filters=_header_filters(dtype_view), 
                                    formatters=_cell_formatters(dtype_view),
                                    pagination='local',
                                    page_size=100000,
                                    #pagination=None,
                                    selectable='checkbox', 
                                    sizing_mode='stretch_width',
                                    max_height=600,
                                    min_height=400,
                                    height_policy='max',
                                    row_content = self.get_row_content,
                                    embed_content=True) 
        
        self.panel_tabulator = pn.Card(self.wtabulator, margin=(5, 0), collapsed=True, 
                                       sizing_mode='stretch_width', 
                                       title='Data '+self.title, collapsible=True, max_height=600)
        
        stylesheet = 'p {padding: 0px; margin: 0px;}'
        self.dt_info = pn.pane.Alert('Detrend data is empty set', margin=(0, 0, 5, 5), align=('start', 'end'), stylesheets=[stylesheet])
        
        self._layout = pn.Column(pn.Row(self.wselection_name, self.dt_info), self.panel_tabulator)

    def clone(self, title=''):
        return DatasetPackage(self.dataset, param_column=self.param_column, param_package=self.param_package, param_detrend=self.param_detrend, param_chronology=self.param_chronology, title=title)

    def get_row_content(self, series):
        def array2html(v):
            l = len(v)
            nl = (l + 1) // self.VALUES_PER_LINE + 1
            tmp = np.array([0.0] * nl * self.VALUES_PER_LINE, dtype=object)
            tmp[0:l] = v
            tmp[tmp == 0] = pd.NA
            tmp[len(v)] = ';'
            c = list(range(0, nl * self.VALUES_PER_LINE, self.VALUES_PER_LINE))
            #print(tmp.reshape(-1, self.VALUES_PER_LINE).T)
            return pd.DataFrame(tmp.reshape(-1, self.VALUES_PER_LINE).T, columns=c).T.style.format(precision=2)
        
        try:
            if self.param_package.show_data:
                lst = []
                if series[DATA_VALUES] is not None:
                    lst.append((RAW, array2html(series[DATA_VALUES])))
                    if self.dt_data is not None:
                        dt_type = self.dt_data.at[series.name, DATA_TYPE]
                        if dt_type != RAW:
                            lst.append((dt_type, array2html(self.dt_data.at[series.name, DATA_VALUES])))
                return pn.Tabs(*lst)
            return pn.pane.Markdown('Show data desactivated in detrend card.')
        except Exception as inst:
            logger.error(f'get_row_content: {inst}', exc_info=True)
            return pn.pane.Markdown('No detrend data.')
        return pn.pane.Markdown('Detrend param is missing')
        
        #a = self.dt_data.at[idx, DATA_VALUES]
        #pn.pane.HTML(f'<span>{self.dt_data.at[idx, DATA_TYPE]}: {a}</span>')        

    def __panel__(self):
        return self._layout

    def sync_columns(self, event):
        self.wtabulator.hidden_columns = _hidden_columns(self.wcolumn_selector.value)

    def sync_dataset(self, event):
        lst = self.dataset.package_keys()
        logger.debug(f'sync_dataset  {self.title}, {lst}')
        self.wselection_name.options = ['None']+lst
        self.wtabulator.value = pd.DataFrame(columns=list(dtype_view.keys()))

    def sync_data(self, event):
        try:
            self._layout.loading = True
            if self.wselection_name.value != 'None':
                #print(self.wchoice.value)
                data = self.dataset.get_package_components(self.wselection_name.value).reset_index()
                data.insert(len(data.columns)-1, OFFSET, data.pop(OFFSET))
                data.insert(2, ICON, data.apply(lambda x: category_html(x), axis=1))
                data = data.sort_values(by=IDX_PARENT)
                self.wtabulator.hidden_columns = _hidden_columns(self.wcolumn_selector.value)
                self.wtabulator.value = data
                self._sync_dt_data(event)
            else:
                data = pd.DataFrame(columns=list(dtype_view.keys()))
                self.wtabulator.value = data
        except Exception as inst:
            logger.error(f'sync_data: {inst}', exc_info=True)
            data = pd.DataFrame(columns=list(dtype_view.keys()))
            self.wtabulator.value = data
        finally:
            self._layout.loading = False
    
    def _sync_dt_data(self, event):
        def get_dt_param():
            dt_param = {}
            if self.param_detrend is not None:
                dt_param[DETREND] = self.param_detrend.detrend
                dt_param[DETREND_WSIZE] = self.param_detrend.window_size
                dt_param[DETREND_LOG] = self.param_detrend.log
                dt_param[CHRONOLOGY_DATE_AS_OFFSET] = self.param_chronology.date_as_offset
                dt_param[CHRONOLOGY_BIWEIGHT_MEAN] = self.param_chronology.biweight_mean
            return dt_param
        
        try:
            self._layout.loading = True
            data = self.wtabulator.value.loc[self.wtabulator.value[CATEGORY].isin([CHRONOLOGY, TREE]),:]
            idxs = data[IDX_CHILD].unique().tolist()
            offset = None
            if len(idxs) == len(data[IDX_CHILD]):
                offset = data[[IDX_CHILD, OFFSET]]
            dt_data = data
            
            if len(idxs) > 0:
                #print('*** dataset_view, _sync_data_indice')
                if (self.param_detrend is not None) and (self.param_detrend.detrend != RAW):
                    dt_data = self.dataset.detrend(idxs, self.param_detrend.detrend, self.param_detrend.window_size, 
                                                        self.param_detrend.log, self.param_chronology.date_as_offset, 
                                                        self.param_chronology.biweight_mean)      
                    if self.param_detrend.log and (self.param_detrend.detrend != BP73):
                        self.dt_info.object = f'Detrend data is log({self.param_detrend.detrend}) data. '
                    else:
                        self.dt_info.object = f'Detrend data is {self.param_detrend.detrend} data. '
                    self.dt_info.alert_type = 'info'
                else:
                    dt_data = self.dataset.get_sequences(idxs)
                    self.dt_info.object = 'Detrend data is raw data. '
                    self.dt_info.alert_type = 'primary'
                if offset is not None:
                    dt_data = dt_data.merge(offset, left_index=True, right_on=IDX_CHILD)
                    self.dt_info.object += f' {OFFSET} is available. '
                else:
                    self.dt_info.object += f' {OFFSET} is unavailable. '
                c = ''
                for index, valeur in dt_data[CATEGORY].value_counts().items():
                    if c != '':
                        c+= ', '
                    c += f'{index}: {valeur}'
                self.dt_info.object += c+' in the package. '
                if dt_data[INCONSISTENT].any():
                    self.dt_info.object += ' one or more series is inconsistent.'
                    self.dt_info.alert_type='warning'
                else:
                    self.dt_info.alert_type='primary'
                
        except Exception as inst:
            #self.wtabulator.value = self.wtabulator.value.copy()
            self.dt_info.object = 'Detrend data is raw data'
            logger.error(f'_sync_dt_data: {inst}', exc_info=True)
        finally:
            #print('*** dataset_view, _sync_dt_data')
            #print(self.dt_data)
            self.dt_data = dt_data
            self.dt_param = get_dt_param()
            self._layout.loading = False

        
        

                
            

        



