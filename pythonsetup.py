#!/usr/bin/python2
# -*- coding: UTF-8 -*-
from os import system
from subprocess import Popen, PIPE

def get_command_output(command):
    cmd = command.split()
    output = Popen(cmd, stdout=PIPE).communicate()[0]
    return output

def get_os_info():
    info = []
    info.append(get_command_output("bash ./distro.sh").split("=")[1])
    print(info)
    if "Red" in info[0]:
        info.append([word for word in get_command_output("cat /etc/redhat-release").split() if not word.isalnum()])
    elif "Cent" in info[0]:
        info.append([word for word in get_command_output(r"rpm -E %{rhel}").split() if not word.isalnum()])
    return info


class Python_Install():

    def __init__(self, pythonVersion):
        self.version = pythonVersion
        self.manual_python = False
        if self.version < 2.7: self.manual_python = self.manual_python_install()
        self.pip_install()


    def manual_python_install(self):
        system("yum install -y gcc openssl-devel bzip2-devel")
        system("wget https://www.python.org/ftp/python/2.7.18/Python-2.7.18.tgz")
        system("tar xzf Python-2.7.18.tgz")
        system("./Python-2.7.18/configure --enable-optimizations")
        system("make altinstall")
        return True


    def pip_install(self):
        system("curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py")
        if self.manual_python: 
            system("/usr/bin/python2.7 ./get-pip.py")
            system("/usr/bin/python2.7 -m pip install --upgrade wheel setuptools pip cx_Oracle==7.3")
        else: 
            system("/usr/bin/python get-pip.py")
            system("/usr/bin/python -m pip install --upgrade wheel setuptools pip cx_Oracle==7.3")


class Zabbix_Install():

    def __init__(self, pySpecial):
        self.distro = get_os_info()[0]
        self.sysVersion = get_os_info()[1]
        self.pySpecial = pySpecial # If python 2.7 was manually installed 
        if "No such file" in get_command_output("cat /etc/zabbix"): self.preInstalled = False
        else: self.preInstalled = True
        self.install_zabbix()
        self.makefiles()
        self.makeconf()
        self.moveBin()


    def install_zabbix(self):
        if "Red" in self.distro or "Cent" in self.distro:
            system("rpm -Uvh https://repo.zabbix.com/zabbix/4.4/rhel/%s/x86_64/zabbix-release-4.4-1.el%s.noarch.rpm" % (str(self.sysVersion)[0], str(self.sysVersion)[0]))
            system("sudo yum install -y zabbix-agent-4.4.6 zabbix-get-4.4.6 zabbix-sender-4.4.6")
            system("rm -rf /etc/zabbix")
        elif "Ubuntu" in self.distro:
            system("sudo apt-get intall wget")
            system("wget https://repo.zabbix.com/zabbix/4.5/ubuntu/pool/main/z/zabbix-release/zabbix-release_4.5-1%2Bfocal_all.deb")
            system("dpkg -i zabbix-release_4.5+Bfocal_all.deb")
            system("apt update")
            system('apt install zabbix-agent')
        system("groupadd zabbix")
        system("usermod -g zabbix -c 'Zabbix monitoring' zabbix")
        system("mkdir -p /var/log/zabbix/")
        system("chown -R zabbix.zabbix /var/log/zabbix")


    def makefiles(self):
        system("mkdir -p /etc/zabbix/bin")
        with open("/etc/zabbix/guardiao_V4.0.txt", "w") as versionControl:
            versionControl.write("Alterações dessa versão:\n")
            versionControl.write("Utilização script pyOracle que detecta instâncias instaladas no sistema")


    def makeconf(self):
        ## Escreve conf do zabbix
        if not self.preInstalled:
            with open("/etc/zabbix/zabbix_agentd.conf", "a") as conf:
                conf.write("LogFile=/var/log/zabbix/guardiao_agentd.log\n")
                conf.write("DebugLevel=3\n")
                conf.write("EnableRemoteCommands=1\n")
                conf.write("LogRemoteCommands=1\n")
                conf.write("Server=186.250.92.79\n")
                conf.write("ListenPort=%s\n"%(raw_input("Listen Port: ")))
                conf.write("StartAgents=3\n")
                conf.write("ServerActive=186.250.92.79:10051\n")
                conf.write("Hostname=%s\n"%(raw_input("Hostname: ")))
                conf.write("RefreshActiveChecks=120\n")
                conf.write("UnsafeUserParameters=1\n")
                conf.write("\n\n")
                if not self.pySpecial:
                    conf.write("#pyOracle Parameters\n")
                    conf.write("UserParameter=pyOracle_version=python /etc/zabbix/guardiao/bin/pyOracle -c pyversion\n")
                    conf.write("UserParameter=sys[*]=python /etc/zabbix/guardiao/bin/pyOracle -c sys -v $1\n")
                    conf.write("UserParameter=pyOracle_configs[*]=python /etc/zabbix/guardiao/bin/pyOracle -c ora_configs\n")
                    conf.write("UserParameter=pyOracle_home[*]=python /etc/zabbix/guardiao/bin/pyOracle -i $1 -c home\n")
                    conf.write("UserParameter=pyOracle[*]=python /etc/zabbix/guardiao/bin/pyOracle -u $1 -p $2 -i $3 -c $4\n")
                    conf.write("UserParameter=pyOracle_performance[*]=python /etc/zabbix/guardiao/bin/pyOracle -u $1 -p $2 -i $3 -c performance -v $4\n")
                elif self.pySpecial:
                    conf.write("\n#Oracle Parameters\n")
                    conf.write("UserParameter=pyOracle_version=python2.7 /etc/zabbix/guardiao/bin/pyOracle -c pyversion\n")
                    conf.write("UserParameter=sys[*]=python2.7 /etc/zabbix/guardiao/bin/pyOracle -c sys -v $1\n")
                    conf.write("UserParameter=pyOracle_configs[*]=python2.7 /etc/zabbix/guardiao/bin/pyOracle -c ora_configs\n")
                    conf.write("UserParameter=pyOracle_home[*]=python2.7 /etc/zabbix/guardiao/bin/pyOracle -i $1 -c home\n")
                    conf.write("UserParameter=pyOracle[*]=python2.7 /etc/zabbix/guardiao/bin/pyOracle -u $1 -p $2 -i $3 -c $4\n")
                    conf.write("UserParameter=pyOracle_performance[*]=python2.7 /etc/zabbix/guardiao/bin/pyOracle -u $1 -p $2 -i $3 -c performance -v $4\n")
                conf.write("Timeout=10")

        else:
            with open("/etc/zabbix/zabbix_agentd.conf", "a") as conf:
                if not self.pySpecial:
                    conf.write("#pyOracle Parameters\n")
                    conf.write("UserParameter=pyOracle_version=python /etc/zabbix/guardiao/bin/pyOracle -c pyversion\n")
                    conf.write("UserParameter=sys[*]=python /etc/zabbix/guardiao/bin/pyOracle -c sys -v $1\n")
                    conf.write("UserParameter=pyOracle_configs[*]=python /etc/zabbix/guardiao/bin/pyOracle -c ora_configs\n")
                    conf.write("UserParameter=pyOracle_home[*]=python /etc/zabbix/guardiao/bin/pyOracle -i $1 -c home\n")
                    conf.write("UserParameter=pyOracle[*]=python /etc/zabbix/guardiao/bin/pyOracle -u $1 -p $2 -i $3 -c $4\n")
                    conf.write("UserParameter=pyOracle_performance[*]=python /etc/zabbix/guardiao/bin/pyOracle -u $1 -p $2 -i $3 -c performance -v $4\n")
                elif self.pySpecial:
                    conf.write("\n#Oracle Parameters\n")
                    conf.write("UserParameter=pyOracle_version=python2.7 /etc/zabbix/guardiao/bin/pyOracle -c pyversion\n")
                    conf.write("UserParameter=sys[*]=python2.7 /etc/zabbix/guardiao/bin/pyOracle -c sys -v $1\n")
                    conf.write("UserParameter=pyOracle_configs[*]=python2.7 /etc/zabbix/guardiao/bin/pyOracle -c ora_configs\n")
                    conf.write("UserParameter=pyOracle_home[*]=python2.7 /etc/zabbix/guardiao/bin/pyOracle -i $1 -c home\n")
                    conf.write("UserParameter=pyOracle[*]=python2.7 /etc/zabbix/guardiao/bin/pyOracle -u $1 -p $2 -i $3 -c $4\n")
                    conf.write("UserParameter=pyOracle_performance[*]=python2.7 /etc/zabbix/guardiao/bin/pyOracle -u $1 -p $2 -i $3 -c performance -v $4\n")


    def moveBin(self):
        system("mv pyOracle/pyOracle.py /etc/zabbix/bin/pyOracle.py")
        system('mv pyOracle/Oracle_Scripts.py /etc/zabbix/bin/Oracle_Scripts.py')


if __name__ == "__main__":
    pythonVersion = float(get_command_output("python -V")[7:10])
    Python_Install(pythonVersion)
    if pythonVersion < 2.7: Zabbix_Install(pySpecial = True)
    else: Zabbix_Install(pySpecial = False)
            
