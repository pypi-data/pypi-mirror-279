"""
File Name: ploter.py
Author: Sylvain Meignier
Organization: Le Mans Université, LIUM (https://lium.univ-lemans.fr/)
Creation Date: 2023-12-03
Description: plotter panel
This file is governed by the terms of the GNU General Public License v3.0.
Please see the LICENSE file for more details.
"""
import numpy as np
import pandas as pd
import json
from datetime import datetime

from pathlib import Path
import param
import panel as pn
from panel.viewable import Viewer
from bokeh.io import export_svgs
from bokeh.models import ColumnDataSource


from pyDendron.app_logger import logger
from pyDendron.dataname import *
from pyDendron.dataset import Dataset
from pyDendron.chronology import data2col
from pyDendron.ploter import Ploter
#from pyDendron.gui_panel.dataset_package import DatasetPackage

class PloterPanel(Viewer):
    cfg_file = f'./cfg/{pn.state.user}/pyDendron.ploter.cfg.json'

    def __init__(self, dataset_package, **params):
        super(PloterPanel, self).__init__(**params)   
            
        self.dataset_package = dataset_package
        self.dataset_package.param.watch(self._sync_data, ['dt_data'], onlychanged=True)

        self.ploter, self.light_ploter = self.load_cfg()
        
        self.sliding_select = pn.widgets.Select(name='Sliding serie', options=[])
        self.fixed_select = pn.widgets.Select(name='Fixed serie', options=[])
        self.sliding_select.param.watch(self.on_xxx_select, ['value'])
        self.fixed_select.param.watch(self.on_xxx_select, ['value'])

        self.x_slider = pn.widgets.IntSlider(name='x Slider', start=0, end=8, step=1, value=0,
                                             sizing_mode='stretch_width')
        self.y_slider = pn.widgets.FloatSlider(name='y Slider', start=0, end=8, step=1, value=0, 
                                             sizing_mode='stretch_width')
        
        self.x_slider.param.watch(self.on_slider, ['value'])
        self.y_slider.param.watch(self.on_slider, ['value'])
        
        layout_light = pn.Column(
            pn.Row(self.sliding_select, self.fixed_select),
            self.x_slider,
            self.y_slider,
            self.light_ploter,
        )
        self.tabs = pn.Tabs(('Plotter', self.ploter), 
                        ('Light table', layout_light), 
                        dynamic=False, styles={'font-size': '16px'})
        self.tabs.param.watch(self.on_active_tab, ['active'])
        self._layout = pn.Column(self.dataset_package, self.tabs,
                                 margin=(5, 0), sizing_mode='stretch_width')
    
    def get_sidebar(self, visible):
        tab_ploter = pn.Param(self.ploter, show_name=False)
        tab_light_ploter = pn.Column(
            self.light_ploter.param.height, 
            self.light_ploter.param.width, 
            self.light_ploter.param.x_range_step, 
            self.light_ploter.param.draw_type, 
        )
        return pn.Card(
                        pn.Tabs( ('Ploter', tab_ploter), ('Light Table', tab_light_ploter)),
                        title='Plot', sizing_mode='stretch_width', margin=(5, 0), collapsed=True, visible=visible)  

    def dump_cfg(self):
        with open(self.cfg_file, 'w') as fd:
            data = {
                'ploter' : self.ploter.param.serialize_parameters(),
                'light_ploter' : self.light_ploter.param.serialize_parameters(),
            }
            json.dump(data, fd)

    def load_cfg(self):
        try:
            ploter = Ploter()
            light_ploter = Ploter(ploter_name='light_ploter', x_offset_mode = 'None', y_offset_mode = 'Center', color=KEYCODE, legend='In figure')
            if Path(self.cfg_file).is_file():
                with open(self.cfg_file, 'r') as fd:
                    data = json.load(fd)
                    ploter = Ploter(**Ploter.param.deserialize_parameters(data['ploter']))
                    light_ploter = Ploter(**Ploter.param.deserialize_parameters(data['light_ploter']))            
        except Exception as inst:
            logger.warrning(f'ignore cfg ploter panel, version change.')
        finally:
            return ploter, light_ploter

    def __panel__(self):
        return self._layout

    def _sync_data(self, event):
        if self.dataset_package.dt_data is not None:
            try:
                self._layout.loading = True
                lst = self.dataset_package.dt_data[KEYCODE].to_list()
                self.sliding_select.options = ['None'] + lst
                self.fixed_select.options = ['None'] + lst
                self.fixed_select.value = 'None'
                self.sliding_select.value = 'None'
                self.on_active_tab(None)
                    
            except Exception as inst:
                logger.error(f'ploter panel: {inst}', exc_info=True)
            finally:
                self._layout.loading = False

    def on_active_tab(self, event):
        if self.tabs.active == 0:
            self.ploter.prepare_and_plot(self.dataset_package.dt_data)
        else:
            self.light_plot()
            
    def light_plot(self):
        if (self.sliding_select.value == 'None') or (self.fixed_select.value == 'None'):
            return
        sliding_keycode = self.sliding_select.value
        fixed_keycode = self.fixed_select.value
        if (sliding_keycode is not None) and (fixed_keycode is not None):
            df = self.dataset_package.dt_data
            df_series = df.loc[df[KEYCODE].isin([fixed_keycode, sliding_keycode])]
            draw_data = self.light_ploter.prepare_data(df_series)
            self.x_slider.start = int(- draw_data[sliding_keycode]['x_max'] - 1)
            self.x_slider.end = int(draw_data[fixed_keycode]['x_max'] + 1)
            self.x_slider.value = 0
            
            delta_sliding = draw_data[sliding_keycode]['w_max'] - draw_data[sliding_keycode]['w_min']
            delta_fixed = draw_data[fixed_keycode]['w_max'] - draw_data[fixed_keycode]['w_min']
            #print(delta_sliding, delta_fixed)
            
            self.y_slider.start = draw_data[fixed_keycode]['w_min'] - delta_sliding
            self.y_slider.end = draw_data[fixed_keycode]['w_max'] - draw_data[sliding_keycode]['w_min']
            self.y_slider.step = (self.y_slider.end - self.y_slider.start) // 20
            self.y_slider.value = 0
            
            #self.y_slider.start = int(- draw_data[sliding_keycode]['y_max'] -1 )
            #self.y_slider.end = int(draw_data[fixed_keycode]['y_max'] + 1)
            #self.y_slider.step = (self.y_slider.end - self.y_slider.start) // 20
            #self.y_slider.value = 0
            
            self.light_ploter.draw_data = draw_data
            self.light_ploter.plot(x_range=(self.x_slider.start, self.x_slider.end + draw_data[sliding_keycode]['x_max']),
                                   y_range=(self.y_slider.start, self.y_slider.end + delta_sliding))
    
    def on_slider(self, event):
        if (self.light_ploter.draw_data is not None) and (self.sliding_select.value in self.light_ploter.draw_data): 
            data_slide = self.light_ploter.draw_data[self.sliding_select.value]
            
            delta_x = data_slide['x_offset'] - self.x_slider.value
            delta_y = data_slide['y_offset'] - self.y_slider.value
            
            data_slide['x_offset'] = self.x_slider.value
            data_slide['y_offset'] = self.y_slider.value
            for key, info in data_slide.items():
                if isinstance(info, ColumnDataSource):
                    if 'x' in info.data:
                        info.data['x'] = [x - delta_x for x in info.data['x']]
                    if 'y' in info.data:
                        info.data['y'] = [y - delta_y for y in info.data['y']]

    def on_xxx_select(self, event):
        self.light_plot()
        
           
        
            
            
            
        

