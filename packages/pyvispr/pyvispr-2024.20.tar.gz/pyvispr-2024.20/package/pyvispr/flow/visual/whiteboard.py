"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2017
SEE COPYRIGHT NOTICE BELOW
"""

import dataclasses as dtcl
import typing as h
from pathlib import Path as path_t

import PyQt6.QtCore as core
import PyQt6.QtGui as qgui
import PyQt6.QtWidgets as wdgt
from pyvispr.config.app import save_mode_h
from pyvispr.constant.flow.node import (
    MSG_NODE_DOCUMENTATION_NEEDED,
    MSG_NODE_IN_OUT_NEEDED,
)
from pyvispr.constant.interface.storage.path import FORMAT_EXTENSION_LENGTH
from pyvispr.constant.interface.widget.menu import WHITEBOARD_MENU
from pyvispr.constant.interface.widget.whiteboard import WHITEBOARD_DEFAULT_NAME
from pyvispr.extension.object.field import NonInitField_NONE
from pyvispr.extension.qt.menu import BuildMenu
from pyvispr.flow.functional.node import state_e
from pyvispr.flow.visual.graph import graph_t
from pyvispr.flow.visual.link import link_t
from pyvispr.flow.visual.node import node_t
from pyvispr.interface.widget.grid import NewGrid
from pyvispr.interface.widget.menu import (
    link_menu_t,
    node_menu_edit_t,
    node_menu_info_t,
)
from pyvispr.runtime.backend import SCREEN_BACKEND
from pyvispr.runtime.naming import NAME_MANAGER
from sio_messenger.instance import MESSENGER

constant_e = core.Qt


@dtcl.dataclass(slots=True, repr=False, eq=False)
class whiteboard_t(wdgt.QGraphicsView):
    paths: dict[save_mode_h, path_t] = dtcl.field(init=False, default_factory=dict)
    zoom_factor: h.ClassVar[float] = 1.25

    graph: graph_t | None = NonInitField_NONE()
    grid: wdgt.QGraphicsItemGroup | None = NonInitField_NONE()

    _whiteboard_menu: wdgt.QMenu | None = NonInitField_NONE()
    _node_menu_info: node_menu_info_t | None = NonInitField_NONE()
    _node_menu_edit: node_menu_edit_t | None = NonInitField_NONE()
    _link_menu: link_menu_t | None = NonInitField_NONE()

    def __post_init__(self) -> None:
        """"""
        wdgt.QGraphicsView.__init__(self)

        self.setRenderHint(qgui.QPainter.RenderHint.Antialiasing)
        self.setDragMode(wdgt.QGraphicsView.DragMode.RubberBandDrag)

        self.SetGraph(graph_t.New(wished_name=WHITEBOARD_DEFAULT_NAME))

        self._whiteboard_menu = wdgt.QMenu()
        self._node_menu_info = node_menu_info_t()
        self._node_menu_edit = node_menu_edit_t()
        self._link_menu = link_menu_t()
        BuildMenu(self._whiteboard_menu, WHITEBOARD_MENU, self)

    def UpdateNameAndPath(self, path: path_t, /) -> None:
        """"""
        self.graph.functional.Rename(path.name[:-FORMAT_EXTENSION_LENGTH])
        self.paths.clear()
        self.paths["save"] = path

    def SetGraph(self, graph: graph_t | None, /, *, should_merge: bool = False) -> None:
        """"""
        if should_merge:
            self.graph.MergeWith(graph)

            for node in graph.nodes:
                node.SetNewNameFromFunctional()
        else:
            if self.graph is not None:
                NAME_MANAGER.RemoveGraphName(self.graph.functional.name)
            self.graph = graph

            self.setScene(self.graph)
            self.grid = None
            SCREEN_BACKEND.AddMessageCanal(
                self.graph, "changed", lambda _: self.AddOrUpdateGrid()
            )

        self.AddOrUpdateGrid()

    def AddOrUpdateGrid(self) -> None:
        """"""
        graph = self.graph
        if graph is None:
            raise RuntimeError(
                "Whiteboard grid can be added only after a graph has been created."
            )

        if self.grid is None:
            previous_geometry = None
        else:
            previous_geometry = self.grid.boundingRect()

        grid = NewGrid(graph.bounding_box)
        # This test prevents infinite self.graph "changed" callback call.
        if (previous_geometry is None) or (grid.boundingRect() != previous_geometry):
            if previous_geometry is not None:
                graph.removeItem(self.grid)
            graph.addItem(grid)
            self.grid = grid

    def ToggleGridVisibility(self) -> None:
        """"""
        self.grid.setVisible(not self.grid.isVisible())

    def SelectOrNotAllNodes(self, should_select: bool, /) -> None:
        """"""
        for node in self.graph.nodes:
            node.setSelected(should_select)

    def Clear(self) -> None:
        """"""
        self.graph.Clear()
        self.graph.setSceneRect(core.QRectF())
        self.AddOrUpdateGrid()

    def Screenshot(self) -> qgui.QPixmap:
        """"""
        frame = self.viewport().rect()
        output = qgui.QPixmap(frame.size())
        painter = qgui.QPainter(output)
        self.render(painter, output.rect().toRectF(), frame)

        return output

    def mousePressEvent(self, event: qgui.QMouseEvent, /) -> None:
        """"""
        if event.buttons() != constant_e.MouseButton.LeftButton:
            wdgt.QGraphicsView.mousePressEvent(self, event)
            return

        view_position = event.pos()
        scene_position = self.mapToScene(view_position)
        # Used to be: self.graph.views()[0].transform().
        transform = self.transform()
        item: node_t | link_t | None = None
        for current_item in self.graph.items(scene_position, deviceTransform=transform):
            if isinstance(current_item, (node_t, link_t)):
                item = current_item
                break

        if item is None:
            wdgt.QGraphicsView.mousePressEvent(self, event)
        elif isinstance(item, node_t):
            should_make_transparent = (
                event.modifiers() == constant_e.KeyboardModifier.AltModifier
            )
            if should_make_transparent:
                for element in item.childItems():
                    element.setAcceptedMouseButtons(constant_e.MouseButton.NoButton)
            self._DealWithNodePressed(item, scene_position, view_position, event)
            if should_make_transparent:
                for element in item.childItems():
                    element.setAcceptedMouseButtons(constant_e.MouseButton.AllButtons)
        else:
            self._DealWithLinkPressed(item, view_position)

    def _DealWithNodePressed(
        self,
        node: node_t,
        scene_position: core.QPointF,
        view_position: core.QPoint,
        event: qgui.QMouseEvent,
        /,
    ) -> None:
        """"""
        position = node.mapFromScene(scene_position)
        if (node.in_btn is not None) and node.in_btn.contains(position):
            position_global = self.mapToGlobal(view_position)
            self.graph.AddLinkMaybe(node, False, position_global)
        elif (node.out_btn is not None) and node.out_btn.contains(position):
            position_global = self.mapToGlobal(view_position)
            self.graph.AddLinkMaybe(node, True, position_global)
        elif node.config_btn.contains(position):
            node.ToggleIIDialog(self.graph.functional.InvalidateNodeOutputs)
        elif node.state_btn.contains(position):
            position_global = self.mapToGlobal(view_position)
            selected_action = self._node_menu_info.exec(position_global)
            if selected_action in (None, self._node_menu_info.cancel_action):
                return

            if selected_action is self._node_menu_info.documentation_action:
                MESSENGER.Transmit(
                    MSG_NODE_DOCUMENTATION_NEEDED, node.functional.description.name
                )
            elif selected_action is self._node_menu_info.in_out_action:
                MESSENGER.Transmit(MSG_NODE_IN_OUT_NEEDED, node)
        elif node.remove_btn.contains(position):
            position_global = self.mapToGlobal(view_position)
            self._node_menu_edit.Update(node.functional.state is state_e.disabled)
            selected_action = self._node_menu_edit.exec(position_global)
            if selected_action in (None, self._node_menu_edit.cancel_action):
                return

            if selected_action is self._node_menu_edit.invalidate_action:
                self.graph.functional.InvalidateNodeOutputs(node.functional)
            elif selected_action is self._node_menu_edit.disable_action:
                self.graph.functional.ToggleNodeAbility(node.functional)
            elif selected_action is self._node_menu_edit.remove_action:
                self.graph.RemoveNode(node)
        else:
            wdgt.QGraphicsView.mousePressEvent(self, event)

    def _DealWithLinkPressed(self, link: link_t, view_position: core.QPoint, /) -> None:
        """"""
        source = link.source_node.functional
        target = link.target_node.functional
        functional_s = self.graph.functional.LinksBetween(source, target)

        position_global = self.mapToGlobal(view_position)
        self._link_menu.Update(functional_s)
        selected_action = self._link_menu.exec(position_global)
        if selected_action in (None, self._link_menu.cancel_action):
            return

        if (self._link_menu.n_links == 1) or (
            selected_action is self._link_menu.remove_all_action
        ):
            self.graph.RemoveLink(link)
        else:
            which = self._link_menu.remove_actions.index(selected_action)
            functional = functional_s[which]
            self.graph.RemoveLink(
                link, output_name=functional[0], input_name=functional[1]
            )

    def wheelEvent(self, event, /) -> None:
        """"""
        if event.modifiers() == constant_e.KeyboardModifier.ControlModifier:
            scale_factor = (
                1 / whiteboard_t.zoom_factor
                if event.angleDelta().y() > 0
                else whiteboard_t.zoom_factor
            )
            self.scale(scale_factor, scale_factor)
        else:
            wdgt.QGraphicsView.wheelEvent(self, event)

    def contextMenuEvent(self, event: qgui.QContextMenuEvent, /) -> None:
        """"""
        self._whiteboard_menu.exec(self.mapToGlobal(event.pos()))

    def AlignGraphOnGrid(self) -> None:
        """"""
        self.graph.AlignOnGrid()

    def RunWorkflow(self) -> None:
        """"""
        self.graph.Run()

    def InvalidateWorkflow(self) -> None:
        """"""
        self.graph.functional.Invalidate()

    def Statistics(self) -> tuple[int, int]:
        """"""
        return self.graph.nodes.__len__(), self.graph.links.__len__()


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
