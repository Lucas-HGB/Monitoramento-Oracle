installs = {"epel_install": True, "pip_install": True , "piplib_install": True , "rpm_add": True , "zabbix_install": True , "zabbix_config": True}

for key, value in zip(installs.keys(), installs.values()):
    print key + " " + str(value)