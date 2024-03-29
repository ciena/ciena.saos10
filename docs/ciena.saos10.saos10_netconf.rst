.. _ciena.saos10.saos10_netconf:


*******************
ciena.saos10.saos10
*******************

**Use saos10 netconf plugin to run netconf commands on Ciena saos10 platform**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This saos10 plugin provides low level abstraction apis for sending and receiving netconf commands from Ciena saos10 network devices.




Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
                <th>Configuration</th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ncclient_device_handler</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"alu"</div>
                </td>
                    <td>
                    </td>
                <td>
                        <div>Specifies the ncclient device handler name for Ciena saos10 network os. To identify the ncclient device handler name refer ncclient library documentation.</div>
                </td>
            </tr>
    </table>
    <br/>








Status
------


Authors
~~~~~~~

- Jeff Groom (@jgroom33)


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.
