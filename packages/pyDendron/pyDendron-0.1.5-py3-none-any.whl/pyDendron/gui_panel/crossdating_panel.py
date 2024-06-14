"""
File Name: crossdating.py
Author: Sylvain Meignier
Organization: Le Mans Université, LIUM (https://lium.univ-lemans.fr/)
Creation Date: 2023-12-03
Description: cross-dating class
This file is governed by the terms of the GNU General Public License v3.0.
Please see the LICENSE file for more details.
"""

import logging
import pandas as pd
import panel as pn
import json
import param
import time
from panel.viewable import Viewer
from bokeh.io import export_svgs
from pathlib import Path

from pyDendron.app_logger import logger#, notification_stream_handler, notification_level
from pyDendron.dataname import *
from pyDendron.crossdating import CrossDating, COLS

from pyDendron.gui_panel.tabulator import (_cell_text_align, _cell_editors, _header_filters_lookup,
                                           _cell_formatters, _hidden_columns)


class CrossDatingPanel(Viewer):
    cfg_file = f'./cfg/{pn.state.user}/pyDendron.crossdating.cfg.json'

    inner =  param.Boolean(True, doc='Inner crossdation')

    class ParamArray(param.Parameterized):
        max_results = param.Integer(default=500000, allow_None=True, bounds=(100000, 3000000), step=100000, doc='Maximum number of results displayed')
        group_by = param.Selector(default=None, objects=[None, DATE_END_ESTIMATED, DATED, T_RANK, Z_RANK, D_RANK], doc='group scores by column')
        columns = param.ListSelector(default=list(set(list(CrossDating.COLS.keys()))- set([IDX, IDX_MASTER])), 
                                objects=list(CrossDating.COLS.keys()),
                                doc='array crossdating columns')
    param_array = ParamArray(name='Array')
    
    class ParamFilter(param.Parameterized):
        score = param.Selector(default=T_SCORE, objects=[T_SCORE, Z_SCORE, DIST], doc='score applyed with threshold')
        filter_threshold = param.Boolean(False, doc='apply filter using score threshold')
        threshold = param.Number(default=0, allow_None=True, bounds=(None, None), step=0.5, doc='Keep results upper the threshold')
        filter_max_rank = param.Boolean(True, doc='apply filter using rank value')
        max_rank = param.Integer(default=10, allow_None=True, bounds=(1, None), step=1, doc='Keep top ranking results')
        filter_dated = param.Boolean(False, doc=f'apply filter on {DATED}')
        dated = param.Boolean(True, doc='apply filter using rank value')
    param_filter = ParamFilter()


    def __init__(self, dataset_package, master_package, **params):
        super(CrossDatingPanel, self).__init__(**params)   
        
        bt_size = 75
        self.results = None
        #self.parray = None
        self.pmatrix = None
        self.pstem = None
        self.gplot = None
        self.dataset_package = dataset_package
        self.master_dataset_package = master_package
        self.master_dataset_package._layout.visible = False

        self.dt_param = None

        self.cross_dating = self.load_cfg()

        row_dataset_view = pn.Row(self.dataset_package, pn.pane.HTML('<span> </span>'), self.master_dataset_package,
                margin=(5, 0), sizing_mode='stretch_width')

        self.bt_compute = pn.widgets.Button(name='Run', icon='sum', button_type='primary', align=('start', 'center'), width=bt_size)
        self.bt_compute.on_click(self.on_compute)
        self.progress = pn.indicators.Progress(name='Run', value=0, width=400, disabled=True, bar_color='primary')
        self.progress_info = pn.pane.HTML()
        self.cross_dating.progress.param.watch(self.on_progress, ['count'])
        self.bt_select = pn.widgets.Button(name='Link selection', icon='line', button_type='primary', align=('start', 'center'), width=2*bt_size)
        self.bt_select.on_click(self.on_link)

        self.bt_dated = pn.widgets.Button(name='dated / undated', icon='swicth', button_type='primary', align=('start', 'center'), width=2*bt_size)
        self.bt_dated.on_click(self.on_dated)
        
        self.param_array.param.watch(self.on_group_by, ['group_by'], onlychanged=True)
        self.param_array.param.watch(self.on_columns, ['columns'], onlychanged=True)
        #self.param_filter.param.watch(self.on_tabs, ['score', 'filter_threshold', 'threshold', 'filter_max_rank', 'max_rank', 'filter_dated', 'dated'], onlychanged=True)
        self.param_filter.param.watch(self.on_tabs, ['score', 'filter_threshold', 'threshold', 'filter_max_rank', 'max_rank'], onlychanged=True)
        
        self.cross_dating.param_matrix.param.watch(self.on_tabs, ['size_scale', 'font_scale',  'method', 'metric', 'sorted'], onlychanged=True)
        self.cross_dating.param_stem.param.watch(self.on_tabs, ['keycode_nrows', 'height', 'win'], onlychanged=True)
        self.cross_dating.param_hist.param.watch(self.on_tabs, ['bullet_size', 'font_size', 'aspect', 'height'], onlychanged=True)
        self.cross_dating.param_map.param.watch(self.on_tabs, ['height_width', 'font_size', 'line_ratio', 'bullet_ratio'], onlychanged=True)
        self.cross_dating.param_graph.param.watch(self.on_tabs, ['height_width', 'font_size', 'line_ratio', 'bullet_ratio', 'layout'], onlychanged=True)

        self.col = self.columns()
        dtype_columns = self.dtype_columns()

        self.wtabulator = pn.widgets.Tabulator(pd.DataFrame(columns=self.col),
                                    hidden_columns=['index', IDX_MASTER, IDX], #_hidden_columns(dtype_view=col), 
                                    text_align=_cell_text_align(dtype_columns),
                                    editors=_cell_editors(dtype_columns, False),
                                    header_filters=_header_filters_lookup(dtype_columns),
                                    #header_filters=True,
                                    formatters=_cell_formatters(dtype_columns),
                                    #pagination='local', #'local',
                                    pagination=None, #'local',
                                    #frozen_rows=[0], 
                                    frozen_columns=[KEYCODE, KEYCODE_MASTER],
                                    selectable='checkbox', 
                                    sizing_mode='stretch_both',
                                    #max_height=700,
                                    #min_height=400,
                                    height_policy='max',
                                    show_index = False,
                                    )

        self.wrun = pn.Row(
                        self.bt_compute,
                        pn.Column(
                            self.progress_info,
                            self.progress),
                    )

        self.warray = pn.Column(pn.Row(self.bt_dated, self.bt_select), 
                                self.wtabulator,    )
#        self.warray = self.wtabulator
        self.wheat_matrix = pn.pane.Matplotlib()
        self.wstem = pn.pane.Bokeh()
        self.wzstem = pn.pane.Bokeh()
        self.whist = pn.Column()
        self.wmap = pn.pane.Bokeh()
        self.wgraph = pn.pane.Bokeh()
        
        self.bt_svg = pn.widgets.Button(name='Save plot', icon='svg', button_type='primary', align=('start', 'end'), width=2*bt_size)
        self.bt_svg.on_click(self.on_save_svg)

        self.tabs = pn.Tabs(('Array', self.warray),
                           ('Matrix', self.wheat_matrix), 
                           ('Timeline', pn.Column(self.wstem, self.wzstem, sizing_mode='stretch_width')), 
                           ('Density', pn.Column(self.bt_svg, self.whist)),
                           ('Map', pn.Column(self.wmap)),
                           ('Graph', pn.Column(self.wgraph)),
                           dynamic=False)
        self.tabs.param.watch(self.on_tabs,  ['active'])

        self._layout = pn.Column(
                row_dataset_view, 
                self.wrun,
                self.tabs,
                margin=(5, 0), sizing_mode='stretch_width')

    def update_col(self):
        #self.param_array = ParamArray(name='Array', method=self.cross_dating.method)
        col = self.columns()
        dtype_columns = self.dtype_columns()
        self.param_array.param.columns.objects = col
        self.param_array.columns = list(set(col)- set([IDX, IDX_MASTER]))
        self.wtabulator.hidden_columns=_hidden_columns(columnList=col, dtype_view=dtype_columns) 
        self.wtabulator.text_align=_cell_text_align(dtype_columns)
        self.wtabulator.editors=_cell_editors(dtype_columns, False)
        self.wtabulator.header_filters=_header_filters_lookup(dtype_columns)
        self.wtabulator.formatters=_cell_formatters(dtype_columns)

    def on_columns(self, event):
        self.wtabulator.hidden_columns=_hidden_columns(columnList=self.param_array.columns, 
                                                       dtype_view=self.dtype_columns()) 

    def on_group_by(self, event):
        if self.param_array.group_by is None:
            self.wtabulator.groupby = []
        else:
            self.wtabulator.groupby = [self.param_array.group_by]
        
    def set_tabulator():
        self.wtabulator.value = pd.DataFrame(columns=self.col)
        df = self.cross_dating.concat_results(**get_filter())
        if len(df) < self.param_array.max_results:
            self.wtabulator.value = df
        else:
            logging.warning(f'Too many results, the displayed array will be limited to {self.param_array.max_results/1000000}M of values.')
            self.wtabulator.value = df.sort_values(by=T_RANK).iloc[ :self.param_array.max_results]

    
    def on_tabs(self, event):
        def get_filter(threshold=True, rank=True, dated=False):
            param = {}
            param['score'] = self.param_filter.score
            if self.param_filter.filter_threshold and threshold:
                param['threshold'] = self.param_filter.threshold
            if self.param_filter.filter_max_rank and rank:
                param['max_rank'] = self.param_filter.max_rank
            if self.param_filter.filter_dated and dated:
                param['dated'] = self.param_filter.dated
            return param
        
        try:
            MAX_VALUES = 5000000
            self._layout.loading = True
            if len(self.cross_dating.results) <= 0:
                #logging.warning(f'No results to display.')
                return 
            if self.tabs.active == 0: 
                self.wtabulator.value = pd.DataFrame(columns=self.col)
                df = self.cross_dating.concat_results(**get_filter())
                if len(df) < self.param_array.max_results:
                    self.wtabulator.value = df
                else:
                    logging.warning(f'Too many results, the displayed array will be limited to {self.param_array.max_results/1000000}M of values.')
                    self.wtabulator.value = df.sort_values(by=T_RANK).iloc[ :self.param_array.max_results]
            elif self.tabs.active == 1: 
                self.wheat_matrix.object = self.cross_dating.heat_matrix(**get_filter(True, False, False), 
                                            metric=self.cross_dating.param_matrix.metric, method=self.cross_dating.param_matrix.method)
            elif self.tabs.active == 2: 
                self.wstem.object, self.wzstem.object = self.cross_dating.stem(**get_filter(True, False, False))
            elif self.tabs.active == 3: 
                #self.whist.object = self.cross_dating.hist(score=self.param_filter.score)
                self.whist.clear()
                cols, self.gplot = self.cross_dating.hist(score=self.param_filter.score)
                self.whist.append(cols)
            elif self.tabs.active == 4: 
                self.wmap.object = self.cross_dating.map( **get_filter(True, True, False), data_dt=self.dataset_package.dt_data)
            elif self.tabs.active == 5: 
                self.wgraph.object = self.cross_dating.graph( **get_filter(True, True, False), data_dt=self.dataset_package.dt_data)
        except Exception as inst:
            logger.error(f'CrossDating: {inst}', exc_info=True)
            self.wtabulator.value = pd.DataFrame(columns=self.col)
            self.wheat_matrix.object = None
            self.wstem.object = None
            self.whist.objects = None
        finally:
            self._layout.loading = False

    @param.depends("inner", watch=True)
    def _update_inner(self):
        if self.inner == True :
            self.master_dataset_package._layout.visible = False
        else:
            self.master_dataset_package._layout.visible = True

    def get_sidebar(self, visible):
        self.p_panel = pn.Param(self.param, show_name=False)
        self.p_filter = pn.Param(self.param_filter, show_name=True)
        self.p_cross = pn.Param(self.cross_dating, show_name=False)
        self.parray = pn.Param(self.param_array, show_name=False)
        self.pmatrix = pn.Param(self.cross_dating.param_matrix, show_name=False)
        self.pstem = pn.Param(self.cross_dating.param_stem, show_name=False)
        self.phist = pn.Param(self.cross_dating.param_hist, show_name=False)
        self.pmap = pn.Param(self.cross_dating.param_map, show_name=False)
        self.pgraph = pn.Param(self.cross_dating.param_graph, show_name=False)
        
        return pn.Card(self.p_panel, self.p_cross, self.p_filter, 
                       pn.Tabs(self.parray, self.pmatrix, self.pstem, self.phist),
                       pn.Tabs(self.pmap, self.pgraph),
                title='Crossdating', sizing_mode='stretch_width', margin=(5, 0), collapsed=True, visible=visible)  

    def dump_cfg(self):
        with open(self.cfg_file, 'w') as fd:
            data = {
                'param' : self.param.serialize_parameters(),
                'param_filter' : self.param_filter.param.serialize_parameters(),
                'param_array' : self.param_array.param.serialize_parameters(),
                'cross_dating' : self.cross_dating.param.serialize_parameters(),
                'cross_dating.param_matrix' : self.cross_dating.param_matrix.param.serialize_parameters(),
                'cross_dating.param_stem' : self.cross_dating.param_stem.param.serialize_parameters(),
                'cross_dating.param_hist' : self.cross_dating.param_hist.param.serialize_parameters(),
                'cross_dating.param_map' : self.cross_dating.param_map.param.serialize_parameters(),
                'cross_dating.param_graph' : self.cross_dating.param_graph.param.serialize_parameters(),
            }
            json.dump(data, fd)

    def load_cfg(self):
        try:
            cross_dating = CrossDating()
            if Path(self.cfg_file).is_file():
                with open(self.cfg_file, 'r') as fd:
                    data = json.load(fd)
                    self.param_filter = self.ParamFilter(**self.ParamFilter.param.deserialize_parameters(data['param_filter']))
                    self.param_array = self.ParamArray(**self.ParamArray.param.deserialize_parameters(data['param_array']))
                    cross_dating = CrossDating(**CrossDating.param.deserialize_parameters(data['cross_dating']))
                    cross_dating.param_matrix = CrossDating.ParamMatrix(** CrossDating.ParamMatrix.param.deserialize_parameters(data['cross_dating.param_matrix']))
                    cross_dating.param_stem =  CrossDating.ParamStem(** CrossDating.ParamStem.param.deserialize_parameters(data['cross_dating.param_stem']))
                    cross_dating.param_hist =  CrossDating.ParamHist(** CrossDating.ParamHist.param.deserialize_parameters(data['cross_dating.param_hist']))
                    cross_dating.param_map =  CrossDating.ParamMap(** CrossDating.ParamMap.param.deserialize_parameters(data['cross_dating.param_map']))
                    cross_dating.param_graph =  CrossDating.ParamGraph(** CrossDating.ParamGraph.param.deserialize_parameters(data['cross_dating.param_graph']))
        except Exception as inst:
            logger.warrning(f'ignore cfg crossdating panel, version change.')
        finally:
            return cross_dating

    def columns(self):
        return list(CrossDating.COLS.keys())

    def dtype_columns(self):
        return CrossDating.COLS
        
    def __panel__(self):
        return self._layout


    def get_selection(self) -> pd.DataFrame:
        """
        Returns the view of selectionned series. 
        """
        is_sortered = len(self.wtabulator.sorters) > 0
        d = self.wtabulator._index_mapping
        is_filtered = sum([ k == v for k, v in d.items()]) != len(d)

        selection = None
        if is_sortered:
            if is_filtered: # sorted and filtered
                idxs = [x for k, x in self.wtabulator._index_mapping.items() if k in self.wtabulator.selection]
                selection = self.wtabulator._processed.loc[idxs,:]
            else: # sorted
                selection = self.wtabulator.value.iloc[self.wtabulator.selection]        
        else: # not sorted
            selection = self.wtabulator.selected_dataframe

        return selection

    def on_link(self, event):
        if not self.inner:
            raise ValueError('Only available for self crossdating (inner parameter must be True)')
        selections = self.get_selection()
        

    def on_dated(self, event):
        selections = self.get_selection()
        df = self.wtabulator.value.copy()        
        dated = selections.loc[selections[DATED] == True]
        if len(dated) > 0:
            logger.warning('dated pairs are ignored')
        undated = selections.loc[selections[DATED] == False]
        for (idx, idx_master), grp in undated.groupby([IDX, IDX_MASTER]):
            #print('groupby', idx, idx_master, len(grp))
            if len(grp) > 1:
                logger.warning('multipled undated pairs are ignored')
            else:        
                mask = (df[IDX] == idx) & (df[IDX_MASTER] == idx_master)
                df.loc[mask, DATED] = False
                df.loc[grp.index[0] , DATED] = True
                date_begin = df.loc[grp.index[0] , DATE_BEGIN_ESTIMATED]
                self.dataset_package.dataset.set_dates(idx, date_begin, warning=False)
                ascendants = self.dataset_package.dataset.get_ascendants(idx)
                if len(ascendants) > 0:
                    self.dataset_package.dataset.edit_sequence(ascendants, {INCONSISTENT: True})
                
                d = df.loc[grp.index[0] ].to_dict()
                d.update(self.dt_param)
                self.dataset_package.dataset.log_crossdating(d)
#                self.dataset_package.dt_data.at[idx, DATE_BEGIN] = date_begin
                self.dataset_package.sync_data(event)
        
        self.dataset_package.dataset.notify_changes('save')
        #print(self.dataset_package.dataset._crossdating)
        self.wtabulator.value = df
                

    
    def on_compute(self, event):
        if self.dataset_package.dt_data is None:
            logger.warning('No data to process.')
            return
        try:
            self._layout.loading = True
            dt_data = self.dataset_package.dt_data
            dt_data_master = self.master_dataset_package.dt_data if not self.inner else None
            self.dt_param = self.dataset_package.dt_param
            if (not self.inner) and (self.dt_param != self.master_dataset_package.dt_param):
                raise ValueError('master and dataset parameters are not equal')
            
            self.results = self.cross_dating.run(dt_data, dt_data_master, self.dt_param)
            self.on_tabs(None)
        except Exception as inst:
            logger.error(f'on_compute: {inst}', exc_info=True)
            self.results = None
            self.wtabulator.value = pd.DataFrame(columns=self.col)
            self.wheat_matrix.object = None
            self.wstem.object = None
            self.wzstem.object = None
            self.whist.object = None
            self.wmap = None
            self.wgraph = None
            #self.dt_data = None
            #self.dt_data_master = None
            self.dt_param = None
        finally:
            rate, info = self.cross_dating.progress.info() 
            self.progress_info.object = f'<span>{info}</span>'
            self.progress.value = rate
            self._layout.loading = False
            self.update_col()
            

    def on_save_svg(self, event):
        try:
            if self.gplot is not None:
                export_svgs(self.gplot, filename="plot.svg")
        except Exception as inst:
            logger.error(f'on_save_svg: {inst}', exc_info=True)

    def on_progress(self, event):
        if self.cross_dating.progress.count == self.cross_dating.progress.max_count:
            self.progress.disabled = True
            return
        self.progress.disabled = False
        rate, info = self.cross_dating.progress.info() 
        self.progress.value = rate
        self.progress_info.object = f'<span>{info}</span>'
        #print(info)
        
