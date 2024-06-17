import os
import getpass

import panel as pn
from pathlib import Path
import json
from pyDendron.dataset import Dataset
from pyDendron.gui_panel.sidebar import ParamColumns, ParamDetrend, ParamChronology, ParamPackage
from pyDendron.gui_panel.dataset_selector import DatasetSelector
from pyDendron.gui_panel.dataset_treeview import DatasetTreeview
from pyDendron.gui_panel.dataset_package import DatasetPackage
from pyDendron.gui_panel.dataset_package_builder import DatasetPackageBuilder
from pyDendron.gui_panel.dataset_package_editor import DatasetPackageEditor
from pyDendron.gui_panel.tools_panel import ToolsPanel
from pyDendron.gui_panel.ploter_panel import PloterPanel
from pyDendron.gui_panel.debug_panel import DebugPanel
from pyDendron.gui_panel.crossdating_panel import CrossDatingPanel
from pyDendron.app_logger import logger


def directory(is_server=False):
    dataset = Path('./dataset')
    cfg = Path('./cfg')
    username = getpass.getuser()
    pydendron = Path('pyDendron')
    if is_server:
        username = pn.state.user if pn.state.user is not None else 'None'
        dataset =  dataset / Path(username)
        cfg =  cfg / Path(username)
    else:
        user_directory = os.path.expanduser("~")
        dataset = Path(user_directory) / pydendron / dataset / Path(username)
        cfg = Path(user_directory) / pydendron / cfg / Path(username)

    os.makedirs(dataset, exist_ok=True)
    os.makedirs(cfg, exist_ok=True) 
    return dataset, cfg, username      

def lauch_panel(is_server=False):
    dataset_path, cfg_path, username = directory(is_server)
    print('*** lauch_panel 2', is_server, dataset_path, cfg_path, username)

    # Extension
    pn.extension(throttled=True)
    pn.extension(notifications=True)
    pn.extension('tabulator')
    pn.extension(loading_spinner='dots')
    pn.param.ParamMethod.loading_indicator = True

    pn.extension('terminal')
    pn.config.console_output = 'disable'

    pn.extension('tabulator')
    pn.extension(
        disconnect_notification="""Server Connected Closed <br /> <button class="btn btn-outline-light" onclick="location.reload();">Click To Reconnect</button> """
    )

    # Dataset
    cfg_file = cfg_path / Path('pyDendron.cfg.json')
    os.makedirs(os.path.dirname(cfg_file), exist_ok=True)

    dataset = Dataset(username=username)

    panel_list = []

    logo = os.path.join(os.path.dirname(__file__), 'data', 'trees.svg')
    # Template MaterialTemplate VanillaTemplate BootstrapTemplate FastListTemplate, EditableTemplate
    template = pn.template.FastListTemplate(title='pyDendron', #editable=True,
                                            logo=logo,
                                            meta_author='LIUM, Le Mans Université',
                                            meta_keywords='Dendrochronology',
                                            )

    # Remove notification
    def on_rm_notification(event):
        pn.state.notifications.clear()
        for pane in panel_list:
            pane._layout.loading = False
        
    rm_notification = pn.widgets.Button(name='Clear notifications', icon="trash", button_type='default', align=('end', 'center'))
    rm_notification.on_click(on_rm_notification)
    template.header.append(rm_notification)

    # Save param

    def on_save_param(event):
        with open(cfg_file, 'w') as f:
            data = {
                'param_detrend' : param_detrend.param.serialize_parameters(),
                'param_chronology' : param_chronology.param.serialize_parameters(),
                'param_column' : param_column.columns.value,
                'param_package' : param_package.param.serialize_parameters(),
            }
            json.dump(data, f)
        ploter.dump_cfg()
        crossdating.dump_cfg()

    save_param = pn.widgets.Button(name='Save parameters', icon="settings", button_type='default', align=('end', 'center'))
    save_param.on_click(on_save_param)
    template.header.append(save_param)

    # GPS 
    gps_code = pn.pane.Markdown("""<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" class="icon icon-tabler icons-tabler-outline icon-tabler-map">
    <path stroke="none" d="M0 0h24v24H0z" fill="none" />
    <path d="M3 7l6 -3l6 3l6 -3v13l-6 3l-6 -3l-6 3v-13" />
    <path d="M9 4v13" />
    <path d="M15 7v13" />
    </svg><a href="https://nominatim.openstreetmap.org" target="_blank">Open GPS site</a>""")
    template.header.append(gps_code)

    # Indice, Chronology, Columns selector
    try:
        if Path(cfg_file).is_file():
            with open(cfg_file, 'r') as f:
                data = json.load(f)
                param_detrend = ParamDetrend(**ParamDetrend.param.deserialize_parameters(data['param_detrend']))
                param_chronology = ParamChronology(**ParamChronology.param.deserialize_parameters(data['param_chronology']))
                param_column = ParamColumns(columnList=data['param_column'])
                param_package = ParamPackage(**ParamPackage.param.deserialize_parameters(data['param_package']))
        else:
                #print('no cfg')
                param_detrend = ParamDetrend()
                param_chronology = ParamChronology()
                param_column = ParamColumns()
                param_package = ParamPackage()
    except Exception as inst:
        logger.warrning(f'ignore cfg file, version change.')
        param_detrend = ParamDetrend()
        param_chronology = ParamChronology()
        param_column = ParamColumns()
        param_package = ParamPackage()

    # Dataset selector
    dataset_selector = DatasetSelector(dataset, path=dataset_path, filters=['dataset*.p'], )

    # Dataset View
    dataset_package_ploter = DatasetPackage(dataset, param_column, param_package, param_detrend, param_chronology, title='hyp')
    dataset_package = DatasetPackage(dataset, param_column, param_package, param_detrend, param_chronology, title='hyp')
    master_dataset_package = DatasetPackage(dataset, param_column, param_package, param_detrend, param_chronology, title='Master')
    panel_list.append(dataset_package_ploter)
    panel_list.append(master_dataset_package)

    # TreeView
    treeview = DatasetTreeview(dataset, param_column, param_chronology)
    sidebar_treeview = treeview.get_sidebar()
    #print('sidebar_treeview', sidebar_treeview.visible)
    panel_list.append(treeview)

    # Add to sidebar
    template.sidebar.append('## Datasets')
    template.sidebar.append(dataset_selector.get_sidebar())
    template.sidebar.append('## Parameters')
    sidebar_column = param_column.get_sidebar()
    template.sidebar.append(sidebar_column)
    template.sidebar.append(sidebar_treeview)
    sidebar_package = param_package.get_sidebar()
    template.sidebar.append(sidebar_package)
    sidebar_detrend = param_detrend.get_sidebar()
    template.sidebar.append(sidebar_detrend) 
    sidebar_chronology = param_chronology.get_sidebar()
    template.sidebar.append(sidebar_chronology)

    # Selection
    package_editor = DatasetPackageEditor(dataset, param_column, param_package)
    panel_list.append(package_editor)

    # Filter
    package_builder = DatasetPackageBuilder(treeview)
    panel_list.append(package_builder)

    #Ploter
    ploter = PloterPanel(dataset_package_ploter)
    sidebar_ploter = ploter.get_sidebar(visible=False)
    template.sidebar.append(sidebar_ploter)
    panel_list.append(ploter)

    # CrossDating
    crossdating = CrossDatingPanel(dataset_package, master_dataset_package)
    sidebar_crossdating = crossdating.get_sidebar(visible=False)
    template.sidebar.append(sidebar_crossdating)
    panel_list.append(crossdating)

    #Tools
    dataset_package_tools = DatasetPackage(dataset, param_column, param_package, title='tools')
    tools = ToolsPanel(dataset, param_column, dataset_package_tools, path=dataset_path, filters=['dataset*.p'])
    sidebar_tools = tools.get_sidebar(visible=False)
    template.sidebar.append(sidebar_tools)
    panel_list.append(tools)

    tab_package = pn.Tabs(('Create', package_builder), 
                            ('Manage', package_editor), 
                            dynamic=True, styles={'font-size': '16px'})

    #Debug / Logs
    debug = DebugPanel(dataset)
    panel_list.append(debug)

    # General tabs
    tabs = pn.Tabs(
                ('Dataset', treeview), 
                ('Package', tab_package),
                ('Ploter', ploter), 
                ('Crossdating', crossdating), 
                ('Tools', tools), 
                ('Debug', debug), 
                dynamic=False, margin=0, styles={'padding' : '0px', 'font-size': '18px'})

    def sidebar_widget(event):
        sidebar_treeview.visible = False
        sidebar_ploter.visible = False
        sidebar_crossdating.visible = False
        sidebar_tools.visible = False
        sidebar_detrend.visible = True
        sidebar_chronology.visible = True
        sidebar_column.visible = True
        sidebar_package.visible = True
        if event.obj.active == 0: # Treeview
            sidebar_treeview.visible = True
            sidebar_detrend.visible = False
            sidebar_package.visible = False
        elif  event.obj.active == 1: # Package
            sidebar_detrend.visible = False
            sidebar_chronology.visible = False
        elif  event.obj.active == 2: # Plot
            sidebar_ploter.visible = True
            dataset_package_ploter.sync_dataset(None)
            sidebar_detrend.visible = True
        elif  event.obj.active == 3: # CrossDating
            sidebar_crossdating.visible = True
            dataset_package.sync_dataset(None)
            master_dataset_package.sync_dataset(None)
            sidebar_detrend.visible = True
        elif  event.obj.active == 4: # Tools
            sidebar_tools.visible = True
            sidebar_detrend.visible = False
            sidebar_chronology.visible = False
        elif  event.obj.active == 5: # Debug
            sidebar_detrend.visible = False
            sidebar_chronology.visible = False
            sidebar_column.visible = False

    template.main.append(tabs)
    template.modal.append(pn.Row())

    tabs.param.watch(sidebar_widget, ['active'], onlychanged=True)
    logger.info('Layout initialisation')


    template.servable()
    tabs.param.trigger('active')        

    #template.show()

def lauch_app():
    import subprocess
    import sys
    try:
        subprocess.run([
            sys.executable, "-m", "panel", "serve", __file__, "--show", "--autoreload"])
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1) 

print('pydendron_app name:', __name__)
if __name__.startswith('bokeh_app'):
    print('pydendron_app is imported by bokeh_app')
    lauch_panel()


