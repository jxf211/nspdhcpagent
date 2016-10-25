from testapi import dhcp_rpc_agent_api

import sys
from oslo_config import cfg
from common import service
import service as neutron_service
#import opts_cfg
import re
from common import config
from common import config as common_config
DHCP_AGENT = 'dhcp_agent'
from kombu import Connection  
from kombu.messaging import Producer
from kombu.transport.base import Message  
from kombu import Exchange, Queue  
import json
  
def register_options():
    cfg.CONF.register_opts(opts_cfg.INTERFACE_DRIVER_OPTS)
    cfg.CONF.register_opts(opts_cfg.USE_NAMESPACES_OPTS)
    cfg.CONF.register_opts(opts_cfg.AGENT_STATE_OPTS, 'AGENT')
    cfg.CONF.register_opts(opts_cfg.DHCP_AGENT_OPTS)
    cfg.CONF.register_opts(opts_cfg.DHCP_OPTS)
    cfg.CONF.register_opts(opts_cfg.DNSMASQ_OPTS)
    cfg.CONF.register_opts(opts_cfg.DRIVER_OPTS)
    cfg.CONF.register_opts(opts_cfg.SHARED_OPTS)

network = {"id": "24783e1a-63fe-43d5-9989-e1515c24eecd",
                                     			   "subnets": [{"id": "ec1028b2-7cb0-4feb-b974-6b8ea7e7f08f",
									"ip_version": 4, "cidr":"10.10.40.0/24", "name":"testsubnet",
									"enable_dhcp": True,
									"network_id" : "24783e1a-63fe-43d5-9989-e1515c24eecd",
									"admin_state_up": True,
									"dns_nameservers":["114.114.114.114"],
									"host_routes":"",
									"ipv6_ra_mode": None,
									"ipv6_address_mode": None,
									"gateway_ip": "10.10.40.1",

									"allocation_pools": [{"start": "10.10.40.2", "end": "10.10.40.254"}],
									},
                                    {"id": "ec1028b2-7cb0-4feb-b974-6b8ea7e7f082",
									"ip_version": 4, "cidr":"10.10.30.0/24", "name":"testsubnet",
									"enable_dhcp": True,
									"network_id" : "24783e1a-63fe-43d5-9989-e1515c24eecd",
									"admin_state_up": True,
									"dns_nameservers":["114.114.114.114"],
									"host_routes":"",
									"ipv6_ra_mode": None,
									"ipv6_address_mode": None,
									"gateway_ip": "10.10.30.1",

									"allocation_pools": [{"start": "10.10.30.2", "end": "10.10.30.254"}],
									}   ],
                                    "ports": [{	"network_id": "24783e1a-63fe-43d5-9989-e1515c24eecd",
						"name":"private-port",
						"admin_state_up":True,
						"id":"cad98138-6e5f-4f83-a4c5-5497fa4758b4",
						"mac_address": "fa:16:3e:65:29:6d",
						"device_owner": "network:dhcp",
						"fixed_ips":
							[{
							    u'subnet_id': u'ec1028b2-7cb0-4feb-b974-6b8ea7e7f08f',
							    u'subnet': {
							       u'name': u'inter-sub',
							       u'enable_dhcp': True,
							       u'network_id': u'8165bc3d-400a-48a0-9186-bf59f7f94b05',
							       u'tenant_id': u'befa06e66e8047a1929a3912fff2c591',
							       u'dns_nameservers': [],
							       u'ipv6_ra_mode': None,
							      u'allocation_pools': [{u'start': u'10.10.40.2', u'end': u'10.10.40.254'}],
							       u'gateway_ip': u'10.10.40.1',
							       u'shared': False,
							       u'ip_version': 4,
							       u'host_routes': [],
							       u'cidr': u'10.10.40.0/24',
							       u'ipv6_address_mode': None,
							       u'id': u'ec1028b2-7cb0-4feb-b974-6b8ea7e7f08f',
							       u'subnetpool_id': None
								},
							     u'ip_address': u'10.10.40.3'
							    }],
						},
						{"network_id": "24783e1a-63fe-43d5-9989-e1515c24eecd",
						"name":"private-port",
						"admin_state_up":True,
						"id":"cad98138-6e5f-4f83-a4c5-5497fa4758b2",
						"mac_address": "fa:16:3e:65:29:62",
						"device_owner": "network:dhcp",
						"fixed_ips":
							[{
							    u'subnet_id': u'ec1028b2-7cb0-4feb-b974-6b8ea7e7f082',
							    u'subnet': {
							       u'name': u'inter-sub',
							       u'enable_dhcp': True,
							       u'network_id': u'8165bc3d-400a-48a0-9186-bf59f7f94b05',
							       u'tenant_id': u'befa06e66e8047a1929a3912fff2c591',
							       u'dns_nameservers': [],
							       u'ipv6_ra_mode': None,
							      u'allocation_pools': [{u'start': u'10.10.40.2', u'end': u'10.10.40.254'}],
							       u'gateway_ip': u'10.10.40.1',
							       u'shared': False,
							       u'ip_version': 4,
							       u'host_routes': [],
							       u'cidr': u'10.10.40.0/24',
							       u'ipv6_address_mode': None,
							       u'id': u'ec1028b2-7cb0-4feb-b974-6b8ea7e7f08v',
							       u'subnetpool_id': None
								},
							     u'ip_address': u'10.10.30.4'
							    }],
						}],
					"admin_state_up":True,
					"tenant_id":"befa06e66e8047a1929a3912fff2c591"}

class controller(object):
    
    def  __init__(self):
        #self._dhcp_agent_notifier = dhcp_rpc_agent_api.DhcpAgentNotifyAPI() 
   	pass 
    def create(self, request=None, body=None, **kwargs):
        """Creates a new instance of the requested entity."""
	print "#"*50
        notifier_method = 'subnet' + '.create.end'
        context = "1212121"
	create_result = {"subnet": 
				{
        			"network_id": "d32019d3-bc6e-4319-9c1d-6722fc136a22",
        			"ip_version": 4,
        			"cidr": "10.0.0.1"
    				}
 			}
	self._send_dhcp_notification(context,
                                         create_result,
                                         notifier_method)

    def _send_dhcp_notification(self, context, data, methodname):
        #self._dhcp_agent_notifier.notify(context, data, methodname)
        task_exchange = Exchange('nspagent', type='topic')   
	create_result = {"oslo.message" :{ 
			  #'message_id': '5c329c20-d435-444c-8fa2-e1b54592219c',
			  #'publisher_id': 'compute.host1',
			  'method': 'network_create_end',
			  #'_context_user_id': None,
		 	  #'_context_project_id': None,
			  #'_context_is_admin': True,
			  "args" : {"payload": {"network": network
					#{"id": "24783e1a-63fe-43d5-9989-e1515c24eecd"}
				      }		
				   }
		         },
			"oslo.version":'2.0',
		      }
	create_result["oslo.message" ] = json.dumps(create_result["oslo.message"])
	connection = Connection('amqp://guest:guest@192.168.49.22:5672//')  
	channel = connection.channel()  
   
	message=Message(channel,body= 'subenet_create_end')  
   
	# produce  
	producer = Producer(channel,serializer='json') 
        print message.body, task_exchange 
	producer.publish(create_result, routing_key='dhcp_agent')  


if __name__ == '__main__':
    #register_options()
    #common_config.init(sys.argv[1:])
    #config.setup_logging()
    contr = controller()
    contr.create()
