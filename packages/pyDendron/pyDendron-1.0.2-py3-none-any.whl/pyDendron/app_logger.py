
"""
App Logger
"""
__license__ = "GPL"
__author__ = "Sylvain Meignier"
__copyright__ = "Copyright 2023 Sylvain Meignier, Le Mans Université, LIUM (https://lium.univ-lemans.fr/)"
__license__ = "GPL"
__maintainer__ = "Sylvain Meignier"
__email__ = "pyDendron@univ-lemans.fr"
__status__ = "Production"

import logging
import sys
import panel as pn
import numpy as np

#pn.extension(notifications=True)

class NotificationStream(): 
    def __init__(self, duration=5000):
        self.duration = duration
        
    def write(self, msg):
        if pn.config.notifications:
            index = np.max(np.array([msg.find("DEBUG"), msg.find("WARNING"), msg.find("INFO"), 
                     msg.find("ERROR"), msg.find("CRITICAL")]))
            if index > -1:
                msg = msg[index:]
            #success, info, warning and error
            if len(msg) > 103:
                msg = msg[:50]+ '...'+msg[-50:]
            if pn.state.notifications is not None:
                if msg.find('DEBUG') >= 0:
                    pn.state.notifications.send(msg, background='hotpink', icon='<i class="fas fa-bug"></i>')
                elif msg.find('WARNING') >= 0:
                    if msg.find('Dropping a patch') >= 0: #can't remove Bokeh message !!!
                        return
                    pn.state.notifications.warning(msg, 0)
                elif msg.find('INFO') >= 0:
                    pn.state.notifications.info(msg, self.duration)
                elif msg.find('ERROR') >= 0:
                    pn.state.notifications.error(msg, 0)
                elif msg.find('CRITICAL') >= 0:
                    pn.state.notifications.send(msg, background='black', icon='<i class="fas fa-burn"></i>')
                else:
                    pn.state.notifications.send(msg, background='gray', icon='<i class="fas fa-bolt"></i>')
            
    def flush(self):
        pass

def add_stream(logger, level=logging.INFO, stream=sys.stdout):
    stream_handler = logging.StreamHandler(stream)
    stream_handler.setLevel(level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler.setFormatter(formatter) # add formatter to ch
    logger.addHandler(stream_handler) # add ch to logger
    return stream_handler

general_level = logging.INFO
notification_level = logging.INFO


FORMAT = '%(asctime)s | %(levelname)s | %(name)s | %(message)s'
logging.basicConfig(format=FORMAT, level=general_level, force=True)
logger = logging.getLogger()

stdout_stream_handler = add_stream(logger, level=general_level, stream=sys.stdout)
notification_stream = NotificationStream()
notification_stream_handler = add_stream(logger, level=notification_level, stream=notification_stream)

logger = logging.getLogger('pyDendron')
logger.setLevel(general_level)
