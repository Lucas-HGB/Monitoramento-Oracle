#!/usr/bin/python2
# -*- coding: UTF-8 -*-
from os import system
from subprocess import Popen, PIPE

global success, install, zabbix_installed
zabbix_installed = system("cat /etc/zabbix/zabbix_agentd.conf")
installs = {"pip_install": True, "cxOracle_install": True, "rpm_add": True, "zabbix_install": True, "zabbix_config": True}
successs = True
log = open("errors.log", "a")
def get_os_ver():
    cmd = ["cat", "/etc/redhat-release"]
    output = Popen(cmd, stdout=PIPE).communicate()[0]
    for word in output.split():
        try:
            ver = float(word)
        except ValueError:
            pass
    return ver


def check_python_ver():
    cmd = ["/usr/bin/python", "-V"]
    system("python -V")
    ver = input("Please insert python version:")
    if ver < 2.7:
        system("yum install -y gcc openssl-devel bzip2-devel")
        system("wget https://www.python.org/ftp/python/2.7.18/Python-2.7.18.tgz")
        system("tar xzf Python-2.7.18.tgz")
        system("./Python-2.7.18/configure --enable-optimizations")
        system("make altinstall")
    else:
        pass
    return str(ver)[2]
    
    
def pyOracle_setup():
    ver = get_os_ver()
    pyver = check_python_ver()
    success = system("curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py")
    if success == 0:
        if pyver >= 7:
            success = system("python get-pip.py")
        elif pyver < 7:
            success = system("python2.7 get-pip.py")
    if success != 0:
        log.write("ERROR!!! when installing pip")
        installs["pip_install"] = False
    success = True
    if success == 0:
        installs["version": pyver]
        if pyver >= 7:
            success = system("python -m pip install --upgrade wheel setuptools pip cx_Oracle==7.3")
        elif pyver < 7:
            success = system("python2.7 -m pip install --upgrade wheel setuptools pip cx_Oracle==7.3")
    if success != 0:
        installs["cxOracle_install"] = False

def install_zabbix():
    ver = get_os_ver()
    success = system("rpm -Uvh https://repo.zabbix.com/zabbix/4.4/rhel/%s/x86_64/zabbix-release-4.4-1.el%s.noarch.rpm" % (str(ver)[0], str(ver)[0]))
    if success != 0:
        installs["rpm_add"] = False
        log.write("ERROR!!! when installing zabbix RPM")
    success = system("sudo yum install -y zabbix-agent-4.4.6 zabbix-get-4.4.6 zabbix-sender-4.4.6")
    system("rm -rf /etc/zabbix")
    if success != 0:
        log.write("ERROR!!! when installing zabbix pkg")
    installs["zabbix_install"] = False


def makefiles():
    system("mkdir /etc/zabbix /etc/zabbix/bin")
    def makeversion():
        with open("/etc/zabbix/guardiao_V4.0.txt", "w") as vercontrol:
            vercontrol.write("Alterações dessa versão:\n")
            vercontrol.write("Utilização script pyOracle que detecta instâncias instaladas no sistema")
        
    def makeinstall():
        ## Escreve conf do zabbix
        try:
            with open("/etc/zabbix/zabbix_agentd.conf", "a") as conf:
                if zabbix_installed != 0:
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
                conf.write("\n#Oracle Parameters\n")
                conf.write("UserParameter=pyOracle_version=/etc/zabbix/guardiao/bin/pyOracle -c pyversion\n")
                conf.write("UserParameter=sys[*]=/etc/zabbix/guardiao/bin/pyOracle -c sys -v $1\n")
                conf.write("UserParameter=pyOracle_configs[*]=/etc/zabbix/guardiao/bin/pyOracle -c ora_configs\n")
                conf.write("UserParameter=pyOracle_home[*]=/etc/zabbix/guardiao/bin/pyOracle -s $1 -c home\n")
                conf.write("UserParameter=pyOracle[*]=/etc/zabbix/guardiao/bin/pyOracle -u $1 -p $2 -s $3 -c $4\n")
                conf.write("UserParameter=pyOracle_performance[*]=/etc/zabbix/guardiao/bin/pyOracle -u $1 -p $2 -s $3 -c performance -v $4\n")
                conf.write("Timeout=10")
        except:
            installs["zabbix_config"] = False
    makeversion()
    makeinstall()
    
def move():
    succes = system("mv pkg/pyOracle.py /etc/zabbix/bin/pyOracle.py")
    system('mv pkg/Oracle_Scripts.py /etc/zabbix/bin/Oracle_Scripts.py')

if __name__ == "__main__":
    check_python_ver()
    if zabbix_installed != 0:
    	install_zabbix()
    makefiles()
    pyOracle_setup()
    move()
    print "\n\n\n"
    for key, value in zip(installs.keys(), installs.values()):
        print key + " " + str(value)
            
