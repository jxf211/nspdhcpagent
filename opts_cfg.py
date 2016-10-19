from oslo_config import cfg

DHCP_AGENT_OPTS = [
    cfg.IntOpt('resync_interval', default=5,
               help=("Interval to resync.")),
    cfg.StrOpt('dhcp_driver',
               default='nspagent.dhcp.linux.dhcp.Dnsmasq',
               help=("The driver used to manage the DHCP server.")),
    cfg.BoolOpt('enable_isolated_metadata', default=False,
                help=("Support Metadata requests on isolated networks.")),
    cfg.BoolOpt('enable_metadata_network', default=False,
                help=("Allows for serving metadata requests from a "
                       "dedicated network. Requires "
                       "enable_isolated_metadata = True")),
    cfg.IntOpt('num_sync_threads', default=4,
               help=('Number of threads to use during sync process.'))
]

DHCP_OPTS = [
    cfg.StrOpt('dhcp_confs',
               default='$state_path/dhcp',
               help=('Location to store DHCP server config files')),
    cfg.StrOpt('dhcp_domain',
               default='openstacklocal',
               help=('Domain to use for building the hostnames')),
]

DNSMASQ_OPTS = [
    cfg.StrOpt('dnsmasq_config_file',
               default='',
               help=('Override the default dnsmasq settings with this file')),
    cfg.ListOpt('dnsmasq_dns_servers',
                help=('Comma-separated list of the DNS servers which will be '
                       'used as forwarders.'),
                deprecated_name='dnsmasq_dns_server'),
    cfg.BoolOpt('dhcp_delete_namespaces', default=False,
                help=("Delete namespace after removing a dhcp server.")),
    cfg.IntOpt(
        'dnsmasq_lease_max',
        default=(2 ** 24),
        help=('Limit number of leases to prevent a denial-of-service.')),
    cfg.BoolOpt('dhcp_broadcast_reply', default=False,
                help=("Use broadcast in DHCP replies")),
]





SHARED_OPTS = [
    cfg.StrOpt('metadata_proxy_socket',
               default='$state_path/metadata_proxy',
               help=('Location for Metadata Proxy UNIX domain socket.')),
    cfg.StrOpt('metadata_proxy_user',
               default='',
               help=("User (uid or name) running metadata proxy after "
                      "its initialization (if empty: agent effective "
                      "user).")),
    cfg.StrOpt('metadata_proxy_group',
               default='',
               help=("Group (gid or name) running metadata proxy after "
                      "its initialization (if empty: agent effective "
                      "group)."))
]


DRIVER_OPTS = [
    cfg.BoolOpt('metadata_proxy_watch_log',
                default=None,
                help=("Enable/Disable log watch by metadata proxy. It "
                       "should be disabled when metadata_proxy_user/group "
                       "is not allowed to read/write its log file and "
                       "copytruncate logrotate option must be used if "
                       "logrotate is enabled on metadata proxy log "
                       "files. Option default value is deduced from "
                       "metadata_proxy_user: watch log is enabled if "
                       "metadata_proxy_user is agent effective user "
                       "id/name.")),
]


METADATA_PROXY_HANDLER_OPTS = [
     cfg.StrOpt('admin_user',
                help=("Admin user")),
     cfg.StrOpt('admin_password',
                help=("Admin password"),
                secret=True),
     cfg.StrOpt('admin_tenant_name',
                help=("Admin tenant name")),
     cfg.StrOpt('auth_url',
                help=("Authentication URL")),
     cfg.StrOpt('auth_strategy', default='keystone',
                help=("The type of authentication to use")),
     cfg.StrOpt('auth_region',
                help=("Authentication region")),
     cfg.BoolOpt('auth_insecure',
                 default=False,
                 help=("Turn off verification of the certificate for"
                        " ssl")),
     cfg.StrOpt('auth_ca_cert',
                help=("Certificate Authority public key (CA cert) "
                       "file for ssl")),
     cfg.StrOpt('endpoint_type',
                default='adminURL',
                help=("Network service endpoint type to pull from "
                       "the keystone catalog")),
     cfg.StrOpt('nova_metadata_ip', default='127.0.0.1',
                help=("IP address used by Nova metadata server.")),
     cfg.IntOpt('nova_metadata_port',
                default=8775,
                help=("TCP Port used by Nova metadata server.")),
     cfg.StrOpt('metadata_proxy_shared_secret',
                default='',
                help=('Shared secret to sign instance-id request'),
                secret=True),
     cfg.StrOpt('nova_metadata_protocol',
                default='http',
                choices=['http', 'https'],
                help=("Protocol to access nova metadata, http or https")),
     cfg.BoolOpt('nova_metadata_insecure', default=False,
                 help=("Allow to perform insecure SSL (https) requests to "
                        "nova metadata")),
     cfg.StrOpt('nova_client_cert',
                default='',
                help=("Client certificate for nova metadata api server.")),
     cfg.StrOpt('nova_client_priv_key',
                default='',
                help=("Private key of client certificate."))
]

DEDUCE_MODE = 'deduce'
USER_MODE = 'user'
GROUP_MODE = 'group'
ALL_MODE = 'all'
SOCKET_MODES = (DEDUCE_MODE, USER_MODE, GROUP_MODE, ALL_MODE)


UNIX_DOMAIN_METADATA_PROXY_OPTS = [
    cfg.StrOpt('metadata_proxy_socket_mode',
               default=DEDUCE_MODE,
               choices=SOCKET_MODES,
               help=("Metadata Proxy UNIX domain socket mode, 3 values "
                      "allowed: "
                      "'deduce': deduce mode from metadata_proxy_user/group "
                      "values, "
                      "'user': set metadata proxy socket mode to 0o644, to "
                      "use when metadata_proxy_user is agent effective user "
                      "or root, "
                      "'group': set metadata proxy socket mode to 0o664, to "
                      "use when metadata_proxy_group is agent effective "
                      "group or root, "
                      "'all': set metadata proxy socket mode to 0o666, to use "
                      "otherwise.")),
    cfg.IntOpt('metadata_workers',
               default=2 // 2,
               help=('Number of separate worker processes for metadata '
                      'server')),
    cfg.IntOpt('metadata_backlog',
               default=4096,
               help=('Number of backlog requests to configure the '
                      'metadata server socket with'))
]




OPTS = [
    cfg.StrOpt('ovs_integration_bridge',
               default='br-int',
               help=('Name of Open vSwitch bridge to use')),
    cfg.BoolOpt('ovs_use_veth',
                default=False,
                help=('Uses veth for an interface or not')),
    cfg.IntOpt('network_device_mtu',
               help=('MTU setting for device.')),
    cfg.StrOpt('meta_flavor_driver_mappings',
               help=('Mapping between flavor and LinuxInterfaceDriver. '
                      'It is specific to MetaInterfaceDriver used with '
                      'admin_user, admin_password, admin_tenant_name, '
                      'admin_url, auth_strategy, auth_region and '
                      'endpoint_type.')),
    cfg.StrOpt('admin_user',
               help=("Admin username")),
    cfg.StrOpt('admin_password',
               help=("Admin password"),
               secret=True),
    cfg.StrOpt('admin_tenant_name',
               help=("Admin tenant name")),
    cfg.StrOpt('auth_url',
               help=("Authentication URL")),
    cfg.StrOpt('auth_strategy', default='keystone',
               help=("The type of authentication to use")),
    cfg.StrOpt('auth_region',
               help=("Authentication region")),
    cfg.StrOpt('endpoint_type',
               default='publicURL',
               help=("Network service endpoint type to pull from "
                      "the keystone catalog")),
]


INTERFACE_DRIVER_OPTS = [
    cfg.StrOpt('interface_driver', default="nspagent.dhcp.linux.interface.OVSInterfaceDriver",
               help=("The driver used to manage the virtual interface.")),
]



USE_NAMESPACES_OPTS = [
    cfg.BoolOpt('use_namespaces', default=True,
                help=("Allow overlapping IP. This option is deprecated and "
                       "will be removed in a future release."),
                deprecated_for_removal=True),
]


AGENT_STATE_OPTS = [
    cfg.FloatOpt('report_interval', default=30,
                 help=('Seconds between nodes reporting state to server; '
                        'should be less than agent_down_time, best if it '
                        'is half or less than agent_down_time.')),
]



