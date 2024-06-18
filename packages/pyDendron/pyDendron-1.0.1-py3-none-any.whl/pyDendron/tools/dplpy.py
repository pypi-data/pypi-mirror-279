import dplpy as dpl
import numpy as np
import pandas as pd
from pyDendron.dataset import Dataset
from pyDendron.trash.indices import Indices

def pyDendron2dlp(dataset, key=Indices.RAW):
    ind = dataset.get_indices_addones().xs(key, level='key', drop_level=True)
    date_min = int(ind[dn.DATE_BEGIN].min())
    date_max = int(ind[dn.DATE_END].max())
    data = pd.DataFrame(columns=ind[dn.KEYCODE], index=range(date_min, date_max))
    vect = np.full(date_max - date_min, np.nan)
    for idx, row in ind.iterrows():
        dec = int(row[dn.DATE_BEGIN]) - date_min
        vect = np.full(date_max - date_min, np.nan)
        if row['values'].ndim == 1:
            vect[dec:dec+row['count']] = row['values']
        else:
            vect[dec:dec+row['count']] = row['values'][0]
        data[row[dn.KEYCODE]] = vect
    
    return data

def dpl_chron(dataset, biweight=False, prewhiten=False, plot=False):
    data = pyDendron2dlp(dataset)
    return dpl.chron(data, biweight=biweight, prewhiten=prewhiten, plot=plot)
    