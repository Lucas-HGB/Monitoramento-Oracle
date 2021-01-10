from platform import system
if system().lower() == "windows":
	import winreg as reg
from timeit import timeit
from argparse import ArgumentParser
from Oracle_Scripts import choose_script
from os import system


global start
start = timeit()
def get_time():
	return abs(timeit() - start)

def args():
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
	
def print_json(values):
	print("{")
	print('    "data": [')
	for varia in values:
		print('        {')
		if varia != values[-1]:
			print('            "{#SID}": "%s"},' % varia)
		else:
			print('            "{#SID}": "%s"}' % varia)
	print('    ]')
	print("}")

class Banco():

	def __init__(self):
		pass

	#Conexão com banco de dados
	def connect(self, ip, user, password, port = 1521,instance = False, Banco = False):
		try:
			from cx_Oracle import connect
			self.connection = connect(user,password,f"{ip}:{port}/{instance}",encoding="UTF-8")
			self.cursor = self.connection.cursor()
		except Exception as e:
			print(f"Error {e} occurred!")

	def run_command(self, command, value):
		output = choose_script(cursor = self.cursor, opc = command, value = value)
		return output

class Ambiente():

	def __init__(self):
		pass

	def run_sys(self, command):
		return system(command)

	def get_pyora_version(self):
		version = 3.2
		return version

	def get_oracle_configs(self):
		global data
		configs = {}
		if system().lower() == "linux":
			try:
				with open(r"/etc/oratab", "r") as oratab:
					lines = oratab.readlines()
					config_line = [line for line in lines if line[0] != "#" and line != "\n"]
					configs[config_line.split(":")[0]] = (config_line.split(":")[1])
				return configs
			except FileNotFoundError:
				print("File /etc/oratab not found!")
		elif system().lower() == "windows":
			reg_path = r'SOFTWARE\Oracle\KEY_HOME_NAME'
			reg_key = reg.OpenKey(reg.HKEY_LOCAL_MACHINE, reg_path, 0, reg.KEY_READ)
			data = reg.QueryValue(reg_key, None)
			reg_key.Close()
			configs[data.split(":")[0]] = (data.split(":")[1])

if __name__ == "__main__":
	Ambiente = Ambiente()
	Banco = Banco()
	args = args()
	if args.debug:
		args.debug = True
	if args.debug:
		print(f"Extraindo argumentos do CMD {get_time()}")
	if args.command != "ora_configs" and args.command != "pyversion" and args.command != "home":
		Banco.connect(ip = "localhost",user = args.user, password = args.password, instance = args.instance)
		if args.debug:
			print(f"Conectado {get_time()}")
		if args.debug:
			print(f"Rodando comando {get_time()}")
		if args.value:
			Banco.run_command(command = args.command, value = args.value)
		elif not args.value:
			Banco.run_command(command = args.command, value = None)
		if args.debug:
			print(f"Comando finalizado {get_time()}")		
	elif args.command == "home":
		if args.debug:
			print(f"Extraindo home de SID específica {get_time()}")
		ora_configs = Ambiente.get_oracle_configs()
		print(ora_configs[args["-s"]])
	elif args.command == "pyversion":
		print(f"pyOracle Version {Ambiente.get_pyora_version()}")
	elif args.command == "ora_configs":
		ora_configs = Ambiente.get_oracle_configs()
		try:
			print_json([f for f in ora_configs.keys()])
		except AttributeError:
			pass