"""
------------------|-----------|------------------
------------------|--YTGet--|------------------
------------------|-----------|------------------

( Easily get data and download youtube videos )
(    Focused on speed and simplicity.         )

"""
__title__ = "ytget"
__author__ = "Cosk"
__license__ = "MIT"

from ytget.__main__ import Video, Search, Playlist, Fetch

from . import console
from . import exceptions
from . import out_colors
from . import utils
