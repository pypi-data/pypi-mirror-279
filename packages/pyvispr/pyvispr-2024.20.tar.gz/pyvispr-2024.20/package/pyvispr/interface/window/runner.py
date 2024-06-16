"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2017
SEE COPYRIGHT NOTICE BELOW
"""

from __future__ import annotations

import dataclasses as dtcl
from pathlib import Path as path_t

import PyQt6.QtWidgets as wdgt
from logger_36 import LOGGER, AddGenericHandler
from pyvispr import __version__
from pyvispr.config.app import load_mode_h, save_mode_h
from pyvispr.config.appearance.color import PLAIN_BLUE, color_e
from pyvispr.constant.app import APP_NAME, DOCUMENTATION_ADDRESS, SOURCE_ADDRESS
from pyvispr.constant.flow.node import (
    MSG_NODE_DOCUMENTATION_NEEDED,
    MSG_NODE_IN_OUT_NEEDED,
)
from pyvispr.constant.interface.widget.menu import MAIN_MENUS, entry_t
from pyvispr.exception.catalog import NodeNotFoundError
from pyvispr.exception.graph import LoadSaveError
from pyvispr.extension.object.field import NON_INIT_FIELD
from pyvispr.extension.qt.menu import AddEntriesToMenu, BuildMenu
from pyvispr.flow.visual.node import node_t
from pyvispr.flow.visual.whiteboard import whiteboard_t
from pyvispr.interface.storage.loading import LoadWorkflow
from pyvispr.interface.storage.stowing import (
    SaveWorkflow,
    SaveWorkflowAsScreenshot,
    SaveWorkflowAsScript,
)
from pyvispr.interface.widget.config import config_wgt_t
from pyvispr.interface.widget.list.node import node_list_wgt_t
from pyvispr.interface.widget.log_area import log_wgt_t
from pyvispr.runtime.backend import SCREEN_BACKEND
from pyvispr.runtime.catalog import NODE_CATALOG
from pyvispr.runtime.config import APP_CONFIG
from pyvispr.runtime.naming import NAME_MANAGER
from sio_messenger.instance import MESSENGER

_DEFAULT_TAB_COLOR: color_e | None = None


# TODO: Typing characters should search nodes in main list if workflow tab active, or
#    search terms in documentation if doc tab active.

@dtcl.dataclass(slots=True, repr=False, eq=False)
class runner_wdw_t(wdgt.QMainWindow):
    node_list: node_list_wgt_t = NON_INIT_FIELD
    recent_list: node_list_wgt_t = NON_INIT_FIELD
    most_used_list: node_list_wgt_t = NON_INIT_FIELD
    active_whiteboard: whiteboard_t = NON_INIT_FIELD
    tabs: wdgt.QTabWidget = NON_INIT_FIELD
    log_area: log_wgt_t = NON_INIT_FIELD
    doc_area: wdgt.QTextEdit = NON_INIT_FIELD
    load_recent_menu: wdgt.QMenu = NON_INIT_FIELD
    status_bar: wdgt.QStatusBar = NON_INIT_FIELD

    def __post_init__(self) -> None:
        """"""
        wdgt.QMainWindow.__init__(self)
        self.setWindowTitle(APP_NAME)
        whiteboard = whiteboard_t()

        self.node_list = node_list_wgt_t(element_name="Nodes")
        self.recent_list = node_list_wgt_t(
            element_name="Recent",
            source=APP_CONFIG.recent_nodes,
            should_be_sorted=False,
        )
        self.most_used_list = node_list_wgt_t(
            element_name="Most Used",
            source=APP_CONFIG.most_used_nodes,
            should_be_sorted=False,
        )
        self.SetActiveWhiteboard(whiteboard)

        log_area = log_wgt_t()
        log_area.setReadOnly(True)
        log_area.setLineWrapMode(wdgt.QTextEdit.LineWrapMode.NoWrap)
        AddGenericHandler(log_area.insertHtml, supports_html=True)
        self.log_area = log_area

        doc_area = wdgt.QTextEdit()
        doc_area.setReadOnly(True)
        doc_area.setLineWrapMode(wdgt.QTextEdit.LineWrapMode.NoWrap)
        self.doc_area = doc_area
        MESSENGER.AddCanal(MSG_NODE_DOCUMENTATION_NEEDED, self.ShowDocumentation)
        MESSENGER.AddCanal(MSG_NODE_IN_OUT_NEEDED, self.ShowInputsAndOutputs)

        tabs = wdgt.QTabWidget()
        tabs.addTab(whiteboard, whiteboard.graph.functional.name)
        tabs.addTab(log_area, "Messages")
        tabs.addTab(doc_area, "Documentation")
        tabs.setStyleSheet("QTabWidget::tab-bar {alignment: center;}")
        tabs.setMovable(True)
        tabs.setTabsClosable(True)
        self.tabs = tabs

        global _DEFAULT_TAB_COLOR
        _DEFAULT_TAB_COLOR = tabs.tabBar().tabTextColor(0)
        self._SetTabColorBlue(0)

        self._BuildMenuBar()
        self.status_bar = self.statusBar()

        layout = wdgt.QGridLayout()
        layout.addWidget(self.node_list.filter_wgt, 0, 0)
        layout.addWidget(self.node_list, 1, 0, 3, 1)
        layout.addWidget(
            wdgt.QLabel('<span style="font-weight:bold; color:blue">Recent</span>'),
            0,
            1,
        )
        layout.addWidget(self.recent_list, 1, 1)
        layout.addWidget(
            wdgt.QLabel('<span style="font-weight:bold; color:blue">Most Used</span>'),
            2,
            1,
        )
        layout.addWidget(self.most_used_list, 3, 1)
        layout.addWidget(tabs, 0, 2, 4, 1)

        central = wdgt.QWidget()
        central.setLayout(layout)
        self.setCentralWidget(central)

        for node_list in (self.node_list, self.recent_list, self.most_used_list):
            SCREEN_BACKEND.AddMessageCanal(
                node_list, "itemClicked", self.AcknowledgeNodeSelected
            )
        SCREEN_BACKEND.AddMessageCanal(
            tabs, "currentChanged", self.UpdateActiveWhiteboard
        )
        SCREEN_BACKEND.AddMessageCanal(tabs, "tabCloseRequested", self.RemoveWhiteboard)

    @staticmethod
    def Instance() -> runner_wdw_t | None:
        """"""
        for widget in wdgt.QApplication.topLevelWidgets():
            if isinstance(widget, runner_wdw_t):
                return widget

        return None

    def _BuildMenuBar(self) -> None:
        """"""
        menu_bar = self.menuBar()
        for text, entries in MAIN_MENUS.items():
            menu = menu_bar.addMenu(text)
            BuildMenu(menu, entries, self)

        found = False
        for action in menu_bar.actions():
            if action.text() == "&File":
                for sub_action in action.menu().actions():
                    if sub_action.text() == "Load Recent...":
                        self.load_recent_menu = sub_action.menu()
                        found = True
                        break
                if found:
                    break
        else:
            raise RuntimeError('No "Load Recent" menu found.')

    def _LoadRecentEntries(self) -> entry_t | tuple[entry_t, ...]:
        """"""
        recent_s = APP_CONFIG.recent_flows
        if recent_s.__len__() > 0:
            return tuple(
                entry_t(
                    text=str(_pth),
                    action="LoadOrSaveWorkflow",
                    args="load recent",
                    kwargs={"recent": _pth},
                )
                for _pth in recent_s
            )

        return entry_t(text="No Recent Workflows")

    def AddWhiteboard(self) -> None:
        """"""
        whiteboard = whiteboard_t()
        self.SetActiveWhiteboard(whiteboard)

        tabs = self.tabs
        tabs.insertTab(0, whiteboard, whiteboard.graph.functional.name)
        self._SetTabColorBlue(0)
        tabs.setCurrentIndex(0)

    @property
    def whiteboard_names(self) -> tuple[str, ...]:
        """"""
        return tuple(self.tabs.tabText(_elm) for _elm in range(self.tabs.count()))

    def SetActiveWhiteboard(self, whiteboard: whiteboard_t, /) -> None:
        """"""
        self.active_whiteboard = whiteboard
        NAME_MANAGER.SetCurrentNodeManager(whiteboard.graph.functional.name)

    def UpdateActiveWhiteboard(self, index: int, /) -> None:
        """"""
        widget = self.tabs.widget(index)
        if isinstance(widget, whiteboard_t):
            self.SetActiveWhiteboard(widget)
            self._SetTabColorBlue(index)

    def _SetTabColorBlue(self, index: int, /) -> None:
        """"""
        tabs = self.tabs
        tab_bar = tabs.tabBar()
        for current in range(tabs.count()):
            if current == index:
                color = PLAIN_BLUE
            else:
                color = _DEFAULT_TAB_COLOR
            tab_bar.setTabTextColor(current, color)

    def RemoveWhiteboard(self, index: int, /) -> None:
        """"""
        tabs = self.tabs
        if tabs.__len__() < 4:
            return

        widget = tabs.widget(index)
        if isinstance(widget, whiteboard_t):
            NAME_MANAGER.RemoveGraphName(tabs.tabText(index))
            tabs.removeTab(index)
            for idx in range(tabs.count()):
                new_widget = tabs.widget(idx)
                if isinstance(new_widget, whiteboard_t):
                    self.SetActiveWhiteboard(new_widget)
                    self._SetTabColorBlue(idx)
                    break

    @property
    def active_paths(self) -> dict[save_mode_h, path_t]:
        """"""
        return self.active_whiteboard.paths

    def AcknowledgeNodeSelected(self, item: wdgt.QListWidgetItem, /) -> None:
        """"""
        name = item.text()
        which = self.tabs.currentIndex()
        if which == 0:
            self.AddNode(name)
        elif which == 2:
            self.ShowDocumentation(name)

    def ShowDocumentation(self, stripe: str, /) -> None:
        """"""
        try:
            description = NODE_CATALOG[stripe]
        except NodeNotFoundError:
            description = None

        doc_area = self.doc_area
        doc_area.clear()
        if description is None:
            doc_area.setText(f"Node {stripe}: Not found in catalog.")
        else:
            description.Activate()
            doc_area.setText(description.AsStr())
        tabs = self.tabs
        if tabs.widget(tabs.currentIndex()) is not doc_area:
            tabs.setCurrentIndex(tabs.indexOf(doc_area))

    def ShowInputsAndOutputs(self, node: node_t, /) -> None:
        """"""
        functional = node.functional
        LOGGER.info(f"NODE {functional.name}")
        for name, elements in zip(
            ("Input(s)", "Output(s)"), (functional.inputs, functional.outputs)
        ):
            as_str = []
            for key, value in elements.items():
                as_str.append(f"{key}: {value}")
            as_str = "\n".join(as_str)
            LOGGER.info(f"{name}\n{as_str}")
        LOGGER.info(
            f"=> Needs running: {functional.needs_running}, Can run: {functional.can_run}"
        )

        log_area = self.log_area
        tabs = self.tabs
        if tabs.widget(tabs.currentIndex()) is not log_area:
            tabs.setCurrentIndex(tabs.indexOf(log_area))

    def AddNode(self, name: str, /) -> None:
        """"""
        whiteboard = self.active_whiteboard
        node = whiteboard.graph.AddNode(name, and_return_it=True)
        node.setPos(whiteboard.mapToScene(whiteboard.viewport().rect().center()))

        APP_CONFIG.UpdateRecentNodes(name)
        APP_CONFIG.UpdateMostUsedNodes(name)
        self.recent_list.UpdateSource(APP_CONFIG.recent_nodes)
        self.most_used_list.UpdateSource(APP_CONFIG.most_used_nodes)

    def LoadOrSaveWorkflow(
        self,
        operation: load_mode_h | save_mode_h,
        /,
        *,
        recent: path_t | None = None,
    ) -> None:
        """"""
        filename = None
        if operation in ("save as script", "save as screenshot"):
            operation: save_mode_h
            last_saving = self.active_paths.get(
                operation, APP_CONFIG.LastSavingFolder(operation)
            )
        else:
            last_saving = None

        if operation == "load":
            filename = LoadWorkflow(
                self, self.active_whiteboard, APP_CONFIG.last_loading_folder
            )
        elif operation == "load recent":
            filename = LoadWorkflow(self, self.active_whiteboard, recent)
        elif operation == "save":
            operation: save_mode_h
            last_saving = self.active_paths.get(operation)
            if last_saving is None:
                self.LoadOrSaveWorkflow("save as")
            else:
                _ = SaveWorkflow(self.active_whiteboard.graph, last_saving, self)
        elif operation == "save as":
            operation: save_mode_h
            filename = SaveWorkflow(
                self.active_whiteboard.graph,
                APP_CONFIG.LastSavingFolder(operation),
                self,
            )
        elif operation == "save as script":
            filename = SaveWorkflowAsScript(
                self.active_whiteboard.graph,
                last_saving,
                self,
            )
        elif operation == "save as screenshot":
            filename = SaveWorkflowAsScreenshot(
                self.active_whiteboard,
                last_saving,
                self,
            )
        else:
            raise LoadSaveError(f"Operation {operation} invalid.")

        if filename is None:
            return

        if operation in ("load", "load recent", "save as"):
            APP_CONFIG.UpdateRecentFlows(filename)
            if operation in ("load", "load recent"):
                APP_CONFIG.UpdateLastLoadingFolder(filename.parent)
                tabs = self.tabs
                index = tabs.indexOf(self.active_whiteboard)
                tabs.setTabText(index, self.active_whiteboard.graph.functional.name)
                tooltip = "\n".join(
                    f"{_key}: {_vle}" for _key, _vle in self.active_paths.items()
                )
                tabs.setTabToolTip(index, tooltip)
            elif operation == "save as":
                operation: save_mode_h
                APP_CONFIG.UpdateLastSavingFolder(operation, filename.parent)

            self.load_recent_menu.clear()
            AddEntriesToMenu(
                self._LoadRecentEntries(),
                self.load_recent_menu,
                self,
            )
        elif operation in ("save as script", "save as screenshot"):
            operation: save_mode_h
            APP_CONFIG.UpdateLastSavingFolder(operation, filename.parent)
            self.active_paths[operation] = filename

    def RunWorkflow(self) -> None:
        """"""
        tabs = self.tabs
        index = tabs.indexOf(self.active_whiteboard)
        LOGGER.info(f"WORKFLOW: {tabs.tabText(index)}")
        self.active_whiteboard.RunWorkflow()

    def OpenAboutDialog(self, _: bool, /) -> None:
        """"""
        wdgt.QMessageBox.about(
            self,
            "About pyVispr",
            f"<b>pyVispr {__version__}</b><br/><br/>"
            f"<i>Documentation:</i><br/>"
            f"<a href={DOCUMENTATION_ADDRESS}>{DOCUMENTATION_ADDRESS}</a><br/>"
            f"<i>Source Code:</i><br/>"
            f"<a href={SOURCE_ADDRESS}>{SOURCE_ADDRESS}</a>",
        )

    def OpenConfiguration(self, _: bool, /) -> None:
        """"""
        config = config_wgt_t()
        config.exec()

    def OpenAboutWorkflowDialog(self, _: bool, /) -> None:
        """"""
        n_nodes, n_links = self.active_whiteboard.Statistics()
        wdgt.QMessageBox.about(
            self,
            "About Workflow",
            f"Nodes: {n_nodes}\nLinks: {n_links}",
        )

    def Close(self) -> None:
        """"""
        if (self.active_paths.get("save") is None) and (
            self.active_whiteboard.graph.nodes.__len__() > 0
        ):
            should_save = wdgt.QMessageBox(parent=self)
            should_save.setText("The workflow has not been saved.")
            should_save.setInformativeText("Do you want to save it?")
            should_save.setStandardButtons(
                wdgt.QMessageBox.StandardButton.Yes | wdgt.QMessageBox.StandardButton.No
            )
            should_save.setDefaultButton(wdgt.QMessageBox.StandardButton.Yes)
            answer = should_save.exec()
            if answer == wdgt.QMessageBox.StandardButton.Yes:
                self.LoadOrSaveWorkflow("save as")
        APP_CONFIG.Save()
        self.close()


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
