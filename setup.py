#!/usr/bin/python2
# -*- coding: UTF-8 -*-
from os import system

global success, install
installs = {"epel_install": True, "pip_install": True, "piplib_install": True, "rpm_add": True, "zabbix_install": True, "zabbix_config": True}
successs = True

def get_os_ver():
    cmd = ["cat", "/etc/redhat-release"]
    output = Popen(cmd, stdout=PIPE).communicate()[0]
    for word in output.split():
        try:
            ver = float(word)
        except ValueError:
            pass
    return ver

def pyOracle_setup():
    success = system("sudo yum install -y oracle-epel-release-e17.x86_64", "Complete!")
    if success != 0:
        installs["epel_install"] = False
	    print "error when running 'sudo yum install -y oracle-epel-release-e17.x86_64 | grep Complete!"
    success = run("sudo yum install -y python-pip", "Complete!")
    if success != 0:
	    print "error when running 'sudo yum install -y python-pip | grep Complete!'"
        install["pip_install"] = False
    success = True
    system("python -m pip install --upgrade pip cx_Oracle==7.3")

def install_zabbix():
    ver = get_os_ver()
    success = run("rpm -Uvh https://repo.zabbix.com/zabbix/4.4/rhel/%s/x86_64/zabbix-release-4.4-1.el%s.noarch.rpm" % (str(ver)[0], str(ver)[0]), "added key")
    if success == 0:
    	system("sudo yum install -y zabbix-agent-4.4.6 zabbix-get-4.4.6 zabbix-sender-4.4.6")
    system("rm -rf /etc/zabbix")
    if success != 0:
        print "error when installing zabbix RPM"
        installs["rpm_add"] = False
	    installs["zabbix_install"] = False



def makefiles():
    system("mkdir /etc/zabbix /etc/zabbix/bin")
    def makeversion():
        with open("/etc/zabbix/guardiao_V4.0.txt", "w") as vercontrol:
            vercontrol.write("Alterações dessa versão:\n")
            vercontrol.write("Utilização script pyOracle que detecta instâncias instaladas no sistema")
        
    def makeinstall():
        ## Escreve conf do zabbix
        with open("/etc/zabbix/zabbix_agentd.conf", "a") as conf:
            conf.write("LogFile=/var/log/zabbix/guardiao_agentd.log\n")
            conf.write("DebugLevel=3\n")
            conf.write("EnableRemoteCommands=1\n")
            conf.write("LogRemoteCommands=1\n")
            conf.write("Server=186.250.92.79\n")
            conf.write("ListenPort=10061\n")
            conf.write("StartAgents=3\n")
            conf.write("ServerActive=186.250.92.79:10051\n")
            conf.write("Hostname=%s\n"%(raw_input("Hostname: ")))
            conf.write("RefreshActiteChecks=120\n")
            conf.write("UnsafeUserParameters=1\n")
            conf.write("\n\n")
            conf.write("#Oracle Parameters\n")
            conf.write("UserParameter=pyOracle_version=/etc/zabbix/guardiao/bin/pyOracle -c pyversion\n")
            conf.write("UserParameter=pyOracle_configs[*]=/etc/zabbix/guardiao/bin/pyOracle -c ora_configs\n")
            conf.write("UserParameter=pyOracle_home[*]=/etc/zabbix/guardiao/bin/pyOracle -s $1 -c home\n")
            conf.write("UserParameter=pyOracle[*]=/etc/zabbix/guardiao/bin/pyOracle -u $1 -p $2 -s $3 -c $4\n")
            conf.write("UserParameter=pyOracle_performance[*]=/etc/zabbix/guardiao/bin/pyOracle -u $1 -p $2 -s $3 -c performance -v $4\n")
            conf.write("Timeout=10")
    makeversion()
    makeinstall()
    
def move():
    succes = run("mv pkg/pyOracle.py /etc/zabbix/bin/pyOracle.py", "")
    system('mv pkg/Oracle_Scripts.py /etc/zabbix/bin/Oracle_Scripts.py')

if __name__ == "__main__":
    install_zabbix()
    makefiles()
    pyOracle_setup()
    move()
    for key, value in zip(installs.keys(), installs.values()):
        print key + " " + str(value)
            
