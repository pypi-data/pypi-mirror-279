"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2017
SEE COPYRIGHT NOTICE BELOW
"""

from __future__ import annotations

import dataclasses as dtcl

import PyQt6.QtWidgets as wdgt
from PyQt6.QtCore import QPointF
from PyQt6.QtGui import QPainterPath, QPolygonF
from pyvispr.config.appearance.color import (
    LINK_BRUSH_ARROW,
    LINK_PEN_EMPTY,
    LINK_PEN_FULL,
)
from pyvispr.config.appearance.geometry import LINK_MIN_HORIZONTAL_SHIFT
from pyvispr.flow.visual.node import node_t


@dtcl.dataclass(slots=True, repr=False, eq=False)
class link_t(wdgt.QGraphicsPathItem):
    """
    Note: Using QGraphicsItemGroup as a base class in order to group the path and the
    arrow together somehow "hides" the path from mouse events: when clicked, the scene
    items are the group (not of interest) and the path (of interest), but as a path item
    instead of a link_t.
    """

    source_node: node_t
    target_node: node_t
    arrow: wdgt.QGraphicsPolygonItem | None = None
    functional_s: list[tuple[str, str]] = dtcl.field(init=False, default_factory=list)

    def __post_init__(self) -> None:
        """"""
        wdgt.QGraphicsPathItem.__init__(self)

        arrow = QPolygonF()
        arrow.append(QPointF(10, 0))
        arrow.append(QPointF(0, 10))
        arrow.append(QPointF(0, -10))
        arrow.append(QPointF(10, 0))
        arrow = wdgt.QGraphicsPolygonItem(arrow)
        arrow.setPen(LINK_PEN_FULL)
        arrow.setBrush(LINK_BRUSH_ARROW)
        arrow.setZValue(1)
        self.arrow = arrow

        if self.source_node.functional.needs_running:
            pen = LINK_PEN_EMPTY
        else:
            pen = LINK_PEN_FULL
        self.setPen(pen)

    @classmethod
    def New(
        cls,
        source_node: node_t,
        source_point: QPointF | None,
        output_name: str,
        target_node: node_t,
        target_point: QPointF | None,
        input_name: str,
        /,
    ) -> link_t:
        """"""
        output = cls(
            source_node=source_node,
            target_node=target_node,
        )
        output.SetPath(source_point, target_point, is_creation=True)
        output.setZValue(1)

        output.AddFunctional(output_name, input_name)

        return output

    def SetPath(
        self,
        source_point: QPointF,
        target_point: QPointF,
        /,
        *,
        is_creation: bool = False,
    ) -> None:
        """"""
        if is_creation:
            translation = source_point
        else:
            translation = source_point - QPointF(self.path().elementAt(0))
        polygon = self.arrow.polygon()
        polygon.translate(translation)
        self.arrow.setPolygon(polygon)

        tangent = 0.4 * (target_point - source_point)
        tangent.setY(0)
        if tangent.x() < 0:
            tangent.setX(-tangent.x())
        if tangent.x() < LINK_MIN_HORIZONTAL_SHIFT:
            tangent.setX(LINK_MIN_HORIZONTAL_SHIFT)

        path = QPainterPath(source_point)
        path.cubicTo(source_point + tangent, target_point - tangent, target_point)
        self.setPath(path)

    def AddFunctional(self, output_name: str, input_name: str, /) -> None:
        """"""
        self.functional_s.append((output_name, input_name))
        self.UpdateTooltip()

    def RemoveFunctional(self, output_name: str, input_name: str, /) -> None:
        """"""
        self.functional_s.remove((output_name, input_name))
        self.UpdateTooltip()

    def UpdateTooltip(self) -> None:
        """"""
        functional_s = (f"{_elm[0]} -> {_elm[1]}" for _elm in self.functional_s)
        self.setToolTip("\n".join(functional_s))


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
