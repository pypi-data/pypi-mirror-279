# -*- coding: utf-8 -*-
# function: lazy import


## ------ System ------
import os
import sys
import gc
import copy
import shutil
import time
# from datetime import datetime
from glob import glob
from pathlib import Path

try:
    from dotted_dict import DottedDict
except:
    pass


## ------ System Pro ------
import _pickle as pickle
try:
    from tqdm import tqdm
except:
    pass

try:
    from joblib import Parallel, delayed
except:
    pass

# try:
    # from func_timeout import func_set_timeout, func_timeout
# except:
    # pass


## ------ Data Analysis ------
import re
import random
import json
import yaml

try:
    from prettytable import PrettyTable
except:
    pass

import numpy as np
try:
    import pandas as pd
except:
    pass
try:
    import polars as pl
except:
    pass

import matplotlib.pyplot as plt
plt.rcParams['font.family'] = ['Arial']
# plt.rcParams['font.family'] = ['sans-serif']
# plt.rcParams['font.sans-serif'] = ['SimHei']
# plt.rcParams['axes.unicode_minus'] = False
plt.ion()
# import scienceplots
plt.style.use('ggplot')

try:
    import seaborn as sns
except:
    pass


## ------ Scientific Calculation ------
import math
from decimal import Decimal


## ------ Audio Video ------
# from moviepy.editor import VideoFileClip, AudioFileClip


## ------ pybw ------
from pybw.core import *


