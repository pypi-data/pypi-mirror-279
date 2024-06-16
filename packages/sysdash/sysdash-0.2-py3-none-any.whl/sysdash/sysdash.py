import psutil
import GPUtil
import uptime
import os
import time
from datetime import timedelta
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
from rich.box import ROUNDED
import platform
import socket
import wmi
import subprocess

console = Console()


def get_cpu_info():
    cpu_usage = psutil.cpu_percent(interval=1)
    per_cpu_usage = psutil.cpu_percent(interval=1, percpu=True)
    per_cpu_info = " | ".join(
        [f"Core {i}: {usage}%" for i, usage in enumerate(per_cpu_usage)])
    return f"Total: {cpu_usage}%\n{per_cpu_info}"


def get_memory_info():
    memory = psutil.virtual_memory()
    return f"{memory.percent}% (Used: {memory.used / (1024 ** 3):.2f}GB, Total: {memory.total / (1024 ** 3):.2f}GB)"


def get_disk_info():
    disk = psutil.disk_usage('/')
    return f"{disk.percent}% (Used: {disk.used / (1024 ** 3):.2f}GB, Total: {disk.total / (1024 ** 3):.2f}GB)"


def get_uptime():
    system_uptime = timedelta(seconds=int(uptime.uptime()))
    return str(system_uptime)


def get_gpu_info():
    gpus = GPUtil.getGPUs()
    if not gpus:
        return "No GPU found."
    info = []
    for gpu in gpus:
        info.append(f"{gpu.name} - Memory Usage: {gpu.memoryUsed / gpu.memoryTotal *
                    100:.2f}% (Used: {gpu.memoryUsed}MB, Total: {gpu.memoryTotal}MB)")
    return "\n".join(info)


def get_motherboard_info():
    c = wmi.WMI()
    for board_id in c.Win32_BaseBoard():
        return board_id.Product
    
def get_packages_info():
    try:
        choco_packages = subprocess.check_output(['choco', 'list', '--local-only'], shell=True).decode().strip().split('\n')
        scoop_packages = subprocess.check_output(['scoop', 'list'], shell=True).decode().strip().split('\n')
        return f"{len(choco_packages)-1} (choco), {len(scoop_packages)-2} (scoop)"  # Adjust for headers
    except Exception as e:
        return "Error fetching packages"

def get_shell_info():
    shell = os.getenv('SHELL') or os.getenv('COMSPEC')
    return shell

def get_resolution():
    try:
        from screeninfo import get_monitors
        monitor = get_monitors()[0]
        return f"{monitor.width}x{monitor.height}"
    except ImportError:
        return "Resolution info requires screeninfo library"    


def get_system_info():
    os_info = f"{platform.system()} {platform.release()} [{
        platform.architecture()[0]}]"
    host = socket.gethostname()
    kernel = platform.version()
    motherboard = get_motherboard_info()
    packages = get_packages_info()
    shell = get_shell_info()
    resolution = get_resolution()
    terminal = os.getenv('TERM_PROGRAM', 'Windows Terminal')

    info = {
        "OS": os_info,
        "Host": host,
        "Kernel": kernel,
        "Motherboard": motherboard,
        "Uptime": get_uptime(),
        "Packages": packages,
        "Shell": shell,
        "Resolution": resolution,
        "Terminal": terminal,
        "CPU": get_cpu_info(),
        "GPU": get_gpu_info(),
        "Memory": get_memory_info(),
        "Disk (C:)": get_disk_info(),
    }
    return info


def create_table(system_info):
    table = Table(
        title="System Information",
        title_style="bold magenta",
        box=ROUNDED,
        expand=True,
        show_edge=False,
        padding=(0, 1),
    )
    table.add_column("Component", style="cyan", no_wrap=True, justify="right")
    table.add_column("Details", style="white", justify="left")

    for key, value in system_info.items():
        table.add_row(key, value)

    return table


def display_system_info():
    with Live(auto_refresh=False) as live:
        while True:
            system_info = get_system_info()
            table = create_table(system_info)
            live.update(
                Panel(table, border_style="bold yellow", padding=(1, 2)))
            live.refresh()
            time.sleep(5)  # Update every 5 seconds


def main():
    display_system_info()


if __name__ == "__main__":
    main()
