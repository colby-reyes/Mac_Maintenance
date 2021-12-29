## Python script to run builtin commands for system maintenance

# import required modules
import os
import sys
import subprocess
import time
from time import sleep
from rich import print, pretty
from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns
from rich.bar import Bar
from rich.prompt import Prompt
from rich.markdown import Markdown

# set up rich modules
pretty.install()
console = Console()


# set up input-response function
def ask_yesno(question):
	"""Standard yes/no question to take input from user.
		  - Takes input "question", a string of the question to ask
		  - Will only continue if input resolves to "y" or "n"
		  - if input resolves to "y": returns True
		  - if input resolves to "n": returns 
	"""
	
	q_txt = f"{question} [Y/n] "
	
	_continue = False
	# set while loop to ensure only acceptable answers are "y" or "n"
	while _continue == False:
		resp = Prompt.ask(q_txt)
		ans = resp.lower()[0]
		if ans == "y":
			_continue = True
			return True
		elif ans == "n":
			_continue = True
			return False
		else:
			_continue = False
		


def purge_ram():
	"""Run built-in function to purge RAM and clear/clean other purgable space"""
	with console.status(f"[bold blue]purging RAM and clearing purgable space[/bold blue]\n   [italic][dim]Note: It is normal for your computer to freeze or lag while this process is taking place.[/dim][/italic]") as status:
		sleep(1)
		os.system("purge")
		print(f"\n[bold green]Done!")
	



def maintenance():
	"""Run built-in periodic maintenance scripts"""
	
	log_dir = '/var/log'
	flst = [f for f  in os.listdir(log_dir) if f.endswith(".out")]
	
	def get_runTimes(f):
		fname = f.split("/")[-1]
		sname = fname.split(".")[0]
		created = time.ctime(os.path.getctime(f))
		modified = time.ctime(os.path.getmtime(f))
		return f"[bold][blue]Script: {sname}[/bold][/blue]\n[yellow]Last run: [/yellow]{modified}"
	
	def show_runTimes(flst, log_dir):
		renderables = []
		for i in flst:
			fh = os.path.join(log_dir,i)
			renderables.append(Panel(get_runTimes(fh)))
		console.print(Columns(renderables))
	
	# show last run times of maintenance scripts
	show_runTimes(flst, log_dir)
	
	# ask user which scripts to run
	maint_cmd = ""
	if ask_yesno("Would you still like to run all 3 scripts?"):
		maint_cmd += " daily weekly monthly"
	else:
		if ask_yesno("Run [bold yellow]daily[/bold yellow] script?"):
			maint_cmd += " daily"
		if ask_yesno("Run [bold yellow]weekly[/bold yellow] script?"):
			maint_cmd += " weekly"
		if ask_yesno("Run [bold yellow]monthly[/bold yellow] script?"):
			maint_cmd += " monthly"
	
	
	# run maintenance scripts
	if maint_cmd != "":
		pass
	else:
		return 0

	with console.status(f"[bold blue]Running maintenance scritps...", spinner='aesthetic') as status:
		os.system(f"periodic {maint_cmd}")
		print(f"\n[bold green]Done!")
	
	# show updated history to check that maintenance was run
	print("[bold yellow]Updated maintenance script history:")
	show_runTimes(flst, log_dir)
	

def clear_caches():
	"""
	TODO: figure out how to check if application is running and ask to quit or skip if it is running
	"""
	"""
	This script is to clear the following caches:
		- in /private/var/log:
			- wifi.log
			- systemlog.2.gz
			- system.log
			- DiagnosticMessages
			- install.log
			- asl
			- ./db/diagnostics
		- for User Application Logs:
			- see symlinks in /Users/colbyr/Documents/GitHub/Mac_Maintenance/symlinks/AppLog_SymLinks
				- delete all files in * for * in AppLog_Symlinks
		- for User Application Caches:
			- see symlinks in /Users/colbyr/Documents/GitHub/Mac_Maintenance/symlinks/
				- delete all files in * for * in AppCache_Symlinks
		- for User Caches:
			- delete all in /Users/{$USER}/Library/Caches? or delete all in subfolders in this location?
		- for User Logs:
			- delete all in /Users/{$USER}/Library/Logs? or delete all in subfolders in this location?
		- for System Logs:
			- delete all in /private/tmp? or delete all in subfolders in this location?
		- for Global Temp Files:
			- delete all in /Users/{$USER}/Library/Preferences? or delete all in subfolders in this location?
		- for User Preferences (note: not recommended to delete >> try moving to trash instead so they can be restored if necessary):
			- selections from /Users/colbyr/Library/Preferences
		- iMessage attachments:
			- 
		
		
		
		Alternatively, based on CleanMyMac:
		- in /Library/Logs:
			- DiagnosticReports
		- in /Users/{$USER}/Library/Logs:
			- 
		- in /System/Library/Caches:
			- 
		- in /Library/Caches:
			- 
		- in /Users/{$USER}/Library/Caches:
			- 
		- for _ in /{$USER}/Library/Containers:
			- _/Data/Library/Caches/*
			- _/Data/Library/Logs/*
	"""



# purge DNS/UDNS
def flush_DNS():
	"""Use built-in functions `dscacheutil` and `kilall` to flush DNS and UDNS caches"""
	with console.status(f"[bold blue]Flushing DNS and UDNS cahces...\n", spinner='aesthetic') as status:
		sleep(1)
		os.system(f"dscacheutil -flushcache")
		os.system(f"killall -HUP mDNSResponder")
		print(f"\n[bold green]Done!")



# reset/rebuild launch services
def rebuild_launchServices():
	"""Call built-in function (`lsregister`) to rebuild launch services
		   - built-in `lsregister` function resides in: `/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister`
	"""
	with console.status("[bold blue]Rebuilding launch services...", spinner='aesthetic') as status:
		cmd = "/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister -kill -r -domain local -domain system -domain user"
		os.system(f"{cmd}")
		print(f"\n[bold green]Done!")
	


# update and restart
def software_updates():
	with console.status("[bold blue]Checking for software updates...", spinner='aesthetic') as status:
		cmd = "softwareupdate --list"
		output = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, universal_newlines=True)
		(out,error) = output.communicate()
		print(f"\n[bold green]Done!")

	if error is None:
		updt_list = out.split("*")	
	else:
		console.log("[red italic]An error ocurred looking for software updates: {error}")
	
	updates = []
	for i in updt_list:
		if 'Label' in i:
			updt = i.replace('\n\t',',')
			result = dict((a.strip(), b.strip()) for a, b in (element.split(':') for element in updt.split(',') if (len(element.split(':')) == 2)))
			updates.append(result)
	
	# set up function to create strings for Rich panels
	def get_Panel_Content(updt_info):
		"""Extract info for Panel from result dict"""
		line1 = f"[b][green]Update: {updt_info.get('Title')}[/bold][/green]"
		line2 = f"[b][yellow]New Version: [/b][/yellow] [blue]{updt_info.get('Version')}[/blue]"
		line3 = f"[b][yellow]Recommended: [/b][/yellow] [blue]{updt_info.get('Recommended')}[/blue]" 
		line4y = f"[b][red]REQUIRES RESTART" 
		line4n = f"[b][yellow]Requires Restart: [/b][/yellow] [blue]No[/blue]"
		line4o = f"[b][yellow]Action: [/b][/yellow][cyan] {updt_info.get('Action')}"
		
		if updt_info.get('Action') == "restart":
			return f"{line1}\n{line2}\n{line3}\n{line4y}"
		elif updt_info.get('Action') == None:
			return f"{line1}\n{line2}\n{line3}"
		else:
			return f"{line1}\n{line2}\n{line3}\n{line4o}"
		
	# create and print panels and columns
	renderables = [Panel(get_Panel_Content(u)) for u in updates]
	print(Columns(renderables))
	
	
	# ask to install 
	if ask_yesno("Would you like to install [u]all[/u] updates? \n[i][dim]Note: If you would like to select specific updates to install, please go to System Preferences >> Software Updates"):
		with console.status(f'Installing updates...', spinner='aesthetic') as status:
			os.system("softwareupdate -ia")
		print(f"\n[bold green]Done!")
	

	
def clear_nvram():
	print("[bold][red]Computer will require power-off after NVRAM is cleared.[/bold][/red]")
	with console.status("[bold blue]Clearing NVRAM...", spinner='aesthetic') as status:
		os.system("nvram -c")
		print(f"\n[bold green]Done!")
	

# clear NVRAM before restart/poweroff
def ask_powerOff():
	"""Give completion options (shutdown, restart, or nothing), then call the built-in function to clear NVRAM, followed by shutdown, restart, or exit (based on user input)"""
	print("[bold][green]Cleanup and maintenance scritps completed!\n   [yellow][1] Shutdown[/yellow]\n   [cyan][2] Restart[/cyan]\n   [magenta][3] Exit Mac_Maintenance.py (keep computer on)[/magenta]")
	
	resp = None
	while resp not in ["1","2","3"]:
		resp = input(" >>> ")
	
	if resp == "1":
		clear_nvram()
		# shutdown
		os.system("shutdown -h now")
	elif resp == "2":
		clear_nvram()
		# reboot
		os.system("shutdown -r now")
	else:
		exit





### Main function to run all functions
def main():
	purge_ram()
	maintenance()
	flush_DNS()
	rebuild_launchServices()
	software_updates()
	purge_ram()
	ask_powerOff()

if os.geteuid() == 0:
    print("[green dim italic]We're root! [dim italic](Some scripts in this module require root privileges in order to run)[/dim italic]")
    main()
else:
    print("[red]We're not root.[/red] [dim italic](Some scripts in this module require root privileges in order to run)[/dim italic]\n[bold blue]Please enter your root password (usually your administrator password) to continue... ")
    subprocess.call(['sudo', 'python3', *sys.argv])
    sys.exit()

