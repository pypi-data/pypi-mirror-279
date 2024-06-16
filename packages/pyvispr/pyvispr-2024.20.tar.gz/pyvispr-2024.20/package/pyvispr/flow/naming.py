"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2017
SEE COPYRIGHT NOTICE BELOW
"""

import dataclasses as dtcl

from pyvispr.constant.flow.uid import UNIQUE_NAME_SEPARATOR
from pyvispr.extension.object.field import NonInitField_NONE


@dtcl.dataclass(slots=True, repr=False, eq=False)
class _name_manager_t(list[str]):

    def NewUniqueName(
        self, wished_name: str, /, *, in_replacement_of: str | None = None
    ) -> str:
        """"""
        if in_replacement_of is not None:
            self.RemoveName(in_replacement_of)

        if wished_name in self:
            where = wished_name[1:-1].find(UNIQUE_NAME_SEPARATOR)
            if (where >= 0) and wished_name[(where + 2) :].isdigit():
                wished_name = wished_name[: (where + 1)]
            version = 1
            while f"{wished_name}{UNIQUE_NAME_SEPARATOR}{version}" in self:
                version += 1

            output = f"{wished_name}{UNIQUE_NAME_SEPARATOR}{version}"
        else:
            output = wished_name

        self.append(output)

        return output

    def RemoveName(self, name: str, /) -> None:
        """"""
        self.remove(name)


@dtcl.dataclass(slots=True, repr=False, eq=False)
class name_manager_t(dict[str, _name_manager_t]):
    """
    Serves as both graph and node name manager.
    str: graph name.
    """

    current_graph_name: str | None = NonInitField_NONE()
    current_node_manager: _name_manager_t | None = NonInitField_NONE()

    def SetCurrentNodeManager(self, graph: str, /) -> None:
        """"""
        self.current_graph_name = graph
        self.current_node_manager = self[graph]

    @property
    def graph_names(self) -> _name_manager_t:
        """"""
        output = _name_manager_t()
        output.extend(self.keys())
        return output

    def NewUniqueGraphName(
        self, wished_name: str, /, *, in_replacement_of: str | None = None
    ) -> str:
        """"""
        graph_names = self.graph_names

        if in_replacement_of is None:
            output = graph_names.NewUniqueName(wished_name)
            self[output] = _name_manager_t()
        else:
            output = graph_names.NewUniqueName(
                wished_name, in_replacement_of=in_replacement_of
            )
            self.DealWithNewGraphName(in_replacement_of, str(output))

        return output

    def DealWithNewGraphName(self, old_name: str, new_name: str, /) -> None:
        """"""
        self[new_name] = self[old_name]
        del self[old_name]

    def RemoveGraphName(self, name: str, /) -> None:
        """"""
        del self[name]


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
