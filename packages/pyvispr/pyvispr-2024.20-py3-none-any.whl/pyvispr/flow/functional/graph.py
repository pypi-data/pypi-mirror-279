"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2017
SEE COPYRIGHT NOTICE BELOW
"""

from __future__ import annotations

import dataclasses as dtcl
import typing as h

from logger_36 import LOGGER
from pyvispr.constant.flow.node import MSG_NODE_STATE_CHANGED, UNIQUE_NAME_INPUT
from pyvispr.flow.functional.link import links_t
from pyvispr.flow.functional.node import node_t, state_e
from pyvispr.flow.functional.value import EncodedValue
from pyvispr.runtime.config import APP_CONFIG
from pyvispr.runtime.naming import NAME_MANAGER
from sio_messenger.instance import MESSENGER


@dtcl.dataclass(repr=False, eq=False)
class graph_t(list[node_t]):
    """
    Cannot be sloted because of QThread issue with weak reference (see visual.graph).
    """

    name: str
    links: links_t = dtcl.field(init=False, default_factory=links_t)

    @classmethod
    def New(cls, /, *, wished_name: str | None = None) -> graph_t:
        """"""
        return cls(name=NAME_MANAGER.NewUniqueGraphName(wished_name))

    def Rename(self, wished_name: str, /) -> None:
        """"""
        self.name = NAME_MANAGER.NewUniqueGraphName(
            wished_name, in_replacement_of=self.name
        )

    def AddNode(
        self,
        stripe: str,
        /,
        *,
        wished_name: str | None = None,
        and_return_it: bool = False,
    ) -> node_t | None:
        """"""
        node = node_t.NewWithTypeForGraph(stripe, self.name, wished_name=wished_name)
        if node is None:
            return None

        self.append(node)
        if and_return_it:
            return node

    def ToggleNodeAbility(self, node: node_t, /) -> None:
        """"""
        if node.state is state_e.disabled:
            node.state = state_e.todo
        else:
            self.InvalidateNodeOutputs(node)
            node.state = state_e.disabled
        MESSENGER.Transmit(MSG_NODE_STATE_CHANGED, node)

    def InvalidateNodeOutputs(self, node: node_t, /) -> None:
        """"""
        if node.state is state_e.disabled:
            return

        node.InvalidateOutputs()

        for descendant in self.links.DescendantsOfNode(node):
            descendant, socket_pairs = descendant
            for _, input_name in socket_pairs:
                descendant.InvalidateInput(name=input_name)

    def RemoveNode(self, node: node_t, /) -> None:
        """"""
        self.InvalidateNodeOutputs(node)

        self.RemoveLink(node, None, None, None)
        self.RemoveLink(None, None, node, None)

        self.remove(node)
        NAME_MANAGER[self.name].RemoveName(node.name)

    def AddLink(
        self, source: node_t, output_name: str, target: node_t, input_name: str, /
    ) -> None:
        """"""
        self.links.Add(
            source,
            output_name,
            target,
            input_name,
        )
        self.InvalidateNodeOutputs(target)

    def LinksBetween(
        self, source: node_t, target: node_t, /
    ) -> tuple[tuple[str, str], ...]:
        """"""
        output = self.links.SocketPairsOfLink(source, target)
        if output is None:
            return ()
        return tuple(output)

    def RemoveLink(
        self,
        source: node_t | None,
        output_name: str | None,
        target: node_t | None,
        input_name: str | None,
        /,
    ) -> None:
        """
        Removes one or several links assuming that the link(s) exist(s).
        """
        if target is not None:
            self.InvalidateNodeOutputs(target)

        self.links.Remove(source, output_name, target, input_name)

    def MergeWith(self, other: graph_t, /) -> None:
        """"""
        name_manager = NAME_MANAGER[self.name]
        for node in other:
            node.name = name_manager.NewUniqueName(node.name)
        NAME_MANAGER.RemoveGraphName(other.name)

        self.extend(other)
        self.links.extend(other.links)

    def Run(
        self,
        /,
        *,
        script_accessor: h.TextIO = None,
    ) -> tuple[node_t, ...]:
        """"""
        if should_log_node_run := APP_CONFIG.should_log_node_run:
            LOGGER.info("START running workflow")

        should_save_as_script = script_accessor is not None

        if should_save_as_script:
            _WritePrologue(self, script_accessor)
            values_script = {}
        else:
            values_script = None

        while True:
            needs_running = tuple(filter(lambda _elm: _elm.needs_running, self))
            if needs_running.__len__() == 0:
                break
            can_run = tuple(filter(lambda _elm: _elm.can_run, needs_running))
            if can_run.__len__() == 0:
                break

            for node in can_run:
                if should_save_as_script:
                    self._UpdateValuesForScript(values_script, node)

                if should_log_node_run:
                    LOGGER.info(f"Running {node.name}")
                node.Run(
                    workflow=self.name,
                    script_accessor=script_accessor,
                    values_script=values_script,
                )
                self.SendNodeOutputsToSuccessors(node)

        if should_save_as_script and (needs_running.__len__() > 0):
            script_accessor.write(
                'print("Workflow saving was incomplete due to some nodes not being '
                'runnable.")'
            )

        if should_log_node_run:
            LOGGER.info(f"DONE running workflow (unrun: {needs_running.__len__()})")

        return needs_running

    def _UpdateValuesForScript(
        self, values_script: dict[str, str], node: node_t, /
    ) -> None:
        """"""
        values_script.clear()

        for name, input_ in node.inputs.items():
            if input_.has_value:
                attached = self.links.InputSocketIsFree(
                    node, name, should_return_socket=True
                )
                if attached is None:
                    value_script = EncodedValue(input_.value)
                else:
                    predecessor, name_s_out = attached
                    value_script = predecessor.UniqueOutputName(name_s_out)
            else:
                default_value = node.description.inputs[name].default_value
                value_script = EncodedValue(default_value)
            values_script[name] = value_script

        if node.description.wants_unique_name:
            values_script[UNIQUE_NAME_INPUT] = f'"{node.name}"'

    def SendNodeOutputsToSuccessors(self, node: node_t, /) -> None:
        """"""
        for name_out, output in node.outputs.items():
            value = output.value
            successors = self.links.SuccessorsOfNode(node, output_name=name_out)
            for successor, socket_pairs in successors:
                for _, name_in in socket_pairs:
                    successor.SetInputValue(name_in, value)

    def Invalidate(self) -> None:
        """"""
        for node in self:
            if node.state is not state_e.disabled:
                node.InvalidateInput()


def _WritePrologue(nodes: h.Sequence[node_t], script_accessor: h.TextIO, /) -> None:
    """"""
    script_accessor.write(
        "from importlib import import_module\n"
        "from importlib import util\n"
        "from pathlib import Path as path_t\n"
        "from json_any import JsonStringOf, ObjectFromJsonString\n\n"
    )

    already_written = []
    for node in nodes:
        if node.state is not state_e.todo:
            continue

        description = node.description
        if description in already_written:
            continue

        actual_path = description.actual.path
        actual_name = description.actual.name
        if isinstance(actual_path, str):
            loading = f'module = import_module("{actual_path}")'
        else:
            ldg_path = f'path = path_t("{actual_path}").expanduser()'
            ldg_spec = "spec = util.spec_from_file_location(path.stem, path)"
            ldg_module = "module = spec.loader.load_module(spec.name)"
            loading = f"{ldg_path}\n{ldg_spec}\n{ldg_module}"
        getting = (
            f"{description.function_name_for_script} = "
            f'getattr(module, "{actual_name}")'
        )
        script_accessor.write(f"{loading}\n{getting}\n\n")
        already_written.append(description)


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
