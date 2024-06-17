# import sys
# import os
# try:
#     import FreeCAD
# except ModuleNotFoundError:
#     import sys
#     # os.environ['LD_LIBRARY_PATH'] = '$LD_LIBRARY_PATH:/tmp/squashfs-root/usr/lib/'
#
#     sys.path.append('/tmp/squashfs-root/usr/lib/python3.10/site-packages/')
#     sys.path.append('/tmp/squashfs-root/usr/lib/')
#     sys.path.append('/usr/lib/python3.10/')
#     sys.path.append('/usr/lib/python3/dist-packages')
#     import FreeCAD
#     import Draft

from PySimultan2.taxonomy_maps import Content, TaxonomyMap

from .core.user import UserManager
user_manager = UserManager()

import nicegui.binding
nicegui.binding.MAX_PROPAGATION_TIME = 0.1

from .main_ui import run_ui
from .views.detail_views import DetailView
from .core.mappers import MethodMapper, Mapping, ViewManager


__all__ = ['run_ui', 'user_manager', 'Content', 'TaxonomyMap', 'DetailView', 'MethodMapper', 'Mapping', 'ViewManager']
