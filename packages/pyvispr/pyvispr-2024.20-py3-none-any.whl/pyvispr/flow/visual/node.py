"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2017
SEE COPYRIGHT NOTICE BELOW
"""

from __future__ import annotations

import dataclasses as dtcl
import typing as h

import PyQt6.QtCore as core
import PyQt6.QtWidgets as wdgt
from conf_ini_g.interface.window.parameter.main import TypeAndValueWidgetsForType
from conf_ini_g.phase.specification.parameter.type import type_t
from pyvispr.config.appearance.color import (
    BUTTON_BRUSH_CONFIG,
    BUTTON_BRUSH_REMOVE,
    BUTTON_BRUSH_STATE_TODO,
    II_WIDGET_BACKGROUND,
    INOUT_BRUSH_INACTIVE,
    NODE_BRUSH_RESTING,
    NODE_BRUSH_SELECTED,
)
from pyvispr.config.appearance.geometry import (
    BUTTON_WIDTH,
    GRID_RESOLUTION_H,
    GRID_RESOLUTION_V,
    NODE_HEIGHT_TOTAL,
    NODE_WIDTH_TOTAL,
)
from pyvispr.constant.flow.value import VALUE_NOT_SET, value_not_set_t
from pyvispr.constant.interface.widget.node import (
    HEIGHT_OF_BOTTOM_BUTTONS,
    HEIGHT_OF_LATERAL_BUTTONS,
    HORIZONTAL_FREE_SPACE,
    NEEDS_RUNNING,
    TOP_OF_BOTTOM_BUTTONS,
    WIDTH_OF_LATERAL_BUTTONS,
)
from pyvispr.exception.node import NotAnInteractiveInputError
from pyvispr.extension.object.field import NON_INIT_FIELD, NonInitField_NONE
from pyvispr.flow.descriptive.input import assignment_e
from pyvispr.flow.functional.graph import graph_t
from pyvispr.flow.functional.node import node_t as functional_t
from pyvispr.flow.visual.value import invalid_ii_value_t
from pyvispr.runtime.backend import SCREEN_BACKEND
from pyvispr.runtime.naming import NAME_MANAGER
from str_to_obj import annotation_t

constant_e = core.Qt


class ii_widget_p(wdgt.QWidget):
    def Assign(
        self,
        value: h.Any,
        stripe: type_t | annotation_t | None,
    ) -> None: ...

    def Text(self) -> str: ...


@dtcl.dataclass(slots=True, repr=False, eq=False)
class node_t(wdgt.QGraphicsRectItem):
    functional: functional_t
    label: wdgt.QGraphicsTextItem
    in_btn: wdgt.QGraphicsRectItem | None
    out_btn: wdgt.QGraphicsRectItem | None

    ii_names: tuple[str, ...]
    ii_dialog: wdgt.QGraphicsProxyWidget | None = NonInitField_NONE()
    ii_widgets: dict[str, ii_widget_p] | None = NonInitField_NONE()

    config_btn: wdgt.QGraphicsRectItem = NON_INIT_FIELD
    state_btn: wdgt.QGraphicsRectItem = NON_INIT_FIELD
    remove_btn: wdgt.QGraphicsRectItem = NON_INIT_FIELD

    position_has_changed: bool = dtcl.field(init=False, default=False)

    def __post_init__(self) -> None:
        """"""
        rectangle = core.QRectF(0, 0, NODE_WIDTH_TOTAL, NODE_HEIGHT_TOTAL)
        wdgt.QGraphicsRectItem.__init__(self, rectangle)

        flag_e = wdgt.QGraphicsItem.GraphicsItemFlag
        for flag in (
            flag_e.ItemIsSelectable,
            flag_e.ItemIsMovable,
            flag_e.ItemClipsChildrenToShape,
            flag_e.ItemSendsGeometryChanges,
        ):
            self.setFlag(flag)
        self.setBrush(NODE_BRUSH_RESTING)
        self.setZValue(2)

        config_btn_width = int(HORIZONTAL_FREE_SPACE / 2.5)
        config_btn = wdgt.QGraphicsRectItem(
            core.QRectF(
                WIDTH_OF_LATERAL_BUTTONS,
                TOP_OF_BOTTOM_BUTTONS,
                config_btn_width,
                HEIGHT_OF_BOTTOM_BUTTONS,
            )
        )
        config_btn.setBrush(BUTTON_BRUSH_CONFIG)
        config_btn.setToolTip(self.details)

        state_btn = wdgt.QGraphicsRectItem(
            core.QRectF(
                WIDTH_OF_LATERAL_BUTTONS + config_btn_width,
                TOP_OF_BOTTOM_BUTTONS,
                config_btn_width,
                HEIGHT_OF_BOTTOM_BUTTONS,
            )
        )
        state_btn.setToolTip(NEEDS_RUNNING)
        state_btn.setBrush(BUTTON_BRUSH_STATE_TODO)

        remove_btn = wdgt.QGraphicsRectItem(
            core.QRectF(
                WIDTH_OF_LATERAL_BUTTONS + 2 * config_btn_width,
                TOP_OF_BOTTOM_BUTTONS,
                HORIZONTAL_FREE_SPACE - 2 * config_btn_width,
                HEIGHT_OF_BOTTOM_BUTTONS,
            )
        )
        remove_btn.setBrush(BUTTON_BRUSH_REMOVE)

        if self.ii_names.__len__() > 0:
            ii_dialog = wdgt.QGraphicsProxyWidget()
            ii_dialog.setZValue(2)
        else:
            ii_dialog = None

        self.config_btn, self.state_btn, self.remove_btn, self.ii_dialog = (
            config_btn,
            state_btn,
            remove_btn,
            ii_dialog,
        )
        for item in (
            self.label,
            self.in_btn,
            self.out_btn,
            self.config_btn,
            self.state_btn,
            self.remove_btn,
        ):
            if item is not None:
                item.setParentItem(self)

        self.setSelected(True)

    @classmethod
    def NewForFunctional(cls, functional: functional_t, /) -> node_t:
        """"""
        label = wdgt.QGraphicsTextItem(functional.name)
        label.setPos(BUTTON_WIDTH, 0)
        label.setTextWidth(NODE_WIDTH_TOTAL - 2 * BUTTON_WIDTH)
        label.setTextInteractionFlags(core.Qt.TextInteractionFlag.TextEditorInteraction)

        if functional.description.n_inputs > 0:
            in_btn = wdgt.QGraphicsRectItem(
                core.QRectF(0, 0, WIDTH_OF_LATERAL_BUTTONS, HEIGHT_OF_LATERAL_BUTTONS)
            )
            in_btn.setBrush(INOUT_BRUSH_INACTIVE)
        else:
            in_btn = None

        if functional.description.n_outputs > 0:
            out_btn = wdgt.QGraphicsRectItem(
                core.QRectF(
                    NODE_WIDTH_TOTAL - WIDTH_OF_LATERAL_BUTTONS,
                    0,
                    WIDTH_OF_LATERAL_BUTTONS,
                    HEIGHT_OF_LATERAL_BUTTONS,
                )
            )
            out_btn.setBrush(INOUT_BRUSH_INACTIVE)
        else:
            out_btn = None

        ii_names = tuple(
            _nme
            for _nme, _rcd in functional.description.inputs.items()
            if _rcd.assignment is assignment_e.full
        )

        output = cls(
            functional=functional,
            label=label,
            in_btn=in_btn,
            out_btn=out_btn,
            ii_names=ii_names,
        )

        SCREEN_BACKEND.AddMessageCanal(
            label.document(),
            "contentsChanged",
            output.SendNewNameToFunctional,
        )

        return output

    def SetNewNameFromFunctional(self) -> None:
        """"""
        label = self.label
        cursor = label.textCursor()
        where = cursor.position()
        name = self.functional.name
        label.setPlainText(name)
        cursor.setPosition(min(where, name.__len__()))
        label.setTextCursor(cursor)

    def SendNewNameToFunctional(self) -> None:
        """"""
        functional = self.functional
        current_name = functional.name
        new_name = NAME_MANAGER.current_node_manager.NewUniqueName(
            self.label.toPlainText(), in_replacement_of=current_name
        )
        if new_name != functional.name:
            functional.name = new_name
            self.SetNewNameFromFunctional()

    @property
    def input_socket_coordinates(self) -> core.QPointF:
        """"""
        return self._SocketCoordinates(True)

    @property
    def output_socket_coordinates(self) -> core.QPointF:
        """"""
        return self._SocketCoordinates(False)

    def _SocketCoordinates(self, endpoint_is_input: bool, /) -> core.QPointF:
        """"""
        output = self.scenePos()
        output.setY(output.y() + int(0.5 * self.boundingRect().height()))

        if not endpoint_is_input:
            output.setX(output.x() + self.boundingRect().width())

        return output

    @property
    def details(self) -> str:
        """"""
        description = self.functional.description

        output = [f"Function: {description.module.__name__}.{description.actual.name}"]

        if description.n_inputs > 0:
            output.append("Input(s):")
            for name, input_ in description.inputs.items():
                if input_.has_default:
                    default = f" = {input_.default_value}"
                else:
                    default = ""
                output.append(f"    {name}:{input_.type.template_as_str}{default}")
        else:
            output.append("No Inputs")

        if description.n_outputs > 0:
            output.append("Output(s):")
            for name, stripe in description.outputs.items():
                output.append(f"    {name}:{stripe.template_as_str}")
        else:
            output.append("No Outputs")

        return "\n".join(output)

    def ToggleIIDialog(self, InvalidateNodeOutputs, /) -> None:
        """
        IIDialog placement could be handled automatically with graphics anchors. Keeping
        manual management for the moment.
        """
        if self.ii_dialog is None:
            return

        if self.ii_widgets is not None:
            if self.ii_dialog.isVisible():
                self.ii_dialog.hide()
            else:
                self.ii_dialog.setPos(self.x(), self.y() + NODE_HEIGHT_TOTAL)
                self.ii_dialog.show()
            return

        ii_widgets = {}
        n_widgets = 0
        layout = wdgt.QGridLayout()
        for i_idx, (name, record) in enumerate(
            self.functional.description.inputs.items()
        ):
            if record.assignment is assignment_e.full:
                type_wgt, value_wgt = TypeAndValueWidgetsForType(
                    record.type, SCREEN_BACKEND
                )
                ii_widgets[name] = value_wgt
                n_widgets += 1

                layout.addWidget(wdgt.QLabel(name), i_idx, 0, 1, 1)
                layout.addWidget(type_wgt, i_idx, 1, 1, 1)
                layout.addWidget(value_wgt.library_wgt, i_idx, 2, 1, 1)

                if isinstance(value_wgt.library_wgt, wdgt.QStackedWidget):
                    widgets = (_elm for _elm in value_wgt.values)
                else:
                    widgets = (value_wgt,)
                for widget in widgets:
                    widget.SetAcknowledgeValueChangeFunction(
                        lambda: InvalidateNodeOutputs(self.functional)
                    )

        if n_widgets > 0:
            self.ii_widgets = ii_widgets

            widget = wdgt.QWidget()
            widget.setLayout(layout)
            widget.setStyleSheet(f"background-color: {II_WIDGET_BACKGROUND.name()};")

            self.ii_dialog.setWidget(widget)
            self.ii_dialog.setPos(self.x(), self.y() + NODE_HEIGHT_TOTAL)

    def AlignOnGrid(self) -> None:
        """"""
        position_x, position_y = (
            round(self.x() / GRID_RESOLUTION_H) * GRID_RESOLUTION_H,
            round(self.y() / GRID_RESOLUTION_V) * GRID_RESOLUTION_V,
        )
        self.setPos(position_x, position_y)

    def SetIIValue(
        self, input_name: str, value: h.Any, InvalidateNodeOutputs, /
    ) -> None:
        """"""
        if self.ii_widgets is None:
            self.ToggleIIDialog(InvalidateNodeOutputs)

        if isinstance(value, value_not_set_t):
            pass
        elif isinstance(value, invalid_ii_value_t):
            # TODO: Implement SetText whenever appropriate.
            widget = self.ii_widgets[input_name]
            if hasattr(widget, "SetText"):
                widget.SetText(value.as_str)
        else:
            stripe = self.functional.description.inputs[input_name].type
            self.ii_widgets[input_name].Assign(value, stripe)

    def IIValue(
        self, graph: graph_t, /, *, input_name: str | None = None
    ) -> h.Any | dict[str, h.Any]:
        """"""
        if (ii_widgets := self.ii_widgets) is None:
            return {}

        if input_name is None:
            input_names = self.ii_names
            return_as_dict = True
        elif input_name in self.ii_names:
            input_names = (input_name,)
            return_as_dict = False
        else:
            raise NotAnInteractiveInputError(f"Not an interactive input: {input_name}.")

        output = {}

        functional = self.functional
        description = functional.description
        for input_name in input_names:
            if not graph.links.InputSocketIsFree(functional, input_name):
                continue

            input_description = description.inputs[input_name]
            value_as_str = ii_widgets[input_name].Text()
            if value_as_str.__len__() > 0:
                expected_type = input_description.type
                value, issues = expected_type.InterpretedValueOf(value_as_str)
                if issues.__len__() > 0:
                    value = invalid_ii_value_t(as_str=value_as_str, issues=issues)
            elif input_description.has_default:
                value = input_description.default_value
            else:
                value = VALUE_NOT_SET
            output[input_name] = value

        if return_as_dict:
            return output
        return output[input_name]

    def itemChange(
        self, change: wdgt.QGraphicsItem.GraphicsItemChange, data: h.Any, /
    ) -> h.Any:
        """"""
        if change is wdgt.QGraphicsItem.GraphicsItemChange.ItemSelectedHasChanged:
            if data:
                self.setBrush(NODE_BRUSH_SELECTED)
            else:
                self.setBrush(NODE_BRUSH_RESTING)
        elif change is wdgt.QGraphicsItem.GraphicsItemChange.ItemPositionHasChanged:
            if (self.ii_dialog is not None) and self.ii_dialog.isVisible():
                self.ii_dialog.setPos(self.x(), self.y() + NODE_HEIGHT_TOTAL)
            self.position_has_changed = True

        return wdgt.QGraphicsRectItem.itemChange(self, change, data)


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
