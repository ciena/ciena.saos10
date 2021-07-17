from plugins.modules import xml_diff

from lxml import etree

def main():
    new = '''
          <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
            <agg-global xmlns="urn:ietf:params:xml:ns:yang:ciena-ieee-lag">
              <global-admin-state>enabled</global-admin-state>
              <marker-timeout xmlns="urn:ietf:params:xml:ns:yang:ciena-ext-lag">50</marker-timeout>
            </agg-global>
            <alarms xmlns="urn:ietf:params:xml:ns:yang:ietf-alarms">
              <control>
                <max-alarm-status-changes>16</max-alarm-status-changes>
                <notify-status-changes>false</notify-status-changes>
              </control>
            </alarms>
            <system xmlns="http://openconfig.net/yang/system">
              <config>
                <hostname>5162-1</hostname>
                <contact xmlns="http://www.ciena.com/ns/yang/ciena-system">Customer Support, Ciena</contact>
                <description xmlns="http://www.ciena.com/ns/yang/ciena-system">5162</description>
                <location xmlns="http://www.ciena.com/ns/yang/ciena-system">Not Specified</location>
              </config>
            </system>
          </config>
'''
    old = '''
          <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
            <agg-global xmlns="urn:ietf:params:xml:ns:yang:ciena-ieee-lag">
              <global-admin-state>enabled</global-admin-state>
              <marker-timeout xmlns="urn:ietf:params:xml:ns:yang:ciena-ext-lag">50</marker-timeout>
            </agg-global>
            <alarms xmlns="urn:ietf:params:xml:ns:yang:ietf-alarms">
              <control>
                <max-alarm-status-changes>16</max-alarm-status-changes>
                <notify-status-changes>false</notify-status-changes>
              </control>
            </alarms>
            <system xmlns="http://openconfig.net/yang/system">
              <config>
                <hostname>5162-1</hostname>
                <contact xmlns="http://www.ciena.com/ns/yang/ciena-system">Customer Support, Ciena</contact>
                <description xmlns="http://www.ciena.com/ns/yang/ciena-system">5162</description>
                <location xmlns="http://www.ciena.com/ns/yang/ciena-system">34.8908084,-40.820916</location>
              </config>
            </system>
          </config>
'''
    new_tree = xml_diff.parse(new)
    old_tree = xml_diff.parse(old)
    result = xml_diff.strip_duplicates(old_tree, new_tree)

    print(etree.tostring(result))


if __name__ == '__main__':
    main()

