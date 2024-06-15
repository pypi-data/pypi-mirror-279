# -*- coding: utf-8 -*-

try:
    from . import climet, gft, io, crs, rsvi, math, osf, smc, rasp, vesp
    from .algos.core import env
 
except ModuleNotFoundError as F:
    raise ModuleNotFoundError(str(F)) from None
except ImportError as I:
    raise ImportError(str(I)) from None

try:
    from importlib.metadata import version
    __version__ = version(__name__)
except: 
    __version__ = "unknown"
finally:
    del version
    
try:
    __gdalversion__ = io._GCT._gdal.VersionInfo("RELEASE_NAME")
except:
    __gdalversion__ = "0.0.0"
      
if __gdalversion__ < '3.4.1':
    raise ImportError(f'The GDAL version is too low, the current version {__gdalversion__}, '
                      'the minimum version is 3.4.1, please update GDAL!')



