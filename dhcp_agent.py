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
import opts_cfg
import re
from common import config
DHCP_AGENT = 'dhcp_agent'

def register_options():
    cfg.CONF.register_opts(opts_cfg.INTERFACE_DRIVER_OPTS)
    cfg.CONF.register_opts(opts_cfg.USE_NAMESPACES_OPTS)
    cfg.CONF.register_opts(opts_cfg.AGENT_STATE_OPTS, 'AGENT')
    cfg.CONF.register_opts(opts_cfg.DHCP_AGENT_OPTS)
    cfg.CONF.register_opts(opts_cfg.DHCP_OPTS)
    cfg.CONF.register_opts(opts_cfg.DNSMASQ_OPTS)
    cfg.CONF.register_opts(opts_cfg.DRIVER_OPTS)
    cfg.CONF.register_opts(opts_cfg.SHARED_OPTS)
    cfg.CONF.register_opts(opts_cfg.OPTS)

def main():
    register_options()
    config.init(sys.argv[1:])
    config.setup_logging()
    server = neutron_service.Service.create(
        binary='neutron-dhcp-agent',
        topic=DHCP_AGENT,
        report_interval=0,
	#periodic_interval=0,
        manager='nspagent.dhcp.agent.DhcpAgentWithStateReport')
    service.launch(server).wait()

if __name__ == '__main__':
    main()
