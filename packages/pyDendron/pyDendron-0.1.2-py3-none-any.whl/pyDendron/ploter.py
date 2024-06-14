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

import param
import panel as pn
from panel.viewable import Viewer

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, FixedTicker
from bokeh.models import Range1d
from bokeh.palettes import Category20, Category10

from pyDendron.dataname import *
from pyDendron.app_logger import logger

class Ploter(Viewer):
    ANATOMY = 'Anatomy'
    ANATOMY_COLOR = {HEARTWOOD: 'black', 
                     PITH: 'blue', PITH_MAXIMUM: 'blue', PITH_OPTIMUM: 'blue', 
                     SAPWOOD:'red', 
                     CAMBIUM_MAXIMUM:'red', CAMBIUM_OPTIMUM:'red', CAMBIUM:'red',
                     BARK: 'red'}
    
    figure_title = param.String(' ')
    y_offset_mode = param.Selector(default='Stack', objects=['None', 'Center', 'Stack'], doc='')
    x_offset_mode = param.Selector(objects=['None', DATE_BEGIN, OFFSET], doc='')
    width = param.Integer(default=1000, bounds=(50, 4000), step=10)
    height = param.Integer(default=500, bounds=(50, 2000), step=10)
    pith_estimation = param.Boolean(False, doc='Draw pith estimation')
    cambium_estimation = param.Boolean(False, doc='Draw cambium estimation')
    line_width_tree = param.Number(default=0.5, bounds=(0.25, 4.0), step=0.25)
    line_width_chronology = param.Number(default=1, bounds=(0.25, 4.0), step=0.25)
    circle_radius = param.Number(default=0.5, bounds=(0.1, 5), step=0.1)
    color = param.Selector(default=ANATOMY, objects=['None', KEYCODE, ANATOMY], 
            doc=f'None: all black, {KEYCODE}: one color per {KEYCODE}, {ANATOMY}: color pith, sapwood... ')
    legend = param.Selector(default='Y axe', objects=['None', 'Y axe', 'In figure'], 
            doc=f'position of the legend')
    legend_font_size = param.Integer(default=14, bounds=(1, 20), step=1)
    x_range_step = param.Integer(default=25, bounds=(5, 200), step=5)
    axis_marge = param.Integer(default=5, bounds=(0, 10), step=1)
    axis_font_size = param.Integer(default=10, bounds=(1, 20), step=1)
    draw_type = param.Selector(default='Line', objects=['Line', 'Step', 'Spaghetti'], doc='') 
    
    def __init__(self, ploter_name='ploter', **params):
        super(Ploter, self).__init__(**params)   
        self.ploter_name = ploter_name
        self.draw_data = None
        self.data = None
        self.figure_pane = pn.pane.Bokeh(height=self.height, width=self.width)
        self._layout = self.figure_pane
 
    def __panel__(self):
        return self._layout
                
    @param.depends("width", watch=True)
    def _update_width(self):
        self.figure_pane.width = self.width

    @param.depends("height", watch=True)
    def _update_height(self):
        self.figure_pane.height = self.height
    
    def get_pith_optimun(self, data_len):
        return int(data_len*0.1)

    def get_cambium_optimun(self, sapwood, data_length):
        optimum = 10 - (data_length - sapwood) if pd.notna(sapwood) and (sapwood > 0) else 10
        maximum = 15 - (data_length - sapwood) if pd.notna(sapwood) and (sapwood > 0) else 15
        return optimum, maximum
     
    def prepare_data(self, data):
        if data is None:
            return
        cum_y_offset = 0

        def init_ColumnDataSource():
            #return {'x': [], 'w': [], 'y': []}
            return ColumnDataSource()

        def get_x_offset(row):
            if self.x_offset_mode == 'None':
                return 0
            elif self.x_offset_mode == DATE_BEGIN:
                return row[DATE_BEGIN]
            return row[OFFSET]

        def get_y_offset(row, cum_y_offset):
            data = row[DATA_VALUES]
            if self.draw_type == 'Spaghetti':
                v = 50
            else:
                #v = (np.nanmax(data) - np.nanmin(data)) if self.y_offset_mode == 'Stack' else 0
                v = (np.nanmax(data) ) if self.y_offset_mode == 'Stack' else 0
            cum_y_offset += v
            #print('get_y_offset', cum_y_offset, v)
            return v, cum_y_offset
        
        def get_values(row, info):
            values = row[DATA_VALUES]

            sapwood_offset = row[SAPWOOD]
            info[SAPWOOD] = init_ColumnDataSource()
            info[HEARTWOOD] = init_ColumnDataSource()
            
            if pd.isna(sapwood_offset) or sapwood_offset < 0:
                sapwood_offset = len(values) - 1
            info[HEARTWOOD].data['x'] = np.arange(0, sapwood_offset + 1) + info['x_offset']
            info[HEARTWOOD].data['w'] = values[:sapwood_offset + 1]
            info[HEARTWOOD].data['y'] = info[HEARTWOOD].data['w'] + info['y_offset'] 
            
            info[SAPWOOD].data['x'] = np.arange(sapwood_offset, len(values)) + info['x_offset']
            info[SAPWOOD].data['w'] = values[sapwood_offset:]
            info[SAPWOOD].data['y'] = info[SAPWOOD].data['w'] + info['y_offset']
            
        def get_pith(row, info):
            values = row[DATA_VALUES]
            x_min = info['x_offset']
            i = np.where(~np.isnan(values))[0][0]
            w = values[i]
            info[PITH] = init_ColumnDataSource()
            info[PITH_OPTIMUM] = init_ColumnDataSource()
            info[PITH_MAXIMUM] = init_ColumnDataSource()
            if pd.notna(row[PITH]) and row[PITH]:
                info[PITH].data['x'] = [info['x_offset']]
                info[PITH].data['w'] = [w]
                info[PITH].data['y'] = [w + info['y_offset']]
            elif self.pith_estimation:#pd.notna(row[PITH_OPTIMUM]):
                optimum = self.get_pith_optimun(row[DATA_LENGTH])
                info[PITH_OPTIMUM].data['x'] = np.array([optimum, 0]) + info['x_offset']
                info[PITH_OPTIMUM].data['w'] = np.array([w, w]) 
                info[PITH_OPTIMUM].data['y'] = np.array([w, w]) + info['y_offset'] 
                x_min = info['x_offset'] = info['x_offset'] + optimum
                #if pd.notna(row[PITH_MAXIMUM]):
                #x_min = info['x_offset'] = info['x_offset'] + row[PITH_MAXIMUM]
                #info[PITH_MAXIMUM].data['x'] = np.array([row[PITH_MAXIMUM], row[PITH_OPTIMUM]]) + info['x_offset']
                #info[PITH_MAXIMUM].data['w'] = np.array([w, w]) 
                #info[PITH_MAXIMUM].data['y'] = np.array([w, w]) + info['y_offset'] 
            return x_min
                
        def get_cambium(row, info):
            values = row[DATA_VALUES]
            x = len(values) - 1
            x_max = x + info['x_offset']

            w = values[np.where(~np.isnan(values))[0][-1]]
            info[CAMBIUM] = init_ColumnDataSource()
            info[CAMBIUM_OPTIMUM] = init_ColumnDataSource()
            info[CAMBIUM_MAXIMUM] = init_ColumnDataSource()
            if pd.notna(row[CAMBIUM]) and row[CAMBIUM]:
                info[CAMBIUM].data['x'] = [x + info['x_offset']]
                info[CAMBIUM].data['w'] = [w]
                info[CAMBIUM].data['y'] = [w + info['y_offset']]
            elif self.cambium_estimation: #pd.notna(row[CAMBIUM_OPTIMUM]):
                optium, maximum = self.get_cambium_optimun(row[SAPWOOD], row[DATA_LENGTH])
                info[CAMBIUM_OPTIMUM].data['x'] = np.array([x, optium]) + info['x_offset']
                info[CAMBIUM_OPTIMUM].data['w'] = np.array([w, w])
                info[CAMBIUM_OPTIMUM].data['y'] = np.array([w, w]) + info['y_offset'] 
                x_max = optium + info['x_offset']
                #if pd.notna(row[CAMBIUM_MAXIMUM]):
                info[CAMBIUM_MAXIMUM].data['x'] = np.array([optium, maximum]) + info['x_offset']
                info[CAMBIUM_MAXIMUM].data['w'] = np.array([w, w]) 
                info[CAMBIUM_MAXIMUM].data['y'] = np.array([w, w]) + info['y_offset']
                x_max = maximum + info['x_offset']
            return x_max

        def get_bark(row, info):
            values = row[DATA_VALUES]
            x = len(values)
            w = values[np.where(~np.isnan(values))[-1]]
            info[BARK] = init_ColumnDataSource()
            if pd.notna(row[BARK]) and row[BARK]:
                info[BARK].data['x'] = [x + info['x_offset']]
                info[BARK].data['w'] = [w]
                info[BARK].data['y'] = [w + info['y_offset']]
        
        draw = {}
        data = data.loc[data[CATEGORY].isin([CHRONOLOGY, TREE]),:]
        if self.x_offset_mode != 'None':
            if data[self.x_offset_mode].isna().any():
                logger.error(f"NA value(s) in {self.x_offset_mode} column, can't draw")
                return draw
        
        for _, row in data.iterrows():      
            #row[DATA_VALUES] -= np.nanmean(row[DATA_VALUES])      
            #print(row[KEYCODE], row[DATA_VALUES])
            info = {}
            info[CATEGORY] = row[CATEGORY]
            if self.draw_type == 'Spaghetti':
                row[DATA_VALUES] = np.array([100] * row[DATA_LENGTH])
            
            info[KEYCODE] = row[KEYCODE]
            info['x_offset'] = get_x_offset(row)
            _, next_cum_y_offset = get_y_offset(row, cum_y_offset)
            
            info['y_offset'] = cum_y_offset
            get_values(row, info)
            get_bark(row, info)
            info['x_min'] = get_pith(row, info)
            info['x_max'] = get_cambium(row, info)

            info['w_min'] = np.nanmin(row[DATA_VALUES])
            info['w_max'] = np.nanmax(row[DATA_VALUES])
            info['w_mean'] = np.nanmean(row[DATA_VALUES])
            info['y_min'] = info['y_offset'] #info['w_min'] + info['y_offset']
            info['y_max'] = info['w_max'] + info['y_offset']
            info['y_mean'] = info['w_mean'] + info['y_offset']
            info['y_label'] = info['y_mean']

            draw[info[KEYCODE]] = info
            cum_y_offset = next_cum_y_offset
        return draw

    @param.depends('x_offset_mode', 'y_offset_mode', 'draw_type', watch=True)
    def prepare_and_plot(self, data=None):
        try:
            self._layout.loading = True
            if data is not None:
                self.data = data
            if self.data is None:
                return
            if len(self.data) == 0:
                return
            self.draw_data = self.prepare_data(self.data) 
        except Exception as inst:
            logger.error(f'plot : {inst}', exc_info=True)
        finally:
            self._layout.loading = False
        
        self.plot()
    
    @param.depends('x_range_step', watch=True)
    def on_x_range_step(self):
        try:
            self._layout.loading = True
            if (self.figure_pane.object is not None) and pd.notna(self.figure_pane.object.x_range.start):
                x_min = self.figure_pane.object.x_range.start + self.axis_marge
                x_max = self.figure_pane.object.x_range.end - self.axis_marge
                self.figure_pane.object.xaxis[0].ticker = FixedTicker(ticks= np.arange(int(x_min), int(x_max), self.x_range_step))
                label = self.x_offset_mode if self.x_offset_mode != 'None' else f'{OFFSET} = 0'
                self.figure_pane.object.xaxis[0].axis_label = label
        except Exception as inst:
            logger.error(f'plot : {inst}', exc_info=True)
        finally:
            self._layout.loading = False
        
    @param.depends('figure_title', watch=True)
    def on_figure_title(self):
        self.figure_pane.object.title.text = self.figure_title
    
    @param.depends('axis_font_size', watch=True)
    def on_axis_font_size(self):
        try:
            self._layout.loading = True
            self.figure_pane.object.yaxis.major_label_text_font_size = f'{self.axis_font_size}px'
            self.figure_pane.object.xaxis.major_label_text_font_size = f'{self.axis_font_size}px'
        except Exception as inst:
            logger.error(f'plot : {inst}', exc_info=True)
        finally:
            self._layout.loading = False
    
    @param.depends('legend', watch=True)
    def on_legend(self):
        if self.figure_pane.object is not None:            
            if self.legend == 'Y axe':
                y_labels = {}
                for keycode, info in self.draw_data.items():
                    y_labels[info['y_label']] = keycode
                self.figure_pane.object.legend.visible = False
                self.figure_pane.object.yaxis.ticker = list(y_labels.keys())
                self.figure_pane.object.yaxis.major_label_overrides = y_labels
            elif  self.legend == 'In figure':
                self.figure_pane.object.legend.location = "top_left"
                self.figure_pane.object.legend.click_policy="mute"
                self.figure_pane.object.legend.visible = True
                
    def get_color(self, kind, rank):
        if self.color == self.ANATOMY:
            return self.ANATOMY_COLOR[kind]
        elif self.color == KEYCODE:
            if len(self.draw_data)  <= 10:
                return Category10[10][rank]
            else:
                return Category20[20][rank % 20]
        return 'black'
    
    @param.depends('line_width_tree','line_width_chronology', 'circle_radius', 'color', 'axis_marge', watch=True)
    def plot(self, x_range = None, y_range = None):   
        try:
            self._layout.loading = True
            if self.draw_data is None:
                return
            fig = figure(margin=(5), title=self.figure_title, toolbar_location="left", height=self.height, width=self.width,
                tools="pan,wheel_zoom,box_zoom,reset,hover,save,crosshair", tooltips=[('(date/offset,value)', '(@x, @w)')])
            
            fig.output_backend = "svg"
            radius = self.circle_radius
            
            x = []
            for i, (keycode, info) in enumerate(self.draw_data.items()):
                line_width = self.line_width_tree if info[CATEGORY] == TREE else self.line_width_chronology
                x.append(info['x_min'])
                x.append(info['x_max'])
                #fig.quad(top=[info['y_max']], bottom=[info['y_min']], left=[info['x_min']], right=[info['x_max']], line_color='black', alpha=0.3, line_width=2, color=self.get_color(HEARTWOOD, i))
                fct = fig.line
                if self.draw_type == 'Step':
                    fct = fig.step
                
                fct(x='x', y='y', source=info[HEARTWOOD], line_width=line_width,  color=self.get_color(HEARTWOOD, i), legend_label=keycode)
                fct(x='x', y='y', source=info[SAPWOOD], line_width=line_width,  color=self.get_color(SAPWOOD, i), legend_label=keycode)
                fct(x='x', y='y', source=info[PITH_OPTIMUM], line_dash='dashed', line_width=line_width, color=self.get_color(PITH_OPTIMUM, i), legend_label=keycode)
                fct(x='x', y='y', source=info[PITH_MAXIMUM], line_dash='dotted', line_width=line_width, color=self.get_color(PITH_MAXIMUM, i), legend_label=keycode)
                fct(x='x', y='y', source=info[CAMBIUM_OPTIMUM], line_dash='dashed', line_width=line_width, color=self.get_color(CAMBIUM_OPTIMUM, i), legend_label=keycode)
                fct(x='x', y='y', source=info[CAMBIUM_MAXIMUM], line_dash='dotted', line_width=line_width, color=self.get_color(CAMBIUM_MAXIMUM, i), legend_label=keycode)

                fig.circle(x='x', y='y', source=info[PITH], radius=radius, color=self.get_color(PITH, i), legend_label=keycode)
                fig.circle(x='x', y='y', source=info[CAMBIUM], radius=radius, color=self.get_color(SAPWOOD, i), legend_label=keycode)
                fig.circle(x='x', y='y', source=info[BARK], radius=radius, color=self.get_color(BARK, i), legend_label=keycode)
            
            fig.xaxis.major_label_text_font_size = f'{self.axis_font_size}px'
            fig.yaxis.major_label_text_font_size = f'{self.axis_font_size}px'

            (x_min, x_max) = (np.min(x), np.max(x)) if x_range is None else x_range
            fig.x_range = Range1d(start=x_min - self.axis_marge, end=x_max + self.axis_marge)
            if y_range is not None:
                fig.y_range = Range1d(y_range[0], y_range[1])

            fig.legend.visible = False
            self.figure_pane.object = fig

            self.on_x_range_step()
            self.on_legend()
        except Exception as inst:
            logger.error(f'plot : {inst}', exc_info=True)
        finally:
            self._layout.loading = False

