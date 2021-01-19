#!/usr/bin/python2
# -*- coding: UTF-8 -*-
from platform import system as arch
from timeit import timeit
from argparse import ArgumentParser
from Oracle_Scripts import choose_script
from os import system, environ
from cx_Oracle import connect


global start
start = timeit()
def get_time():
	return abs(timeit() - start)

def get_args():
    parser = ArgumentParser()
    parser.add_argument("-u", "--user", dest="user",
                        help="Banco user", metavar="user")
    parser.add_argument("-p", "--pswd", dest="password",
                        help="Databse password", metavar="password")
    parser.add_argument("-i", "--instance", dest="instance",
                        help="Banco instance", metavar="instance")
    parser.add_argument("-c", "--command", dest="command",
                        help="Command to be executed", metavar="command")
    parser.add_argument("-v", "--value", dest="value",
                        help="Value to execute with command", metavar="value", default=False)
    parser.add_argument("-d", "--debug", dest="debug",
                        help="Debug", metavar="debug", default=False)
    args = parser.parse_args()
    return args

global args
args = get_args()
if args.debug:
	args.debug = True

def print_json(values):
	print "{"
	print '    "data": ['
	for varia in values:
		if varia != "+ASM":
			print '        {'
			if varia != values[-1]:
				print '            "{#SID}": "%s"},' % varia
			else:
				print '            "{#SID}": "%s"}' % varia
	print '    ]'
	print "}"

class Banco():

	def __init__(self, ip, user, password, instance, port = 1521):
		from cx_Oracle import connect
		try:
			self.connection = connect(user, password, "%s:%s/%s" % (ip, port, instance), encoding="UTF-8")
			self.cursor = self.connection.cursor()
			if args.debug:
				print "Conectado %s" % get_time()
		except Exception as excp:
			if args.debug:
				print excp
			else:
				pass

	def run_command(self, command, value):
		try:
			if args.debug:
				print "Rodando comando %s" % get_time()
			output = choose_script(cursor = self.cursor, opc = command, value = value)[0]
			for word in output:
				print output
			if args.debug:
				print "Comando finalizado %s" % get_time()	
		except Exception as excp:
			if args.debug:
				print excp
			else:
				pass
		

class Ambiente():

	def __init__(self):
		pass

	def run_sys(self, command):
		return system(command)

	def get_pyora_version(self):
		version = 4.0
		return version

	def set_environ(self, instance):
		self.get_oracle_configs()
		environ["LD_LIBRARY_PATH"] = "%s/lib:/lib:/usr/lib" % (self.configs[instance])
		if args.debug:
			print "LD_LIBRARY_PATH:  %s" % (environ["LD_LIBRARY_PATH"])

	def get_oracle_configs(self):
		global data
		configs = {}
		if arch().lower() == "linux":
			try:
				with open(r"/etc/oratab", "r") as oratab:
					lines = oratab.readlines()
					config_lines = [line for line in lines if line[0] != "#" and line != "\n"]
					for config in config_lines:
						configs[config.split(":")[0]] = (config.split(":")[1])
				self.configs = configs
				return configs
			except Exception as excp:
				print excp
		elif arch().lower() == "windows":
			reg_path = r'SOFTWARE\Oracle\KEY_HOME_NAME'
			reg_key = reg.OpenKey(reg.HKEY_LOCAL_MACHINE, reg_path, 0, reg.KEY_READ)
			data = reg.QueryValue(reg_key, None)
			reg_key.Close()
			configs[data.split(":")[0]] = (data.split(":")[1])

if __name__ == "__main__":
	Ambiente = Ambiente()
	if args.command != "ora_configs" and args.command != "pyversion" and args.command != "home" and args.command != "sys":
		Ambiente.set_environ(args.instance)
		Banco = Banco(ip = "localhost",user = args.user, password = args.password, instance = args.instance)
		if args.value:
			Banco.run_command(command = args.command, value = args.value)
		elif not args.value:
			Banco.run_command(command = args.command, value = None)
	elif args.command == "home":
		if args.debug:
			print "Extraindo home de SID específica %s" % get_time()
		ora_configs = Ambiente.get_oracle_configs()
		print(ora_configs[args.instance])
	elif args.command == "pyversion":
		print "pyOracle Version %s" % Ambiente.get_pyora_version()
	elif args.command == "ora_configs":
		ora_configs = Ambiente.get_oracle_configs()
		try:
			print_json([f for f in ora_configs.keys()])
		except AttributeError:
			pass
	elif args.command == "sys":
		Ambiente.run_sys(args.value)

