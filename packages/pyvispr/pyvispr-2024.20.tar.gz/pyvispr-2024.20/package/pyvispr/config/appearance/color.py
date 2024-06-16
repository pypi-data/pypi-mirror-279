"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2017
SEE COPYRIGHT NOTICE BELOW
"""

from PyQt6.QtCore import Qt as constant_e
from PyQt6.QtGui import QBrush
from PyQt6.QtGui import QColorConstants as _colors
from PyQt6.QtGui import QPen
from pyvispr.config.appearance.geometry import GRID_LINE_WIDTH, LINK_WIDTH

color_e = _colors.Svg

PLAIN_BLUE = color_e.blue
MAIN_BLUE = color_e.dodgerblue

NODE_BRUSH_RESTING = QBrush(color_e.lightgray)
NODE_BRUSH_RUNNING = QBrush(color_e.limegreen)
NODE_BRUSH_SELECTED = QBrush(color_e.chartreuse)

BUTTON_BRUSH_CONFIG = QBrush(MAIN_BLUE)
BUTTON_BRUSH_REMOVE = QBrush(color_e.crimson)
BUTTON_BRUSH_STATE_DISABLED = QBrush(color_e.crimson)
BUTTON_BRUSH_STATE_DOING = QBrush(MAIN_BLUE)
BUTTON_BRUSH_STATE_DONE = QBrush(color_e.limegreen)
BUTTON_BRUSH_STATE_TODO = QBrush(color_e.gold)

INOUT_BRUSH_ACTIVE = QBrush(color_e.chartreuse)
INOUT_BRUSH_INACTIVE = QBrush(MAIN_BLUE)

II_WIDGET_BACKGROUND = color_e.lightblue

LINK_PEN_EMPTY = QPen(MAIN_BLUE, LINK_WIDTH, style=constant_e.PenStyle.DashLine)
LINK_PEN_FULL = QPen(MAIN_BLUE, LINK_WIDTH, style=constant_e.PenStyle.SolidLine)
LINK_BRUSH_ARROW = QBrush(MAIN_BLUE)

GRID_PEN = QPen(color_e.gainsboro, GRID_LINE_WIDTH, style=constant_e.PenStyle.DashLine)

ORANGE_BRUSH = QBrush(color_e.orange)
BLACK_BRUSH = QBrush(color_e.black)

"""
COPYRIGHT NOTICE

This software is governed by the CeCILL  license under French law and
abiding by the rules of distribution of free software.  You can  use,
modify and/ or redistribute the software under the terms of the CeCILL
license as circulated by CEA, CNRS and INRIA at the following URL
"http://www.cecill.info".

As a counterpart to the access to the source code and  rights to copy,
modify and redistribute granted by the license, users are provided only
with a limited warranty  and the software's author,  the holder of the
economic rights,  and the successive licensors  have only  limited
liability.

In this respect, the user's attention is drawn to the risks associated
with loading,  using,  modifying and/or developing or reproducing the
software by the user in light of its specific status of free software,
that may mean  that it is complicated to manipulate,  and  that  also
therefore means  that it is reserved for developers  and  experienced
professionals having in-depth computer knowledge. Users are therefore
encouraged to load and test the software's suitability as regards their
requirements in conditions enabling the security of their systems and/or
data to be ensured and,  more generally, to use and operate it in the
same conditions as regards security.

The fact that you are presently reading this means that you have had
knowledge of the CeCILL license and that you accept its terms.

SEE LICENCE NOTICE: file README-LICENCE-utf8.txt at project source root.

This software is being developed by Eric Debreuve, a CNRS employee and
member of team Morpheme.
Team Morpheme is a joint team between Inria, CNRS, and UniCA.
It is hosted by the Centre Inria d'Université Côte d'Azur, Laboratory
I3S, and Laboratory iBV.

CNRS: https://www.cnrs.fr/index.php/en
Inria: https://www.inria.fr/en/
UniCA: https://univ-cotedazur.eu/
Centre Inria d'Université Côte d'Azur: https://www.inria.fr/en/centre/sophia/
I3S: https://www.i3s.unice.fr/en/
iBV: http://ibv.unice.fr/
Team Morpheme: https://team.inria.fr/morpheme/
"""
