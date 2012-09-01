#from zabbix.zabbix_api import ZabbixAPI
from pprint import pprint as pp
from zabbix.z import zabbix
from zabbix.log import Logging,setup_logging

accno=1234
accname="Welby"

_log = setup_logging(console_level="INFO",file_level="INFO")
_log.info("Connecting to zabbix")
z = zabbix(server="http://zabbix",log=_log,log_level=0)
z.login(username='zabbix',password='zabbix')

_log.info("Attempting to create new Host group")
hg = z.create_hostgroup(name="[%d] %s" % (accno,accname))

_log.info("Cloning Templates")
templates = [ 
      {"name":"%d - F5" %(accno),"group": hg, "master": 10093}] 
      {"name":"%d - Mikrotik" %(accno),"group": hg, "master": 10092},
      {"name":"%d - ACTIVE_WINDOWS_LLD" %(accno),"group": hg, "master": 10090},
      {"name":"%d - ACTIVE_LINUX" %(accno),"group": hg, "master": 10089},
      ]

zabbix_template = {}
for template in templates:
    zabbix_template["%s" %( template['name'] ) ] = z.create_template(name=template['name'],group=template['group'],master=template['master'])

hosts = [
  {"name": "F5", "vname": "%d F5" %(accno), "ip": "1.2.3.4","itype":2, "port":161, "templates": [{ "templateid": zabbix_template["1234 - F5"] }], "groups" : [{ "groupid": "%s" %(hg) }] } 
]
for host in hosts:
    z.create_host(name=host['name'], ip = host['ip'], port=host['port'], itype=host['itype'],
          templates=host['templates'], groups=host['groups'],vname=host['vname'])
