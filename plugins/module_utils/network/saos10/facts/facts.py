# Copyright 2019 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
The facts class for saos10
this file validates each subset of facts and selectively
calls the appropriate facts gathering function
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.facts.facts import (
    FactsBase,
)
from ansible_collections.ciena.saos10.plugins.module_utils.network.saos10.facts.legacy.base import (
    Default,
    Config,
)
from ansible_collections.ciena.saos10.plugins.module_utils.network.saos10.facts.classifiers.classifiers import (
    ClassifiersFacts,
)
from ansible_collections.ciena.saos10.plugins.module_utils.network.saos10.facts.fds.fds import (
    FdsFacts,
)
from ansible_collections.ciena.saos10.plugins.module_utils.network.saos10.facts.fps.fps import (
    FpsFacts,
)

from ansible_collections.ciena.saos10.plugins.module_utils.network.saos10.facts.bgp.bgp import (
    BgpFacts,
)

from ansible_collections.ciena.saos10.plugins.module_utils.network.saos10.facts.isis.isis import (
    IsisFacts,
)

from ansible_collections.ciena.saos10.plugins.module_utils.network.saos10.facts.ldp.ldp import (
    LdpFacts,
)

from ansible_collections.ciena.saos10.plugins.module_utils.network.saos10.facts.logical_ports.logical_ports import (
    Logical_portsFacts,
)

from ansible_collections.ciena.saos10.plugins.module_utils.network.saos10.facts.mpls.mpls import (
    MplsFacts,
)

from ansible_collections.ciena.saos10.plugins.module_utils.network.saos10.facts.ptps.ptps import (
    PtpsFacts,
)

FACT_LEGACY_SUBSETS = dict(default=Default, config=Config)
FACT_RESOURCE_SUBSETS = dict(
    ptps=PtpsFacts,
    mpls=MplsFacts,
    logical_ports=Logical_portsFacts,
    ldp=LdpFacts,
    isis=IsisFacts,
    bgp=BgpFacts,
    fps=FpsFacts,
    fds=FdsFacts,
    classifiers=ClassifiersFacts,
)


class Facts(FactsBase):
    """The fact class for saos10"""

    VALID_LEGACY_GATHER_SUBSETS = frozenset(FACT_LEGACY_SUBSETS.keys())
    VALID_RESOURCE_SUBSETS = frozenset(FACT_RESOURCE_SUBSETS.keys())

    def __init__(self, module):
        super(Facts, self).__init__(module)

    def get_facts(self, legacy_facts_type=None, resource_facts_type=None, data=None):
        """Collect the facts for saos10

        :param legacy_facts_type: List of legacy facts types
        :param resource_facts_type: List of resource fact types
        :param data: previously collected conf
        :rtype: dict
        :return: the facts gathered
        """
        if self.VALID_RESOURCE_SUBSETS:
            self.get_network_resources_facts(FACT_RESOURCE_SUBSETS, resource_facts_type, data)

        if self.VALID_LEGACY_GATHER_SUBSETS:
            self.get_network_legacy_facts(FACT_LEGACY_SUBSETS, legacy_facts_type)

        return self.ansible_facts, self._warnings
