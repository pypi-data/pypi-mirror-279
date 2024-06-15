# -*- coding: utf-8 -*-
"""
author: Bowei Pu at 2023.03.01
version: 2024.01.15
function: Some useful tools
"""

from pybw.tricks.lazy_import import *


__author__ = 'Bowei Pu'
__version__ = '2024.01.15'
__maintainer__ = 'Bowei Pu'
__email__ = 'pubowei@foxmail.com'
__status__ = 'Beta'
__date__ = '2024-01-15'


def time_parser(sec):
    s = int(sec)
    m, sec = s // 60, s % 60
    h, mins = m // 60, m % 60
    day, hour = h // 24, h % 24
    return {'day': day, 'hour': hour, 'min': mins, 'sec': sec, 's': s}


def getsizeof(obj):
    """
    Get size of a object.
    """
    return sys.getsizeof(pickle.dumps(obj))


class EasyPickle():
    """
    Easy use of pickle.
    """
    def __init__(self):
        self._function = 'Easy use of pickle'
    
    @classmethod
    def dump(cls, obj, file_obj):
        pickle.dump(obj, file_obj)
    
    @classmethod
    def load(cls, file_obj):
        return pickle.load(file_obj)
    
    @classmethod
    def save(cls, obj, file):
        if not os.path.exists(Path(file).parent):
            os.makedirs(Path(file).parent)
        with open(file, 'wb') as f:
            pickle.dump(obj, f)
    
    @classmethod
    def read(cls, file):
        with open(file, 'rb') as f:
            return pickle.load(f)


class easypickle(EasyPickle):
    """
    Easy usage of pickle.
    """
    def __init__():
        EasyPickle.__init__(self)


class PickleDump(EasyPickle):
    """
    Compatible to old version programs.
    """
    def __init__():
        EasyPickle.__init__(self)


class DictDoc():
    """
    Pack dict to class for easy use.
    """
    def __init__(self, dic: dict={}):
        self._dic = dic
        self._generate_attributes()
    
    def __repr__(self):
        return '<DictDoc>'
    
    def __str__(self):
        return self.__repr__()

    def __getitem__(self, key):
        return self._dic[key]

    def _generate_attributes(self):
        """
        Only used when first time load dic.
        """
        for k, v in self._dic.items():
            setattr(self, k, v)
    
    @property
    def dict(self):
        """
        Generate vars dict up-to-date.
        """
        new_dic = vars(self).copy()
        _ = new_dic.pop('_dic')
        return new_dic
    
    @property
    def dic(self):
        return self.dict
    
    def as_dict(self):
        return self.dict
    
    def keys(self):
        return self.dict.keys()
    
    def values(self):
        return self.dict.values()
    
    def setattr(self, name, value):
        setattr(self, name, value)
    
    def add(self, name, value):
        self._dic[name] = value
        self.setattr(name, value)
    

class OsPath():
    """
    For some low version python that do not have pathlib.
    """
    def __init__(self, file):
        self.file = file
        
        self.path = self.abspath = os.path.abspath(self.file)
        self.parent, self.name = os.path.split(self.abspath)
        self.dirname, self.basename, self.filename = self.parent, self.name, self.name
        self.stem, self.suffix = os.path.splitext(self.name)
        self.path_stem = self.abs_stem = os.path.splitext(self.abspath)[0]
        
        self.str = self.string = self.abspath

    def __repr__(self):
        return self.abspath
        
    def __str__(self):
        return self.__repr__()
        
    def __fspath__(self):
        return self.abspath
    
    def absolute(self):
        return self.abspath
    
    def as_posix(self):
        return Path(self.abspath).as_posix()
    
    @property
    def posix(self):
        return self.as_posix()
    
    @staticmethod
    def get_posix(cls, path):
        return Path(path).as_posix()
    
    def join(self, other: str):
        return self.__class__(os.path.join(self.abspath, other))
    
    def joinpath(self, other: str):
        return self.join(other)
    
    @property
    def exists(self):
        return os.path.exists(self.abspath)
    
    def is_existes(self):
        return os.path.exists(self.abspath)
    
    def isfile(self):
        return os.path.isfile(self.abspath)
    
    def isdir(self):
        return os.path.isdir(self.abspath)
    
    def rename(self, new_name):
        return self.__class__(os.path.join(self.dirname, new_name))


def Progress(total, progress, symbol='-', arrow=False, time0=False):
    
    length = 30
    
    if isinstance(total, (int, float)):
        total = int(total)
    else:
        total = len(total)
    
    scale = total / length
    index = int(progress / scale)
    
    if len(symbol) > 1:
        symbol = symbol[0]
    if arrow:
        index = index - 1
        arrow = 1
    else:
        arrow = 0
    
    percent = progress / total
    
    if not time0 or not isinstance(time0, (int, float)):
        time_used = 0
        time_left = 0
    else:
        time_used = time.time() - time0
        time_total = time_used / percent
        time_left = time_total - time_used
        
        time_used = int(round(time_used))
        time_total = int(round(time_total))
        time_left = int(round(time_left))
    
    time_used = time_parser(time_used)
    
    bar = '{}%[{}{}{}] {}/{} [{}s<{}s]'.format(
        int(percent * 100), 
        symbol * index, 
        '>' * arrow,
        ' ' * (length - index), 
        progress, 
        total, 
        time_used, 
        time_left)
    
    print('\r{}'.format(bar), end='', file=sys.stderr, flush=True)
    
    
    
    
    
    