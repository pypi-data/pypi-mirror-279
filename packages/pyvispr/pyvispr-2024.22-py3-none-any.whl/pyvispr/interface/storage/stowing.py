"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2017
SEE COPYRIGHT NOTICE BELOW
"""

from pathlib import Path as path_t

import PyQt6.QtWidgets as wdgt
from json_any.task.storage import StoreAsJSON
from logger_36 import LOGGER
from pyvispr.extension.object.exception import AsStr as ExceptionAsStr
from pyvispr.flow.visual.graph import graph_t
from pyvispr.flow.visual.whiteboard import whiteboard_t


def SaveWorkflow(
    graph: graph_t, last_saving: path_t, manager: wdgt.QWidget, /
) -> path_t | None:
    """"""
    filename = _FilenameFromLast(
        last_saving, "Save Workflow", "pyVispr Workflows (*.json.*)", manager
    )
    if filename is None:
        return None

    try:
        filename = StoreAsJSON(
            graph,
            filename,
            should_continue_on_error=True,
            should_overwrite_path=True,
            indent=2,
        )
    except Exception as exception:
        as_str = ExceptionAsStr(exception)
        LOGGER.error(as_str)
        wdgt.QMessageBox.critical(
            None,
            f"Workflow Saving Error",
            as_str,
        )
        return None

    if isinstance(filename, path_t):
        wdgt.QMessageBox.about(
            None,
            "Workflow Successfully Saved",
            f"Workflow Successfully Saved in: {filename}.",
        )
        return filename

    message = "Workflow Saving Error:\n" + "\n".join(filename)
    LOGGER.error(message)
    wdgt.QMessageBox.critical(None, "Workflow Saving Error", message)

    return None


def SaveWorkflowAsScript(
    graph: graph_t, last_saving: path_t, manager: wdgt.QWidget, /
) -> path_t | None:
    """"""
    filename = _FilenameFromLast(
        last_saving, "Save Workflow as Script", "Python Scripts (*.py)", manager
    )
    if filename is None:
        return None

    if filename.suffix.__len__() == 0:
        filename = filename.with_suffix(".py")

    graph.functional.Invalidate()
    try:
        with open(filename, mode="w") as accessor:
            graph.Run(script_accessor=accessor)
    except Exception as exception:
        as_str = ExceptionAsStr(exception)
        LOGGER.error(as_str)
        wdgt.QMessageBox.critical(
            None,
            f"Workflow Saving as Script Error",
            as_str,
        )
        return None

    return filename


def SaveWorkflowAsScreenshot(
    whiteboard: whiteboard_t, last_saving: path_t, manager: wdgt.QWidget, /
) -> path_t | None:
    """"""
    filename = _FilenameFromLast(
        last_saving, "Save Workflow as Screenshot", "Images (*.png *.jpg)", manager
    )
    if filename is None:
        return None

    if filename.suffix.__len__() == 0:
        filename = filename.with_suffix(".png")

    try:
        whiteboard.Screenshot().save(str(filename))
    except Exception as exception:
        as_str = ExceptionAsStr(exception)
        LOGGER.error(as_str)
        wdgt.QMessageBox.critical(
            None,
            f"Workflow Saving as Screenshot Error",
            as_str,
        )
        return None

    return filename


def _FilenameFromLast(
    last_saving: path_t, caption: str, formats: str, manager: wdgt.QWidget, /
) -> path_t | None:
    """"""
    if last_saving.is_file():
        return last_saving

    filename = wdgt.QFileDialog.getSaveFileName(
        manager,
        caption,
        str(last_saving),
        formats,
    )
    if (filename is None) or (filename[0].__len__() == 0):
        return None

    return path_t(filename[0])


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
