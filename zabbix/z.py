from zabbix_api import ZabbixAPI
from zabbix_api import Already_Exists
from log import Logging,setup_logging
import sys


class zabbix:
    def __init__(self,server=None,log_level=0,log=None):
        """
        Accepts keyword args for Server and log_level

        @type server: str
        @param server: Zabbix Server URL
        @type log_level: int
        @param log_level: Logging level for this class
        
        """
        self.zapi = ZabbixAPI(server=server,log_level=log_level)
        if log == None:
            self._log = setup_logging()
        else:
            self._log = log

    def login(self,username=None,password=None):
        """
        Login handler

        """
        try:
            self._log.debug("Attempting to login")
            self.zapi.login(username,password)
            self._log.debug("Login successfull")
        except Exception, e:
            # Unable to login, lets just bomb out
            self._log.error("Failed to login - exiting")
            sys.exit()

    def create_hostgroup(self,name):
        try:
            self._log.debug("Attempting to create hostgroup: %s" % name)
            r = self.zapi.hostgroup.create({"name":"%s" % name})
            hg = r['groupids'][0]
            self._log.info("Created HostGroup %s : %s" % (name, hg ))
            return hg
        except Already_Exists:
            self._log.error("Failed to create hostgroup ( %s ) as it already exists - exiting" % name)
            sys.exit()
        except Exception, e:
            self._log.error("Failed to create hostgroup ( %s ) - exiting" % name)
            sys.exit()

    def create_template(self,name,group,master):
        try:
            self._log.debug("Attempting to create template: %s" % name)
            r = self.zapi.template.create({"host":"%s" % (name),
                     "groups":[{"groupid": "%s" %(group)}]})
            t = r['templateids'][0]
            self._log.debug("Attempting to link template %s to %d" % (name,master))
            self.zapi.template.massAdd({"templates": [{"templateid": "%s" %(t)}],
                 "templates_link": [{"templateid": "%d" %(master)}]})
            self._log.info("Created template %s : %s" % (name, t ))
            return t
        except Already_Exists:
            self._log.error("Failed to create template ( %s ) as it already exists - exiting" % name)
            sys.exit()
        except Exception, e:
            self._log.error("Failed to create template ( %s ) - exiting" % name)
            raise e
            sys.exit()

    def create_host(self,name,ip,itype,port,templates,groups,vname):
        try:
            self._log.debug("Attempting to create host: %s" % name)
            r = self.zapi.host.create({
    "host": "%s" %(name), "name": "%s" %(vname),
    "interfaces": [
            {
                "type": "%d" %(itype),
                "main": 1,
                "useip": 1,
                "ip": "%s" %(ip),
                "dns": "",
                "port": "%d" %(port)
            }
        ],
    "groups": groups,
    "templates": templates
})
            h = r['hostids'][0]
            self._log.info("Created host %s : %s" % (name, h ))
            return h
        except Already_Exists:
            self._log.error("Failed to create host ( %s ) as it already exists - exiting" % name)
            sys.exit()
        except Exception, e:
            self._log.error("Failed to create host ( %s ) - exiting" % name)
            raise e
            sys.exit()
