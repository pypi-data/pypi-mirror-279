"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2017
SEE COPYRIGHT NOTICE BELOW
"""

import PyQt6.QtWidgets as wdgt
from pyvispr.config.appearance.color import GRID_PEN
from pyvispr.config.appearance.geometry import (
    GRID_RESOLUTION_H,
    GRID_RESOLUTION_V,
    NODE_HEIGHT_TOTAL,
    NODE_WIDTH_TOTAL,
)


def NewGrid(bound_box: tuple[float, float, float, float], /) -> wdgt.QGraphicsItemGroup:
    """"""
    output = wdgt.QGraphicsItemGroup()
    output.setZValue(0)

    if all(_elm == 0 for _elm in bound_box):
        south, east = 2.0 * NODE_HEIGHT_TOTAL, 2.0 * NODE_WIDTH_TOTAL
        north, west = -south, -east
    else:
        north, east, south, west = bound_box
        north = int(GRID_RESOLUTION_V * round(north / GRID_RESOLUTION_V))
        west = int(GRID_RESOLUTION_H * round(west / GRID_RESOLUTION_H))

    for (
        lower,
        higher,
        lower_orthogonal,
        higher_orthogonal,
        increment,
        where,
    ) in (
        (west, east, north, south, GRID_RESOLUTION_H, 1),
        (north, south, west, east, GRID_RESOLUTION_V, 2),
    ):
        # where: 1=vertical lines, 2=horizontal lines.
        n_lines = int(round((higher - lower) / increment)) + 1
        for l_idx in range(n_lines):
            current = lower + l_idx * increment
            if where == 1:
                line = wdgt.QGraphicsLineItem(
                    current, lower_orthogonal, current, higher_orthogonal
                )
            else:
                line = wdgt.QGraphicsLineItem(
                    lower_orthogonal, current, higher_orthogonal, current
                )
            line.setPen(GRID_PEN)
            output.addToGroup(line)

    return output


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
