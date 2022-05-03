.. _ciena.saos10.xmldiff_module:


********************
ciena.saos10.xmldiff
********************

**return diff for a pair of xml inputs**


Version added: 1.1.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- return diff for a pair of xml inputs




Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>new</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>xml string of config</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>old</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>xml string of config</div>
                </td>
            </tr>
    </table>
    <br/>




Examples
--------

.. code-block:: yaml

    # Consider the following
    # OLD XML string:
    # <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    #   <agg-global xmlns="urn:ietf:params:xml:ns:yang:ciena-ieee-lag">
    #     <global-admin-state>enabled</global-admin-state>
    #     <marker-timeout xmlns="urn:ietf:params:xml:ns:yang:ciena-ext-lag">50</marker-timeout>
    #   </agg-global>
    #   <alarms xmlns="urn:ietf:params:xml:ns:yang:ietf-alarms">
    #     <control>
    #       <max-alarm-status-changes>16</max-alarm-status-changes>
    #       <notify-status-changes>false</notify-status-changes>
    #     </control>
    #   </alarms>
    #   <system xmlns="http://openconfig.net/yang/system">
    #     <config>
    #       <hostname>5162-1</hostname>
    #       <contact xmlns="http://www.ciena.com/ns/yang/ciena-system">Customer Support, Ciena</contact>
    #       <description xmlns="http://www.ciena.com/ns/yang/ciena-system">5162</description>
    #       <location xmlns="http://www.ciena.com/ns/yang/ciena-system">Not Specified</location>
    #     </config>
    #   </system>
    # </config>

    # NEW XML string:
    # <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    #   <agg-global xmlns="urn:ietf:params:xml:ns:yang:ciena-ieee-lag">
    #     <global-admin-state>enabled</global-admin-state>
    #     <marker-timeout xmlns="urn:ietf:params:xml:ns:yang:ciena-ext-lag">50</marker-timeout>
    #   </agg-global>
    #   <alarms xmlns="urn:ietf:params:xml:ns:yang:ietf-alarms">
    #     <control>
    #       <max-alarm-status-changes>16</max-alarm-status-changes>
    #       <notify-status-changes>false</notify-status-changes>
    #     </control>
    #   </alarms>
    #   <system xmlns="http://openconfig.net/yang/system">
    #     <config>
    #       <hostname>5162-1</hostname>
    #       <contact xmlns="http://www.ciena.com/ns/yang/ciena-system">Customer Support, Ciena</contact>
    #       <description xmlns="http://www.ciena.com/ns/yang/ciena-system">5162</description>
    #       <location xmlns="http://www.ciena.com/ns/yang/ciena-system">34.8908084,-40.820916</location>
    #     </config>
    #   </system>
    # </config>

    - name: Get config differences
      ciena.saos10.saos10_xmldiff:
        new: {{ new_xml }}
        old: {{ old_xml }}



Return Values
-------------
Common return values are documented `here <https://docs.ansible.com/ansible/latest/reference_appendices/common_return_values.html#common-return-values>`_, the following are the fields unique to this module:

.. raw:: html

    <table border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Key</th>
            <th>Returned</th>
            <th width="100%">Description</th>
        </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>xmlstring</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                    </div>
                </td>
                <td>always</td>
                <td>
                            <div>An XML string of the resulting differences</div>
                    <br/>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Jeff Groom (@jgroom33)
