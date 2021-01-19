from os import system
from subprocess import Popen, PIPE

global success, install

def check_python_ver():
    cmd = ["/usr/bin/python", "-V"]
    system("python -V")
    ver = raw_input("Please insert python version:")
    ver = float(str(ver[0:3]))
    return ver
    
    
def pyOracle_setup():
    ver = get_os_ver()
    pyver = check_python_ver()
    success = system("curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py")
    if success == 0:
        installs["Python version"] = pyver
        if pyver >= 2.7:
            success = system("python get-pip.py")
        elif pyver < 2.7:
            success = system("python2.7 get-pip.py")
    if success != 0:
        log.write("ERROR!!! when installing pip")
        installs["pip_install"] = False
    success = True
    if success == 0:
        if pyver >= 2.7:
            success = system("python -m pip install --upgrade wheel setuptools pip cx_Oracle==7.3")
        elif pyver < 2.7:
            success = system("python2.7 -m pip install --upgrade wheel setuptools pip cx_Oracle==7.3")
    if success != 0:
        installs["cxOracle_install"] = False


if __name__ == "__main__":
    pyOracle_setup()