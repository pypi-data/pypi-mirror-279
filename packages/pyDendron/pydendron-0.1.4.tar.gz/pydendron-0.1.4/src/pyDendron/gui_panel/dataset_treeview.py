"""
File Name: dataset_tabulator.py
Author: Sylvain Meignier
Organization: Le Mans Université, LIUM (https://lium.univ-lemans.fr/)
Creation Date: 2023-12-03
Description: fontend application based on sidecar
This file is governed by the terms of the GNU General Public License v3.0.
Please see the LICENSE file for more details.
"""
import warnings
import re
import copy
import pandas as pd

import numpy as np
import panel as pn
import param
from panel.viewable import Viewer
from pyDendron.tools.location import fullgeocode

from pyDendron.app_logger import logger
from pyDendron.dataname import *
#from pyDendron.gui_panel.dataset_treeview_filter import DatasetTreeviewFilter
from pyDendron.gui_panel.tabulator import (_cell_text_align, _cell_editors, _header_filters, 
                                           _cell_formatters, _hidden_columns, _cell_transform)

class DatasetTreeview(Viewer):
    """
    Treeview to manage dataset.  
    """
    flat =  param.Boolean(False, doc='show all components / sequences')
    #save_auto =  param.Boolean(True, doc='show all components / sequences')
    show_stat =  param.Boolean(True, doc='show data statistics')
    path = param.List([]) # sets and chronologies (IDX_PARENT) form the root to the current set/chronology
    clicked = param.List([])
    
    def __init__(self, dataset, param_column, param_chronology, **params):
        super(DatasetTreeview, self).__init__(**params)   
        self.param_chronology = param_chronology
        self.dataset = dataset
        self.param_column = param_column
        self.wcolumn_selector = self.param_column.columns

        self.data = self.load() # join components & sequences from dataset        
        self.wpath, self.wstat, self.wtabulator = self.get_tabulator()
        
        bt_size = 90
    
        self.dataset.param.watch(self.on_reload,  ['notify_reload'], onlychanged=True)
        self.dataset.param.watch(self.on_synchronize,  ['notify_synchronize'], onlychanged=True)
        
        self.param.watch(self.set_wstat, ['clicked'], onlychanged=True)
        
        self.wcolumn_selector.param.watch(self.sync_columns, ['value'], onlychanged=True, queued=True)
        
        self.param.watch(self.sync_flat, ['flat'], onlychanged=True)

        offsets_items = [('Normalize offsets', 'o'), ('Offsets to Years', 'o2y'), ('Years to offsets', 'y2o'), ('Get GPS code', 'localisation'), ('Current column values to children', 'propchild'), ('Current values to selected', 'propselect')]
        self.bt_tools = pn.widgets.MenuButton(name='Tools', items=offsets_items, icon='adjustments', button_type='primary', align=('start', 'end'), width=int(bt_size*1.5))
        self.bt_tools.on_click(self.on_tools)

        self.bt_chronology = pn.widgets.Button(name='Average', icon='tournament', button_type='primary', align=('start', 'end'), width=int(bt_size*1.5))
        self.bt_chronology.on_click(self.on_chronology)
        
        create_items = [('Create & add selection', 'a'), ('Regexp create & add selection', 'b')]
        self.bt_create = pn.widgets.MenuButton(name='Create', items=create_items, split=True, icon='folder-plus', button_type='primary', align=('start', 'end'), width=int(bt_size*1.5))
        self.bt_create.on_click(self.on_create)
        self.w_set_name = pn.widgets.TextInput(name='', placeholder='Tools/Create parameters')
        
        self.bt_delete = pn.widgets.Button(name='Delete', icon='trash', button_type='primary', align=('start', 'end'), width=bt_size)
        self.bt_delete.on_click(self.on_delete)
        self.bt_paste = pn.widgets.Button(name='Paste', icon='clipboard', button_type='primary', align=('start', 'end'), width=bt_size)
        self.bt_paste.on_click(self.on_paste)
        self.bt_copy = pn.widgets.Button(name='Copy', icon='copy', button_type='primary', align=('start', 'end'), width=bt_size)
        self.bt_copy.on_click(self.on_copy)
        self.bt_cut = pn.widgets.Button(name='Cut', icon='cut', button_type='primary', align=('start', 'end'), width=bt_size)
        self.bt_cut.on_click(self.on_cut)
        
        self._layout = pn.Column(
                self.wpath,
                self.wtabulator,
                self.wstat,
                pn.layout.Divider(margin=(-10,0)),
                pn.Row(self.bt_chronology, self.bt_tools, self.bt_create, self.w_set_name), 
                pn.Row(self.bt_copy, self.bt_cut, self.bt_paste, self.bt_delete),
                #pn.Row(*self.wtabulator.download_menu())
            )
        if self.dataset.is_empty():
            self._layout.visible = False

    def __panel__(self):
        return self._layout
    
    def get_sidebar(self):
        """
        Create the sidebar Card. 
        """
        
        col = pn.Column(
            #self.param.save_auto, 
            self.param.flat, 
            self.param.show_stat, 
        )
        
        return pn.Card(col,                 
                margin=(5, 0), 
                sizing_mode='stretch_width', 
                title='TreeView',
                collapsed=True)
    
    def set_clipboard(self, selection):
        self.clipboard.value = selection.loc[:, [ICON, KEYCODE]]
    
    def get_tabulator(self):
        """
        Configure the main panel. 
        """   
        wpath = pn.Row(margin=(-10,0))
        #wstat = pn.pane.Markdown(margin=(-45,-10, 0, 0))
        
        
        stylesheet = """
        p {
        padding: 0px;
        margin: 0px;
        }
        """
        
        wstat = pn.pane.Alert(margin=(-27,-10, 0, 0), stylesheets=[stylesheet])
        tab = pn.widgets.Tabulator(pd.DataFrame(columns=list(dtype_view.keys())),
                                    on_click=self.on_click, 
                                    on_edit=self.on_edit, 
                                    hidden_columns=_hidden_columns(self.wcolumn_selector.value), 
                                    text_align=_cell_text_align(dtype_view),
                                    editors=_cell_editors(dtype_view, True), 
                                    header_filters=_header_filters(dtype_view), 
                                    formatters=_cell_formatters(dtype_view),
                                    pagination='local',
                                    page_size=100000,
                                    frozen_columns=[ICON, KEYCODE], 
                                    selectable='checkbox',
                                    sizing_mode='stretch_both',
                                    height_policy='max',
                                    show_index=False,
                                    layout='fit_data_fill',
                                    margin=(0,0)
                                    ) 
        return wpath, wstat, tab

    #def do_save_auto(self):
    #    """
    #    Save dataset if auto_save is True.
    #    """
    #    if self.save_auto:
    #        #print('save_auto')
    #        self.dataset.dump()

    def on_synchronize(self, event):
        """ 
        Synchronize Dataset and TreeView, path is keep. 
        """
        self.load_refresh(False)

    def on_reload(self, event):
        """ 
        Synchronize Dataset and TreeView, path is reset.
        """
        self.load_refresh(True)
        
    def load_refresh(self, reset_path=False):
        """ 
        Load data from dataset and show data 
        """
        self.wtabulator.selection = []
        self.data = self.load()
        self._layout.visible = False if self.data is None else True
        if reset_path:
            self.path.clear()
        self.show_data()
    
    def color_inconsistent(self, row):
        style = [][''] * len(row)
        return style
        #for index, value in s.items():
        
        #if row[INCONSISTENT] == False:
        #    print('color_inconsistent', row[INCONSISTENT])
        #    return ['background-color: #FFD1D1']  # Light red
        
        #return ['background-color: yellow' if row[INCONSISTENT] == False for v in row else '']

     
    def load(self):
        """ 
        Load data from dataset 
        """

        data = None
        if not self.dataset.is_empty():
            try:
                self._layout.loading = True
                data1 = self.dataset.components.join(self.dataset.sequences, on=IDX_CHILD, how='left').reset_index()
                data2 = self.dataset.sequences.loc[self.dataset.get_roots(),:].reset_index()
                data2.insert(0, IDX_PARENT, -1)
                data2.rename(columns={IDX:IDX_CHILD}, inplace=True)
                with warnings.catch_warnings():
                    # TODO: pandas 2.1.0 has a FutureWarning for concatenating DataFrames with Null entries
                    warnings.filterwarnings("ignore", category=FutureWarning)
                    data = pd.concat([data2, data1], ignore_index=True)
                data.insert(len(data.columns)-1, OFFSET, data.pop(OFFSET))
                data.insert(0, ICON, data.apply(lambda x: category_html(x), axis=1))
                data = _cell_transform(data)
                data = data.set_index([IDX_PARENT, IDX_CHILD])
            except Exception as inst:
                logger.error(f'init_data : {inst}', exc_info=True)
            finally:
                self._layout.loading = False
        return data

    def show_data(self):
        """ 
        Show data selection according path 
        """
        try:
            view = None
            self._layout.loading = True
            if self.flat:
                view = self.data.reset_index()
            else:
                len_path = len(self.path)
                if len_path == 0: #root nodes
                    parent = pd.DataFrame([{IDX_PARENT:-2, IDX_CHILD:-1, ICON:'/', KEYCODE:'/', CATEGORY:'/'}])
                    mask = self.data.index.get_level_values(IDX_PARENT) == -1
                else: # a node and its children
                    idx_grand_parent = self.path[-2] if len_path > 1 else -1
                    parent = self.data.loc[(idx_grand_parent, self.path[-1])].to_frame().T
                    parent.index.names= [IDX_PARENT, IDX_CHILD]
                    parent = parent.reset_index()
                    mask = self.data.index.get_level_values(IDX_PARENT) == self.path[-1]
                children = self.data.iloc[mask].reset_index()
                view = children
        except Exception as inst:
            logger.error(f'set_data: {inst}', exc_info=True)
            view = pd.DataFrame(columns=list(dtype_view.keys()))
        finally:
            #print('***col order value:',self.wtabulator.value.columns)
            #print('***col order default:',list(dtype_view.keys()))
            self.wtabulator.value = view 
            #print('show_data')
            #self.wtabulator.style.apply(self.color_inconsistent, axis=1)
            #print('_stylesheets', self.wtabulator.style)
            self.set_wpath()
            self.set_wstat()
            self._layout.loading = False

    def on_create(self, event):
        """
        Create a new Set and add selections if menu is 'a'.
        """
        if len(self.path) == 0:
            logger.warning(f'cannot perform set creation in root')            
        try:
            self._layout.loading = True
            if event.obj.clicked == 'b':
                d = {}
                selection = self.get_selection()
                for i, row in selection.iterrows():
                    pattern = self.w_set_name.value if self.w_set_name.value != '' else r'(.+?\(\d+\)).*'
                    res = re.match(pattern, row[KEYCODE])
                    if res:
                        folder = res.group(1)
                        if folder not in d:
                            d[folder] = [i]
                        else:
                            d[folder].append(i)
                for keycode, idxs in d.items():
                    #print(keycode, idxs)
                    triplets = self.get_triplets(selection.loc[idxs])
                    idx = self.dataset.new(keycode=keycode, category=SET, idx_parent=self.path[-1])
                    self.dataset.cut(triplets, self.path + [idx])
                        
            else:
                if event.obj.clicked == 'a':
                    triplets = self.get_triplets(self.get_selection())
                    #print(triplets)
                keycode = self.w_set_name.value if self.w_set_name.value != '' else 'new set'
                idx = self.dataset.new(keycode=keycode, category=SET, idx_parent=self.path[-1])
                if event.obj.clicked == 'a':
                    self.dataset.cut(triplets, self.path + [idx])
                
            # self.do_save_auto()

        except Exception as inst:
            logger.error(f'on_create: {inst}', exc_info=True)
        finally:
            self._layout.loading = False
    
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
            
    def get_triplets(self, selection):
        if selection is not None:
            lst = []
            for i, row in  selection.iterrows():
                idx_parent = row[IDX_PARENT]
                idx_child = row[IDX_CHILD]
                offset = row[OFFSET]
                if idx_child not in [TRASH, CLIPBOARD, ROOT]:
                    lst.append((idx_parent, idx_child, offset))
                else:
                    logger.warning(f"Cannot copy/cut/paste {ROOT}, {CLIPBOARD} or {TRASH}.")
            return lst
        else:
            return []

    def on_delete(self, event):
        #print('on_cut')
        if len(self.path) == 0:
            logger.warning(f'cannot perform delete in root')            
        try:
            self._layout.loading = True
            triplets = self.get_triplets(self.get_selection())
            if self.path[-1] == TRASH:
                #print('on_delete drop: ', self.path)
                self.dataset.drop(triplets)
            else:
                #print('on_delete soft_drop: ', self.path)
                self.dataset.soft_drop(triplets)
            # self.do_save_auto()
        except Exception as inst:
            logger.error(f'perform: {inst}', exc_info=True)
        finally:
            self._layout.loading = False
        
    def on_copy(self, event):
        #print('on_copy')
        if len(self.path) == 0:
            logger.warning(f'cannot perform copy in root')            
        try:
            self._layout.loading = True
            selection = self.get_selection()
            #self.set_clipboard(selection)
            triplets = self.get_triplets(selection)
            self.dataset.copy(triplets, [CLIPBOARD])
            # self.do_save_auto()
        except Exception as inst:
            logger.error(f'perform: {inst}', exc_info=True)
        finally:
            self._layout.loading = False
        
    def on_cut(self, event):
        #print('on_cut')
        if len(self.path) == 0:
            logger.warning(f'cannot perform cut in root')            
        try:
            self._layout.loading = True
            selection = self.get_selection()
            #self.set_clipboard(selection)
            triplets = self.get_triplets(selection)
            self.dataset.cut(triplets, [CLIPBOARD])
            # self.do_save_auto()
        except Exception as inst:
            logger.error(f'perform: {inst}', exc_info=True)
        finally:
            self._layout.loading = False
    
    def on_paste(self, event):
        #print('on_paste')
        if self.flat: 
            logger.warning(f'cannot perform paste in flat mode')
        if len(self.path) == 0:
            logger.warning(f'cannot perform paste in root')            
        try:
            self._layout.loading = True
            mask = self.data.index.get_level_values(IDX_PARENT) == CLIPBOARD
            selection = self.data.iloc[mask].reset_index()
            triplets = self.get_triplets(selection)
            #self.set_clipboard(None)
            self.dataset.cut(triplets, self.path)
            # self.do_save_auto()
        except Exception as inst:
            logger.error(f'perform: {inst}', exc_info=True)
        finally:
            self._layout.loading = False

    def sync_flat(self, event):
        self.path.clear()
        self.show_data()

    def sync_columns(self, event):
        self.wtabulator.hidden_columns = _hidden_columns(self.wcolumn_selector.value)
    
    def on_path_click(self, event):
        i = event.obj.tags[0]
        logger.debug(f'on_path_click: i={i}, len={len(self.path)}, path={self.path}')
        if i < len(self.path):
            self.path = self.path[:i]
            logger.debug(f'on_path_click: new path={self.path}')
            self.show_data()
    
    def set_wstat(self, event=None):
        if self.show_stat:
            self.wpath.visible = True
            data = self.wtabulator.value
            self.wstat.object = ''
            if data is not None:
                count = len(data)
                date_begin = data[DATE_BEGIN].min()
                date_begin = int(date_begin) if pd.notna(date_begin) else '-'
                date_end = data[DATE_END].max()
                date_end = int(date_end) if pd.notna(date_end) else '-'
                freq = data[CATEGORY].value_counts().to_dict()
                freq_str = ''
                
                for i, (k, v) in enumerate(freq.items()):
                    if i == 0:
                        freq_str += f'{k}: {v}'
                    else:
                        freq_str += f', {k}: {v}'
                self.wstat.object = f'**Date** [{date_begin}, {date_end}]. **Count** {count} ({freq_str}).'
                if len(self.clicked) > 0:
                    self.wstat.object += f' **Current** [{self.clicked[3]}, {self.clicked[1]}] = {self.clicked[2]}'
                
        else:
            self.wpath.visible = False
        
    def set_wpath(self):
        """
        Create a list of Button that represent the path (Breadcrumb navigation).
        """
        def add(i, keycode, icon=None):
            if keycode != '':
                wkeycode = f'{keycode[:15]}...' if len(keycode) > 18 else f'{keycode}'
            else:
                wkeycode = keycode
            bt = pn.widgets.Button(name=wkeycode, icon=icon, button_type='light', button_style='outline', 
                                   align=('start', 'center'), tags=[i], margin=(0, 0), width_policy='min')
            bt.on_click(self.on_path_click)
            tmp_wpath.append(bt)
        
        def add_sep():
            tmp_wpath.append(pn.pane.HTML('<span>\U000025B6</span>', align=('start', 'center'), 
                                    margin=(0, 0), width_policy='min')) 
            
        tmp_wpath = []
        tmp_wpath.append(pn.pane.Markdown('**Path:**', align=('start', 'center'), margin=(0, 0), width_policy='min'))
        add(0, '', icon='folder')
        for i, idx in enumerate(self.path):
            add_sep()
            keycode = self.dataset.sequences.at[idx, KEYCODE]
            cat = self.dataset.sequences.at[idx, CATEGORY]
            icon = 'trees' if cat == CHRONOLOGY else 'folder'
            add(i + 1, keycode, icon)
            
        self.wpath.objects = tmp_wpath 
    
    def localisation(self):
        for idx, row in self.get_selection().iterrows():
            keycode = row[KEYCODE]
            (lat, lon, alt, country, state, district, town, zip_code, site) = fullgeocode(keycode, r"^([\w/-]+(?:\s+[\w/-]+)*)")
            #print(lat, lon, alt, country, state, district, town, zip_code, site)
            if lat != '':
                self.dataset.sequences.loc[row[IDX_CHILD],[SITE_LATITUDE, SITE_LONGITUDE, SITE_CODE]] = [float(lat), float(lon), site]
                self.dataset.notify_changes('localisation')
                # self.do_save_auto()
            
            #self.data.loc[(row[IDX_PARENT], row[IDX_CHILD]),[SITE_LATITUDE, SITE_LONGITUDE, SITE_CODE]] = [lat, lon, site]
            #self.wtabulator.value.loc[idx,[SITE_LATITUDE, SITE_LONGITUDE, SITE_CODE]] = [lat, lon, site]
    
    def value2selection(self):
        if self.clicked is not None:
            idx, col, value, keycode = self.clicked
            if col in [KEYCODE, OFFSET, CATEGORY, DATA_VALUES, DATA_INFO, DATA_LENGTH, DATA_WEIGHTS]:
                logger.warning(f'The {col} column is not suitable for this operation.')
                return
            
            idxs = self.get_selection()[IDX_CHILD]
            self.dataset.sequences.loc[idxs,col] = value
            self.dataset.notify_changes('localisation')
            # self.do_save_auto()

    def value2children(self):
        if self.clicked is not None:
            idx, col, value, keycode = self.clicked
            if col in [KEYCODE, OFFSET, CATEGORY, DATA_VALUES, DATA_INFO, DATA_LENGTH, DATA_WEIGHTS]:
                logger.warning(f'The {col} column is not suitable for this operation.')
                return 
            
            for _, row in self.get_selection().iterrows():
                value = row[col]
                keycode = row[KEYCODE]
                idx = row[IDX_CHILD]
                #print('value2children idx:', idx)
                tree = self.dataset.get_descendants(idx)
                idx_children = [node.idx for node in tree.filter().keys()]
                #print('value2children idx_children', idx_children, len(idx_children))
                #print('value2children ', col, value,' keycode', keycode)
                
                self.dataset.sequences.loc[idx_children, col] = value
            self.dataset.notify_changes('value2children')
            # self.do_save_auto()
                                     
    def on_tools(self, event):
        """
        Set offsets or dates. 
        """
        try:
            self._layout.loading = True
            if event.obj.clicked == 'o':
                self.dataset.shift_offsets(self.path[-1])
            elif event.obj.clicked == 'y2o':
                self.dataset.copy_dates_to_offsets(self.path[-1])
            elif event.obj.clicked == 'o2y':
                self.dataset.set_offsets_to_dates(self.path[-1])
            elif event.obj.clicked == 'localisation':
                self.localisation()
            elif event.obj.clicked == 'propchild':
                self.value2children()
            elif event.obj.clicked == 'propselect':
                self.value2selection()
                
        except Exception as inst:
            logger.error(f'set_data: {inst}', exc_info=True)
            view = pd.DataFrame(columns=list(dtype_view.keys()))
        finally:
            self._layout.loading = False
    
    def on_chronology(self, event):
        """
        Compute Chronology. 
        """
        try:
            self._layout.loading = True
            selection = self.get_selection()
            idx_children = selection.loc[selection[CATEGORY] != TREE, IDX_CHILD].to_list()
            date_as_offset = self.param_chronology.date_as_offset, 
            biweight = self.param_chronology.biweight_mean
            num_threads = self.param_chronology.num_threads
            
            self.dataset.chronologies(idx_children, date_as_offset=date_as_offset, biweight=biweight, num_threads=num_threads)
            
            # for idx in idx_children:
            #     logger.debug(f'on_chronology {idx}, {self.dataset.sequences.at[idx, KEYCODE]}')
            #     date_as_offset = self.param_chronology.date_as_offset, 
            #     biweight = self.param_chronology.biweight_mean
            #     #print(f'on_chronology {biweight}')
            #     self.dataset.chronology(idx, date_as_offset=date_as_offset, biweight=biweight)
            # self.do_save_auto()
        except Exception as inst:
            logger.error(f'set_data: {inst}', exc_info=True)
            self.show_data()
        finally:
            self._layout.loading = False

    def on_click(self, event):
        """
        Navigation between sets and chronologies. 
        """
        if self.flat: 
            return
        #print('on_click', event)
        id_row = event.row
        selected = self.wtabulator.value.iloc[id_row]
        if event.column == ICON:
            len_path = len(self.path)
            if selected[CATEGORY] != TREE:
                self.path.append(selected[IDX_CHILD])
                self.show_data()
        else:
            self.clicked = [id_row, event.column, event.value, selected[KEYCODE]]


    def on_edit(self, event):
        try:
            self._layout.loading = True
            col = event.column
            row = self.wtabulator.value.iloc[event.row]
            new = event.value
            idx_parent, idx_child = row[IDX_PARENT], row[IDX_CHILD]
        
            if col == OFFSET:
                self.dataset.edit_component(idx_parent, idx_child, new)
            else:            
                self.dataset.edit_sequence(idx_child, {col: new})
            # self.do_save_auto()
        except Exception as inst:
            logger.error(f'on_edit: {inst}', exc_info=True)
        finally:
            self._layout.loading = False

    """
    def on_edit(self, event):
        try:
            self._layout.loading = True
            col = event.column
            row = self.wtabulator.value.iloc[event.row]
            new = event.value
            idx_parent, idx_child = row[IDX_PARENT], row[IDX_CHILD]
            
            if col == OFFSET:
                new_value = np.round(new)
                self.data.loc[(idx_parent, idx_child), col] = new_value
                self.dataset.components.at[(idx_parent, idx_child), col] = new_value
                print(f'edit: components[({idx_parent}, {idx_child}), {col}] = {new_value}')
                logger.debug(f'edit: components[({idx_parent}, {idx_child}), {col}] = {new_value}')
            else:            
                new_value = new
                if dtype_view[col].lower().startswith('int'):
                    new_value = np.round(new) if pd.notna(new) else pd.NA
                elif dtype_view[col].lower().startswith('float'):
                    new_value = new if pd.notna(new) else pd.NA   
                elif dtype_view[col].lower().startswith('boolean'):
                    if new == 'true':
                        new_value = True
                    elif new == 'False':
                        new_value = False
                    else:
                        new_value = pd.NA
                self.dataset.sequences.at[idx_child, col] = new_value
                self.dataset.notify_changes('edit')
                # self.do_save_auto()
                logger.debug(f'edit: sequences[{idx_child}, {col}] = {new_value}')
        except Exception as inst:
            logger.error(f'on_edit: {inst}', exc_info=True)
        finally:
            self._layout.loading = False
        self.show_data()
        """
            
            




