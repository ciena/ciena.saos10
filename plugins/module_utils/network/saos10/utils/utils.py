#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2021 Ciena
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# utils


def config_is_diff(new_config, actual_config):
    """Compares actual configuration with intended new

    :rtype: Bool
    :returns: True if configs are equal, False if not. 

    """
    return new_config != actual_config
