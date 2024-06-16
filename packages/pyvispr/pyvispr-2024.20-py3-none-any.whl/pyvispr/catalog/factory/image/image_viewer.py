"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2017
SEE COPYRIGHT NOTICE BELOW
"""

from __future__ import annotations

from pathlib import Path as path_t

import numpy
import PyQt6.QtCore as core
import PyQt6.QtGui as qtui
import PyQt6.QtWidgets as wdgt
from logger_36 import LOGGER
from pyvispr.extension.qt.app import ExecuteApp, QtApp
from pyvispr.interface.window.runner import runner_wdw_t
from pyvispr.runtime.backend import SCREEN_BACKEND
from pyvispr.runtime.persistence import PERSISTENCE

DEFAULT_SAVE_EXTENSION = "png"  # lowercase

_IMG_FORMAT = {
    1: qtui.QImage.Format.Format_Indexed8,
    3: qtui.QImage.Format.Format_RGB888,
    4: qtui.QImage.Format.Format_RGBA8888,
}
_IMG_FORMAT_AS_STR = {1: "Grayscale 8 bits", 3: "RGB 8 bits", 4: "RGBA 8 bits"}

# Action name {...}_action, menu text, shortcut, method name
_MENU_ENTRIES = (
    ("quit", "&Quit", qtui.QKeySequence.StandardKey.Quit, "close"),
    (
        "save",
        "&Save",
        qtui.QKeySequence.StandardKey.Save,
        "SaveImage",
    ),
    ("copy", "&Copy", qtui.QKeySequence.StandardKey.Copy, "CopyImage"),
    ("zoom_in", "Zoom &In (25%)", "Ctrl++", "ZoomImageIn"),
    ("zoom_out", "Zoom &Out (25%)", "Ctrl+-", "ZoomImageOut"),
    ("original_size", "Original Si&ze", "Ctrl+=", "RevertImageToOriginalSize"),
    ("fit_to_window", "&Fit to Window", "Ctrl+/", "FitImageToWindow"),
)

_statistic_h = int | float | numpy.ndarray


def pyVisprImageViewer(
    image: numpy.ndarray, /, *, pyvispr_name: str | None = None
) -> None:
    """"""
    if (
        (not isinstance(image, numpy.ndarray))
        or (image.size < 1)
        or numpy.any(numpy.isnan(image))
        or numpy.any(numpy.isinf(image))
    ):
        LOGGER.error(
            f"{pyVisprImageViewer.__name__}.{pyvispr_name}: "
            f"Image is empty or contains NaN or Inf."
        )
        return

    img_shape = image.shape
    if 1 < len(img_shape) < 4:
        width = img_shape[1]
        height = img_shape[0]
        if len(img_shape) == 2:
            depth = 1
        else:
            depth = img_shape[2]
            if depth not in (3, 4):
                LOGGER.error(
                    f"{pyVisprImageViewer.__name__}.{pyvispr_name}: "
                    f"Input 3rd dimension is {depth}; It must be 3 or 4 instead."
                )
                return
    else:
        LOGGER.error(
            f"{pyVisprImageViewer.__name__}.{pyvispr_name}: "
            f"Input must be a 2D or 3D numpy array"
        )
        return

    if pyvispr_name in PERSISTENCE:
        viewer = PERSISTENCE[pyvispr_name]
        viewer.Update(image, width, height, depth)
    else:
        app, should_exec = QtApp()
        viewer = viewer_t(
            pyvispr_name,
            image,
            width,
            height,
            depth,
        )
        viewer.show()
        ExecuteApp(app, should_exec=should_exec, should_exit=False)


class viewer_t(wdgt.QMainWindow):
    def __init__(
        self,
        name: str | None,
        image: numpy.ndarray,
        width: int,
        height: int,
        depth: int,
    ):
        """"""
        wdgt.QMainWindow.__init__(self, runner_wdw_t.Instance())
        self.setAttribute(core.Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setWindowTitle("pyVispr Image Viewer")
        if name is None:
            self.name = f"Unknown Node {id(self)}"
        else:
            self.name = name
        PERSISTENCE[self.name] = self

        self.menu_info: wdgt.QMenu | None = None
        self.quit_action: qtui.QAction | None = None
        self.save_action: qtui.QAction | None = None
        self.copy_action: qtui.QAction | None = None
        self.zoom_in_action: qtui.QAction | None = None
        self.zoom_out_action: qtui.QAction | None = None
        self.original_size_action: qtui.QAction | None = None
        self.fit_to_window_action: qtui.QAction | None = None
        self._CreateActions()

        self.last_save_location = path_t.home()

        screen_size = self.screen().availableGeometry()
        wdw_width = min(width, int(0.75 * screen_size.width()))
        wdw_height = min(height, int(0.75 * screen_size.height()))
        self.resize(wdw_width, wdw_height)

        min_value, max_value, mean_value, median_value = _ImageStatistics(image, depth)
        self._CreateMenus(
            width,
            height,
            depth,
            min_value,
            max_value,
            mean_value,
            median_value,
        )

        name_wgt = wdgt.QLabel(f'<span style="font-weight:bold">{self.name}</span>')
        name_wgt.setContentsMargins(6, 6, 0, 0)

        self.status_bar = wdgt.QStatusBar()
        self.image_container = _image_container(image, depth, self.status_bar)
        self.image_container.setBackgroundRole(qtui.QPalette.ColorRole.Base)
        self.image_container.setSizePolicy(
            wdgt.QSizePolicy.Policy.Ignored, wdgt.QSizePolicy.Policy.Ignored
        )
        self.image_container.setScaledContents(True)

        self.scroll_area = wdgt.QScrollArea()
        self.scroll_area.setBackgroundRole(qtui.QPalette.ColorRole.Dark)
        self.scroll_area.setWidget(self.image_container)

        layout = wdgt.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(name_wgt)
        layout.addWidget(self.scroll_area)
        layout.addWidget(self.status_bar)

        central_widget = wdgt.QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self._SetPixmap(image, width, height, depth, min_value, max_value)

    def _CreateActions(self) -> None:
        """"""
        for action_name, entry, shortcut, method_name in _MENU_ENTRIES:
            action = qtui.QAction(entry, self)
            action.setShortcut(shortcut)
            setattr(self, f"{action_name}_action", action)

            method = getattr(self, method_name)

            SCREEN_BACKEND.AddMessageCanal(action, "triggered", method)

        self.fit_to_window_action.setCheckable(True)

    def _UpdateActions(self) -> None:
        """"""
        self.zoom_in_action.setEnabled(not self.fit_to_window_action.isChecked())
        self.zoom_out_action.setEnabled(not self.fit_to_window_action.isChecked())
        self.original_size_action.setEnabled(not self.fit_to_window_action.isChecked())

    def _CreateMenus(
        self,
        width: int,
        height: int,
        depth: int,
        min_value: _statistic_h,
        max_value: _statistic_h,
        mean_value: _statistic_h,
        median_value: _statistic_h,
    ) -> None:
        """"""
        numpy.set_printoptions(precision=1, floatmode="fixed")

        menu_bar = self.menuBar()

        menu = wdgt.QMenu("&Viewer", self)
        menu.addAction(self.quit_action)
        menu_bar.addMenu(menu)

        menu = wdgt.QMenu("&Image", self)
        menu.addAction(self.save_action)
        menu.addAction(self.copy_action)
        menu_bar.addMenu(menu)

        menu = wdgt.QMenu("Image &Size", self)
        menu.addAction(self.zoom_in_action)
        menu.addAction(self.zoom_out_action)
        menu.addAction(self.original_size_action)
        menu.addSeparator()
        menu.addAction(self.fit_to_window_action)
        menu_bar.addMenu(menu)

        menu = wdgt.QMenu("Image I&nfo", self)
        menu.addAction(f"WxH: {width}x{height}")
        menu.addAction(_IMG_FORMAT_AS_STR[depth])
        menu.addAction(f"min: {min_value}")
        menu.addAction(f"max: {max_value}")
        menu.addAction(f"mean: {mean_value}")
        menu.addAction(f"median: {median_value}")
        self.menu_info = menu
        for action in menu.actions():
            action.setEnabled(False)
        menu_bar.addMenu(menu)

        self._UpdateActions()

    def _SetPixmap(
        self,
        image: numpy.ndarray,
        width: int,
        height: int,
        depth: int,
        min_value: _statistic_h,
        max_value: _statistic_h,
        /,
    ) -> None:
        """"""
        image_0_255, depth_0_255 = _NewNImage_0_255(image, min_value, max_value, depth)
        self.q_img, self.np_img = _NewQImage(image_0_255, width, height, depth_0_255)

        self.image_container.setPixmap(qtui.QPixmap.fromImage(self.q_img))

        if not self.fit_to_window_action.isChecked():
            self.image_container.adjustSize()

    def Update(
        self,
        image: numpy.ndarray,
        width: int,
        height: int,
        depth: int,
    ) -> None:
        """"""
        min_value, max_value, mean_value, median_value = _ImageStatistics(image, depth)
        new_texts = (
            f"WxH: {width}x{height}",
            _IMG_FORMAT_AS_STR[depth],
            f"min: {min_value}",
            f"max: {max_value}",
            f"mean: {mean_value}",
            f"median: {median_value}",
        )
        for action, text in zip(self.menu_info.actions(), new_texts):
            action.setText(text)

        self.image_container.Update(image, depth)
        self._SetPixmap(image, width, height, depth, min_value, max_value)

    def ZoomImageIn(self) -> None:
        """"""
        self._ScaleImage(1.25)

    def ZoomImageOut(self) -> None:
        """"""
        self._ScaleImage(0.8)

    def _ScaleImage(self, factor: float, /) -> None:
        """"""
        self.image_container.scale *= factor
        self.image_container.resize(
            self.image_container.scale * self.image_container.pixmap().size()
        )

        _AdjustScrollBarPosition(self.scroll_area.horizontalScrollBar(), factor)
        _AdjustScrollBarPosition(self.scroll_area.verticalScrollBar(), factor)

        self.zoom_in_action.setEnabled(self.image_container.scale < 3.0)
        self.zoom_out_action.setEnabled(self.image_container.scale > 0.333)

    def RevertImageToOriginalSize(self) -> None:
        """"""
        self.image_container.adjustSize()
        self.image_container.scale = 1.0

    def FitImageToWindow(self) -> None:
        """"""
        img_should_fit_to_wdw = self.fit_to_window_action.isChecked()
        self.scroll_area.setWidgetResizable(img_should_fit_to_wdw)
        if img_should_fit_to_wdw:
            self.image_container.scale = -1.0
        else:
            self.RevertImageToOriginalSize()

        self._UpdateActions()

    def CopyImage(self) -> None:
        """"""
        wdgt.QApplication.clipboard().setImage(self.q_img)

    def SaveImage(self) -> None:
        """"""
        supported_formats = list(
            map(
                lambda elm: bytearray(elm).decode().lower(),
                qtui.QImageWriter.supportedImageFormats(),
            )
        )
        supported_formats.sort()

        default_save_extension = DEFAULT_SAVE_EXTENSION
        if default_save_extension not in supported_formats:
            default_save_extension = supported_formats[0]
        default_save_format = _NewFileFormatFilter(default_save_extension)

        supported_formats = ";;".join(map(_NewFileFormatFilter, supported_formats))

        filename = wdgt.QFileDialog.getSaveFileName(
            self,
            "Save Image",
            str(self.last_save_location),
            supported_formats,
            default_save_format,
        )
        if (filename is None) or (len(filename[0]) == 0):
            return
        filename = filename[0]

        self.last_save_location = path_t(filename).parent

        img_writer = qtui.QImageWriter(filename)

        if not img_writer.write(self.q_img):
            LOGGER.error(
                f"{pyVisprImageViewer.__name__}.{self.name}: "
                f"Failure in saving image to '{filename}': {img_writer.errorString()}"
            )

    def closeEvent(self, event: qtui.QCloseEvent, /) -> None:
        """"""
        del PERSISTENCE[self.name]
        wdgt.QMainWindow.closeEvent(self, event)


class _image_container(wdgt.QLabel):
    def __init__(
        self,
        image: numpy.ndarray,
        depth: int,
        status_bar: wdgt.QStatusBar,
        *args,
        **kwargs,
    ) -> None:
        """"""
        wdgt.QLabel.__init__(self, *args, **kwargs)

        self.image: numpy.ndarray | None = None
        self.row_width: str = ""
        self.col_width: str = ""
        self.scale: float = 1.0
        self.should_color_sb: bool = False
        self.Update(image, depth)

        self.status_bar = status_bar
        self.setMouseTracking(True)

    def Update(
        self,
        image: numpy.ndarray,
        depth: int,
    ) -> None:
        """"""
        self.image = image
        self.row_width = str(self.image.shape[0]).__len__()
        self.col_width = str(self.image.shape[1]).__len__()
        self.scale = 1.0
        self.should_color_sb = (
            (depth > 2)
            and numpy.issubdtype(image.dtype, numpy.integer)
            and (not numpy.any(image < 0))
            and (not numpy.any(image > 255))
        )

    def mouseMoveEvent(self, event: qtui.QMoveEvent, /) -> None:
        """"""
        position = event.pos()
        if self.scale > 0.0:
            row = int(round(position.y() / self.scale))
            col = int(round(position.x() / self.scale))
        else:
            row = int(
                round(position.y() * ((self.image.shape[0] - 1) / (self.height() - 1)))
            )
            col = int(
                round(position.x() * ((self.image.shape[1] - 1) / (self.width() - 1)))
            )
        color = self.image[row, col, ...]
        if self.should_color_sb:
            self.status_bar.setStyleSheet(
                f"font-weight: bold; "
                f"background-color: rgb({color[0]}, {color[1]}, {color[2]}); "
                f"color: rgb({255 - color[0]}, {255 - color[1]}, {255 - color[2]})"
            )
        self.status_bar.showMessage(
            f"ROWxCOL:{row:{self.row_width}}x{col:{self.col_width}} = {color}"
        )


def _ImageStatistics(image: numpy.ndarray, depth: int, /) -> tuple[
    _statistic_h,
    _statistic_h,
    _statistic_h,
    _statistic_h,
]:
    """"""
    if depth == 1:
        min_value = numpy.amin(image).item()
        max_value = numpy.amax(image).item()
        mean_value = numpy.around(numpy.mean(image), decimals=2).item()
        median_value = numpy.around(numpy.median(image), decimals=2).item()
    else:
        min_value = numpy.amin(numpy.amin(image, axis=0), axis=0)
        max_value = numpy.amax(numpy.amax(image, axis=0), axis=0)
        mean_value = numpy.around(
            numpy.mean(numpy.mean(image, axis=0), axis=0), decimals=2
        )
        median_value = numpy.around(
            [numpy.median(image[:, :, _elm]) for _elm in range(depth)],
            decimals=2,
        )

    return min_value, max_value, mean_value, median_value


def _NewNImage_0_255(
    image: numpy.ndarray,
    min_value: _statistic_h,
    max_value: _statistic_h,
    depth: int,
    /,
) -> tuple[numpy.ndarray, int]:
    """"""
    if numpy.issubdtype(image.dtype, bool):
        output = numpy.zeros_like(image, dtype=numpy.uint8)
        output[image] = 255
        return output, depth

    if isinstance(min_value, numpy.ndarray):
        if (depth == 4) and (min_value[3] == max_value[3]):
            image = image[..., :3]
            depth = 3
            global_min = min(min_value[:3])
            global_max = max(max_value[:3])
        else:
            global_min = min(min_value)
            global_max = max(max_value)
    else:
        global_min, global_max = min_value, max_value
    if global_max == global_min:
        return numpy.full_like(image, 255, dtype=numpy.uint8), depth

    if (global_min, global_max) != (0, 255):
        factor = 255.0 / (global_max - global_min)
        with_min_zero = image.astype(numpy.float64, copy=False) - global_min
        output = numpy.round(factor * with_min_zero)
    else:
        output = image

    return output.astype(numpy.uint8, copy=False), depth


def _NewQImage(
    image: numpy.ndarray,
    width: int,
    height: int,
    depth: int,
    /,
) -> tuple[qtui.QImage, numpy.ndarray]:
    """"""
    np_img = image
    try:
        q_img = qtui.QImage(
            np_img.data, width, height, depth * width, _IMG_FORMAT[depth]
        )
    except TypeError:
        # /!\ Without .copy(), qtui.QImage sometimes complains with:
        #     QImage(): too many arguments
        #     ...
        np_img = np_img.copy()
        q_img = qtui.QImage(
            np_img.data, width, height, depth * width, _IMG_FORMAT[depth]
        )

    return q_img, np_img


def _AdjustScrollBarPosition(scroll_bar: wdgt.QScrollBar, factor: float, /) -> None:
    """"""
    scroll_bar.setValue(
        int(factor * scroll_bar.value() + ((factor - 1) * scroll_bar.pageStep() / 2))
    )


def _NewFileFormatFilter(extension: str, /) -> str:
    """"""
    return f"{extension.upper()} Images (*.{extension})"


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
