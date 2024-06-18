"""
File Name: selector.py
Author: Sylvain Meignier
Organization: Le Mans Université, LIUM (https://lium.univ-lemans.fr/)
Creation Date: 2023-12-03
Description: panel to select path
This file is governed by the terms of the GNU General Public License v3.0.
Please see the LICENSE file for more details.
"""
import param
import panel as pn
from panel.viewable import Viewer

from pathlib import Path

from pyDendron.app_logger import logger
from pyDendron.dataname import *
from pyDendron.dataset import Dataset

class DatasetSelector(Viewer):
    """
    Show dataset tree as list of panel 
    """
    path = param.Foldername('./', doc='path of the data')
    filters = param.List(['*.p', '*.xlsx', '*.json'], doc='glob filter')
    options = param.Dict({}, doc='options')
    save_auto =  param.Boolean(False, doc='show all components / sequences')
    
    def __init__(self, dataset, **param):
        super(DatasetSelector, self).__init__(**param)
        self.dataset = dataset

        self.wselect = pn.widgets.Select(name='Selection', options=self.get_options())
        
        self.bt_load = pn.widgets.Button(name='Load', icon='loader', button_type='primary')
        self.bt_load.on_click(self.on_load)
        self.bt_refresh = pn.widgets.Button(name='Refresh', icon='refresh', button_type='primary')
        self.bt_refresh.on_click(self.on_refresh)
        self.bt_save = pn.widgets.Button(name='Save', icon='file-download', button_type='primary')        
        self.bt_save.on_click(self.on_save)
        
        self._layout = pn.Column(self.wselect, pn.Row(self.bt_load, self.bt_refresh, self.bt_save), self.param.save_auto)

        self.param.watch(self.on_save_auto,  ['save_auto'], onlychanged=True)
        
    def __panel__(self):
        return self._layout

    def get_sidebar(self):
        box = pn.Card(
            self._layout, 
            margin=(5, 0), 
            #styles={'background': 'WhiteSmoke'}, 
            sizing_mode='stretch_width',
            hide_header=True, 
            title='Dataset')
        return box

    def get_options(self):
        options = {}
        for flt in self.filters:
            for file in Path(self.path).glob(flt):
                options[f'\U0001F4E6 {str(file.name)}'] = file
        return options

    def on_load(self, event):
        try:
            self._layout.loading = True
            file = self.wselect.value
            self.dataset.load(file)
            #msg = f'Load {str(file.name)}, #sequences: {len(self.dataset.sequences)}'
            #logger.info(msg)
        except Exception as inst:
            logger.error(f'DatasetSelector, on_load: {inst}', exc_info=True)
        finally:
            self._layout.loading = False
        
    def on_refresh(self, event):
        #print('on_refresh')
        self.wselect.options = self.get_options()

    def on_save_auto(self, event):
        self.dataset.save_auto = event.new
        
    def on_save(self, event):
        try:
            self._layout.loading = True
            #file = self.wselect.value
            self.dataset.dump()
            #logger.info(f'Save {str(file.name)}, #sequences: {len(self.dataset.sequences)}')
        except Exception as inst:
            logger.error(f'on_save: {inst}')
        finally:
            self._layout.loading = False

    @property  
    def _values(self):
        return self.wselect.value        

