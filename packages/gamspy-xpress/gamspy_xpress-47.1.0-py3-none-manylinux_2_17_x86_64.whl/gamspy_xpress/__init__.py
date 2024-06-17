import os
from pathlib import Path

from .version import __version__

directory = str(Path(__file__).resolve().parent)

files = ['libxpxcclib64.so', 'optxpress.def', 'xpauth.xpr', 'libxprs.so.43', 'libxprs.so.43.01.01', 'libxprl.so.x9.4', 'libxprl-3.3.0-x9.4.so']

file_paths = [directory + os.sep + file for file in files]
verbatim = 'XPRESS 11 5 XPXLXSXXXG 1 0 2 LP MIP RMIP NLP CNS DNLP RMINLP MINLP QCP MIQCP RMIQCP\ngmsgenus.run\ngmsgenux.out\nlibxpxcclib64.so xpx 1 1'
