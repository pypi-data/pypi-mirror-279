#!/usr/bin/env python


colbase = '\033'

class termcol:
	ENDC =				f'{colbase}[0m'
	RESET =				f'{colbase}[39m{colbase}[49m' #         - Reset color
	#CLEAR_LINE =		f'{colbase}[2K                          - Clear Line
	#MOVE_CURSOR = 		f'{colbase}[<L>;<C>H or \\033[<L>;<C>f  - Put the cursor at line L and column C.
	#XXX =				f'{colbase}[<N>A                        - Move the cursor up N lines
	#XXX =				f'{colbase}[<N>B                        - Move the cursor down N lines
	#XXX =				f'{colbase}[<N>C                        - Move the cursor forward N columns
	#XXX =				f'{colbase}[<N>D                        - Move the cursor backward N columns
	#CLEAR_SCREEN =		f'{colbase}[2J                          - Clear the screen, move to (0,0)
	#ERASE_TO_END_OF_LINE =			f'{colbase}[K               - Erase to end of line
	#SAVE_CURSOR =		f'{colbase}[s                           - Save cursor position
	#RESTORE_CURSOR =	f'{colbase}[u                           - Restore cursor position\n
	UNDERLINE_ON =		f'{colbase}[4m' #                       - Underline on
	UNDERLINE_OFF =		f'{colbase}[24m' #                      - Underline off
	BOLD_ON =			f'{colbase}[1m' #                       - Bold on
	BOLD_OFF =			f'{colbase}[21m' #                      - Bold off
	
	
	#ORANGE = f'{colbase}[94m'
	DEFAULT =			f'{colbase}[39m'
	BLACK =				f'{colbase}[30m'
	DARK_RED =			f'{colbase}[31m'
	DARK_GREEN =		f'{colbase}[32m'
	DARK_YELLOW =		f'{colbase}[33m'
	ORANGE =			f'{colbase}[33m' # Helper
	DARK_BLUE =			f'{colbase}[34m'
	DARK_MAGENTA =		f'{colbase}[35m'
	DARK_CYAN =			f'{colbase}[36m'
	LIGHT_GRAY =		f'{colbase}[37m'
	DARK_GRAY =			f'{colbase}[90m'
	RED =				f'{colbase}[91m'
	GREEN =				f'{colbase}[92m'
	YELLOW =			f'{colbase}[93m'
	BLUE =				f'{colbase}[94m'
	MAGENTA =			f'{colbase}[95m'
	PURPLE =			f'{colbase}[95m' # Helper
	CYAN =				f'{colbase}[96m'
	WHITE =				f'{colbase}[97m'
	BG_DEFAULT =		f'{colbase}[49m'
	BG_BLACK =			f'{colbase}[40m'
	BG_DARK_RED =		f'{colbase}[41m'
	BG_DARK_GREEN =		f'{colbase}[42m'
	BG_DARK_YELLOW =	f'{colbase}[43m'
	BG_DARK_BLUE =		f'{colbase}[44m'
	BG_DARK_MAGENTA =	f'{colbase}[45m'
	BG_DARK_CYAN =		f'{colbase}[46m'
	BG_LIGHT_GRAY =		f'{colbase}[47m'
	BG_DARK_GRAY =		f'{colbase}[100m'
	BG_RED =			f'{colbase}[101m'
	BG_GREEN =			f'{colbase}[101m'
	BG_ORANGE =			f'{colbase}[103m'
	BG_BLUE =			f'{colbase}[104m'
	BG_MAGENTA =		f'{colbase}[105m'
	BG_CYAN =			f'{colbase}[106m'
	BG_WHITE =			f'{colbase}[107m'


import sys
print(f"{termcol.GREEN}{'sys.executable':>20}{termcol.WHITE}: {termcol.ORANGE}{sys.executable}{termcol.ENDC}\n")
print(f"{termcol.GREEN}{'sys.path':>20}{termcol.WHITE}: {termcol.ORANGE}{sys.path}{termcol.ENDC}\n")

import pprint
import pkgutil
import importlib.metadata

import inspect

	

def list_packages_and_modules():
	sep = f'{termcol.WHITE},{termcol.BLUE} '
	print(f"{termcol.GREEN}Listing started{termcol.ENDC}\n")
	names = []
	for dist in importlib.metadata.distributions():
		package_name = dist.metadata.get('Name')
		names.append(package_name)
	print(", ".join(names))
	for dist in importlib.metadata.distributions():
		try:
			package_name = dist.metadata.get('Name')
			if not package_name.startswith("octo"):
				continue
			'''
			import_name = package_name.replace('-', '_')
			package = __import__(import_name)
			if hasattr(package, '__path__'):  # Check if the package has a path, i.e., is a package
				modules = list()
				for _, module, _ in pkgutil.iter_modules(package.__path__):
					modules.append(module)
			'''
			# Iterate over files in the distribution looking for Python files
			modules_list = set()
			
			if True:
				print(pprint.pformat(dist.files))
				if dist.files:
					for file in dist.files:
						# Only consider files that are in packages (contain '/')
						if file.name.endswith('.py'):
							# Extract the module name from the path by taking the first part of the path
							module_name = file.name
							modules_list.add(module_name)
						else:
							pass
							#modules_list.add(f"Skipping {file.name}")
				else:
					modules_list.add("No dist.files")
			#modules_list.add("test")
			modules_list = list(modules_list)
			print(f"{termcol.GREEN}{package_name:>20}{termcol.WHITE}: {sep.join(modules_list)}{termcol.ENDC}\n")
		except Exception as e:
			print(f"{termcol.GREEN}{package_name:>20}{termcol.WHITE}: {termcol.RED}ERROR{termcol.WHITE}: {termcol.ORANGE}{e}{termcol.ENDC}\n")
	print(f"{termcol.GREEN}Listing complete{termcol.ENDC}\n")




list_packages_and_modules()

#sys.exit(0)

import asyncio
import pydantic
import datetime
import octomy.config
import octomy.db
from functools import lru_cache


die_sec = 3



class DbTime(pydantic.BaseModel):
	now:datetime.datetime

class DatabaseCheck:
	def __init__(self, config):
		config:octomy.config.OctomyConfig = octomy.config.get_config()
		self.dbc:octomy.db.Database
		self.dbc, db_err = octomy.db.get_database(config)
		#assert self.dbc.is_ok()
		#self.create_tables()


	# Get current time from db
	async def get_now(self, do_debug=False) -> (DbTime, str|None):
		db_ret, db_err = await self.dbc.query_one("octomy.db.get_now", params=dict(), item_type=DbTime, prepare=False, do_debug=do_debug)
		return db_ret, db_err
 

	async def verify(self):
		try:
			db_ret, db_err = await self.get_now()
			return None == db_err
		except Exception as e:
			logger.warning(f"Unknown error '{e}':", exc_info=True)
			return False


#@lru_cache()
def get_db_checker(config) -> DatabaseCheck:
	dbc = DatabaseCheck(config)
	return dbc

async def entrypoint():
	try:
		import sys
		import os
		import signal
		def signal_handler(sig, frame):
			print('SIGINT Received, closing...')
			sys.exit(0)
		
		signal.signal(signal.SIGINT, signal_handler)
		# Facilitate local override of octomy packages
		local_modules_path = os.path.join(os.path.dirname(__file__), 'octomy')
		sys.path.insert(0, local_modules_path)
		from octomy.log import setup_logging
	
		logger = setup_logging(__name__)
		import datetime
		import octomy.utils
		import octomy.batch
		from octomy.version import get_version
	
		octomy_batch_version = get_version("octomy.batch")
	
		logger.info(f"Batch version {octomy_batch_version} starting...")
	
	except Exception as e:
		import time
		import sys
		logger.error("INIT FAILED - waiting {octomy.utils.human_delta(delay)} before terminating", exc_info=True)
		time.sleep(die_sec)
		#raise e
		sys.exit(5)
	
	try:
		import sys
		import octomy.config
		import octomy.batch.server
		#from octomy.db.check import DatabaseCheck
	except:
		delay = datetime.timedelta(seconds=die_sec)
		logger.error(f"IMPORT FAILED - waiting {octomy.utils.human_delta(delay)} before terminating", exc_info=True)
		octomy.utils.sleep(delay.total_seconds())
		sys.exit(2)
	
	
	config:octomy.config.OctomyConfig = octomy.config.get_config()
	
	db = get_db_checker(config)
	if await db.verify():
		logger.info("DB OK")
	else:
		delay = datetime.timedelta(seconds=die_sec)
		logger.error(f"DB FAILED - waiting {octomy.utils.human_delta(delay)} before terminating", exc_info=True)
		octomy.utils.sleep(delay.total_seconds())
		sys.exit(3)
	
	try:
		# Make sure to completely free database resources before we start Flask to avoid nasty multi trheading/processing issues
		del db
		server = octomy.batch.server.Server(config)
		ok, message = await server.verify()
		if ok:
			logger.info("BatchProcessor OK")
		else:
			logger.error(f"BatchProcessor failed with {message}")
			raise Exception(f"Error while preparing batch processor: {message}")
		await server.run()
	
	except:
		delay = datetime.timedelta(seconds=die_sec)
		logger.error(f"MAIN FAILED - waiting {octomy.utils.human_delta(delay)} before terminating", exc_info=True)
		octomy.utils.sleep(delay.total_seconds())
		sys.exit(4)


def main():
	asyncio.run(entrypoint())

if __name__ == '__main__':
	main()
