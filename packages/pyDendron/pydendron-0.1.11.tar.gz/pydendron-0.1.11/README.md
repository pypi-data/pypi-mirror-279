# pyDendron

## Dendrochronology: Wikipedia

``Dendrochronology (or tree-ring dating) is the scientific method of dating tree rings (also called growth rings) to the exact year they were formed in a tree. As well as dating them, this can give data for dendroclimatology, the study of climate and atmospheric conditions during different periods in history from the wood of old trees. Dendrochronology derives from the Ancient Greek dendron (δένδρον), meaning "tree", khronos (χρόνος), meaning "time", and -logia (-λογία), "the study of".''

## pyDendron

*pyDendron* is an open-source python package dedicated to dendrochronology. It provides a web GUI to manage, trace, interdate data. *pyDendron* is developed by members of the *GROUping Research On Tree-rings Database* ([GROOT] (https://bioarcheodat.hypotheses.org/6241)), one of the three workshops of the [BioArcheoDat] (https:// bioarcheodat. hypotheses.org/) CNRS interdisciplinary research network.

Development is in its early stages. Bugs are provided free of charge like the source code.

## Requirements 

- [Anaconda](https://docs.anaconda.com/anaconda/install/index.html) or [Miniconda](https://docs.anaconda.com/free/miniconda/miniconda-install/). Miniconda is recommended.
- Git

## Installation
- Donwlod miniconda and install it. Default options are OK. 
Choose the version that corresponds to our OS: https://docs.anaconda.com/free/miniconda/miniconda-other-installer-links/

- In Linux and MacOs, open a terminal. On Windows open Anaconda Prompt available from the windows menu.
- Install git with command `conda install git -y`
- Get *pyDendron* with the commands:
    - Ignore SSL error: `git config --global http.sslverify false`
    - Get the *pyDendron* repository: `git clone https://git-lium.univ-lemans.fr/Meignier/pyDendron.git`.
- Go to `pyDendron` folder: `$ cd pydendron`
Note: in the folder `pyDendron`, there is an other `pyDendron` folder. It second folder contains the code sources.
- Install *pyDendron* environnement: `conda env create -f environment.yml`

Install is done !

## Run application
- In Linux and MacOs open a terminal. On Windows open Anaconda Prompt (available from the windows menu).
- Activate *pyDendron* environnement: `conda activate pyDendron`
- go to *pyDendron*: `cd pyDendron`
- Run: `panel serve pyDendron.py --show`

The application open a web navigator page.

### Update pyDendron environnement
Before updating *pyDendron*, it may be necessary to update the *pyDendron* environment. This information will be noted in the release notes. 
- Activate *pyDendron* environnement: `conda activate pyDendron`
- go to *pyDendron*: `cd pyDendron`
- Update the pydendron environnement: `conda env update --file ./environment.yml`  

### Update pyDendron repository
- In Linux and MacOs open a terminal. On Windows open Anaconda Prompt available in the windows menu.
- If *pyDendron* environment is activate, deactivate it. Run in a terminal: `$ conda deactivate pyDendron`
- go to *pyDendron*: `cd pyDendron`
- executes a git pull request :`git pull`


