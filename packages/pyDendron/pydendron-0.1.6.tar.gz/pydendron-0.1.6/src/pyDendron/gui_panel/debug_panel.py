"""
Debug and log class
"""
__author__ = "Sylvain Meignier"
__copyright__ = "Copyright 2023 Sylvain Meignier, Le Mans Université, LIUM (https://lium.univ-lemans.fr/)"
__license__ = "GPL"

import pandas as pd
import panel as pn
import param
import sys
from panel.viewable import Viewer

from pyDendron.dataname import *
from pyDendron.app_logger import logger, stdout_stream_handler

class DebugPanel(Viewer):
    """ Tools to manage dataset. """
        
    def __init__(self, dataset, **params):
        super().__init__(**params)
        self.dataset = dataset
        self.wlog = None
        self.wcrossdating_log = None
        
        # Logger
        self.terminal = pn.widgets.Terminal(
            "Debugger terminal\n\n",
            options={"cursorBlink": True},
            sizing_mode='stretch_both'
        )
        sys.stdout = self.terminal
        stdout_stream_handler.setStream(self.terminal)
        
        self._layout = pn.Tabs(
            ('Debug', self.terminal), 
            ('Dataset Log', self._log()),
            ('Crossdating Log', self._crossdating_log()),
            dynamic=False, margin=0, styles={'font-size': '16px'})
        
        self._layout.param.watch(self.on_tab_change, ['active'], onlychanged=True)

    def __panel__(self):
        """ Return the panel layout."""
        return self._layout

    def _log(self):
        self.wlog = pn.widgets.Tabulator(
                            show_index=False,
                            sizing_mode='stretch_width',
                            max_height=800,
                            min_height=400,
                            height_policy='max',
                            )
        return pn.Column(
            self.wlog
        )
    
    def _crossdating_log(self):
        self.wcrossdating_log = pn.widgets.Tabulator(
                            show_index=False,
                            sizing_mode='stretch_width',
                            max_height=800,
                            min_height=400,
                            height_policy='max',
                            )
        return pn.Column(
            self.wcrossdating_log
        )

    def on_tab_change(self, event):
        """ Handle tab change event. """
        if self._layout.active == 1:
            self.wlog.value = self.dataset.get_log()
        elif self._layout.active == 2:
            self.wcrossdating_log.value = self.dataset.get_crossdating_log()
