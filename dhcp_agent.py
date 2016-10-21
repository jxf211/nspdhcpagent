# Copyright 2015 OpenStack Foundation
#
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
from common import eventlet_utils
eventlet_utils.monkey_patch()
import sys
from oslo_config import cfg
from common import service
import service as neutron_service
import re
from common import topics
from common import config as common_config
from nspagent.dhcpcommon import config
from nspagent.dhcp.linux import interface
from nspagent.dhcp import config as dhcp_config
from nspagent.dhcp.metadata import config as metadata_config

def register_options():
    config.register_interface_driver_opts_helper(cfg.CONF)
    config.register_use_namespaces_opts_helper(cfg.CONF)
    config.register_agent_state_opts_helper(cfg.CONF)
    cfg.CONF.register_opts(dhcp_config.DHCP_AGENT_OPTS)
    cfg.CONF.register_opts(dhcp_config.DHCP_OPTS)
    cfg.CONF.register_opts(dhcp_config.DNSMASQ_OPTS)
    cfg.CONF.register_opts(metadata_config.DRIVER_OPTS)
    cfg.CONF.register_opts(metadata_config.SHARED_OPTS)
    cfg.CONF.register_opts(interface.OPTS)


def main():
    register_options()
    common_config.init(sys.argv[1:])
    config.setup_logging()
    server = neutron_service.Service.create(
        binary='neutron-dhcp-agent',
        topic=topics.DHCP_AGENT,
        report_interval=cfg.CONF.AGENT.report_interval,
        manager='nspagent.dhcp.agent.DhcpAgentWithStateReport')
    service.launch(server).wait()

if __name__ == '__main__':
    main()
