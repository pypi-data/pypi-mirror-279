"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2017
SEE COPYRIGHT NOTICE BELOW
"""

from pathlib import Path as path_t

import numpy
from conf_ini_g.catalog.specification.annotation.path import path_t as path_annotation_t
from skimage.io import imsave as SaveImage


def pyVisprImageSaver(
    image: numpy.ndarray,
    wished_path: path_annotation_t.NewAnnotatedType(
        path_annotation_t.TARGET_TYPE.document, False
    ),
    /,
    *,
    prefix: str = "",
    postfix: str = "",
    should_override: bool = False,
) -> path_t:
    """
    _ii_inputs: wished_path, prefix, postfix, should_override
    _outputs: actual_path
    """
    if isinstance(wished_path, str):
        wished_path = path_t(wished_path)

    path = (
        wished_path.parent / f"{prefix}{wished_path.stem}{postfix}{wished_path.suffix}"
    )
    if path.exists():
        if (not path.is_file()) or not should_override:
            version = 1
            while True:
                path = (
                    wished_path.parent / f"{prefix}{wished_path.stem}{postfix}"
                    f"_{version}{wished_path.suffix}"
                )
                if path.exists():
                    version += 1
                else:
                    break

    SaveImage(str(path), image)

    return path


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
