import os
import sys
import subprocess
import time
from time import sleep
from rich import print, pretty
from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns
from rich.markdown import Markdown
from rich.bar import Bar

pretty.install()
console = Console()


console.print(Markdown("# Done!"))


"""## 
## Test getting commandline output into a variable
## 
cmd = "softwareupdate --list"
output = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, universal_newlines=True)
(out,error) = output.communicate()

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

def get_Panel_Content(updt_info):
	# Extract info for Panel from result dict
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
	
renderables = [Panel(get_Panel_Content(u)) for u in updates]

print(Columns(renderables))

"""


"""
##
## Test getting file info and returning as panel/columns with Rich
##
log_dir = '/var/log'
flst = [f for f  in os.listdir(log_dir) if f.endswith(".out")]

def get_times(f):
	fname = f.split("/")[-1]
	sname = fname.split(".")[0]
	created = time.ctime(os.path.getctime(f))
	modified = time.ctime(os.path.getmtime(f))
	return f"[bold][blue]Script: {sname}[/bold][/blue]\n[yellow]Last run:[/yellow]{modified}"

renderables = []
for i in flst:
	fh = os.path.join(log_dir,i)
	renderables.append(Panel(get_times(fh)))
console.print(Columns(renderables))

x = input("Would you still like to run all 3 scripts? [Y/n] >>>  ")
print(x)
"""



"""
##
## Test functions to run as root
##

def purge_ram():
	with console.status("[bold green]Purging RAM and cleaning local storage...") as status:
		sleep(2)
		os.system('purge')
# 		try:
# 			os.system('purge')
# 		except Exception as e:
# 			print(e)
			
datas = [1,2,3,4,5]

def test_pop():
	with console.status("[bold green]Scraping data...") as status:
	    while datas:
	        data = datas.pop(0)
	        sleep(1)
	        console.log(f"[green]Finish scraping data[/green] {data}")
	    
	    console.log(f'[bold][red]Done!')

if os.geteuid() == 0:
    print("We're root!")
    test_pop()
    purge_ram()
else:
    print("We're not root.")
    subprocess.call(['sudo', 'python3', *sys.argv])
    sys.exit()
"""