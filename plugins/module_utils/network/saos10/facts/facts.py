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

FACT_LEGACY_SUBSETS = dict(default=Default, config=Config)


class Facts(FactsBase):
    """The fact class for saos 10"""

    VALID_LEGACY_GATHER_SUBSETS = frozenset(FACT_LEGACY_SUBSETS.keys())

    def __init__(self, module):
        super(Facts, self).__init__(module)

    def get_facts(
        self, legacy_facts_type=None, resource_facts_type=None, data=None
    ):
        """Collect the facts for saos 10
        :param legacy_facts_type: List of legacy facts types
        :param data: previously collected conf
        :rtype: dict
        :return: the facts gathered
        """

        if self.VALID_LEGACY_GATHER_SUBSETS:
            self.get_network_legacy_facts(
                FACT_LEGACY_SUBSETS, legacy_facts_type
            )
        return self.ansible_facts, self._warnings
