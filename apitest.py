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
        task_exchange = Exchange('neutron', type='topic')   
	create_result = {"oslo.message" :{ 
			  'message_id': '5c329c20-d435-444c-8fa2-e1b54592219c',
			  'publisher_id': 'compute.host1',
			  'method': 'network_create_end',
			  '_context_user_id': None,
		 	  '_context_project_id': None,
			  '_context_is_admin': True, 
			  "args" : {"payload": {"network": 
					{"id": "24783e1a-63fe-43d5-9989-e1515c24eecd"}  
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
