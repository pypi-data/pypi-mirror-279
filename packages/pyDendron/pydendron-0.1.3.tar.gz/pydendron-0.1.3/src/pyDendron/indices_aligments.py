#!/usr/bin/env python
# coding: utf-8

__name__ = "Data Validation"
__license__ = "GPL"
__author__ = "Sylvain Meignier"
__copyright__ = "Copyright 2023 Sylvain Meignier, Le Mans Université, LIUM (https://lium.univ-lemans.fr/)"
__license__ = "GPL"
__maintainer__ = "Sylvain Meignier"
__email__ = "pyDendron@univ-lemans.fr"
__status__ = "Production"

import pandas as pd
import numpy as np

from pathlib import Path

from pyDendron.app_logger import logger
from pyDendron.sylphe import Sylphe
from pyDendron.dataset import Dataset
from pyDendron.trash.indices import Indices
from pyDendron.healthiness.aligment import Aligment


path=Path('./dataset')

dataset= Dataset.load(path)

keycodes = dataset._sequences.loc[dataset._sequences['type'] == dn.TREE, dn.KEYCODE]
ind_seq = dataset.indices.join(keycodes, on=dn.IDX, how='inner', lsuffix='.seq', rsuffix='.ind')
ind_seq = Indices(ind_seq.reset_index())

data = Aligment.ndiff_indices(ind_seq)

with open(path / Path('aligments.txt'), 'w') as fic:
    for sublist in data:
        line = ' '.join(map(str, sublist))
        fic.write(line + '\n')
