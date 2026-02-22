import random
import subprocess
import os
from rich.console import Console

console = Console()


def run():
    console.print("[#818cf8]  MAC Spoofer[/]")
    console.print("[dim]  Ag arayuzunun MAC adresini degistirir.[/]\n")

    if os.name == "nt":
        console.print("[yellow]  Windows'ta MAC degistirme registry uzerinden yapilir.[/]")
    
    interface = console.input("[bold white]  Ag arayuzu (orn: eth0, wlan0): [/]").strip()
    if not interface:
        console.print("[red]  Arayuz bos olamaz.[/]")
        return

    mode = console.input("[bold white]  1=Rastgele, 2=Ozel MAC: [/]").strip() or "1"
    
    if mode == "2":
        new_mac = console.input("[bold white]  Yeni MAC (XX:XX:XX:XX:XX:XX): [/]").strip()
    else:
        oui = [0x02, 0x00, 0x00]
        nic = [random.randint(0, 255) for _ in range(3)]
        mac_bytes = oui + nic
        new_mac = ":".join(f"{b:02x}" for b in mac_bytes)

    console.print(f"\n[#818cf8]  Yeni MAC: {new_mac}[/]")

    if os.name != "nt":
        try:
            console.print(f"[dim]  $ ifconfig {interface} down[/]")
            subprocess.run(["ifconfig", interface, "down"], capture_output=True)
            console.print(f"[dim]  $ ifconfig {interface} hw ether {new_mac}[/]")
            subprocess.run(["ifconfig", interface, "hw", "ether", new_mac], capture_output=True)
            console.print(f"[dim]  $ ifconfig {interface} up[/]")
            subprocess.run(["ifconfig", interface, "up"], capture_output=True)
            console.print(f"[green]  MAC degistirildi![/]")
        except Exception as e:
            console.print(f"[red]  Hata: {e}[/]")
            console.print("[dim]  Root yetkisi gerekebilir (sudo ile calistirin).[/]")
    else:
        console.print("[yellow]  Windows icin komutlar:[/]")
        console.print(f"  [dim]1. Ayarlar > Ag > Gelismis > MAC[/]")
        console.print(f"  [dim]2. Registry: HKLM\\SYSTEM\\CurrentControlSet\\Control\\Class[/]")
        console.print(f"  [dim]   NetworkAddress = {new_mac.replace(':', '')}[/]")
