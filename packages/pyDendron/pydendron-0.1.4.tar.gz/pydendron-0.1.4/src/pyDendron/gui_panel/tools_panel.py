"""
Dataset tools class
"""
__author__ = "Sylvain Meignier"
__copyright__ = "Copyright 2023 Sylvain Meignier, Le Mans Université, LIUM (https://lium.univ-lemans.fr/)"
__license__ = "GPL"

import pandas as pd
from pathlib import Path
import panel as pn
import param
import copy
from panel.viewable import Viewer

from pyDendron.dataset import Dataset
from pyDendron.alien.io_besancon import IOBesancon
from pyDendron.alien.io_heidelberg import IOHeidelberg
from pyDendron.alien.io_rwl import IORWL
from pyDendron.tools.alignment import Alignment
from pyDendron.dataname import *
from pyDendron.gui_panel.dataset_package import DatasetPackage
from pyDendron.gui_panel.tabulator import (_cell_text_align, _cell_editors, _header_filters,
                                           _cell_formatters, _hidden_columns)

from pyDendron.app_logger import logger

class ToolsPanel(Viewer):
    """ Tools to manage dataset. """
    path = param.Foldername('./', doc='path of the data')
    filters = param.List(['*.p', '*.xlsx', '*.json'], doc='glob filter')
    encoding = param.Selector(default='utf-8', objects=['utf-8', 'latin1'], doc='')
    tolerance = param.Integer(default=5, bounds=(1, 10), step=1, doc='number of equal values tolerated')
        
    def __init__(self, dataset, column_selector, dataset_package, **params):
        super().__init__(**params)
        self.dataset = dataset
        self.column_selector = column_selector
        self.dataset_package = dataset_package.clone()
        
        self.bt_size = 90
        #self.import_dataset = None

        self._layout = pn.Tabs(
            ('Import', self._import()),
            ('Export', self._export()),
            ('Merge', self._merge()),
            ('Validate', self._validate()),
            ('Statistics', self._stat()),
            ('Edit rings', self._edit_ring()),
             dynamic=False, styles={'font-size': '15px'})

    def get_sidebar(self, visible):   
        return pn.Card(pn.Param(self, show_name=False),                 
                margin=(5, 0), 
                sizing_mode='stretch_width', 
                title='Tools',
                collapsed=True, visible=visible)
  
    def get_options(self):
        """ Retrieve file options based on filters. """
        options = {}
        for flt in self.filters:
            for file in Path(self.path).glob(flt):
                options[f'\U0001F4E6 {str(file.name)}'] = file
        return options
    
    def _import(self):
        def on_import(event):   
            """ Handle importing of datasets. """     
            parent_keycode = Path(file_input.filename).stem
            buffer =  file_input.value
            if file_format.value == 'Besançon':
                bes = IOBesancon()
                import_dataset = bes.read_buffer(parent_keycode, buffer)
            elif file_format.value == 'Heidelberg':
                fh = IOHeidelberg()
                import_dataset = fh.read_buffer(parent_keycode, buffer)
            elif file_format.value == 'RWL':
                rwl = IORWL()
                import_dataset = rwl.read_buffer(parent_keycode, buffer)
            if import_dataset is not None:
                #print(self.import_dataset.sequences)
                wtabulator.value = import_dataset.get_data()

        def on_save(event):
            """ Handle saving of the imported dataset. """
            if import_dataset is None:
                raise ValueError('The imported dataset is empty.')
            if dataset_name.value == '':
                raise ValueError('The dataset name is empty.')
            import_dataset.dump(Path(self.path) / dataset_name.value)

        def on_file_input(event):
            dataset_name.value = f'dataset_{Path(file_input.filename).stem}.p'
            ch = file_input.filename.lower()
            if ch.endswith('.fh'):
                file_format.value = 'Heidelberg'
            elif ch.endswith('.rwl') or ch.endswith('.crn'): 
                file_format.value = 'RWL'
            else:
                file_format.value = 'Besançon'
        
        """ Create the import tab layout. """
        file_format = pn.widgets.RadioBoxGroup(name='Format', options=['Besançon', 'Heidelberg', 'RWL'], inline=True, align=('end', 'end'))

        file_input = pn.widgets.FileInput(sizing_mode='stretch_width')
        file_input.param.watch(on_file_input, ['filename'])
        
        bt_import = pn.widgets.Button(name='Import', icon='import', button_type='primary', align=('end', 'end'), width=self.bt_size)
        bt_import.on_click(on_import)
        wtabulator = pn.widgets.Tabulator(
                                    pd.DataFrame(columns=list(dtype_view.keys())),
                                    hidden_columns=_hidden_columns(), 
                                    text_align=_cell_text_align(dtype_view),
                                    editors=_cell_editors(dtype_view), 
                                    header_filters=_header_filters(dtype_view), 
                                    formatters=_cell_formatters(dtype_view),
                                    #pagination=None,
                                    #page_size=100000,
                                    sizing_mode='stretch_width',
                                    max_height=800,
                                    min_height=400,
                                    height_policy='max',
                                    )
        
        dataset_name = pn.widgets.TextInput(name='Dataset name', placeholder='dataset_import.p')
        bt_save = pn.widgets.Button(name='Save', icon='save', button_type='primary', align=('start', 'end'), width=self.bt_size)
        bt_save.on_click(on_save)

        return pn.Column(
                        pn.Row(file_input, file_format, bt_import ),
                        wtabulator,
                        pn.Row(dataset_name, bt_save)
                    )

    def _export(self):
        def on_save_dataset(event):
            if self.dataset.filename is None:
                logger.warning('Dataset is not loaded.')
                return
            fn = Path(self.dataset.filename)
            if file_export_format.value == 'Pickle':
                fn = fn.with_suffix('.p')
            elif file_export_format.value == 'JSON':
                fn = fn.with_suffix('.json')
            else:
                fn = fn.with_suffix('.xlsx')
            logger.info(f'Tools export, filename: {fn} (format {file_export_format.value})')
            self.dataset.dump(fn)
            
        def on_save_dataset_package(event):
            if self.dataset.filename is None:
                logger.warning('Dataset is not loaded.')
                return
            data = dataset_package.dt_data
            if data is None:
                logger.warning('No package to export.')
                return
            package = dataset_package.wselection_name.value
            if file_export_format_package.value == 'Besançon':
                bes = IOBesancon()
                fn = Path(self.path) / f'{package}.txt'
                bes.write_package(self.dataset, data, fn)
                logger.info(f'Tools export {package}, filename: {fn} (format {file_export_format_package.value})')
            elif file_export_format_package.value == 'Heidelberg':
                fh = IOHeidelberg()
                fn = Path(self.path) / f'{package}.fh'
                fh.write_package(self.dataset, data, fn)
                logger.info(f'Tools export {package}, filename: {fn} (format {file_export_format_package.value})')
            elif file_export_format_package.value == 'RWL':
                rwl = IORWL()
                fn = Path(self.path) / f'{package}.rwl'
                rwl.write_package(self.dataset, data, fn)
                logger.info(f'Tools export {package}, filename: {fn} (format {file_export_format_package.value})')
              
        file_export_format = pn.widgets.RadioBoxGroup(name='file format', options=['Pickle', 'Excel', 'JSON'], inline=True, align=('start', 'end'))
        bt_save_dataset = pn.widgets.Button(name='Save', icon='save', button_type='primary', align=('start', 'end'), width=self.bt_size)
        bt_save_dataset.on_click(on_save_dataset)
        
        file_export_format_package = pn.widgets.RadioBoxGroup(name='file format', options=['Heidelberg', 'Besançon', 'RWL'], inline=True, align=('start', 'end'))
        bt_save_dataset_package = pn.widgets.Button(name='Save', icon='save', button_type='primary', align=('start', 'end'), width=self.bt_size)
        bt_save_dataset_package.on_click(on_save_dataset_package)
        
        dataset_package = self.dataset_package.clone()
        return pn.Column(
                    pn.pane.Markdown('### Export current dataset'),
                    file_export_format,
                    bt_save_dataset,
                    pn.pane.Markdown('### Export current package'),
                    dataset_package,
                    file_export_format_package,
                    bt_save_dataset_package,
        )
  
    def _merge(self):
        """ Create the dataset merge tab layout. """
        
        def load(dataset_src_name, dataset_dest_name):
            #print('load:', dataset_src_name.value, dataset_dest_name.value)
            dataset_src = Dataset()
            dataset_src.load(dataset_src_name.value)
            
            dataset_dest = Dataset()
            dataset_dest.load(dataset_dest_name.value)
            
            return  dataset_src, dataset_dest

        def on_merge(event):
            """ Handle merging of datasets. """
            dataset_src, dataset_dest = load(dataset_src_name, dataset_dest_name)
            dataset_dest.append(dataset_src)
            #print(dataset_dest_name.value)
            dataset_dest.dump(dataset_dest_name.value)

        options = self.get_options()
        
        dataset_src_name = pn.widgets.Select(name='Merge', options=options)
        dataset_dest_name = pn.widgets.Select(name='In', options=options)

        bt_merge = pn.widgets.Button(name='Merge', icon='bolt', button_type='primary', align=('start', 'end'), width=self.bt_size)
        bt_merge.on_click(on_merge)

        return pn.Column(
                        dataset_src_name, 
                        dataset_dest_name,
                        bt_merge
                    )
        
    def _stat(self):
        """ Perform stats on a package."""
        def on_stats(event):
            try:
                self._layout.loading = True
                data = dataset_package.dt_data
                if data is None:
                    logger.warning('No package.')
                    return
                wtabstats.value = self.dataset.statistics(data)
                    
            except Exception as inst:
                logger.error(f'on_duplicate2 : {inst}', exc_info=True)
            finally:
                self._layout.loading = False

        bt_stats = pn.widgets.Button(name=f'Statistics', icon='bolt', button_type='primary')
        bt_stats.on_click(on_stats)

        wtabstats = pn.widgets.Tabulator(
                                    show_index=False,
                                    sizing_mode='stretch_width',
                                    max_height=800,
                                    min_height=400,
                                    height_policy='max',
                                    )

        dataset_package = self.dataset_package.clone()
        
        return pn.Column(
            dataset_package,
            bt_stats,
            wtabstats,
        )

    def _validate(self):
        """ Create the duplicate detection tab layout."""
        
        def on_duplicate(event):
            counts = self.dataset.sequences[KEYCODE].value_counts()
            lst = list(counts[counts > 1].to_dict().keys())
            wduplicate.value =  '\n'.join(lst) if len(lst) > 0 else 'No duplicate'

        def on_duplicate2(event):
            try:
                self._layout.loading = True
                data = dataset_package.dt_data
                if data is None:
                    logger.warning('No package.')
                    return
                wduplicate2.options = alignment.ndiff_sequences(data, n=self.tolerance)
                progress.value = 100
            except Exception as inst:
                logger.error(f'on_duplicate2 : {inst}', exc_info=True)
            finally:
                self._layout.loading = False
        
        def on_progress(event):
            progress.value = alignment.rate
            
        def on_outliers(event):
            data = dataset_package.dt_data
            outliers = {}
            for _, row in data.iterrows():
                vec = row[DATA_VALUES]
                idx = row[IDX_CHILD]
                med, std = np.nanmedian(vec), np.nanstd(vec)
                cut_off = std * 5 
                lower, upper = med - cut_off, med + cut_off
                keycode = row[KEYCODE]
                for i, x in enumerate(vec):
                    if (x < lower) or (x > upper) or (abs(x) <= 1e-7):
                        outliers[f'{keycode}[{i}] = {x}'] = ({IDX: idx, KEYCODE: keycode, 'Index':i, 'Value': x})
            woutliers.options = outliers

        def on_set_nan(event):
            for d in woutliers.value:
                self.dataset.sequences.at[d[IDX], DATA_VALUES][d['Index']] = np.nan
            self.dataset.notify_changes('outliers')
        
        dataset_package = self.dataset_package.clone()
        bt_duplicate = pn.widgets.Button(name=f'Detect duplicate {KEYCODE}', icon='bolt', button_type='primary')
        bt_duplicate.on_click(on_duplicate)
        wduplicate = pn.widgets.TextAreaInput(name=f'Duplicate {KEYCODE}', value='', sizing_mode='stretch_width')

        alignment = Alignment()
        bt_duplicate2 = pn.widgets.Button(name=f'Detect duplicate {DATA_VALUES}', icon='bolt', button_type='primary')
        bt_duplicate2.on_click(on_duplicate2)
        progress = pn.indicators.Progress(name='Run', value=0, sizing_mode='stretch_width', disabled=True, bar_color='primary')
        alignment.param.watch(on_progress, ['rate'])
        wduplicate2 = pn.widgets.MultiSelect(name=f'Duplicate {DATA_VALUES}', value=[], sizing_mode='stretch_width')

        bt_outliers = pn.widgets.Button(name=f'Detect outliers {DATA_VALUES}', icon='bolt', button_type='primary')
        bt_outliers.on_click(on_outliers)
        woutliers = pn.widgets.MultiSelect(name=f'Outliers {DATA_VALUES}', options=[], sizing_mode='stretch_width')
        bt_set_nan = pn.widgets.Button(name='Set value to NaN', icon='bolt', button_type='primary')
        bt_set_nan.on_click(on_set_nan)

        return pn.Tabs(
            (f'Duplicate {KEYCODE}', pn.Column(bt_duplicate, wduplicate)),
            (f'Duplicate {DATA_VALUES}', pn.Column(dataset_package, pn.Row(bt_duplicate2,  progress), wduplicate2)),
            (f'Outliers {DATA_VALUES}', pn.Column(dataset_package, bt_outliers, woutliers, bt_set_nan))
        )

    def _edit_ring(self):
        def on_insert(event):
            if len(wtabulator.selection) > 0:
                df = wtabulator.value
                i = wtabulator.selection[0]
                wtabulator.value = pd.concat([df.iloc[:i], pd.DataFrame({'value' : [pd.NA]}), df.iloc[i:]]).reset_index(drop=True)
        
        def on_append(event):
            wtabulator.value = pd.concat([wtabulator.value, pd.DataFrame({'value' : [pd.NA]})]).reset_index(drop=True)

        def on_delete(event):
            if len(wtabulator.selection) > 0:
                i = wtabulator.selection[0]
                wtabulator.value = wtabulator.value.drop(i).reset_index(drop=True)
        
        def on_save(event):
            try:
                self._layout.loading = True

                idx = select.value
                array = wtabulator.value['value'].to_numpy()
                old_len = dataset_package.dataset.sequences.at[idx, DATA_LENGTH]
                length = len(array)
                data = {DATA_VALUES : array}            
                if length != old_len :
                    data[DATA_LENGTH] = length
                    data[DATE_END] = dataset_package.dataset.sequences.at[idx, DATE_BEGIN] + length
                self.dataset_package.dataset.edit_sequence(idx, data)
                
                    #dataset_package.dataset.sequences.at[idx, DATA_LENGTH] = len(array)
                    #dataset_package.dataset.sequences.at[idx, DATE_END] += len(array) - old_len
                ascendants = self.dataset_package.dataset.get_ascendants(idx)
                if len(ascendants) > 0:
                    self.dataset_package.dataset.edit_sequence(ascendants, {INCONSISTENT: True})
                wtabulator.value 
            except Exception as inst:
                logger.error(f'on_save : {inst}', exc_info=True)
            finally:
                self._layout.loading = False

        def sync_data(event):
            #print('sync_data')
            options = {}
            for i, row in dataset_package.dt_data.iterrows():
                #print(row[KEYCODE], row[IDX_CHILD])
                options[row[KEYCODE]] = row[IDX_CHILD]
            #print('sync_data', options)
            select.options = options

        def sync_tabulator(event):
            if select.value is not None:
                data = dataset_package.dataset.sequences.loc[select.value, DATA_VALUES]
                wtabulator.value = pd.DataFrame({'value' : data})

        dataset_package = self.dataset_package.clone()
        dataset_package.param.watch(sync_data, ['dt_data'], onlychanged=True)
        
        select = pn.widgets.Select(name=f'Select {KEYCODE}', options=[])
        select.param.watch(sync_tabulator, ['value'], onlychanged=True)
        
        bt_insert = pn.widgets.Button(name=f'Insert', icon='insert', button_type='primary')
        bt_insert.on_click(on_insert)

        bt_append = pn.widgets.Button(name=f'Append', icon='append', button_type='primary')
        bt_append.on_click(on_append)

        bt_delete = pn.widgets.Button(name=f'Delete', icon='delete', button_type='primary')
        bt_delete.on_click(on_delete)

        bt_save = pn.widgets.Button(name=f'Save', icon='save', button_type='primary')
        bt_save.on_click(on_save)

        wtabulator = pn.widgets.Tabulator(
                                    sizing_mode='stretch_width',
                                    max_height=600,
                                    min_height=300,
                                    height_policy='max',
                                    selectable=True,
                                    show_index = True
                                    )
        
        return pn.Column(
            dataset_package,
            select,
            wtabulator,
            pn.Row(bt_insert, bt_append, bt_delete, bt_save)
        )
     
    def __panel__(self):
        """ Return the panel layout."""
        return self._layout
    

    


        



